#!/usr/bin/env python3
"""统计 Claude Code 技能使用情况"""

import json
import locale
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List

# 检测系统语言
LANG = locale.getdefaultlocale()[0]
IS_ZH = LANG and LANG.startswith('zh')


def get_cutoff_timestamp(period: str) -> Optional[int]:
    """根据时间段返回截止时间戳（毫秒），None 表示不过滤"""
    now = datetime.now()
    if period == "today":
        # 今天 00:00
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        return int(start_of_day.timestamp() * 1000)
    elif period == "past_7_days":
        return int((now - timedelta(days=7)).timestamp() * 1000)
    elif period == "past_30_days":
        return int((now - timedelta(days=30)).timestamp() * 1000)
    elif period == "past_90_days":
        return int((now - timedelta(days=90)).timestamp() * 1000)
    elif period == "all":
        return None


def get_installed_skills() -> List[str]:
    """获取已安装的技能列表"""
    skills_dir = Path.home() / ".claude" / "skills"
    if not skills_dir.exists():
        return []
    return [d.name for d in skills_dir.iterdir() if d.is_dir()]


def build_skill_patterns(skills: List[str]) -> Dict[str, re.Pattern]:
    """为每个技能构建正则表达式模式"""
    patterns = {}
    for skill in skills:
        # 匹配 /skill-name 或 /skill-name 后跟空格/参数
        patterns[skill] = re.compile(rf"/{re.escape(skill)}\b")
    return patterns


def process_file(file_path: Path, skill_patterns: Dict[str, re.Pattern], cutoff_ts: Optional[int]) -> Dict[str, int]:
    """处理单个 JSONL 文件，返回技能计数"""
    counts = {}
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    # 检查时间戳
                    if cutoff_ts is not None and "timestamp" in entry:
                        ts = entry.get("timestamp")
                        if isinstance(ts, (int, float)) and ts < cutoff_ts:
                            continue
                    # 检查 display 字段
                    if "display" in entry:
                        display = entry.get("display", "")
                        for skill, pattern in skill_patterns.items():
                            if pattern.search(display):
                                counts[skill] = counts.get(skill, 0) + 1
                except (json.JSONDecodeError, KeyError, TypeError):
                    continue
    except (IOError, OSError):
        pass
    return counts


def collect_stats(period: str) -> Dict[str, int]:
    """收集指定时间段的技能使用统计"""
    cutoff_ts = get_cutoff_timestamp(period)
    skills = get_installed_skills()
    skill_patterns = build_skill_patterns(skills)
    skill_counts = {skill: 0 for skill in skills}

    # 处理全局历史文件
    history_file = Path.home() / ".claude" / "history.jsonl"
    if history_file.exists():
        counts = process_file(history_file, skill_patterns, cutoff_ts)
        for skill, count in counts.items():
            skill_counts[skill] = skill_counts.get(skill, 0) + count

    # 处理项目会话文件
    projects_dir = Path.home() / ".claude" / "projects"
    if projects_dir.exists():
        for jsonl_file in projects_dir.rglob("*.jsonl"):
            counts = process_file(jsonl_file, skill_patterns, cutoff_ts)
            for skill, count in counts.items():
                skill_counts[skill] = skill_counts.get(skill, 0) + count

    return skill_counts


def get_skill_last_modified() -> str:
    """获取技能目录的最后修改日期（YYYYMMDD 格式）"""
    skill_dir = Path(__file__).parent.parent
    try:
        result = subprocess.run(
            ["git", "log", "--format=%ct", "-1", str(skill_dir)],
            capture_output=True,
            text=True,
            check=True
        )
        timestamp = int(result.stdout.strip())
        return datetime.fromtimestamp(timestamp).strftime("%Y%m%d")
    except (subprocess.CalledProcessError, ValueError, FileNotFoundError):
        return datetime.now().strftime("%Y%m%d")


def get_banner() -> str:
    """获取技能 Banner"""
    last_modified = get_skill_last_modified()
    return f"""
═══════════════════════════════════════════════════════════════
▌ 技能使用统计 ▐
统计已安装技能在指定时间段内的使用次数，以美观的 TUI 格式展示结果
═══════════════════════════════════════════════════════════════
磊叔 │ 微信：AIRay1015 │ github.com/akira82-ai
────────────────────────────────────────────────────────────
最后修改：{last_modified}
────────────────────────────────────────────────────────────
• 每个技能的调用次数统计
• 使用频率排名展示
• 总使用次数汇总
• 时间趋势分析
═══════════════════════════════════════════════════════════════
"""

def format_report(period: str, period_label: str, skill_counts: Dict[str, int]) -> str:
    """格式化统计报告"""
    sorted_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)
    total = sum(skill_counts.values())
    max_count = max(skill_counts.values()) if skill_counts else 1

    # 语言文本
    texts = {
        'title': f"📊 {'技能使用统计报告' if IS_ZH else 'Skill Usage Statistics'} ({period_label})",
        'header': f"{'排名 | 技能名称        | 调用次数 | 使用频率' if IS_ZH else 'Rank | Skill Name      | Count    | Frequency'}",
        'separator': "─────┼────────────────┼──────────┼──────────",
        'total': f"     │ {'总计           ' if IS_ZH else 'Total           '} │",
    }

    lines = [
        texts['title'],
        "═══════════════════════════════════════",
        "",
        texts['header'],
        texts['separator'],
    ]

    for rank, (skill, count) in enumerate(sorted_skills, 1):
        if total > 0:
            percentage = int((count / total) * 100)
        else:
            percentage = 0
        bar = "█" * (percentage // 10) + "░" * (10 - (percentage // 10))
        lines.append(f" {rank:2d}  │ {skill:<14s} │   {count:4d}   │ {bar} {percentage}%")

    lines.append(texts['separator'])
    lines.append(f"{texts['total']}   {total:4d}   │")
    lines.append("")

    return "\n".join(lines)


def main():
    period = sys.argv[1] if len(sys.argv) > 1 else "past_30_days"

    period_labels = {
        "today": "今天" if IS_ZH else "Today",
        "past_7_days": "过去 7 天" if IS_ZH else "Past 7 Days",
        "past_30_days": "过去 30 天" if IS_ZH else "Past 30 Days",
        "past_90_days": "过去 90 天" if IS_ZH else "Past 90 Days",
        "all": "全部" if IS_ZH else "All Time",
    }

    period_label = period_labels.get(period, period)
    skill_counts = collect_stats(period)

    # 输出 banner
    print(get_banner())

    report = format_report(period, period_label, skill_counts)
    print(report)


if __name__ == "__main__":
    main()
