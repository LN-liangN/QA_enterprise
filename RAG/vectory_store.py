"""
加载本地知识文档，生成知识向量库
"""

import os
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.config_handler import chroma_config
from model.factory import embed_model
from utils.file_handler import txt_loader, pdf_loader, listdir_with_allowed_type, get_file_md5_hex
from utils.logger_handler import logger
from utils.path_tool import get_abs_path


class VectoryStoreService:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.persist_directory = os.path.join(self.current_dir, chroma_config["persist_directory"])
        self.vectory_store = Chroma(
            collection_name=chroma_config["collection_name"],
            embedding_function=embed_model,
            persist_directory=get_abs_path(chroma_config["persist_directory"]),
        ) # 向量存储实例

        self.spliter = RecursiveCharacterTextSplitter(
            separators = chroma_config["separators"],
            chunk_size = chroma_config["chunk_size"],
            chunk_overlap = chroma_config["chunk_overlap"],
            length_function = len,
        )

    def get_retriever(self):
        return self.vectory_store.as_retriever(search_kwargs={"k": chroma_config["k"]})


    def load_document(self):
        """
        从数据文件夹内读取数据文件，转为向量存入向量库
        要计算文件的md5去重
        :return: None
        """
        def check_md5_hex(md5_doc: str):
            if not os.path.exists(get_abs_path(chroma_config["md5_hex_store"])):
                open(get_abs_path(chroma_config["md5_hex_store"]), 'w', encoding="utf-8").close()
                return False  # 文件没处理过

            with open(get_abs_path(chroma_config["md5_hex_store"]), 'r', encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line == md5_doc:
                        return True  # 文件处理过
                return False  # 文件没处理过

        def save_md5(md5_doc: str):
            with open(get_abs_path(chroma_config["md5_hex_store"]), 'a', encoding='utf-8') as f:
                f.write(md5_doc + "\n")

        def get_file_doc(read_path: str): # 读取文件
            if read_path.endswith(".txt") or read_path.endswith(".md"):
                return txt_loader(read_path)
            if read_path.endswith(".pdf"):
                return pdf_loader(read_path)
            return []

        allowed_file_path = listdir_with_allowed_type(
            get_abs_path(chroma_config["data_path"]), tuple(chroma_config["allow_knowledge_file_type"])
        ) # 读取指定文件格式的文件路径,返回可执行的文件列表

        for file_path in allowed_file_path:
            # 获取文件的md5
            md5_hex = get_file_md5_hex(file_path)
            if check_md5_hex(md5_hex):
                logger.info(f"[加载知识库]{file_path}内容已经存在知识库内")
                continue

            try:
                docs: list[Document] = get_file_doc(file_path)

                if not docs:
                    logger.info(f"[加载知识库]{file_path}内没有有效内容，跳过")
                    continue

                split_docs: list[Document] = self.spliter.split_documents(docs)

                if not split_docs:
                    logger.info(f"[加载知识库]{file_path}分片后没有有效内容")

                # 将内容存入向量库
                self.vectory_store.add_documents(split_docs)
                save_md5(md5_hex)  # 记录这个已经处理好的文件的md5，避免下次重复加载

                logger.info(f"[加载知识库]{file_path}内容加载成功")
            except Exception as e:
                logger.error(f"[加载知识库>]{file_path}加载失败：{str(e)}", exc_info=True)
                continue

if __name__ == "__main__":
    vs = VectoryStoreService()
    # vs.load_document()
    retriever = vs.get_retriever()
    res = retriever.invoke("年假怎么计算")
    for r in res:
        print("-"*20)
        print(r.page_content)



