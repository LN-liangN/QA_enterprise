from utils.config_handler import prompts_config
from utils.logger_handler import logger
from utils.path_tool import get_abs_path

def load_system_prompts():
    try:
        system_prompts_path = get_abs_path(prompts_config["system_prompt_path"])  # prompts_config返回yaml文件的字典内容key和value
    except KeyError as e:
        logger.error(f"[load_system_prompts]在yaml配置项中没有system提示词[system_prompt_path]配置项")
        raise e

    try:
        return open(system_prompts_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_system_prompts]解析system提示词错误， {str(e)}")
        raise e

def load_sql_prompts():
    try:
        sql_prompts_path = get_abs_path(prompts_config["SQL_prompts_path"])
    except KeyError as e:
        logger.error(f"[load_sql_prompts]在yaml配置项中没有sql提示词[SQL_prompts_path]配置项")
        raise e

    try:
        return open(sql_prompts_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_sql_prompts]解析rag提示词错误， {str(e)}")
        raise e

def load_rag_prompts():
    try:
        rag_prompts_path = get_abs_path(prompts_config["rag_prompts_path"])
    except KeyError as e:
        logger.error(f"[load_rag_prompts]在yaml配置项中没有rag提示词[rag_prompts_path]配置项")
        raise e

    try:
        return open(rag_prompts_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_rag_prompts]解析rag提示词错误， {str(e)}")
        raise e


if __name__ == "__main__":
    res = load_sql_prompts()
    print(res)


