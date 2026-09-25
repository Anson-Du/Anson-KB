"""核心数据模型 - Document 和 Section 数据类"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


@dataclass
class Section:
    """文档段落/章节"""
    heading: str                              # 段落标题（纪要格式）或 "转写原文"（转写格式）
    content: str                              # 纯文本内容
    keywords_found: dict = field(default_factory=dict)  # {维度名: [(关键词, 上下文片段)]}
    start_line: int = 0                       # 在原文件中的起始行号
    speaker: Optional[str] = None             # 发言人（转写格式）


@dataclass
class Document:
    """文档数据模型"""
    path: str                                 # 文件相对路径（相对于 workspace_root）
    date: datetime                            # 文件日期
    doc_type: str                             # "transcript" | "minutes" | "docx"
    sections: list = field(default_factory=list)
    raw_length: int = 0                       # 原始文本总字符数
    title: str = ""                           # 文档标题

    @property
    def full_text(self) -> str:
        """获取文档全文"""
        return "\n\n".join(s.heading + "\n" + s.content for s in self.sections)

    @property
    def age_days(self) -> float:
        """文档距今天数"""
        doc_date = self.date
        # 去除时区信息以确保可比较
        if doc_date.tzinfo is not None:
            doc_date = doc_date.replace(tzinfo=None)
        now = datetime.now()
        return (now - doc_date).total_seconds() / 86400.0

    @property
    def freshness_coefficient(self, max_days: float = 90.0) -> float:
        """时间新鲜度系数：越新越接近 1.0，超过 max_days 天后衰减至 0.1"""
        days = min(self.age_days, max_days)
        return max(0.1, 1.0 - (days / max_days) * 0.9)
