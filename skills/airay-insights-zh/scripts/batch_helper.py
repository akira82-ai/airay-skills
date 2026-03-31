#!/usr/bin/env python3
"""
批量翻译助手
提供更好的交互体验，自动循环显示批次、接收翻译、更新 TSV
"""
import sys
import csv
from pathlib import Path

TSV_PATH = Path('/tmp/insights_blocks.tsv')
BATCH_SIZE = 15


def load_tsv(tsv_path):
    """加载整个 TSV 到内存"""
    rows = []
    with open(tsv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            rows.append(row)
    return rows


def save_tsv(tsv_path, rows):
    """保存 TSV 到文件"""
    with open(tsv_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(rows)


def get_next_batch_indices(rows, batch_size):
    """获取下一批未翻译的行索引"""
    indices = []
    for i, row in enumerate(rows):
        if len(row) < 2 or not row[1].strip():
            indices.append(i)
            if len(indices) >= batch_size:
                break
    return indices


def print_progress(rows):
    """打印进度"""
    total = len(rows)
    translated = sum(1 for row in rows if len(row) >= 2 and row[1].strip())
    percent = translated / total * 100 if total > 0 else 0

    bar_length = 40
    filled = int(bar_length * translated / total)
    bar = '█' * filled + '░' * (bar_length - filled)

    print(f"[{bar}] {percent:.1f}% ({translated}/{total})")
    return translated == total


def print_batch_content(rows, indices):
    """打印批次内容"""
    print(f"\n待翻译的 {len(indices)} 行：")
    print("─" * 60)

    for idx, i in enumerate(indices, 1):
        text = rows[i][0] if rows[i] else ''
        print(f"{idx}. {text}")

    print("─" * 60)


def update_translations(rows, indices, translations):
    """更新指定索引的翻译"""
    updated_count = 0
    for i, trans in enumerate(translations):
        if i < len(indices):
            idx = indices[i]
            if trans.strip():
                if len(rows[idx]) < 2:
                    rows[idx].append(trans)
                else:
                    rows[idx][1] = trans
                updated_count += 1
    return updated_count


def main():
    if not TSV_PATH.exists():
        print(f"❌ TSV 文件不存在: {TSV_PATH}", file=sys.stderr)
        print(f"\n请先运行：python3 {baseDir}/scripts/translate.py")
        sys.exit(1)

    print("=" * 60)
    print("批量翻译助手")
    print("=" * 60)
    print("\n按 Ctrl+C 随时中断，进度会自动保存\n")

    try:
        while True:
            # 加载 TSV
            rows = load_tsv(TSV_PATH)

            # 打印当前进度
            print("\n当前进度：", end='')
            is_complete = print_progress(rows)

            if is_complete:
                print("\n\n✅ 所有行已翻译完成！")
                print(f"\n下一步：运行合并脚本")
                print(f"  python3 {baseDir}/scripts/translate.py")
                break

            # 获取下一批
            indices = get_next_batch_indices(rows, BATCH_SIZE)

            print_batch_content(rows, indices)

            # 提示用户输入
            print("\n翻译要求：")
            print("1. 保留专有名词：Claude Code、GitHub、Python、API、HTML、CSS")
            print("2. 保留技术术语：TUI、JSON、SSH")
            print("3. 不要使用引号（中文或英文）")
            print("4. 日期保留原样（如 2026-02-24）")
            print("\n请提供翻译（每行一个，空行跳过）：")

            # 读取翻译
            translations = []
            for i in range(len(indices)):
                try:
                    line = input(f"{i+1}> ").strip()
                    translations.append(line)
                except EOFError:
                    print("\n\n⚠️  输入结束")
                    return

            # 更新翻译
            updated = update_translations(rows, indices, translations)
            save_tsv(TSV_PATH, rows)

            print(f"\n✅ 已更新 {updated} 行翻译")

    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
        print(f"进度已保存到 {TSV_PATH}")
        print(f"可以重新运行此脚本继续翻译")
        sys.exit(0)


if __name__ == '__main__':
    main()
