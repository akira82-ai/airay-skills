#!/usr/bin/env python3
"""
批量翻译 TSV 文件
在主会话中逐批处理，确保 100% 翻译
"""
import sys
import csv
from pathlib import Path

TSV_PATH = Path('/tmp/insights_blocks.tsv')
BATCH_SIZE = 15


def load_tsv(tsv_path):
    """加载 TSV 文件"""
    rows = []
    with open(tsv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            rows.append(row)
    return rows


def save_tsv(tsv_path, rows):
    """保存 TSV 文件"""
    with open(tsv_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(rows)


def update_batch(rows, start_idx, translations):
    """更新一批翻译"""
    for i, translation in enumerate(translations):
        idx = start_idx + i
        if idx < len(rows):
            # 确保行有两列
            if len(rows[idx]) < 2:
                rows[idx].append('')
            rows[idx][1] = translation
    return rows


def print_progress(rows):
    """打印进度"""
    total = len(rows)
    translated = sum(1 for row in rows if len(row) >= 2 and row[1].strip())
    percent = translated / total * 100 if total > 0 else 0

    bar_length = 40
    filled = int(bar_length * translated / total)
    bar = '█' * filled + '░' * (bar_length - filled)

    print(f"\n进度: [{bar}] {percent:.1f}% ({translated}/{total})")
    return translated, total, percent


def get_next_batch(rows, batch_size):
    """获取下一批待翻译的内容"""
    batch = []
    indices = []
    for i, row in enumerate(rows):
        if len(row) < 2 or not row[1].strip():
            batch.append(row[0])
            indices.append(i)
            if len(batch) >= batch_size:
                break
    return batch, indices


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法:")
        print("  查看进度: python3 batch_translator.py status")
        print("  更新翻译: python3 batch_translator.py update <start_idx> <trans1> <trans2> ...")
        print("  获取批次: python3 batch_translator.py next")
        sys.exit(1)

    command = sys.argv[1]

    # 加载文件
    rows = load_tsv(TSV_PATH)

    if command == 'status':
        translated, total, percent = print_progress(rows)
        if translated == total:
            print("\n✅ 所有行已翻译完成！")
            print(f"\n运行合并脚本:")
            print(f"  python3 {baseDir}/scripts/translate.py")

    elif command == 'next':
        batch, indices = get_next_batch(rows, 15)
        if not batch:
            print("\n✅ 所有行已翻译完成！")
            print(f"\n运行合并脚本:")
            print(f"  python3 {baseDir}/scripts/translate.py")
            return

        print(f"\n待翻译批次（{len(batch)} 行）：")
        print("=" * 60)
        for i, (text, idx) in enumerate(zip(batch, indices), 1):
            print(f"\n[{i}] 行 {idx}:")
            print(f"  {text}")

    elif command == 'update':
        if len(sys.argv) < 4:
            print("错误：需要提供起始索引和翻译内容")
            print("用法: python3 batch_translator.py update <start_idx> <trans1> <trans2> ...")
            sys.exit(1)

        start_idx = int(sys.argv[2])
        translations = sys.argv[3:]

        # 更新翻译
        rows = update_batch(rows, start_idx, translations)

        # 保存文件
        save_tsv(TSV_PATH, rows)

        # 打印进度
        translated, total, percent = print_progress(rows)
        print(f"\n✅ 已更新 {len(translations)} 行翻译")

        if translated == total:
            print(f"\n🎉 翻译全部完成！")
            print(f"\n运行合并脚本:")
            print(f"  python3 {baseDir}/scripts/translate.py")

    else:
        print(f"未知命令: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
