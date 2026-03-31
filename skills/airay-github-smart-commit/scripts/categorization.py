#!/usr/bin/env python3
"""
智能分类模块
将代码变更归类到不同类别：核心改进、新增功能、文档、配置等
"""

import re
from pathlib import Path
from typing import Dict, List

import utils


# 预编译的正则表达式模式
class ClassificationPatterns:
    """文件分类相关的预编译正则表达式"""

    # 文档类模式
    DOC_PATTERNS = [
        re.compile(r"\.md$"),
        re.compile(r"readme", re.IGNORECASE),
        re.compile(r"changelog", re.IGNORECASE),
        re.compile(r"contributing", re.IGNORECASE),
        re.compile(r"license", re.IGNORECASE),
        re.compile(r"docs/"),
        re.compile(r"documentation/")
    ]

    # 配置类模式
    CONFIG_PATTERNS = [
        re.compile(r"config", re.IGNORECASE),
        re.compile(r"\.json$"),
        re.compile(r"\.yaml$"),
        re.compile(r"\.yml$"),
        re.compile(r"\.toml$"),
        re.compile(r"\.xml$"),
        re.compile(r"\.env", re.IGNORECASE),
        re.compile(r"settings", re.IGNORECASE),
        re.compile(r"\.conf$"),
        re.compile(r"\.ini$")
    ]

    # 测试类模式
    TEST_PATTERNS = [
        re.compile(r"test", re.IGNORECASE),
        re.compile(r"spec", re.IGNORECASE),
        re.compile(r"__tests__"),
        re.compile(r"\.test\."),
        re.compile(r"\.spec\."),
        re.compile(r"mock", re.IGNORECASE),
        re.compile(r"fixture", re.IGNORECASE)
    ]

    # 性能相关模式
    PERF_PATTERNS = [
        re.compile(r"cache", re.IGNORECASE),
        re.compile(r"optimize", re.IGNORECASE),
        re.compile(r"performance", re.IGNORECASE),
        re.compile(r"lazy", re.IGNORECASE)
    ]


def categorize_changes(analysis, language="zh"):
    """
    智能分类变更内容

    根据文件路径、变更类型、文件内容分析，
    将变更归类到：核心改进、新增功能、文档、配置等

    Args:
        analysis: analyze_changes.py 的输出结果
        language: "zh" 或 "en"

    Returns:
        分类字典：
        {
            "core_improvements": [],
            "new_features": [],
            "bug_fixes": [],
            "documentation": [],
            "configuration": [],
            "testing": [],
            "performance": [],
            "breaking_changes": [],
            "other": []
        }
    """
    categories = {
        "core_improvements": [],
        "new_features": [],
        "bug_fixes": [],
        "documentation": [],
        "configuration": [],
        "testing": [],
        "performance": [],
        "breaking_changes": [],
        "other": []
    }

    change_type = analysis.get("type", "")
    modified_files = analysis.get("modified_files", [])
    added_files = analysis.get("added_files", [])
    deleted_files = analysis.get("deleted_files", [])
    is_breaking = analysis.get("is_breaking", False)

    # 所有文件列表
    all_files = list(zip(
        modified_files + added_files + deleted_files,
        ["modified"] * len(modified_files) +
        ["added"] * len(added_files) +
        ["deleted"] * len(deleted_files)
    ))

    # 如果是破坏性变更，添加到 breaking_changes
    if is_breaking:
        categories["breaking_changes"].append({
            "type": "breaking",
            "description": get_breaking_description(language),
            "files": [f[0] for f in all_files]
        })

    # 分类每个文件
    for filepath, change_status in all_files:
        category = classify_file(filepath, change_type, change_status)
        if category:
            categories[category].append({
                "file": filepath,
                "status": change_status,
                "description": utils.describe_file_change(filepath, change_status)
            })

    return categories


