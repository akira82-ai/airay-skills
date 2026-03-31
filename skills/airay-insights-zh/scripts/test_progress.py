#!/usr/bin/env python3
"""
测试进度监控功能
模拟翻译过程中的进度更新
"""
import json
import time
from pathlib import Path
from datetime import datetime

PROGRESS_FILE = Path('/tmp/insights_progress.json')

def simulate_translation():
    """模拟翻译过程并更新进度"""
    total = 50  # 模拟 50 个文本块

    # 创建初始进度
    progress = {
        "total": total,
        "translated": 0,
        "percent": 0.0,
        "start_time": datetime.now().isoformat(),
        "last_update": datetime.now().isoformat()
    }

    print(f"开始模拟翻译，总共 {total} 个文本块")
    print(f"进度文件: {PROGRESS_FILE}")
    print("\n在另一个终端运行以下命令查看进度：")
    print(f"  python3 {baseDir}/scripts/monitor_progress.py")
    print("\n按 Ctrl+C 停止测试\n")

    try:
        with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
            json.dump(progress, f, indent=2, ensure_ascii=False)

        for i in range(0, total + 1, 5):  # 每 5 个更新一次
            progress["translated"] = i
            progress["percent"] = round(i / total * 100, 1)
            progress["last_update"] = datetime.now().isoformat()

            with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
                json.dump(progress, f, indent=2, ensure_ascii=False)

            print(f"[主进程] 更新进度: {progress['percent']}% ({i}/{total})")
            time.sleep(1)  # 模拟翻译耗时

        print("\n✅ 翻译完成！")

        # 等待几秒让监控脚本显示完成状态
        time.sleep(2)

        # 清理测试文件
        PROGRESS_FILE.unlink()
        print(f"✅ 已清理测试文件: {PROGRESS_FILE}")

    except KeyboardInterrupt:
        print("\n\n⚠️  测试中断")
        if PROGRESS_FILE.exists():
            PROGRESS_FILE.unlink()
            print(f"✅ 已清理测试文件")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        if PROGRESS_FILE.exists():
            PROGRESS_FILE.unlink()

if __name__ == '__main__':
    simulate_translation()
