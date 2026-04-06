#!/usr/bin/env python3
"""从 Claude Code 对话记录中提取数据，用于生成每日复盘报告"""

import argparse
import json
import datetime
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple, Any


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


def get_history_sessions(history_file: Path, start_ms: int, end_ms: int) -> List[Dict[str, Any]]:
    """
    从 history.jsonl 获取指定时间范围内的 session 列表

    Args:
        history_file: history.jsonl 文件路径
        start_ms: 开始时间戳（毫秒）
        end_ms: 结束时间戳（毫秒）

    Returns:
        session 列表，每个包含：sessionId, project_path, message_count
    """
    sessions = []

    if not history_file.exists():
        return sessions

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

                if session_id and project_path:
                    # 检查是否已存在该 session
                    existing = next((s for s in sessions if s['sessionId'] == session_id), None)
                    if existing:
                        existing['message_count'] += 1
                    else:
                        sessions.append({
                            'sessionId': session_id,
                            'project_path': project_path,
                            'message_count': 1
                        })
            except (json.JSONDecodeError, TypeError):
                continue

    return sessions


def analyze_session_data(project_path: str, session_id: str, start_ms: int, end_ms: int) -> Dict[str, Any]:
    """
    分析单个 session 的详细数据

    Args:
        project_path: 项目路径
        session_id: Session ID
        start_ms: 开始时间戳（毫秒）
        end_ms: 结束时间戳（毫秒）

    Returns:
        包含用户消息、工具调用统计、错误统计等数据的字典
    """
    # 路径编码：将 / 替换为 -
    encoded_path = project_path.replace('/', '-')
    session_file = Path.home() / '.claude' / 'projects' / encoded_path / f'{session_id}.jsonl'

    result = {
        'user_messages': [],
        'tool_calls': defaultdict(int),
        'tool_errors': defaultdict(int),
        'files_touched': set(),
        'total_tool_calls': 0,
        'total_errors': 0
    }

    if not session_file.exists():
        # 转换为可 JSON 序列化的格式
        return {
            'user_messages': [],
            'tool_calls': {},
            'tool_errors': {},
            'files_touched': [],
            'total_tool_calls': 0,
            'total_errors': 0
        }

    with open(session_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                entry_type = entry.get('type')

                # 关键 1：使用 to_ms() 转换时间戳
                ts_ms = to_ms(entry.get('timestamp'))

                # 关键 2：过滤日期范围
                if not (start_ms <= ts_ms < end_ms):
                    continue

                # 关键 3：处理不同类型的记录
                if entry_type == 'assistant':
                    msg = entry.get('message', {})
                    content = msg.get('content', [])

                    # 关键 4：遍历 content 数组（重要！）
                    for item in content:
                        if isinstance(item, dict):
                            item_type = item.get('type')

                            # 检查 tool_use 和 server_tool_use
                            if item_type in ('tool_use', 'server_tool_use'):
                                tool_name = item.get('name', 'unknown')
                                result['tool_calls'][tool_name] += 1
                                result['total_tool_calls'] += 1

                                # 记录文件操作
                                if tool_name in ('Edit', 'Write', 'Read'):
                                    input_data = item.get('input', {})
                                    file_path = input_data.get('file_path')
                                    if file_path:
                                        result['files_touched'].add(file_path)

                elif entry_type == 'user':
                    content = entry.get('content', [])

                    # 遍历 content 数组
                    for item in content:
                        if isinstance(item, dict) and item.get('type') == 'tool_result':
                            # 统计错误
                            if item.get('is_error'):
                                tool_use_id = item.get('tool_use_id', 'unknown')
                                result['tool_errors'][tool_use_id] += 1
                                result['total_errors'] += 1

                        # 提取用户文本消息
                        elif isinstance(item, str):
                            result['user_messages'].append(str(item))

            except (json.JSONDecodeError, TypeError):
                continue

    # 转换 set 为 list 以便 JSON 序列化
    result['files_touched'] = list(result['files_touched'])
    # 转换 defaultdict 为 dict
    result['tool_calls'] = dict(result['tool_calls'])
    result['tool_errors'] = dict(result['tool_errors'])

    return result


def extract_all_data(start_ms: int, end_ms: int) -> Dict[str, Any]:
    """
    提取指定时间范围内的所有数据

    Args:
        start_ms: 开始时间戳（毫秒）
        end_ms: 结束时间戳（毫秒）

    Returns:
        包含所有统计数据的字典
    """
    history_file = Path.home() / '.claude' / 'history.jsonl'

    # 获取 session 列表
    sessions = get_history_sessions(history_file, start_ms, end_ms)

    # 聚合所有数据
    all_data = {
        'sessions': [],
        'total_messages': 0,
        'tool_calls': defaultdict(int),
        'tool_errors': defaultdict(int),
        'files_touched': set(),
        'projects': set(),
        'user_messages': []
    }

    # 分析每个 session
    for session in sessions:
        session_data = analyze_session_data(
            session['project_path'],
            session['sessionId'],
            start_ms,
            end_ms
        )

        all_data['sessions'].append({
            'sessionId': session['sessionId'],
            'project_path': session['project_path'],
            'message_count': session['message_count'],
            'tool_calls': session_data['tool_calls'],
            'tool_errors': session_data['tool_errors'],
            'files_touched': session_data['files_touched']
        })

        # 聚合统计
        all_data['total_messages'] += session['message_count']
        all_data['user_messages'].extend(session_data['user_messages'])

        for tool, count in session_data['tool_calls'].items():
            all_data['tool_calls'][tool] += count

        for tool, count in session_data['tool_errors'].items():
            all_data['tool_errors'][tool] += count

        all_data['files_touched'].update(session_data['files_touched'])
        all_data['projects'].add(session['project_path'])

    # 转换为可 JSON 序列化的格式
    all_data['tool_calls'] = dict(sorted(
        all_data['tool_calls'].items(),
        key=lambda x: x[1],
        reverse=True
    ))
    all_data['tool_errors'] = dict(all_data['tool_errors'])
    all_data['files_touched'] = sorted(list(all_data['files_touched']))
    all_data['projects'] = sorted(list(all_data['projects']))

    return all_data


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='提取 Claude Code 对话记录数据')
    parser.add_argument('--start_ms', type=int, required=True, help='开始时间戳（毫秒）')
    parser.add_argument('--end_ms', type=int, required=True, help='结束时间戳（毫秒）')

    args = parser.parse_args()

    data = extract_all_data(args.start_ms, args.end_ms)

    # 输出 JSON 格式
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
