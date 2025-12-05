import json
import os

def get_available_datasets():
    """扫描 data 目录，返回所有可用 json 文件列表"""
    data_dir = "data"
    if not os.path.exists(data_dir):
        return []
    # 只读取 .json 文件
    files = [f for f in os.listdir(data_dir) if f.endswith(".json")]
    return sorted(files)

def load_data(filename):
    """读取指定的数据文件"""
    file_path = os.path.join("data", filename)
    if not os.path.exists(file_path):
        return []
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return []