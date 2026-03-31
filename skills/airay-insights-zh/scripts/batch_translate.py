#!/usr/bin/env python3
"""
可靠的批量翻译脚本
确保每一行都被翻译完成
"""
import sys
import csv
from pathlib import Path

TSV_PATH = Path('/tmp/insights_blocks.tsv')
BATCH_SIZE = 20  # 每批翻译的行数


def count_translated(tsv_path):
    """统计翻译进度"""
    total = 0
    translated = 0
    untranslated_lines = []

    with open(tsv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for i, row in enumerate(reader):
            total += 1
            if len(row) >= 2 and row[1].strip():
                translated += 1
            else:
                untranslated_lines.append(i)

    return total, translated, untranslated_lines


def get_next_batch(tsv_path, batch_size):
    """获取下一批未翻译的行"""
    batch = []
    line_numbers = []

    with open(tsv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for i, row in enumerate(reader):
            if len(row) < 2 or not row[1].strip():
                batch.append(row)
                line_numbers.append(i)
                if len(batch) >= batch_size:
                    break

    return batch, line_numbers


def print_batch(batch, line_numbers):
    """打印当前批次"""
    print(f"\n{'='*60}")
    print(f"当前批次：{len(batch)} 行待翻译")
    print(f"{'='*60}")

    for i, (line_num, row) in enumerate(zip(line_numbers, batch)):
        print(f"\n[{i+1}] 行 {line_num}:")
        print(f"    原文: {row[0][:80]}{'...' if len(row[0]) > 80 else ''}")
        if len(row) >= 2 and row[1]:
            print(f"    译文: {row[1][:80]}{'...' if len(row[1]) > 80 else ''}")


def main():
    if not TSV_PATH.exists():
        print(f"❌ TSV 文件不存在: {TSV_PATH}")
        sys.exit(1)

    print("=" * 60)
    print("可靠的批量翻译工具")
    print("=" * 60)

    # 检查当前进度
    total, translated, untranslated = count_translated(TSV_PATH)
    print(f"\n当前进度: {translated}/{total} 行已翻译 ({translated/total*100:.1f}%)")
    print(f"待翻译: {len(untranslated)} 行")

    if translated == total:
        print("\n✅ 所有行已翻译完成！")
        print(f"可以运行合并脚本生成 HTML 了")
        sys.exit(0)

    # 获取下一批
    batch, line_numbers = get_next_batch(TSV_PATH, BATCH_SIZE)
    print_batch(batch, line_numbers)

    print(f"\n{'='*60}")
    print("请使用以下命令翻译这批内容：")
    print(f"{'='*60}")
    print(f"\nAgent 工具命令：")
    print(f'  请翻译以下 {len(batch)} 行文本为中文：\n')

    for i, (line_num, row) in enumerate(zip(line_numbers, batch)):
        text = row[0]
        print(f'{i+1}. {text}')

    print(f'\n要求：')
    print(f'1. 只提供中文翻译，不需要原文')
    print(f'2. 每行一个翻译')
    print(f'3. 保留专有名词（Claude Code、GitHub 等）')
    print(f'4. 保留技术术语（API、HTML、CSS 等）')
    print(f'5. 不要使用引号')
    print(f'6. 日期保留原样')

    print(f'\n翻译完成后，将结果填入 TSV 文件')
    print(f'然后重新运行此脚本继续下一批\n')


if __name__ == '__main__':
    main()
