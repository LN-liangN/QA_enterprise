"""
读取配置文件的工具(函数)
yaml
｛k: v｝
"""
import yaml
from utils.path_tool import get_abs_path


def load_rag_config(config_path: str=get_abs_path("config/rag.yml"), encoding="utf-8"):
    """
    rag相关的配置文件
    """
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)

def load_chroma_config(config_path: str=get_abs_path("config/chroma.yml"), encoding="utf-8"):
    """
    chroma相关的配置文件
    """
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)

def load_prompts_config(config_path: str=get_abs_path("config/prompts.yml"), encoding="utf-8"):
    """
    prompts相关的配置文件
    """
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


rag_config = load_rag_config()
chroma_config = load_chroma_config()
prompts_config = load_prompts_config()
