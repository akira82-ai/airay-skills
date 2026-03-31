#!/usr/bin/env python3
"""
自动化批量翻译脚本
在主会话中逐批翻译，确保 100% 完成
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

    print(f"\n进度: [{bar}] {percent:.1f}% ({translated}/{total})")
    return translated == total


def print_batch_content(rows, indices):
    """打印批次内容"""
    print(f"\n{'='*60}")
    print(f"待翻译批次：{len(indices)} 行")
    print(f"{'='*60}\n")

    for idx, i in enumerate(indices, 1):
        text = rows[i][0] if rows[i] else ''
        print(f"{idx}. {text}")


def update_translations(tsv_path, start_idx, translations):
    """更新指定索引的翻译"""
    rows = load_tsv(tsv_path)
    updated_count = 0
    for i, trans in enumerate(translations):
        idx = start_idx + i
        if idx < len(rows):
            if len(rows[idx]) < 2:
                rows[idx].append(trans)
            else:
                rows[idx][1] = trans
            if trans.strip():  # 只记录非空翻译
                updated_count += 1
    save_tsv(tsv_path, rows)
    return updated_count


def main():
    import argparse

    parser = argparse.ArgumentParser(description='自动化批量翻译脚本')
    parser.add_argument('--update', nargs='+', metavar='TRANSLATION',
                        help='更新翻译：--update <start_idx> <trans1> <trans2> ...')
    parser.add_argument('--quiet', action='store_true',
                        help='静默模式，减少输出')

    args = parser.parse_args()

    if not TSV_PATH.exists():
        print(f"❌ TSV 文件不存在: {TSV_PATH}", file=sys.stderr)
        sys.exit(1)

    # 处理 --update 参数
    if args.update:
        try:
            start_idx = int(args.update[0])
            translations = args.update[1:]
            count = update_translations(TSV_PATH, start_idx, translations)
            if not args.quiet:
                print(f"✅ 已更新 {count} 行翻译")
                # 显示更新后的进度
                rows = load_tsv(TSV_PATH)
                print_progress(rows)
            return
        except (ValueError, IndexError) as e:
            print(f"❌ 参数错误: {e}", file=sys.stderr)
            print(f"用法: --update <start_idx> <trans1> <trans2> ...", file=sys.stderr)
            sys.exit(1)

    if not args.quiet:
        print("=" * 60)
        print("自动化批量翻译")
        print("=" * 60)

    # 加载 TSV
    rows = load_tsv(TSV_PATH)

    # 打印当前进度
    is_complete = print_progress(rows)

    if is_complete:
        if not args.quiet:
            print("\n✅ 所有行已翻译完成！")
            print(f"\n下一步：运行合并脚本")
            print(f"  python3 {baseDir}/scripts/translate.py")
        sys.exit(0)

    # 获取下一批
    indices = get_next_batch_indices(rows, BATCH_SIZE)

    if not args.quiet:
        print_batch_content(rows, indices)

        # 输出提示
        print(f"\n{'='*60}")
        print("翻译要求")
        print(f"{'='*60}")
        print("""
1. 保留专有名词：Claude Code、GitHub、Python、API、HTML、CSS
2. 保留技术术语：TUI、JSON、SSH
3. 不要使用引号（中文或英文）
4. 日期保留原样（如 2026-02-24）
5. 只提供翻译结果，格式：

行1翻译
行2翻译
行3翻译
...

完成后，使用以下命令更新翻译：
  python3 {baseDir}/scripts/auto_batch.py --update {idx} <trans1> <trans2> ...
或者直接编辑 TSV 文件：{tsv}
        """.format(idx=indices[0] if indices else 0, tsv=TSV_PATH))
    else:
        # 静默模式：只显示索引和原文
        for i in indices:
            print(f"{i}\t{rows[i][0]}")


if __name__ == '__main__':
    main()
