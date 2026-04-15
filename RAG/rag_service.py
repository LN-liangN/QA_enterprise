
"""
用户提问，搜索参考资料，将提问和参考资料提交给模型，让模型总结回复
"""
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableWithMessageHistory

from model.factory import chat_model
from RAG.vectory_store import VectoryStoreService

"""
chain输入输出检查函数
def print_prompt(prompt):
    print('='*20)
    print(prompt.to_string())
    print('=' * 20)
    return prompt
"""

class RagSummarizeService(object):
    def __init__(self):
        self.vector_store = VectoryStoreService()
        self.retriever = self.vector_store.get_retriever()  # 知识库检索器
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system",
                 "以我提供的资料为主，详细和专业的回答用户的问题，不要生成与参考资料无关的内容，否则会产生错误。参考资料：{context}"),
                ("user", "请回答用户提问：{input}")
            ]
        )
        self.chat_model = chat_model
        self.chain = self.get_chain()


    def get_chain(self):
        retriever = self.retriever
        """
        format函数格式化chain各环节的输入输出
        """
        def format_document_str(docs: list[Document]):
            if not docs:
                return "无相关参考资料"
            formatted_str = ""
            for doc in docs:
                formatted_str += f"文档片段：{doc.page_content}\n文档元数据：{doc.metadata}\n\n"
            return formatted_str

        def formatted_for_retriever(value):
            return value["input"]

        def formatted_for_prompt_template(value):
            new_value = {}
            new_value["input"] = value["input"]["input"]
            new_value["context"] = value["context"]
            return new_value

        chain = (
                {
                    "input": RunnablePassthrough(),
                    "context": RunnableLambda(formatted_for_retriever) | retriever | format_document_str
                } | RunnableLambda(formatted_for_prompt_template) | self.prompt_template |  self.chat_model | StrOutputParser()
        )


        return chain

if __name__ == "__main__":
    rag = RagSummarizeService()
    res = rag.chain.invoke({"input": "年假怎么算？"})
    print(res)