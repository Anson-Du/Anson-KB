"""文本解析器 - 自动识别转写原文和纪要两种格式"""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

from .document import Document, Section


class TextParser:
    """文本解析器：读取 .txt 文件，自动识别格式类型"""

    # 纪要文件前缀标记
    MINUTES_PREFIXES = ["纪要_", "纪要-", "纪要 ", "纪要", "summary_", "Summary_"]

    # 转写格式：匹配 "**发言人** HH:MM:SS" 模式
    TRANSCRIPT_SPEAKER_RE = re.compile(r'^\*\*(.+?)\*\*\s*(\d{2}:\d{2}:\d{2})$')
    # 纪要格式：匹配 "## " 或 "### " 或数字编号标题（如 "1. "、"1、"）
    MINUTES_HEADING_RE = re.compile(r'^(#{1,4}\s+|[一二三四五六七八九十]+[、．.]\s*|\d+[、．.)]\s*)')

    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root

    def parse_file(self, file_path: str) -> Optional[Document]:
        """解析单个 .txt 文件，自动识别格式"""
        full_path = os.path.join(self.workspace_root, file_path) if not os.path.isabs(file_path) else file_path

        if not os.path.exists(full_path):
            return None

        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            try:
                with open(full_path, 'r', encoding='gbk') as f:
                    lines = f.readlines()
            except Exception:
                return None

        if not lines:
            return None

        # 自动识别格式类型
        filename = os.path.basename(file_path)
        doc_type = self._detect_format(lines, filename)

        # 提取日期
        doc_date = self._extract_date(file_path, lines)

        # 解析为 sections
        if doc_type == "transcript":
            sections = self._parse_transcript(lines)
        else:
            sections = self._parse_minutes(lines)

        # 提取标题
        title = self._extract_title(lines)

        doc = Document(
            path=file_path,
            date=doc_date,
            doc_type=doc_type,
            sections=sections,
            raw_length=sum(len(s.content) for s in sections),
            title=title,
        )
        return doc

    def _detect_format(self, lines: list, filename: str) -> str:
        """自动识别文件格式"""
        # 文件名包含"纪要"前缀
        basename = os.path.basename(filename).lower()
        for prefix in self.MINUTES_PREFIXES:
            if basename.startswith(prefix.lower()):
                return "minutes"

        # 第一行包含"纪要"
        if lines and "纪要" in lines[0]:
            return "minutes"

        # 检查"**发言人** HH:MM:SS"模式
        transcript_count = 0
        for line in lines[:20]:
            if self.TRANSCRIPT_SPEAKER_RE.match(line.strip()):
                transcript_count += 1
        if transcript_count >= 2:
            return "transcript"

        # 检查纪要模式
        minutes_count = 0
        for line in lines[:30]:
            stripped = line.strip()
            if stripped.startswith(('主题:', '时间:', '参与人:', '## ', '### ')):
                minutes_count += 1
        if minutes_count >= 2:
            return "minutes"

        # 默认按纪要处理
        return "minutes"

    def _extract_date(self, file_path: str, lines: list) -> datetime:
        """从文件名或内容提取日期"""
        # 1. 从文件名提取日期模式 YYYY-MM-DD / YYYYMMDD
        basename = os.path.basename(file_path)
        date_patterns = [
            r'(\d{4}-\d{2}-\d{2})',
            r'(\d{4}\d{2}\d{2})',
            r'(\d{2}-\d{2})',  # MM-DD 格式
        ]

        for pattern in date_patterns:
            match = re.search(pattern, basename)
            if match:
                date_str = match.group(1)
                try:
                    if len(date_str) == 8 and date_str.isdigit():
                        return datetime.strptime(date_str, '%Y%m%d')
                    elif '-' in date_str and len(date_str) == 10:
                        return datetime.strptime(date_str, '%Y-%m-%d')
                    elif '-' in date_str and len(date_str) == 5:
                        # 假定当年
                        year = datetime.now().year
                        return datetime.strptime(f'{year}-{date_str}', '%Y-%m-%d')
                except ValueError:
                    pass

        # 2. 从内容提取 "时间:" 行
        for line in lines[:30]:
            match = re.search(r'时间[：:]\s*(\d{4}-\d{2}-\d{2})', line)
            if match:
                try:
                    return datetime.strptime(match.group(1), '%Y-%m-%d')
                except ValueError:
                    pass

        # 3. 回退到文件修改时间
        full_path = os.path.join(self.workspace_root, file_path) if not os.path.isabs(file_path) else file_path
        mtime = os.path.getmtime(full_path)
        return datetime.fromtimestamp(mtime)

    def _extract_title(self, lines: list) -> str:
        """提取文档标题"""
        for line in lines[:5]:
            stripped = line.strip()
            if stripped.startswith('# '):
                return stripped[2:].strip()
            if stripped.startswith('纪要'):
                for l in lines[:20]:
                    l2 = l.strip()
                    if l2.startswith('主题') and ('：' in l2 or ':' in l2):
                        return l2.split('：' if '：' in l2 else ':', 1)[-1].strip()
        return ""

    def _parse_transcript(self, lines: list) -> list:
        """解析转写原文格式：按发言人+时间戳分段"""
        sections = []
        current_speaker = None
        current_time = None
        current_lines = []
        line_number = 1
        start_line = 0

        for i, line in enumerate(lines):
            stripped = line.strip()
            # 跳过标题和分隔线
            if stripped.startswith('#') or stripped.startswith('---') or stripped == '':
                if current_speaker and current_lines:
                    content = '\n'.join(current_lines)
                    if content.strip():
                        sections.append(Section(
                            heading=f"{current_speaker} {current_time}" if current_time else current_speaker,
                            content=content,
                            start_line=start_line,
                            speaker=current_speaker,
                        ))
                    current_speaker = None
                    current_time = None
                    current_lines = []
                continue

            match = self.TRANSCRIPT_SPEAKER_RE.match(stripped)
            if match:
                # 保存上一段
                if current_speaker and current_lines:
                    content = '\n'.join(current_lines)
                    if content.strip():
                        sections.append(Section(
                            heading=f"{current_speaker} {current_time}" if current_time else current_speaker,
                            content=content,
                            start_line=start_line,
                            speaker=current_speaker,
                        ))
                # 开启新段
                current_speaker = match.group(1).strip()
                current_time = match.group(2)
                current_lines = []
                start_line = i + 1
            else:
                current_lines.append(stripped)

        # 处理最后一段
        if current_speaker and current_lines:
            content = '\n'.join(current_lines)
            if content.strip():
                sections.append(Section(
                    heading=f"{current_speaker} {current_time}" if current_time else current_speaker,
                    content=content,
                    start_line=start_line,
                    speaker=current_speaker,
                ))

        return sections

    def _parse_minutes(self, lines: list) -> list:
        """解析纪要格式：按结构化标题分段"""
        sections = []
        current_heading = "纪要摘要"
        current_lines = []
        start_line = 1

        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped:
                if current_lines:
                    sections.append(Section(
                        heading=current_heading,
                        content='\n'.join(current_lines),
                        start_line=start_line,
                    ))
                    current_lines = []
                continue

            # 检测标题
            is_heading = False
            if stripped.startswith(('# ', '## ', '### ', '#### ')):
                is_heading = True
                heading_text = re.sub(r'^#+\s*', '', stripped)
            elif stripped.startswith(('主题:', '时间:', '参与人:', '背景:', '结论:', '下一步:')):
                is_heading = True
                heading_text = stripped
            else:
                # 数字或中文编号标题
                num_match = re.match(r'^(\d+[、．.)]\s*|第[一二三四五六七八九十百千万\d]+[章节部分]\s*)', stripped)
                if num_match:
                    is_heading = True
                    heading_text = stripped

            if is_heading and len(stripped) < 60:
                # 保存上一段
                if current_lines:
                    sections.append(Section(
                        heading=current_heading,
                        content='\n'.join(current_lines),
                        start_line=start_line,
                    ))
                current_heading = heading_text
                current_lines = []
                start_line = i + 1
            else:
                current_lines.append(stripped)

        # 最后一段
        if current_lines:
            sections.append(Section(
                heading=current_heading,
                content='\n'.join(current_lines),
                start_line=start_line,
            ))

        return sections
