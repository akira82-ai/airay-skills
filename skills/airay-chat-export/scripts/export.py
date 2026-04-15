#!/usr/bin/env python3
"""导出 Claude Code 对话 session 记录到本地 JSON 文件"""

import argparse
import json
import datetime
import os
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Any, Optional


def to_ms(ts) -> int:
    """
    统一时间戳转换函数（关键！）

    处理两种时间戳格式：
    - int/float：Unix 毫秒时间戳（如 1775299268460）
    - str：ISO 8601 格式（如 "2026-04-05T01:15:03.074Z"）

    返回：统一的毫秒时间戳（int）
    """
    if isinstance(ts, (int, float)):
        return int(ts)
    if isinstance(ts, str):
        # 处理 ISO 8601 格式，替换 Z 为 +00:00
        dt = datetime.datetime.fromisoformat(ts.replace('Z', '+00:00'))
        return int(dt.timestamp() * 1000)
    return 0


def get_sessions_in_range(history_file: Path, start_ms: int, end_ms: int, project_filter: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    从 history.jsonl 获取指定时间范围内的 session 列表

    Args:
        history_file: history.jsonl 文件路径
        start_ms: 开始时间戳（毫秒）
        end_ms: 结束时间戳（毫秒）
        project_filter: 可选的项目路径筛选

    Returns:
        session 列表，每个包含：sessionId, project_path, message_count, first_timestamp, last_timestamp
    """
    sessions = {}

    if not history_file.exists():
        return []

    with open(history_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                ts_ms = to_ms(entry.get('timestamp'))

                # 过滤时间范围
                if not (start_ms <= ts_ms < end_ms):
                    continue

                session_id = entry.get('sessionId')
                project_path = entry.get('project')

                if not session_id or not project_path:
                    continue

                # 项目路径筛选
                if project_filter and project_filter not in project_path:
                    continue

                # 更新 session 信息
                if session_id not in sessions:
                    sessions[session_id] = {
                        'sessionId': session_id,
                        'project_path': project_path,
                        'message_count': 0,
                        'first_timestamp': ts_ms,
                        'last_timestamp': ts_ms
                    }

                sessions[session_id]['message_count'] += 1
                sessions[session_id]['first_timestamp'] = min(sessions[session_id]['first_timestamp'], ts_ms)
                sessions[session_id]['last_timestamp'] = max(sessions[session_id]['last_timestamp'], ts_ms)

            except (json.JSONDecodeError, TypeError):
                continue

    return list(sessions.values())


def extract_session_content(project_path: str, session_id: str, start_ms: int, end_ms: int) -> Dict[str, Any]:
    """
    提取单个 session 的完整对话内容

    Args:
        project_path: 项目路径
        session_id: Session ID
        start_ms: 开始时间戳（毫秒）
        end_ms: 结束时间戳（毫秒）

    Returns:
        包含完整对话内容的字典
    """
    # 路径编码：将 / 替换为 -
    encoded_path = project_path.replace('/', '-')
    session_file = Path.home() / '.claude' / 'projects' / encoded_path / f'{session_id}.jsonl'

    result = {
        'session_id': session_id,
        'project_path': project_path,
        'messages': [],
        'start_time': None,
        'end_time': None,
        'message_count': 0
    }

    if not session_file.exists():
        return result

    tool_calls = defaultdict(int)
    messages = []
    timestamps = []

    with open(session_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                entry_type = entry.get('type')

                # 使用 to_ms() 转换时间戳
                ts_ms = to_ms(entry.get('timestamp'))

                # 过滤日期范围
                if not (start_ms <= ts_ms < end_ms):
                    continue

                timestamps.append(ts_ms)

                # 构建消息对象
                message = {
                    'type': entry_type,
                    'timestamp': entry.get('timestamp'),  # 保留原始 ISO 格式
                    'role': entry.get('role', entry_type)
                }

                # 提取内容
                if entry_type == 'assistant':
                    msg = entry.get('message', {})
                    message['content'] = msg.get('content', [])

                    # 统计工具调用
                    for item in message['content']:
                        if isinstance(item, dict):
                            item_type = item.get('type')
                            if item_type in ('tool_use', 'server_tool_use'):
                                tool_name = item.get('name', 'unknown')
                                tool_calls[tool_name] += 1

                    # 保存 cwd（工作目录）
                    if 'cwd' in entry:
                        message['cwd'] = entry['cwd']

                elif entry_type == 'user':
                    # 用户消息内容在 message.content 中
                    msg_data = entry.get('message', {})
                    content = msg_data.get('content', [])
                    message['content'] = content

                    # 保存 cwd
                    if 'cwd' in entry:
                        message['cwd'] = entry['cwd']

                elif entry_type == 'user:continue':
                    # 用户消息内容在 message.content 中
                    msg_data = entry.get('message', {})
                    content = msg_data.get('content', [])
                    message['content'] = content

                messages.append(message)

            except (json.JSONDecodeError, TypeError):
                continue

    # 更新结果
    result['messages'] = messages
    result['message_count'] = len(messages)

    if timestamps:
        # 转换回 ISO 8601 格式
        start_dt = datetime.datetime.fromtimestamp(min(timestamps) / 1000, tz=datetime.timezone.utc)
        end_dt = datetime.datetime.fromtimestamp(max(timestamps) / 1000, tz=datetime.timezone.utc)
        result['start_time'] = start_dt.isoformat().replace('+00:00', 'Z')
        result['end_time'] = end_dt.isoformat().replace('+00:00', 'Z')

    return result


def export_conversations(start_ms: int, end_ms: int, project_filter: Optional[str] = None, output_file: Optional[str] = None) -> Dict[str, Any]:
    """
    导出所有符合条件对话记录

    Args:
        start_ms: 开始时间戳（毫秒）
        end_ms: 结束时间戳（毫秒）
        project_filter: 可选的项目路径筛选
        output_file: 可选的输出文件路径

    Returns:
        导出的数据结构
    """
    history_file = Path.home() / '.claude' / 'history.jsonl'

    # 获取 session 列表
    sessions = get_sessions_in_range(history_file, start_ms, end_ms, project_filter)

    # 提取每个 session 的完整内容
    exported_sessions = []
    all_tool_calls = defaultdict(int)
    projects_involved = set()
    total_messages = 0

    for session in sessions:
        session_data = extract_session_content(
            session['project_path'],
            session['sessionId'],
            start_ms,
            end_ms
        )

        if session_data['messages']:  # 只添加有消息的 session
            exported_sessions.append(session_data)
            total_messages += session_data['message_count']
            projects_involved.add(session['project_path'])

            # 统计工具调用
            for msg in session_data['messages']:
                if msg.get('type') == 'assistant':
                    for item in msg.get('content', []):
                        if isinstance(item, dict) and item.get('type') in ('tool_use', 'server_tool_use'):
                            tool_name = item.get('name', 'unknown')
                            all_tool_calls[tool_name] += 1

    # 计算时间跨度
    time_span_hours = 0
    if exported_sessions:
        all_timestamps = []
        for s in exported_sessions:
            if s['start_time']:
                all_timestamps.append(to_ms(s['start_time']))
            if s['end_time']:
                all_timestamps.append(to_ms(s['end_time']))

        if all_timestamps:
            time_span_hours = (max(all_timestamps) - min(all_timestamps)) / (1000 * 60 * 60)

    # 生成日期范围标签
    now = datetime.datetime.now(datetime.timezone.utc)
    today_start = int(now.replace(hour=0, minute=0, second=0, microsecond=0).timestamp() * 1000)
    yesterday_start = today_start - 86400000

    if start_ms >= today_start:
        date_label = "今天"
    elif start_ms >= yesterday_start:
        date_label = "昨天"
    elif start_ms >= yesterday_start - 2 * 86400000:
        date_label = "近 3 天"
    elif start_ms >= yesterday_start - 6 * 86400000:
        date_label = "近 7 天"
    else:
        date_label = "自定义"

    # 构建导出结果
    export_data = {
        "export_metadata": {
            "export_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00', 'Z'),
            "date_range": {
                "start_ms": start_ms,
                "end_ms": end_ms,
                "label": date_label
            },
            "project_filter": project_filter,
            "total_sessions": len(exported_sessions),
            "total_messages": total_messages
        },
        "sessions": exported_sessions,
        "statistics": {
            "total_tool_calls": sum(all_tool_calls.values()),
            "tool_breakdown": dict(sorted(all_tool_calls.items(), key=lambda x: x[1], reverse=True)),
            "projects_involved": sorted(list(projects_involved)),
            "time_span_hours": round(time_span_hours, 2)
        }
    }

    # 如果指定了输出文件，保存到文件
    if output_file:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)

    return export_data


def generate_output_filename(start_ms: int, end_ms: int) -> str:
    """生成输出文件名"""
    start_dt = datetime.datetime.fromtimestamp(start_ms / 1000, tz=datetime.timezone.utc)
    end_dt = datetime.datetime.fromtimestamp(end_ms / 1000, tz=datetime.timezone.utc)

    start_str = start_dt.strftime('%Y-%m-%d')
    end_str = end_dt.strftime('%Y-%m-%d')

    if start_str == end_str:
        return f"chat-export-{start_str}.json"
    else:
        return f"chat-export-{start_str}~{end_str}.json"


def format_date_range_label(start_ms: int, end_ms: int) -> str:
    """格式化日期范围标签"""
    start_dt = datetime.datetime.fromtimestamp(start_ms / 1000, tz=datetime.timezone.utc)
    return start_dt.strftime('%Y-%m-%d')


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='导出 Claude Code 对话记录')
    parser.add_argument('--start_ms', type=int, required=True, help='开始时间戳（毫秒）')
    parser.add_argument('--end_ms', type=int, required=True, help='结束时间戳（毫秒）')
    parser.add_argument('--project', type=str, help='筛选项目路径')
    parser.add_argument('--output', type=str, help='输出文件路径')

    args = parser.parse_args()

    # 如果没有指定输出文件，自动生成
    output_file = args.output
    if not output_file:
        output_file = generate_output_filename(args.start_ms, args.end_ms)

    # 执行导出
    data = export_conversations(
        args.start_ms,
        args.end_ms,
        args.project,
        output_file
    )

    # 输出结果摘要
    date_label = format_date_range_label(args.start_ms, args.end_ms)
    project_info = args.project if args.project else "所有项目"
    file_size = os.path.getsize(output_file) if output_file else 0
    file_size_kb = file_size / 1024

    print(f"""✅ 对话导出完成！

导出范围：{date_label}
项目：{project_info}
会话数：{data['export_metadata']['total_sessions']}
消息数：{data['export_metadata']['total_messages']}

保存位置：./{output_file}
文件大小：{file_size_kb:.0f} KB

💡 提示：使用 jq 或 Python 脚本进一步分析导出的数据""")


if __name__ == '__main__':
    main()
