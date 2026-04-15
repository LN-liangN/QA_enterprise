"""
为整个工程提供绝对路径
"""

import os

def get_project_root() -> str:
    """
    获取工程所在根目录
    :return: 字符串根目录
    """
    current_file = os.path.abspath(__file__)  # 当前文件的绝对路径path_tool.py
    current_dir = os.path.dirname(current_file)  # 路径向上跳一级
    project_root = os.path.dirname(current_dir)  # 路径向上跳一级,根目录
    return project_root


def get_abs_path(relative_path: str) -> str:
    """
    传递相对路径，得到绝对路径
    :param relative_path:
    :return: 绝对路径
    """
    return os.path.join(get_project_root(), relative_path)

if __name__ == '__main__':
    from QA_enterprise.utils.config_handler import chroma_config
    path1 = get_project_root()
    print(path1)
    path2 = get_abs_path(path1)
    print(path2)
    print(get_abs_path(chroma_config["data_path"]))