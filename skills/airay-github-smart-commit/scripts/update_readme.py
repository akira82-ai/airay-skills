#!/usr/bin/env python3
"""
智能更新 README.md
支持多种风格：赛博朋克、标准格式、Badges、极简格式
"""

import re
import sys
from pathlib import Path

from . import utils


def detect_readme_style(content):
    """检测 README 风格"""
    # 使用预编译的正则表达式计算得分
    cyberpunk_score = sum(1 for pattern in utils.Patterns.CYBERPUNK_PATTERNS if pattern.search(content))
    standard_score = sum(1 for pattern in utils.Patterns.STANDARD_PATTERNS if pattern.search(content))
    badges_score = sum(1 for pattern in utils.Patterns.BADGES_PATTERNS if pattern.search(content))

    if cyberpunk_score >= 3:
        return "cyberpunk"
    elif badges_score >= 2:
        return "badges"
    elif standard_score >= 2:
        return "standard"
    else:
        return "minimal"


def update_badges_readme(content, new_version, analysis):
    """更新 Badges 格式的 README"""
    updated = content

    # 使用 utils 模块更新版本号
    updated = utils.replace_version(updated, new_version)

    # 使用 utils 模块更新日期
    updated = utils.replace_date(updated)

    return updated


def update_standard_readme(content, new_version, analysis):
    """更新标准格式的 README"""
    updated = content

    # 使用 utils 模块更新版本号和日期
    updated = utils.replace_version(updated, new_version)
    updated = utils.replace_date(updated)

    return updated


def update_minimal_readme(content, new_version, analysis):
    """更新极简格式的 README（只更新明显的版本号和日期）"""
    updated = content
    today = utils.get_today()

    # 更新明显的版本号模式
    updated = utils.replace_version(updated, new_version)

    # 更新日期
    updated = utils.replace_date(updated, today)

    return updated


def update_cyberpunk_readme(content, new_version, analysis):
    """更新赛博朋克风格的 README"""
    updated = content
    today = utils.get_today()
    build_date = utils.get_build_date()

    # 使用 utils 模块更新版本号
    updated = utils.replace_version(updated, new_version)

    # 更新构建日期
    # 中文版本
    updated = re.sub(
        r"(构建：)\d{8}",
        f"\\1{build_date}",
        updated
    )
    # 英文版本
    updated = re.sub(
        r"(Build: )\d{8}",
        f"\\1{build_date}",
        updated
    )

    # 使用 utils 模块更新日期
    updated = utils.replace_date(updated, today)

    # 5. 如果是新功能，添加到核心模块进度条（可选）
    if analysis.get("type") == "feat":
        # 这部分需要更智能的实现，暂时跳过
        pass

    return updated


def main():
    """主函数"""
    if len(sys.argv) < 3:
        print("Usage: update_readme.py <readme_path> <new_version> [analysis_json]", file=sys.stderr)
        sys.exit(1)

    readme_path = Path(sys.argv[1])
    new_version = sys.argv[2]

    # 读取 analysis（可选）
    analysis = {}
    if len(sys.argv) > 3:
        import json
        try:
            analysis = json.loads(sys.argv[3])
        except json.JSONDecodeError:
            pass

    # 检查 README 是否存在
    if not readme_path.exists():
        print(f"错误：README 文件不存在：{readme_path}", file=sys.stderr)
        sys.exit(1)

    # 读取 README 内容
    content = readme_path.read_text(encoding="utf-8")

    # 检测风格
    style = detect_readme_style(content)

    print(f"检测到 README 风格: {style}", file=sys.stderr)

    # 根据风格选择更新函数
    update_functions = {
        "cyberpunk": update_cyberpunk_readme,
        "badges": update_badges_readme,
        "standard": update_standard_readme,
        "minimal": update_minimal_readme
    }

    update_func = update_functions.get(style)
    if not update_func:
        print(f"警告：不支持的 README 风格 '{style}'，跳过自动更新", file=sys.stderr)
        sys.exit(0)

    # 更新 README
    updated_content = update_func(content, new_version, analysis)

    # 检查是否有变化
    if updated_content == content:
        print("提示：README 内容无需更新", file=sys.stderr)
        sys.exit(0)

    # 写回文件
    readme_path.write_text(updated_content, encoding="utf-8")

    print(f"✓ README 已更新到版本 v{new_version}")
    print(f"  风格: {style}", file=sys.stderr)


if __name__ == "__main__":
    main()
