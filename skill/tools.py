from langchain_core.tools import tool

from RAG.rag_service import RagSummarizeService
from SQL.SQL_query import EnterpriseSQLQueryBot

sql = EnterpriseSQLQueryBot()  # sql查询执行器
rag = RagSummarizeService()    # 知识文档查询执行器

@tool(description="使用sql语句从数据库中查找资料")
def sql_query(question: str):
    return sql.ask(question)

@tool(description="从向量存储中检索参考资料。请直接将用户的原始问题原封不动地传入，不要进行任何改写或提炼。")
def rag_summarize(question: str):
    return rag.chain.invoke({"input": question})

if __name__ == '__main__':
    rag = RagSummarizeService()
    res = rag.chain.invoke({"input": "年假怎么计算"})
    print(res)
