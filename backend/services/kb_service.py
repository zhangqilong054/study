import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import KNOWLEDGE_BASE_PATH


def load_knowledge_base():
    """加载校园知识库"""
    if os.path.exists(KNOWLEDGE_BASE_PATH):
        with open(KNOWLEDGE_BASE_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}


def search_knowledge(query, category=None):
    """在知识库中检索相关内容"""
    kb = load_knowledge_base()
    results = []
    query_lower = query.lower()

    target = kb.get(category, kb) if category and category in kb else kb

    def _search(data, path=""):
        if isinstance(data, dict):
            for key, val in data.items():
                _search(val, f"{path}/{key}" if path else key)
        elif isinstance(data, list):
            for item in data:
                _search(item, path)
        elif isinstance(data, str):
            if any(kw in data.lower() for kw in query_lower.split()):
                results.append({"path": path, "content": data})

    _search(target)
    return results[:5]


def get_affair_info(affair_type):
    """获取特定事务的知识库内容"""
    kb = load_knowledge_base()
    affairs = kb.get("affairs", {})
    for key, val in affairs.items():
        if affair_type in key or key in affair_type:
            return val
    return None


def get_all_affair_types():
    """获取所有事务类型"""
    kb = load_knowledge_base()
    affairs = kb.get("affairs", {})
    return list(affairs.keys())
