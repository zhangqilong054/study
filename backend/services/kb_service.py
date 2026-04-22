import json
import logging
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import KNOWLEDGE_BASE_PATH

logger = logging.getLogger(__name__)

_KB_CACHE = {
    "mtime": None,
    "data": {},
}

_STOP_WORDS = {
    "请问",
    "如何",
    "怎么",
    "怎样",
    "什么",
    "一下",
    "详细",
    "说明",
    "需要",
    "可以",
    "注意事项",
    "吗",
    "呢",
    "的",
}


def load_knowledge_base():
    """加载校园知识库（带文件变更缓存）"""
    if not os.path.exists(KNOWLEDGE_BASE_PATH):
        return {}

    try:
        mtime = os.path.getmtime(KNOWLEDGE_BASE_PATH)
    except OSError:
        return {}

    if _KB_CACHE["mtime"] == mtime and _KB_CACHE["data"]:
        return _KB_CACHE["data"]

    try:
        with open(KNOWLEDGE_BASE_PATH, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError):
        logger.exception("知识库加载失败：%s", KNOWLEDGE_BASE_PATH)
        return {}

    _KB_CACHE["mtime"] = mtime
    _KB_CACHE["data"] = data
    return data


def _extract_keywords(query):
    query = (query or "").strip().lower()
    if not query:
        return []

    tokens = re.findall(r"[\u4e00-\u9fff]{2,}|[a-z0-9]{2,}", query)

    expanded = []
    for token in tokens:
        # 中文长串（无空格）做 2 字切片，提升召回率
        if re.fullmatch(r"[\u4e00-\u9fff]+", token) and len(token) > 4:
            for i in range(len(token) - 1):
                expanded.append(token[i : i + 2])
            expanded.append(token)
        else:
            expanded.append(token)

    filtered = [t for t in expanded if t not in _STOP_WORDS]

    # 去重并保序
    deduped = []
    seen = set()
    for t in filtered:
        if t in seen:
            continue
        seen.add(t)
        deduped.append(t)

    # 防止全是停用词导致无结果
    if deduped:
        return deduped[:20]
    return [query[:20]]


def search_knowledge(query, category=None):
    """在知识库中检索相关内容"""
    kb = load_knowledge_base()
    if not kb:
        return []

    query = (query or "").strip().lower()
    if not query:
        return []

    keywords = _extract_keywords(query)
    target = kb.get(category, kb) if category and category in kb else kb
    scored_results = []

    def _search(data, path=""):
        if isinstance(data, dict):
            for key, val in data.items():
                _search(val, f"{path}/{key}" if path else key)
        elif isinstance(data, list):
            for item in data:
                _search(item, path)
        elif isinstance(data, str):
            haystack = data.lower()
            path_lower = path.lower()
            score = 0

            for kw in keywords:
                if kw in haystack:
                    score += 2
                if kw in path_lower:
                    score += 1

            if query in haystack:
                score += 3

            if score > 0:
                scored_results.append(
                    {
                        "path": path,
                        "content": data,
                        "score": score,
                    }
                )

    _search(target)

    # 去重 + 按分数排序
    seen = set()
    deduped = []
    for item in sorted(scored_results, key=lambda x: x["score"], reverse=True):
        key = (item["path"], item["content"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append({"path": item["path"], "content": item["content"]})
        if len(deduped) >= 5:
            break

    return deduped


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
