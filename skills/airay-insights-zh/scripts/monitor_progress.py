#!/usr/bin/env python3
"""
监控翻译进度的辅助脚本
"""
import json
import time
from pathlib import Path
from datetime import datetime

PROGRESS_FILE = Path('/tmp/insights_progress.json')

def monitor_progress(refresh_interval=2):
    """持续监控进度并显示"""
    print("等待翻译开始...")

    while True:
        if not PROGRESS_FILE.exists():
            time.sleep(refresh_interval)
            continue

        try:
            with open(PROGRESS_FILE, encoding='utf-8') as f:
                data = json.load(f)
        except:
            time.sleep(refresh_interval)
            continue

        total = data.get('total', 0)
        translated = data.get('translated', 0)
        percent = data.get('percent', 0)

        if total > 0:
            bar_len = 40
            filled = int(bar_len * translated / total)
            if filled < bar_len:
                bar = "=" * filled + ">" + " " * (bar_len - filled - 1)
            else:
                bar = "=" * bar_len

            print(f"\r[{bar}] {percent:.1f}% ({translated}/{total})", end='', flush=True)

            if translated >= total:
                print("\n翻译完成！")
                break

        time.sleep(refresh_interval)

if __name__ == '__main__':
    monitor_progress()