def classify_file(filepath, change_type, change_status):
    """
    对单个文件进行分类

    Returns:
        类别名称字符串
    """
    filename = Path(filepath).name.lower()
    path_lower = filepath.lower()
    path_parts = Path(filepath).parts

    # 文档类
    if any(p.search(path_lower) for p in ClassificationPatterns.DOC_PATTERNS):
        return "documentation"

    # 配置类
    if any(p.search(path_lower) for p in ClassificationPatterns.CONFIG_PATTERNS):
        return "configuration"

    # i18n 国际化相关
    if "i18n" in filename or "locale" in filename or "lang" in filename:
        return "configuration"

    # 测试类
    if any(p.search(path_lower) for p in ClassificationPatterns.TEST_PATTERNS):
        return "testing"

    # 性能优化相关
    if any(p.search(path_lower) for p in ClassificationPatterns.PERF_PATTERNS):
        return "performance"

    # 生成器、分析器、工具等核心模块
    if any(keyword in filename for keyword in ["generate", "analyze", "parser", "builder", "compiler"]):
        if change_type == "refactor":
            return "core_improvements"
        elif change_type == "feat":
            return "new_features"

    # 分类、路由等核心代码
    if path_parts and path_parts[0] in ["src", "lib", "core", "app", "scripts"]:
        if change_type == "feat":
            return "new_features"
        elif change_type == "refactor":
            return "core_improvements"
        elif change_type == "fix":
            return "bug_fixes"

    # 根据变更类型判断
    if change_type == "feat":
        return "new_features"
    elif change_type == "fix":
        return "bug_fixes"
    elif change_type == "refactor":
        return "core_improvements"

    # 默认归类到 other
    return "other"


def get_breaking_description(language):
    """获取破坏性变更的描述"""
    descriptions = {
        "zh": "此更新包含不兼容的 API 变更，请注意迁移",
        "en": "This update contains incompatible API changes"
    }
    return descriptions.get(language, descriptions["zh"])


def extract_line_changes(analysis):
    """
    从 git diff --stat 中提取代码行数变化

    解析格式：
    filename | 5 ++++---
    filename | 10 +++++-----

    Returns:
        {filename: (added, deleted)} 字典
    """
    stat_summary = analysis.get("stat_summary", "")
    line_changes = {}

    for line in stat_summary.split("\n"):
        if "|" not in line:
            continue

        parts = line.split("|")
        if len(parts) < 2:
            continue

        filename = parts[0].strip()
        changes = parts[1].strip()

        # 解析行数变化（单次遍历）
        # 格式：5 ++++--- 或 10 +++++-----
        added = sum(1 for c in changes if c == '+')
        deleted = sum(1 for c in changes if c == '-')

        if added > 0 or deleted > 0:
            line_changes[filename] = (added, deleted)

    return line_changes


def get_total_line_changes(line_changes):
    """
    获取总行数变化

    Returns:
        (total_added, total_deleted) 元组
    """
    total_added = sum(changes[0] for changes in line_changes.values())
    total_deleted = sum(changes[1] for changes in line_changes.values())
    return (total_added, total_deleted)


def generate_smart_summary(analysis, categories, language):
    """
    智能生成总体说明（第一段）

    例如："完整实现 GitHub Smart Commit 技能的所有计划功能："

    Returns:
        总体说明字符串
    """
    change_type = analysis.get("type", "")
    scope = analysis.get("scope", "")

    # 统计各类别数量
    category_counts = {
        cat: len(items) for cat, items in categories.items()
        if items and cat != "breaking_changes"
    }

    if not category_counts:
        # 没有具体分类，使用默认描述
        default_desc = {
            "zh": "更新代码",
            "en": "Update code"
        }
        return default_desc.get(language, "Update code")

    # 根据主要类别生成描述
    main_category = max(category_counts, key=category_counts.get)

    summaries = {
        "zh": {
            "new_features": f"添加新功能，增强系统能力",
            "core_improvements": f"重构代码结构，提升可维护性",
            "bug_fixes": f"修复已知问题，提升稳定性",
            "documentation": f"更新项目文档",
            "configuration": f"更新配置文件",
            "testing": f"完善测试覆盖",
            "performance": f"优化性能，提升响应速度"
        },
        "en": {
            "new_features": "Add new features to enhance system capabilities",
            "core_improvements": "Refactor code structure for better maintainability",
            "bug_fixes": "Fix known issues and improve stability",
            "documentation": "Update project documentation",
            "configuration": "Update configuration files",
            "testing": "Improve test coverage",
            "performance": "Optimize performance for better response time"
        }
    }

    return summaries.get(language, summaries["zh"]).get(
        main_category,
        "更新代码"
    )


def main():
    """测试主函数"""
    import json
    import sys

    # 测试数据
    test_analysis = {
        "type": "feat",
        "scope": "core",
        "is_breaking": False,
        "modified_files": ["src/auth.py", "README.md"],
        "added_files": ["src/api/user.py", "tests/test_auth.py"],
        "deleted_files": [],
        "stat_summary": "src/auth.py | 10 +++++-----\nREADME.md | 5 +++---"
    }

    categories = categorize_changes(test_analysis, "zh")
    print(json.dumps(categories, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
