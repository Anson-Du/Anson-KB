"""快照管理器 - JSON 快照写入和历史 diff 对比"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional


def _safe_isoformat(dt: datetime) -> str:
    """安全转换为 ISO 格式，处理时区信息"""
    if dt.tzinfo is not None:
        dt = dt.replace(tzinfo=None)
    return dt.isoformat()


class SnapshotManager:
    """管理分析快照的存储、读取和对比"""

    VERSION = "1.0.0"

    def __init__(self, snapshot_dir: str):
        """
        :param snapshot_dir: 快照存储目录
        """
        self.snapshot_dir = snapshot_dir
        os.makedirs(snapshot_dir, exist_ok=True)

    def create_snapshot(
        self,
        report_date: str,
        scores: list,
        documents: list,
        config_meta: dict,
    ) -> dict:
        """
        创建快照数据
        :param report_date: 报告日期 YYYY-MM-DD
        :param scores: 评分结果列表
        :param documents: 分析文档列表
        :param config_meta: 配置元数据
        """
        snapshot = {
            "version": self.VERSION,
            "report_date": report_date,
            "generated_at": datetime.now().isoformat(),
            "dimension_scores": {s["dimension"]: s for s in scores},
            "documents_scanned": [
                {
                    "path": doc.path,
                    "date": _safe_isoformat(doc.date),
                    "type": doc.doc_type,
                    "title": doc.title,
                    "chars": doc.raw_length,
                }
                for doc in documents if doc is not None
            ],
            "document_count": len([d for d in documents if d is not None]),
            "total_chars_analyzed": sum(d.raw_length for d in documents if d is not None),
            "config_meta": config_meta,
        }

        # 写入文件
        filename = f"{report_date}.json"
        filepath = os.path.join(self.snapshot_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(snapshot, f, ensure_ascii=False, indent=2)

        return snapshot

    def load_snapshot(self, date_str: str) -> Optional[dict]:
        """加载指定日期的快照"""
        filepath = os.path.join(self.snapshot_dir, f"{date_str}.json")
        if not os.path.exists(filepath):
            return None
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def load_latest_snapshot(self) -> Optional[dict]:
        """加载最新快照（排除当前报告日期）"""
        snapshots = self.list_snapshots()
        if not snapshots:
            return None
        latest_file = sorted(snapshots, reverse=True)[0]
        with open(os.path.join(self.snapshot_dir, latest_file), 'r', encoding='utf-8') as f:
            return json.load(f)

    def load_recent_snapshots(self, count: int = 4) -> list:
        """
        加载最近 count 周的快照（按日期降序）
        :return: [(date_str, snapshot_dict), ...]
        """
        files = sorted(self.list_snapshots(), reverse=True)[:count]
        snapshots = []
        for f in files:
            date_str = f.replace('.json', '')
            with open(os.path.join(self.snapshot_dir, f), 'r', encoding='utf-8') as fp:
                snapshots.append((date_str, json.load(fp)))
        return snapshots

    def diff_with_previous(self, current_scores: list) -> dict:
        """
        与上一周快照进行 diff 对比
        :param current_scores: 当前评分列表
        :return: {dim_key: {"current": float, "previous": float|None, "change": float, "trend": "up"|"down"|"flat"|"new"}}
        """
        previous = self.load_latest_snapshot()
        current_map = {s["dimension"]: s["score"] for s in current_scores}

        diff_results = {}

        for dim_key, current_score in current_map.items():
            prev_data = None
            prev_score = None
            if previous and "dimension_scores" in previous:
                prev_data = previous["dimension_scores"].get(dim_key)
                if prev_data:
                    prev_score = prev_data.get("score")

            if prev_score is not None:
                change = round(current_score - prev_score, 2)
                if abs(change) < 0.3:
                    trend = "flat"
                elif change > 0:
                    trend = "up"
                else:
                    trend = "down"
            else:
                change = 0
                trend = "new"

            diff_results[dim_key] = {
                "current": current_score,
                "previous": prev_score,
                "change": change,
                "trend": trend,
            }

        return diff_results

    def generate_trend_table(self, dim_names: dict, weeks: int = 4) -> list:
        """
        生成趋势面板数据（最近 weeks 周评分表格）
        :param dim_names: {dim_key: display_name}
        :return: [{dimension, dates: [str], scores: [float], trend_icon: str}, ...]
        """
        recent = self.load_recent_snapshots(weeks)

        if not recent:
            return []

        # 按时间正序
        recent = list(reversed(recent))
        dates = [r[0] for r in recent]

        trend_rows = []
        for dim_key, name in dim_names.items():
            scores = []
            for _, snap in recent:
                dim_data = snap.get("dimension_scores", {}).get(dim_key, {})
                scores.append(dim_data.get("score", 0))

            # 趋势方向
            if len(scores) >= 2:
                if scores[-1] > scores[-2] + 0.3:
                    icon = "↗"
                elif scores[-1] < scores[-2] - 0.3:
                    icon = "↘"
                else:
                    icon = "→"
            else:
                icon = "·"

            trend_rows.append({
                "dimension": name,
                "dim_key": dim_key,
                "dates": dates,
                "scores": scores,
                "trend_icon": icon,
            })

        return trend_rows

    def list_snapshots(self) -> list:
        """列出所有快照文件名"""
        if not os.path.exists(self.snapshot_dir):
            return []
        return sorted([
            f for f in os.listdir(self.snapshot_dir)
            if f.endswith('.json') and not f.startswith('.')
        ])
