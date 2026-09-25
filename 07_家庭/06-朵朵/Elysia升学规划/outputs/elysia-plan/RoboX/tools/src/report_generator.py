"""报告生成器 - 输出 Markdown 周报和 index.md 索引"""

import os
from datetime import datetime
from typing import Optional


class ReportGenerator:
    """生成 Markdown 格式的结构化分析报告"""

    def __init__(self, report_dir: str, config: dict):
        """
        :param report_dir: 报告输出目录
        :param config: 完整配置
        """
        self.report_dir = report_dir
        self.config = config
        self.dimensions = config.get("dimensions", {})
        self.report_config = config.get("report", {})
        os.makedirs(report_dir, exist_ok=True)

    def generate_report(
        self,
        report_date: str,
        scores: list,
        diff_results: dict,
        documents: list,
        trend_rows: list,
        competitor_summary: str = "",
        new_files: list = None,
        last_report_date: str = "",
    ) -> str:
        """
        生成完整的 Markdown 周报
        :return: 报告文本
        """
        sections_config = self.report_config.get("include_sections", [
            "overview", "paradigm_analysis", "lockin_analysis",
            "trend_panel", "file_manifest", "competitor_dynamics", "recommendations",
        ])

        parts = []

        # 标题页
        parts.append(self._render_header(report_date, last_report_date))

        # 概览
        if "overview" in sections_config:
            parts.append(self._render_overview(scores, diff_results, documents, report_date))

        # 七范式分析
        if "paradigm_analysis" in sections_config:
            parts.append(self._render_paradigm_analysis(scores))

        # 三重锁定分析
        if "lockin_analysis" in sections_config:
            parts.append(self._render_lockin_analysis(scores))

        # 趋势面板
        if "trend_panel" in sections_config:
            parts.append(self._render_trend_panel(trend_rows, report_date))

        # 文件清单
        if "file_manifest" in sections_config:
            parts.append(self._render_file_manifest(documents))

        # 竞对动态
        if "competitor_dynamics" in sections_config and competitor_summary:
            parts.append(self._render_competitor_dynamics(competitor_summary))

        # 改进建议
        if "recommendations" in sections_config:
            parts.append(self._render_recommendations(scores, diff_results))

        report = "\n\n".join(parts)

        # 写入文件
        filename = f"report-{report_date}.md"
        filepath = os.path.join(self.report_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)

        # 更新 index.md
        self._update_index(report_date, filename, scores)

        return report

    def _render_header(self, report_date: str, last_report_date: str) -> str:
        title = self.report_config.get("title", "RoboX 商业模式分析报告")
        subtitle = self.report_config.get("subtitle", "企业商业模式持续追踪")
        return f"""# {title}

> {subtitle}

**报告日期**: {report_date}  
**上一报告**: {last_report_date if last_report_date else '首期报告'}  
**分析框架**: 七范式 + 三重锁定  
**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

"""

    def _render_overview(self, scores: list, diff_results: dict, documents: list, report_date: str) -> str:
        doc_count = len([d for d in documents if d is not None])
        total_chars = sum(d.raw_length for d in documents if d is not None)

        # 统计趋势
        up_count = sum(1 for v in diff_results.values() if v["trend"] == "up")
        down_count = sum(1 for v in diff_results.values() if v["trend"] == "down")
        flat_count = sum(1 for v in diff_results.values() if v["trend"] == "flat")

        # 平均分
        avg_score = sum(s["score"] for s in scores) / max(len(scores), 1)

        # Top 3 / Bottom 3
        top3 = sorted(scores, key=lambda x: x["score"], reverse=True)[:3]
        bottom3 = sorted(scores, key=lambda x: x["score"])[:3]

        lines = [
            "## 一、本周概览",
            "",
            "| 指标 | 数值 |",
            "|------|------|",
            f"| 分析文档数 | {doc_count} |",
            f"| 分析总字数 | {total_chars:,} |",
            f"| 十维度平均分 | **{avg_score:.2f}/10** |",
            f"| 上升维度 | {up_count} ↑ |",
            f"| 下降维度 | {down_count} ↓ |",
            f"| 持平维度 | {flat_count} → |",
            "",
            "### 高活跃度维度（Top 3）",
            "",
        ]

        for i, s in enumerate(top3):
            lines.append(f"{i+1}. **{s['dimension_name']}** — 评分 {s['score']:.1f}/10（{s['evidence_strength']}）")
            lines.append(f"   {s['summary']}")

        lines += [
            "",
            "### 需关注维度（Bottom 3）",
            "",
        ]

        for i, s in enumerate(bottom3):
            lines.append(f"{i+1}. **{s['dimension_name']}** — 评分 {s['score']:.1f}/10（{s['evidence_strength']}）")
            lines.append(f"   {s['summary']}")

        return "\n".join(lines)

    def _render_dimension_detail(self, score: dict, diff: Optional[dict] = None) -> str:
        """渲染单个维度的详细分析"""
        name = score["dimension_name"]
        s = score["score"]
        hit_count = score["hit_count"]

        # 评分条可视化
        bar_len = 20
        filled = int(s / 10 * bar_len)
        bar = "█" * filled + "░" * (bar_len - filled)

        # 趋势箭头
        trend_sign = ""
        if diff:
            if diff["trend"] == "up":
                trend_sign = f" ↑ +{diff['change']:.1f}"
            elif diff["trend"] == "down":
                trend_sign = f" ↓ {diff['change']:.1f}"
            elif diff["trend"] == "flat":
                trend_sign = " → 持平"
            else:
                trend_sign = " ● 新"

        lines = [
            f"### {name}{trend_sign}",
            "",
            f"**评分**: `{s:.1f}/10` | **命中**: {hit_count} 次 | **证据强度**: {score['evidence_strength']}",
            f"",
            f"`{bar}`",
            f"",
            f"**分析摘要**: {score['summary']}",
            f"",
        ]

        # 关键引用
        quotes = score.get("key_quotes", [])
        if quotes:
            lines.append("**关键引用**:")
            for q in quotes[:3]:
                lines.append(f"> {q}")
            lines.append("")

        # 分项得分
        lines.extend([
            f"| 分项 | 得分 |",
            f"|------|------|",
            f"| 命中密度 | {score['density_score']:.1f}/10 |",
            f"| 证据强度 | {score['evidence_score']:.1f}/10 |",
            f"| 时间新鲜度 | {score['freshness_score']:.1f}/10 |",
            f"",
        ])

        return "\n".join(lines)

    def _render_paradigm_analysis(self, scores: list) -> str:
        """渲染七范式分析"""
        paradigm_scores = [s for s in scores if s["category"] == "paradigm"]
        if not paradigm_scores:
            return ""

        lines = [
            "## 二、七范式——合作协同分析",
            "",
            "> 按七种合作协同范式对各维度的本周活跃度和证据强度进行独立分析。",
            "",
        ]

        for score in paradigm_scores:
            lines.append(self._render_dimension_detail(score))

        return "\n".join(lines)

    def _render_lockin_analysis(self, scores: list) -> str:
        """渲染三重锁定分析"""
        lockin_scores = [s for s in scores if s["category"] == "lockin"]
        if not lockin_scores:
            return ""

        lines = [
            "## 三、三重锁定——竞争壁垒分析",
            "",
            "> 按三种锁定机制评估 RoboX 的竞争壁垒建设进度。",
            "",
        ]

        for score in lockin_scores:
            lines.append(self._render_dimension_detail(score))

        # 综合风险评估
        lines.append("### 锁定健康度综合")
        lines.append("")
        avg_lock = sum(s["score"] for s in lockin_scores) / max(len(lockin_scores), 1)

        if avg_lock >= 7:
            health = "🟢 健康"
            advice = "三重锁定均在积极推进中，护城河建设良好。建议持续保持力度。"
        elif avg_lock >= 4:
            health = "🟡 关注"
            advice = "部分锁定机制存在问题或推进缓慢，建议重点关注低分维度。"
        else:
            health = "🔴 警示"
            advice = "多个锁定机制表现薄弱，竞争壁垒面临风险，需紧急采取措施。"

        lines.append(f"**锁定健康度**: {health}（平均 {avg_lock:.1f}/10）")
        lines.append(f"")
        lines.append(f"> {advice}")
        lines.append("")

        return "\n".join(lines)

    def _render_trend_panel(self, trend_rows: list, report_date: str) -> str:
        """渲染趋势面板"""
        if not trend_rows:
            return "## 四、趋势面板\n\n> 暂无足够历史数据生成趋势面板（需至少2周数据）。\n"

        lines = ["## 四、趋势面板（最近4周）", ""]

        # 生成 Markdown 表格
        dates = trend_rows[0]["dates"] if trend_rows else []
        date_headers = " | ".join(dates)
        lines.append(f"| 维度 | {date_headers} | 趋势 |")

        score_headers = " | ".join(["-:" for _ in dates])
        lines.append(f"|------|{score_headers}|:--:|")

        for row in trend_rows:
            score_strs = " | ".join([f"{s:.1f}" for s in row["scores"]])
            lines.append(f"| {row['dimension']} | {score_strs} | {row['trend_icon']} |")

        lines += ["", "*注：趋势箭头基于最近两周变化。*", ""]
        return "\n".join(lines)

    def _render_file_manifest(self, documents: list) -> str:
        """渲染本周分析文件清单"""
        valid_docs = [d for d in documents if d is not None]
        if not valid_docs:
            return "## 五、文件清单\n\n> 本周期未发现新文件。\n"

        lines = [
            "## 五、分析文件清单",
            "",
            f"共扫描 **{len(valid_docs)}** 份文件，总字符数 {sum(d.raw_length for d in valid_docs):,}。",
            "",
            "| 文件 | 类型 | 日期 | 字符数 |",
            "|------|------|------|--------|",
        ]

        for doc in valid_docs:
            fname = os.path.basename(doc.path)
            date_str = doc.date.strftime('%Y-%m-%d') if doc.date else "未知"
            d_type = {"transcript": "转写", "minutes": "纪要", "docx": "文档"}.get(doc.doc_type, doc.doc_type)
            lines.append(f"| {fname} | {d_type} | {date_str} | {doc.raw_length:,} |")

        return "\n".join(lines)

    def _render_competitor_dynamics(self, competitor_summary: str) -> str:
        """渲染竞对动态"""
        return f"## 六、竞争对手动态\n\n{competitor_summary}\n"

    def _render_recommendations(self, scores: list, diff_results: dict) -> str:
        """渲染改进建议"""
        low_scores = [s for s in scores if s["score"] < 4.0]
        declining = [
            s for s in scores
            if diff_results.get(s["dimension"], {}).get("trend") == "down"
        ]

        lines = ["## 七、改进建议与行动项", ""]

        if low_scores:
            lines.append("### 重点改进维度（评分 < 4.0）")
            for s in low_scores:
                lines.append(f"- **{s['dimension_name']}**（{s['score']:.1f}/10）：{s['summary']}")
                lines.append(f"  - 建议：增加该维度在团队讨论和外部分享中的覆盖密度。")
            lines.append("")

        if declining:
            lines.append("### 下降趋势维度")
            for s in declining:
                change = diff_results.get(s["dimension"], {}).get("change", 0)
                lines.append(f"- **{s['dimension_name']}**：较上周 {change:+.1f}，需关注为何活跃度下降。")
            lines.append("")

        if not low_scores and not declining:
            lines.append("本周各维度表现良好，未发现需要紧急干预的低分或下降维度。保持当前推进节奏即可。")
            lines.append("")

        lines.append("### 常规建议")
        lines.append("- 确保每次对外沟通中覆盖至少 3 个范式的差异化表述")
        lines.append("- 每两周更新一次锁定机制的进展状态")
        lines.append("- 关注竞对在触觉和 System 2 方向的最新动作")

        return "\n".join(lines)

    def _update_index(self, report_date: str, filename: str, scores: list):
        """更新 index.md 汇总索引"""
        index_path = os.path.join(self.report_dir, "index.md")

        avg_score = sum(s["score"] for s in scores) / max(len(scores), 1)

        existing = ""
        if os.path.exists(index_path):
            with open(index_path, 'r', encoding='utf-8') as f:
                existing = f.read()
        else:
            existing = "# RoboX 商业模式分析报告索引\n\n> 基于七范式与三重锁定框架\n\n| 报告日期 | 文件 | 平均分 | 备注 |\n|----------|------|--------|------|\n"

        new_entry = f"| {report_date} | [{filename}](./{filename}) | {avg_score:.2f} | - |"

        if new_entry not in existing:
            existing += "\n" + new_entry

        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(existing)
