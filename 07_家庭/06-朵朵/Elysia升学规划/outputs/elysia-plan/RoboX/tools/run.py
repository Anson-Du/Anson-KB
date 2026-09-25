#!/usr/bin/env python3
"""
RoboX 商业模式自动化分析工具 - 主入口
========================================
按照"七范式 + 三重锁定"框架，扫描工作区文档，
进行十维度加权评分分析，生成 Markdown 周报和 JSON 历史快照。

用法:
    python run.py                          # 默认：增量分析
    python run.py --force                  # 全量重新分析
    python run.py --date 2026-08-07        # 指定报告日期
    python run.py --force --date 2026-08-07
"""

import argparse
import logging
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

import yaml

# 添加 src 到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.document import Document
from src.text_parser import TextParser
from src.docx_parser import DocxParser
from src.keyword_engine import KeywordEngine
from src.scoring import ScoringCalculator
from src.snapshot_manager import SnapshotManager
from src.report_generator import ReportGenerator


def setup_logging(log_dir: str, report_date: str):
    """配置日志系统"""
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"run_{report_date}.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(),
        ],
    )
    return logging.getLogger("RoboX-Analyzer")


def load_config(config_path: str) -> dict:
    """加载 YAML 配置"""
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def scan_documents(
    workspace_root: str,
    scan_dirs: list,
    text_parser: TextParser,
    docx_parser: DocxParser,
    force: bool = False,
) -> list:
    """
    扫描工作区文档
    :return: Document 对象列表
    """
    documents = []
    supported_types = {'.txt': text_parser, '.docx': docx_parser}
    last_week = datetime.now() - timedelta(days=7)

    for scan_dir in scan_dirs:
        full_dir = os.path.join(workspace_root, scan_dir)
        if not os.path.exists(full_dir):
            logging.warning(f"目录不存在，跳过: {full_dir}")
            continue

        for root, dirs, files in os.walk(full_dir):
            for filename in files:
                # 跳过临时文件和隐藏文件
                if filename.startswith('~$') or filename.startswith('.'):
                    continue

                ext = os.path.splitext(filename)[1].lower()
                if ext not in supported_types:
                    continue

                file_path = os.path.relpath(os.path.join(root, filename), workspace_root)
                # 替换反斜杠为斜杠
                file_path = file_path.replace('\\', '/')

                parser = supported_types[ext]

                # 增量模式：检查文件修改时间
                if not force:
                    full_path = os.path.join(workspace_root, file_path)
                    mtime = datetime.fromtimestamp(os.path.getmtime(full_path))
                    if mtime < last_week:
                        continue

                try:
                    doc = parser.parse_file(file_path)
                    if doc:
                        documents.append(doc)
                        logging.debug(f"已解析: {file_path} [{doc.doc_type}, {doc.raw_length} 字符]")
                except Exception as e:
                    logging.error(f"解析失败 {file_path}: {e}")

    return documents


def extract_competitor_summary(config: dict, workspace_root: str) -> str:
    """提取竞对动态摘要（从明修65.txt）"""
    source_file = config.get("competitors", {}).get("source_file", "")
    if not source_file:
        return ""

    full_path = os.path.join(workspace_root, source_file)
    if not os.path.exists(full_path):
        return ""

    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()

        competitors = config.get("competitors", {}).get("tracking", [])
        if not competitors:
            return ""

        lines = content.split('\n')
        summary_lines = ["以下为受追踪竞对的本周动态摘要：", ""]

        for comp in competitors:
            summary_lines.append(f"### {comp}")
            found = False
            for i, line in enumerate(lines):
                if comp in line:
                    # 取前后各 3 行
                    start = max(0, i - 1)
                    end = min(len(lines), i + 3)
                    snippet = '\n'.join(lines[start:end]).strip()
                    if len(snippet) > 20:
                        summary_lines.append(f"> {snippet[:300]}...")
                        found = True
                        break
            if not found:
                summary_lines.append("> 本周无更新。")
            summary_lines.append("")

        return '\n'.join(summary_lines)
    except Exception as e:
        logging.warning(f"提取竞对摘要失败: {e}")
        return ""


