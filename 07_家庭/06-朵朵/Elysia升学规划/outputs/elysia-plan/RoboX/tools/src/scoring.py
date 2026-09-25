"""评分计算器 - 基于命中密度、证据强度、时间新鲜度计算 0-10 分加权评分"""

import re
from datetime import datetime
from typing import Optional


class ScoringCalculator:
    """十维度加权评分计算器"""

    def __init__(self, config: dict):
        """
        :param config: 评分配置（config.yaml 中的 weights 部分 + dimensions 部分）
        """
        self.weights = config.get("weights", {
            "hit_density": 0.50,
            "evidence_strength": 0.35,
            "freshness": 0.15,
        })
        self.dimensions = config.get("dimensions", {})
        self._quant_pattern = re.compile(r'\d+[万千百万亿]?[小时台个套家次]|[0-9,.]+[BKMG]?[bhw]?')

    def score_dimension(
        self,
        dim_key: str,
        matches: list,
        stats: dict,
        doc_freshness_scores: dict,
        total_docs: int,
        max_hit_density: float = 1.0,
    ) -> dict:
        """
        计算单个维度的 0-10 分加权评分
        :param dim_key: 维度键名
        :param matches: 该维度的所有命中
        :param stats: 统计信息（来自 keyword_engine.get_dimension_stats）
        :param doc_freshness_scores: {doc_path: freshness_coefficient}
        :param total_docs: 总文档数
        :param max_hit_density: 归一化参考最大命中密度
        """
        dim_config = self.dimensions.get(dim_key, {})

        # ---- 1. 命中密度分（0-10） ----
        hit_density = stats.get("hit_density", 0)
        if max_hit_density > 0:
            density_score = min(10.0, (hit_density / max_hit_density) * 10.0)
        else:
            density_score = 0.0

        # ---- 2. 证据强度分（0-10） ----
        # 纪要格式权重更高 + 量化数据存在加分
        minutes_ratio = stats.get("minutes_hits", 0) / max(stats.get("hit_count", 1), 1)
        has_quant = self._check_quant_data(matches)
        evidence_score = minutes_ratio * 6.0 + (2.0 if has_quant else 0.0) + \
                         min(2.0, stats.get("unique_docs", 0) * 0.5)
        evidence_score = min(10.0, evidence_score)

        # ---- 3. 时间新鲜度分（0-10） ----
        # 取涉及文档的平均新鲜度
        involved_docs = set(m.get("doc_path", "") for m in matches)
        if involved_docs and doc_freshness_scores:
            avg_freshness = sum(
                doc_freshness_scores.get(dp, 0.5) for dp in involved_docs
            ) / len(involved_docs)
        else:
            avg_freshness = 0.3
        freshness_score = avg_freshness * 10.0

        # ---- 4. 加权总分 ----
        raw_score = (
            self.weights["hit_density"] * density_score +
            self.weights["evidence_strength"] * evidence_score +
            self.weights["freshness"] * freshness_score
        )

        # 维度权重修正
        dim_weight = dim_config.get("weighting", 1.0)
        final_score = min(10.0, raw_score * dim_weight)

        # ---- 5. 证据摘要 ----
        evidence_strength = self._classify_evidence(hit_density, evidence_score, freshness_score)

        # 提取关键引用（取前5条，优先来自纪要的）
        key_quotes = self._extract_key_quotes(matches, max_quotes=5)

        # 生成摘要
        summary = self._generate_summary(dim_key, stats, evidence_strength, final_score)

        return {
            "dimension": dim_key,
            "dimension_name": dim_config.get("name", dim_key),
            "category": dim_config.get("category", "unknown"),
            "score": round(final_score, 2),
            "raw_score": round(raw_score, 2),
            "density_score": round(density_score, 2),
            "evidence_score": round(evidence_score, 2),
            "freshness_score": round(freshness_score, 2),
            "hit_count": stats.get("hit_count", 0),
            "hit_density": stats.get("hit_density", 0),
            "evidence_strength": evidence_strength,
            "unique_docs": stats.get("unique_docs", 0),
            "key_quotes": key_quotes,
            "summary": summary,
        }

    def score_all(
        self,
        all_matches: dict,
        all_stats: dict,
        documents: list,
    ) -> list:
        """
        对所有维度进行评分
        :return: 按评分降序排列的 DimensionScore 列表
        """
        # 计算文档新鲜度
        doc_freshness_scores = {}
        for doc in documents:
            if doc:
                doc_freshness_scores[doc.path] = doc.freshness_coefficient

        total_docs = len([d for d in documents if d is not None])

        # 找出最大命中密度用于归一化
        max_density = 0.001
        for stats in all_stats.values():
            if stats.get("hit_density", 0) > max_density:
                max_density = stats["hit_density"]

        scores = []
        for dim_key in self.dimensions:
            matches = all_matches.get(dim_key, [])
            stats = all_stats.get(dim_key, {
                "hit_count": 0, "hit_density": 0,
                "unique_keywords": 0, "minutes_hits": 0, "unique_docs": 0,
            })
            score = self.score_dimension(
                dim_key=dim_key,
                matches=matches,
                stats=stats,
                doc_freshness_scores=doc_freshness_scores,
                total_docs=total_docs,
                max_hit_density=max_density,
            )
            scores.append(score)

        # 按评分降序排列
        scores.sort(key=lambda x: x["score"], reverse=True)
        return scores

    def _check_quant_data(self, matches: list) -> bool:
        """检查是否包含量化数据"""
        for m in matches:
            if self._quant_pattern.search(m.get("context", "")):
                return True
        return False

    def _classify_evidence(self, hit_density: float, evidence_score: float, freshness_score: float) -> str:
        """分类证据强度"""
        combined = evidence_score * 0.6 + (min(hit_density * 100, 10)) * 0.4
        if combined >= 7.0:
            return "strong"
        elif combined >= 4.0:
            return "moderate"
        return "weak"

    def _extract_key_quotes(self, matches: list, max_quotes: int = 5) -> list:
        """提取关键引用，优先纪要格式"""
        # 排序：纪要优先 -> 上下文长度适中优先
        sorted_matches = sorted(
            matches,
            key=lambda m: (
                0 if m.get("doc_type") == "minutes" else 1,
                -(len(m.get("context", ""))),
            )
        )
        seen = set()
        quotes = []
        for m in sorted_matches:
            context = m.get("context", "")
            # 去重相似的上下文
            key = context[:30]
            if key not in seen and len(context) > 10:
                seen.add(key)
                quotes.append(f"**[{m.get('doc_path', '?')}]** {context.strip()}")
                if len(quotes) >= max_quotes:
                    break
        return quotes

    def _generate_summary(self, dim_key: str, stats: dict, evidence_strength: str, score: float) -> str:
        """生成维度分析摘要"""
        dim_config = self.dimensions.get(dim_key, {})
        name = dim_config.get("name", dim_key)
        hit_count = stats.get("hit_count", 0)
        unique_docs = stats.get("unique_docs", 0)

        evidence_labels = {"strong": "证据充分", "moderate": "证据中等", "weak": "证据较弱"}
        ev_label = evidence_labels.get(evidence_strength, "待观察")

        if score >= 7.0:
            status = "活跃推进中"
        elif score >= 4.0:
            status = "持续关注中"
        elif score >= 2.0:
            status = "有提及但推进缓慢"
        else:
            status = "本周期未见显著提及"

        return (
            f"{name}：{status}（评分 {score:.1f}/10）。"
            f"共命中 {hit_count} 次，覆盖 {unique_docs} 份文档，{ev_label}。"
        )
