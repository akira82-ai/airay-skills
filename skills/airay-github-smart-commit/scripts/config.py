#!/usr/bin/env python3
"""
配置管理系统
支持项目级和全局配置
"""

import json
import sys
from pathlib import Path


DEFAULT_CONFIG = {
    # 语言配置
    "language": "zh",

    # README 更新风格
    "readme_style": "auto",

    # 版本号方案
    "version_scheme": "semver",

    # Commit 消息格式：simple | detailed | compact
    "commit_message_format": "simple",

    # 是否包含文件统计
    "include_file_stats": True,

    # 是否包含智能分类（详细格式）
    "include_categorization": False,

    # 摘要中最多显示的文件数
    "max_files_in_summary": 10,

    # 是否显示代码行数变化
    "show_line_changes": False,

    # 使用 emoji 作为列表符号（详细格式）
    "show_emoji_bullets": False
}


def find_config_file(project_dir=None):
    """
    查找配置文件
    优先级：项目级 > 全局级 > 默认配置
    """
    project_dir = Path(project_dir) if project_dir else Path.cwd()

    project_config = project_dir / ".smart-commit.json"
    if project_config.exists():
        return project_config, "project"

    home_config = Path.home() / ".smart-commit.json"
    if home_config.exists():
        return home_config, "global"

    return None, "default"


def load_config(project_dir=None):
    """
    加载配置
    返回合并后的配置字典
    """
    config_file, level = find_config_file(project_dir)

    if level == "default":
        return DEFAULT_CONFIG.copy(), "default"

    try:
        with open(config_file, "r", encoding="utf-8") as f:
            user_config = json.load(f)

        merged_config = DEFAULT_CONFIG.copy()
        merged_config.update(user_config)

        return merged_config, level

    except json.JSONDecodeError as e:
        print(f"错误：配置文件格式无效：{e}", file=sys.stderr)
        return DEFAULT_CONFIG.copy(), "error"


def create_default_config(output_path=None):
    """创建默认配置文件"""
    if output_path:
        output_path = Path(output_path)
    else:
        output_path = Path.cwd() / ".smart-commit.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(DEFAULT_CONFIG, f, indent=2, ensure_ascii=False)
        f.write("\n")

    return output_path


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("Usage: config.py <command> [args]", file=sys.stderr)
        print("Commands:", file=sys.stderr)
        print("  find [path]     查找配置文件", file=sys.stderr)
        print("  init [path]     创建配置文件", file=sys.stderr)
        print("  load [path]     加载并显示配置", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]

    if command == "find":
        project_dir = sys.argv[2] if len(sys.argv) > 2 else None
        config_file, level = find_config_file(project_dir)
        if config_file:
            print(f"{level}:{config_file}")
        else:
            print("default")

    elif command == "init":
        output_path = sys.argv[2] if len(sys.argv) > 2 else None
        config_path = create_default_config(output_path)
        print(f"✓ 配置文件已创建：{config_path}")

    elif command == "load":
        project_dir = sys.argv[2] if len(sys.argv) > 2 else None
        config, level = load_config(project_dir)
        print(f"配置级别: {level}")
        print(json.dumps(config, indent=2, ensure_ascii=False))

    else:
        print(f"未知命令：{command}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