def main():
    parser = argparse.ArgumentParser(
        description="RoboX 商业模式自动化分析工具 - 七范式与三重锁定框架",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--force", action="store_true",
        help="全量扫描所有文档（默认仅扫描本周新增/修改）",
    )
    parser.add_argument(
        "--date", type=str, default=None,
        help="指定报告日期，格式: YYYY-MM-DD（默认为今天）",
    )
    parser.add_argument(
        "--config", type=str, default=None,
        help="指定配置文件路径（默认为当前目录的 config.yaml）",
    )
    args = parser.parse_args()

    # 工作目录
    tools_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.dirname(os.path.dirname(tools_dir))

    # 配置
    config_path = args.config or os.path.join(tools_dir, "config.yaml")
    if not os.path.exists(config_path):
        print(f"错误: 配置文件不存在: {config_path}")
        sys.exit(1)

    config = load_config(config_path)

    # 报告日期
    report_date = args.date or datetime.now().strftime("%Y-%m-%d")

    # 目录路径
    data_dir = os.path.join(tools_dir, "data")
    log_dir = os.path.join(data_dir, "logs")
    report_dir = os.path.join(data_dir, "reports")
    snapshot_dir = os.path.join(data_dir, "snapshots")

    # 日志
    logger = setup_logging(log_dir, report_date)
    logger.info("=" * 60)
    logger.info(f"RoboX 商业模式分析工具 v1.0.0")
    logger.info(f"报告日期: {report_date}")
    logger.info(f"模式: {'全量扫描' if args.force else '增量扫描（本周）'}")
    logger.info(f"工作区: {workspace_root}")
    logger.info("=" * 60)

    # 初始化组件
    scan_dirs = config.get("global", {}).get("scan_dirs", [])
    text_parser = TextParser(workspace_root)
    docx_parser = DocxParser(workspace_root)
    keyword_engine = KeywordEngine(config)
    scoring_calc = ScoringCalculator(config)
    snapshot_mgr = SnapshotManager(snapshot_dir)
    report_gen = ReportGenerator(report_dir, config)

    # 1. 扫描文档
    logger.info("正在扫描文档...")
    documents = scan_documents(
        workspace_root, scan_dirs, text_parser, docx_parser, force=args.force,
    )
    valid_docs = [d for d in documents if d is not None]
    logger.info(f"扫描完成: 找到 {len(valid_docs)} 份文档" + ("（仅本周）" if not args.force else "（全量）"))

    if not valid_docs:
        logger.warning("未发现可分析的文档，退出。")
        sys.exit(0)

    # 日志文件分布
    for doc in valid_docs:
        logger.debug(f"  {doc.path} | {doc.doc_type} | {doc.date.strftime('%Y-%m-%d')} | {doc.raw_length} 字符")

    # 2. 关键词分析
    logger.info("正在执行关键词分析...")
    all_matches = keyword_engine.analyze_all(valid_docs)
    for dim_key in sorted(all_matches.keys()):
        logger.debug(f"  维度 [{dim_key}]: {len(all_matches[dim_key])} 次命中")

    # 3. 统计 + 评分
    logger.info("正在计算维度评分...")
    total_chars = sum(d.raw_length for d in valid_docs)
    all_stats = {}
    for dim_key, matches in all_matches.items():
        all_stats[dim_key] = keyword_engine.get_dimension_stats(dim_key, matches, total_chars)

    scores = scoring_calc.score_all(all_matches, all_stats, valid_docs)

    # 打印评分概览
    logger.info("十维度评分结果:")
    logger.info(f"  {'维度':<25s} {'评分':>6s} {'命中':>6s} {'证据':>8s}")
    logger.info(f"  {'-'*25} {'-'*6} {'-'*6} {'-'*8}")
    for s in scores:
        logger.info(f"  {s['dimension_name']:<25s} {s['score']:>5.1f}/10 {s['hit_count']:>5d}  {s['evidence_strength']:>8s}")

    # 4. Diff 对比
    logger.info("正在对比历史数据...")
    diff_results = snapshot_mgr.diff_with_previous(scores)
    changes = [v for v in diff_results.values() if v["trend"] != "new"]
    up = sum(1 for v in changes if v["trend"] == "up")
    down = sum(1 for v in changes if v["trend"] == "down")
    flat = sum(1 for v in changes if v["trend"] == "flat")
    logger.info(f"Diff 完成: {up}↑ {down}↓ {flat}→")

    # 5. 保存快照
    logger.info(f"正在保存快照: {report_date}.json")
    config_meta = config.get("meta", {})
    snapshot_mgr.create_snapshot(report_date, scores, valid_docs, config_meta)

    # 6. 趋势面板
    dim_names = {
        k: v.get("name", k) for k, v in config.get("dimensions", {}).items()
    }
    trend_rows = snapshot_mgr.generate_trend_table(dim_names, weeks=4)

    # 7. 竞对摘要
    logger.info("正在提取竞对动态...")
    competitor_summary = extract_competitor_summary(config, workspace_root)
    if competitor_summary:
        logger.info("竞对动态提取完成")
    else:
        logger.info("无竞对动态数据")

    # 8. 查找上次报告日期
    last_report_date = ""
    recent_snapshots = snapshot_mgr.load_recent_snapshots(2)
    if len(recent_snapshots) >= 2:
        last_report_date = recent_snapshots[1][0]

    # 9. 生成报告
    logger.info("正在生成 Markdown 报告...")
    report = report_gen.generate_report(
        report_date=report_date,
        scores=scores,
        diff_results=diff_results,
        documents=valid_docs,
        trend_rows=trend_rows,
        competitor_summary=competitor_summary,
        last_report_date=last_report_date,
    )

    report_path = os.path.join(report_dir, f"report-{report_date}.md")
    logger.info(f"报告已生成: {report_path}")
    logger.info(f"索引已更新: {os.path.join(report_dir, 'index.md')}")

    # 摘要
    avg_score = sum(s["score"] for s in scores) / max(len(scores), 1)
    logger.info("=" * 60)
    logger.info(f"分析完成！十维度平均分: {avg_score:.2f}/10")
    logger.info(f"报告路径: {report_path}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
