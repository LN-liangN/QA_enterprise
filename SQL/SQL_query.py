import sqlite3
import json
import re
from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple
from langchain_core.messages import SystemMessage, HumanMessage
from model.factory import chat_model
from utils.path_tool import get_abs_path
from utils.prompts_loader import load_sql_prompts

class EnterpriseSQLQueryBot:
    """
    企业智能问答 SQL 查询助手
    使用 LLM 将自然语言问题转换为 SQL，在 SQLite 数据库上执行查询并返回结果。
    """
    def __init__(self):
        self.db_path = get_abs_path(r'enterprise-qa-data\enterprise.db')
        self.connection = None
        self.sql_prompt_template = load_sql_prompts()
        self.model = chat_model

    def _connect(self):
        """建立数据库连接"""
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row

    def _close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            self.connection = None

    def _is_safe_sql(self, sql: str) -> bool:
        """安全检查：仅允许 SELECT 语句"""
        cleaned = re.sub(r'--.*$', '', sql, flags=re.MULTILINE)
        cleaned = re.sub(r'/\*.*?\*/', '', cleaned, flags=re.DOTALL)
        cleaned = cleaned.strip().upper()
        dangerous_keywords = ['INSERT', 'UPDATE', 'DELETE', 'DROP', 'ALTER', 'CREATE', 'TRUNCATE', 'REPLACE']
        if not cleaned.startswith('SELECT'):
            return False
        for keyword in dangerous_keywords:
            if re.search(r'\b' + keyword + r'\b', cleaned):
                return False
        return True

    def generate_sql(self, question: str) -> str:
        """
        调用 LLM 将自然语言问题转换为 SQL 查询语句
        """
        current_date = "2026-03-27"
        filled_prompt = self.sql_prompt_template.replace("{current_date}", current_date)
        messages = [
            SystemMessage(content=filled_prompt),
            HumanMessage(content=question)
        ]
        response = self.model.invoke(messages)
        content = response.content.strip()

        # 解析 JSON 获取 SQL
        try:
            # 提取 JSON 对象（可能被包裹在 markdown 代码块中）
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                data = json.loads(json_str)
            else:
                data = json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"LLM 返回的内容无法解析为 JSON: {content}") from e

        # 提示词示例中 JSON 包含一个数组，但标准格式应直接是对象，做兼容处理
        if isinstance(data, list) and len(data) > 0:
            data = data[0]  # 取第一个元素
        if "sql" not in data:
            raise ValueError(f"LLM 返回的 JSON 缺少 'sql' 字段: {data}")

        return data["sql"]

    def execute_query(self, sql: str) -> Tuple[List[Dict[str, Any]], int]:
        """执行 SQL 查询并返回结果"""
        if not self._is_safe_sql(sql):
            raise ValueError("不安全的 SQL 语句：仅允许 SELECT 查询。")

        self._connect()
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            results = [dict(row) for row in rows]
            return results, len(results)
        except sqlite3.Error as e:
            raise e
        finally:
            self._close()

    def ask(self, question: str) -> Dict[str, Any]:
        """完整流程：自然语言 -> SQL -> 查询执行 -> 返回结果"""
        sql = self.generate_sql(question)
        results, count = self.execute_query(sql)
        return {
            "question": question,
            "sql": sql,
            "results": results,
            "count": count
        }

    def __enter__(self):
        self._connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._close()

if __name__ == "__main__":
    print("初始化 EnterpriseSQLQueryBot...")
    bot = EnterpriseSQLQueryBot()

    test_questions = [
        "张三2月份迟到了几次？",
        "所有部门的员工人数是多少？",
        "项目P001的负责人是谁？"
    ]

    for question in test_questions:
        print(f"\n问题: {question}")
        try:
            response = bot.ask(question)
            print(f"生成的 SQL: {response['sql']}")
            print(f"结果: {response['results']}")

        except Exception as e:
            print(f"查询失败: {e}")
