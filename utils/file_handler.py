import os
import hashlib
from xml.dom.minidom import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader

from utils.logger_handler import logger


def get_file_md5_hex(filepath: str): # 获取文件的md5的十六进制字符串

    if not os.path.exists(filepath):
        logger.error(f"[md5计算]文件 {filepath} 不存在")
        return

    if not os.path.isfile(filepath):
        logger.error(f"[md5计算]路径 {filepath} 不是文件")
        return

    md5_obj = hashlib.md5()
    chunk_size = 1024  # 1KB分片，避免文件过大爆内存
    try:
        with open(filepath, "rb") as f:    # 必须二进制读取
            while chunk := f.read(chunk_size):
                md5_obj.update(chunk)  # 使用md5对象转化字节数组，更新

            md5_hex = md5_obj.hexdigest()
            return md5_hex
    except  Exception as e:
        logger.error(f"计算文件 {filepath} md5失败，{str(e)}")
        return None


def listdir_with_allowed_type(path: str, allowed_types: tuple[str]): # 返回文件夹内的文件列表(允许的文件后缀)
    files = []
    if not os.path.isdir(path):
        logger.error(f"{path}不是文件夹")
        return allowed_types
    for f in os.listdir(path):
        if f.endswith(allowed_types):
            files.append(os.path.join(path, f))
    return tuple(files)



def pdf_loader(filepath: str, password=None) -> list[Document]: # 使用pdfplumber提取文本
    return PyPDFLoader(filepath, password).load()

def txt_loader(filepath: str) -> list[Document]:
    return TextLoader(filepath, encoding="utf-8").load()
