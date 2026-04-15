# 🤖 LangChain ReAct 企业智能问答助手 Skill


## 项目概述

- 本项目构建智能问答系统，能够同时查询**结构化数据**（员工信息、项目记录、考勤数据等）和**结构化知识**（公司制度、技术文档、会议纪要等），回答员工的各种工作相关问题。

---

## 核心特性

#### 1. ReAct skill 多工具调用
- 集成结构化数据和结构化知识信息查询、用户信息获取等工具能力，支持 SKill 根据任务自动选择合适工具完成辅助推理。

#### 2. RAG 检索增强问答
- 基于向量数据库构建知识库检索能力，支持对企业结构化知识相关文档进行召回与问答生成，提升回复准确性。

#### 3. SQL query
- 基于数据库构建结构化知识检索能力，提升回复准确性。

#### 4. Streamlit 流式对话界面
- 提供可交互的聊天界面，支持流式输出，便于展示完整的 Agent 问答过程与使用体验。

#### 5. 模块化工程结构
- 项目按 Skill、RAG、SQL、模型层、配置层、工具层等模块进行拆分，便于理解整体架构并支持后续扩展。

---
## 项目结构

```bash
.
├── skill/                       # skill 核心逻辑
│   ├── skill.py                 # ReAct智能体主逻辑
│   ├── tools/                   # 工具函数集合
│   └── middleware.py            # 中间件管理
├── SQL/                         # 数据库查询逻辑
│   ├── SQL_query.py             # 数据库查询
├── RAG/                         # 知识库文档查询逻辑
│   └── vectory_store.py         # 加载本地知识库
│   └── rag_service.py           # 知识库文档查询
├── model/                       # 模型工厂与模型初始化
├── prompts/                     # 提示词模板
│   ├── main_prompt.txt          # skill问答提示词模板
│   ├── rag_prompt.txt           # 知识库检索提示词模板
│   ├── SQL_prompt.txt           # 数据库查询提示词模板
├── utils/                       # 通用工具函数
│   ├── config_handler.py        # 配置加载
│   └── file_handler.py          # 文件处理
│   └── logger_handler.py        # 日志管理
│   └── path_tool.py             # 路径工具
│   └── prompts_loader.py        # 提示词加载
├── skill_app.py                 # Streamlit 应用入口
├── md5.txt                      # 本地文件加载去重
├── requirements.txt
└── README.md
```

## 工作流程


1. 用户在 Streamlit 页面输入问题

2. Skill 判断当前任务类型 -> 普通问答 / 总结生成

3. 普通问答场景下，调用 RAG 模块检索知识库内容

4. 普通问答场景下，调用 SQL 模块检索数据库内容

5. 最终结果通过流式方式返回到前端界面