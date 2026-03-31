#!/usr/bin/env python3
"""
Insights 报告翻译脚本（重构版）
使用 TSV 格式 + Task 子代理，避免嵌套会话和 JSON 转义问题
"""
import os
import sys
import csv
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# ==================== 配置 ====================
DEFAULT_REPORT_PATH = Path.home() / '.claude/usage-data/report.html'
MAX_REPORT_AGE_DAYS = 3


# ==================== 报告检查 ====================
def check_report_freshness(report_path, max_days=MAX_REPORT_AGE_DAYS):
    """检查报告是否新鲜（max_days 天内）

    Returns:
        tuple: (is_fresh, message)
            - is_fresh: None=文件不存在, True=新鲜, False=过期
            - message: 描述信息
    """
    report_path = Path(report_path)

    if not report_path.exists():
        return None, f"报告文件不存在: {report_path}"

    mtime = report_path.stat().st_mtime
    file_date = datetime.fromtimestamp(mtime)
    age_days = (datetime.now() - file_date).days

    if age_days > max_days:
        return False, f"报告已过期 {age_days - max_days} 天（生成于 {file_date.strftime('%Y-%m-%d')}）"

    return True, f"报告新鲜（{age_days} 天前生成）"


# ==================== HTML 解析 ====================
def extract_text_blocks(html_path):
    """使用 BeautifulSoup 提取文本块，返回 (节点对象, 文本) 列表"""
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    nodes = []

    for string in soup.find_all(string=True):
        # 跳过 script/style 和文档节点
        if string.parent.name in ['script', 'style', '[document]']:
            continue

        text = string.strip()
        if text:
            nodes.append((string, text))  # 保存节点对象和文本

    return nodes


def save_to_tsv(nodes, tsv_path):
    """保存文本块到 TSV 文件"""
    with open(tsv_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t')
        for node, text in nodes:
            writer.writerow([text, ''])  # 原文、译文（空）


def load_from_tsv(tsv_path):
    """从 TSV 文件加载翻译，返回 {原文: 译文} 字典"""
    translations = {}
    with open(tsv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            if len(row) >= 2:
                original, translated = row[0], row[1]
                if translated:
                    translations[original] = translated
    return translations


# ==================== HTML 生成 ====================
def merge_translations(html_path, translations, output_path):
    """合并翻译结果到 HTML"""
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # 重新提取节点（确保与提取阶段一致）
    nodes = extract_text_nodes(soup)

    # 按原文匹配替换
    replace_count = 0
    for node, original in nodes:
        if original in translations:
            node.replace_with(translations[original])
            replace_count += 1

    # 保存结果
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    print(f"✅ 生成完成: {output_path}")
    print(f"   替换了 {replace_count} 个文本节点")
    return output_path


def extract_text_nodes(soup):
    """从 BeautifulSoup 对象提取文本节点，返回 (节点对象, 文本) 列表"""
    nodes = []
    for string in soup.find_all(string=True):
        # 跳过 script/style 和文档节点
        if string.parent.name in ['script', 'style', '[document]']:
            continue

        text = string.strip()
        if text:
            nodes.append((string, text))
    return nodes


# ==================== 主流程 ====================
def main():
    """主流程"""
    import argparse

    parser = argparse.ArgumentParser(description='Insights 报告翻译工具（重构版）')
    parser.add_argument('--path', type=str, help='源 HTML 报告路径')
    parser.add_argument('--output', type=str, default='./report-zh.html', help='输出 HTML 路径')
    parser.add_argument('--force', action='store_true', help='忽略报告过期检查')

    args = parser.parse_args()

    report_path = Path(args.path) if args.path else DEFAULT_REPORT_PATH
    output_path = Path(args.output)
    tsv_path = Path('/tmp/insights_blocks.tsv')

    print("=" * 60)
    print("Insights 报告翻译工具")
    print("=" * 60)

    # 检查报告
    print("\n[1/4] 检查报告状态...")
    is_fresh, msg = check_report_freshness(report_path)

    if is_fresh is None:
        print(f"❌ {msg}")
        print("\n请先运行 /insights 命令生成报告")
        return 1
    elif not is_fresh and not args.force:
        print(f"⚠️  {msg}")
        print("\n请运行 /insights 生成最新报告后再翻译")
        print("或使用 --force 参数强制翻译过期报告")
        return 1
    else:
        print(f"✅ {msg}")

    # 检查是否已有翻译内容
    try:
        translations = load_from_tsv(tsv_path)
        if translations:
            print(f"\n[3/4] 发现已翻译内容，跳过提取步骤")
            print(f"✅ 找到 {len(translations)} 条翻译")
        else:
            # 提取文本块
            print(f"\n[2/4] 提取文本块...")
            nodes = extract_text_blocks(report_path)
            total_chars = sum(len(text) for _, text in nodes)
            print(f"✅ 提取了 {len(nodes)} 个文本块，共 {total_chars} 字符")

            # 保存到 TSV
            save_to_tsv(nodes, tsv_path)
            print(f"✅ 已保存到 {tsv_path}")

            print(f"\n[3/4] 等待翻译...")
            print(f"请使用 Task 工具翻译 {tsv_path}")
            print(f"翻译完成后，将结果保存到 {tsv_path}")
            print(f"然后运行:")
            print(f"  python3 {__file__} --path {report_path} --output {output_path}")
            return 0
    except FileNotFoundError:
        # 提取文本块
        print(f"\n[2/4] 提取文本块...")
        nodes = extract_text_blocks(report_path)
        total_chars = sum(len(text) for _, text in nodes)
        print(f"✅ 提取了 {len(nodes)} 个文本块，共 {total_chars} 字符")

        # 保存到 TSV
        save_to_tsv(nodes, tsv_path)
        print(f"✅ 已保存到 {tsv_path}")

        print(f"\n[3/4] 等待翻译...")
        print(f"请使用 Task 工具翻译 {tsv_path}")
        print(f"翻译完成后，将结果保存到 {tsv_path}")
        print(f"然后运行:")
        print(f"  python3 {__file__} --path {report_path} --output {output_path}")
        return 0

    # 合并翻译结果
    print(f"\n[4/4] 合并翻译...")
    merge_translations(report_path, translations, output_path)

    # 清理临时文件
    try:
        tsv_path.unlink()
        progress_path = Path('/tmp/insights_progress.json')
        if progress_path.exists():
            progress_path.unlink()
        print(f"✅ 已清理临时文件: {tsv_path}")
    except Exception as e:
        print(f"⚠️  清理临时文件失败: {e}")

    # 在浏览器中打开
    try:
        subprocess.run(['open', str(output_path)])
    except:
        pass

    print("\n" + "=" * 60)
    print("✅ 翻译完成！")
    print(f"输出文件: {output_path.absolute()}")
    print("=" * 60)

    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
