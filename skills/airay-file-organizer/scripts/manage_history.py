#!/usr/bin/env python3
"""
目录历史记录管理工具
管理 file-organizer 技能的源目录和目标目录历史记录
"""

import json
import os
from pathlib import Path


HISTORY_FILE = Path(__file__).parent.parent / "history.json"
MAX_HISTORY = 2


def _ensure_history_file():
    """确保历史记录文件存在"""
    if not HISTORY_FILE.exists():
        HISTORY_FILE.write_text(json.dumps({"source": [], "target": []}, indent=2, ensure_ascii=False))


def _normalize_path(path):
    """规范化路径：转换为绝对路径，展开 ~"""
    expanded = os.path.expanduser(path)
    absolute = os.path.abspath(expanded)
    return absolute


def read_history(history_type):
    """读取历史记录

    Args:
        history_type: 历史记录类型 ("source" 或 "target")

    Returns:
        list: 历史路径列表
    """
    _ensure_history_file()
    data = json.loads(HISTORY_FILE.read_text())
    return data.get(history_type, [])


def add_history(history_type, path):
    """添加路径到历史记录

    Args:
        history_type: 历史记录类型 ("source" 或 "target")
        path: 要添加的路径
    """
    # 规范化路径
    normalized_path = _normalize_path(path)

    _ensure_history_file()
    data = json.loads(HISTORY_FILE.read_text())

    # 移除已存在的相同路径
    if normalized_path in data[history_type]:
        data[history_type].remove(normalized_path)

    # 添加到开头
    data[history_type].insert(0, normalized_path)

    # 只保留最近的 N 个
    data[history_type] = data[history_type][:MAX_HISTORY]

    # 写回文件
    HISTORY_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))


def main():
    import argparse

    parser = argparse.ArgumentParser(description="管理 file-organizer 历史记录")
    subparsers = parser.add_subparsers(dest="command", required=True, help="子命令")

    # read 命令
    read_parser = subparsers.add_parser("read", help="读取历史记录")
    read_parser.add_argument("--type", required=True, choices=["source", "target"], help="历史记录类型")

    # add 命令
    add_parser = subparsers.add_parser("add", help="添加历史记录")
    add_parser.add_argument("--type", required=True, choices=["source", "target"], help="历史记录类型")
    add_parser.add_argument("--path", required=True, help="目录路径")

    args = parser.parse_args()

    if args.command == "read":
        history = read_history(args.type)
        print(json.dumps(history, ensure_ascii=False))

    elif args.command == "add":
        add_history(args.type, args.path)


if __name__ == "__main__":
    main()
