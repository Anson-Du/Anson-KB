"""关键词引擎 - 从配置加载词库，对文档执行正则匹配"""

import re
from collections import defaultdict
from datetime import datetime
from typing import Optional

from .document import Document, Section


def _safe_isoformat(dt):
    """安全转换为 ISO 格式"""
    if dt.tzinfo is not None:
        dt = dt.replace(tzinfo=None)
    return dt.isoformat()


class KeywordEngine:
    """关键词匹配引擎"""

    def __init__(self, config: dict):
        """
        初始化引擎
        :param config: 从 config.yaml 加载的完整配置字典
        """
        self.dimensions = config.get("dimensions", {})
        self._compiled_patterns = self._compile_patterns()

    def _compile_patterns(self) -> dict:
        """预编译所有维度的正则表达式"""
        compiled = {}
        for dim_key, dim_config in self.dimensions.items():
            keywords = dim_config.get("keywords", [])
            patterns = []
            for kw in keywords:
                try:
                    patterns.append(re.compile(kw, re.IGNORECASE))
                except re.error:
                    # 无效正则时作为纯文本
                    patterns.append(re.compile(re.escape(kw), re.IGNORECASE))
            compiled[dim_key] = patterns
        return compiled

    def analyze_document(self, doc: Document) -> dict:
        """
        对文档执行全维度关键词分析
        :return: {dim_key: [(keyword_pattern, context_text, section_heading), ...]}
        """
        results = defaultdict(list)

        for section in doc.sections:
            text = section.content
            if len(text) < 3:
                continue

            for dim_key, patterns in self._compiled_patterns.items():
                for pattern in patterns:
                    for match in pattern.finditer(text):
                        # 提取上下文（前后各 40 字符）
                        start = max(0, match.start() - 40)
                        end = min(len(text), match.end() + 40)
                        context = text[start:end].replace('\n', ' ')
                        results[dim_key].append({
                            "keyword": pattern.pattern,
                            "match": match.group(),
                            "context": f"...{context}...",
                            "heading": section.heading,
                            "speaker": section.speaker,
                        })

        # 更新 section 级别的 keywords_found
        for section in doc.sections:
            section.keywords_found = {}
            for dim_key, matches in results.items():
                section_matches = [m for m in matches if m["heading"] == section.heading]
                if section_matches:
                    section.keywords_found[dim_key] = section_matches

        return dict(results)

    def analyze_all(self, documents: list) -> dict:
        """
        对所有文档执行全维度分析
        :return: {dim_key: [aggregated_matches across all docs]}
        """
        all_results = defaultdict(list)

        for doc in documents:
            if doc is None:
                continue
            doc_results = self.analyze_document(doc)
            for dim_key, matches in doc_results.items():
                for m in matches:
                    m["doc_path"] = doc.path
                    m["doc_date"] = _safe_isoformat(doc.date)
                    m["doc_type"] = doc.doc_type
                all_results[dim_key].extend(matches)

        return dict(all_results)

    def get_dimension_stats(self, dim_key: str, matches: list, total_chars: int) -> dict:
        """
        计算单个维度的统计信息
        :param dim_key: 维度键名
        :param matches: 命中列表
        :param total_chars: 文档总字符数
        """
        if total_chars == 0:
            total_chars = 1

        hit_count = len(matches)
        hit_density = (hit_count / total_chars) * 1000  # 每千字命中密度

        # 唯一关键词数
        unique_keywords = set(m["keyword"] for m in matches)

        # 统计来自纪要格式的命中有多少（证据强度更高）
        minutes_hits = sum(1 for m in matches if m.get("doc_type") == "minutes")

        return {
            "hit_count": hit_count,
            "hit_density": round(hit_density, 4),
            "unique_keywords": len(unique_keywords),
            "minutes_hits": minutes_hits,
            "unique_docs": len(set(m.get("doc_path", "") for m in matches)),
        }
