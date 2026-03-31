#!/usr/bin/env python3
"""
生成美观的 Commit 消息
格式：<emoji> <type>(<scope>): <subject>
"""

import json
import sys
import os

# 添加 scripts 目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import i18n
import utils
import categorization


def generate_commit_message(analysis, custom_message=None, language="zh", config=None):
    """
    生成 commit 消息

    Args:
        analysis: analyze_changes.py 的输出结果
        custom_message: 用户自定义的 commit 消息（可选）
        language: "en" 或 "zh"，决定 commit 消息语言
        config: 配置字典（可选），用于控制消息格式

    Returns:
        完整的 commit 消息字符串
    """
    if custom_message:
        return custom_message

    # 加载配置
    if config is None:
        config = {}
    message_format = config.get("commit_message_format", "simple")
    include_categorization = config.get("include_categorization", False)
    show_line_changes = config.get("show_line_changes", False)
    show_emoji_bullets = config.get("show_emoji_bullets", False)

    emoji = analysis.get("emoji", "🔧")
    change_type = analysis.get("type", "chore")
    scope = analysis.get("scope", "")
    is_breaking = analysis.get("is_breaking", False)

    # 生成 subject
    subject = generate_smart_subject(analysis, emoji, change_type, scope, is_breaking, language)

    # 根据格式选择不同的生成方式
    if message_format == "detailed" or include_categorization:
        body = generate_detailed_body(
            analysis, language, config,
            show_line_changes, show_emoji_bullets
        )
    else:
        body = generate_simple_body(analysis, language)

    # 构建 footer
    footer_parts = []

    if is_breaking:
        warning = i18n.BREAKING_WARNING.get(language, i18n.BREAKING_WARNING.get("zh", ""))
        footer_parts.append(warning)
        footer_parts.append("")

    # Claude 署名
    footer_parts.append("Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>")

    # 组合完整消息
    commit_message = subject
    if body:
        commit_message += "\n\n" + body
    if footer_parts:
        commit_message += "\n" + "\n".join(footer_parts)

    return commit_message


def generate_smart_subject(analysis, emoji, change_type, scope, is_breaking, language):
    """智能生成 subject（符合 Conventional Commits 规范）"""
    # 分析变更内容，生成更准确的 subject
    subject_desc = generate_subject_description(analysis, change_type, scope, language)

    # 构建 subject（简化格式，更符合中文习惯）
    if scope and subject_desc:
        subject = f"{emoji} {change_type}({scope}): {subject_desc}"
    elif scope:
        subject = f"{emoji} {change_type}({scope}): 更新"
    elif subject_desc:
        subject = f"{emoji} {change_type}: {subject_desc}"
    else:
        # 如果没有明确目标，使用通用描述
        generic_descriptions = {
            "feat": "添加新功能",
            "fix": "修复问题",
            "refactor": "重构代码",
            "docs": "更新文档",
            "style": "调整样式",
            "test": "添加测试",
            "chore": "更新配置",
            "perf": "优化性能",
            "ci": "更新 CI",
            "build": "更新构建"
        }
        subject = f"{emoji} {change_type}: {generic_descriptions.get(change_type, '更新')}"

    if is_breaking:
        subject += " !"

    return subject


def generate_subject_description(analysis, change_type, scope, language):
    """根据文件变更生成 subject 描述"""
    modified_files, added_files, deleted_files = utils.extract_files_from_analysis(analysis)
    all_files = modified_files + added_files + deleted_files
    if not all_files:
        return None

    # 特殊文件优先
    for file in all_files:
        if "README" in file.upper():
            return "更新项目文档"

    # 根据 scope 和 change_type 判断（更准确）
    scope_action_map = {
        ("feat", "auth"): "添加认证功能",
        ("feat", "api"): "添加 API 接口",
        ("feat", "ui"): "添加 UI 组件",
        ("fix", "auth"): "修复认证问题",
        ("fix", "api"): "修复 API 问题",
        ("refactor", "core"): "重构核心代码",
        ("refactor", ""): "重构代码结构",
    }

    key = (change_type, scope)
    if key in scope_action_map:
        return scope_action_map[key]

    # 根据变更类型和 scope 生成通用描述
    if scope:
        action_map = {
            "feat": "添加",
            "fix": "修复",
            "refactor": "重构",
            "docs": "更新",
            "style": "调整",
            "test": "添加",
            "chore": "更新",
            "perf": "优化",
        }
        return f"{action_map.get(change_type, '更新')}{scope}"

    # 根据变更类型判断
    if change_type == "docs":
        return "更新文档"

    # 根据主要文件类型判断
    file_types = {}
    for file in all_files:
        ext = file.split(".")[-1] if "." in file else "unknown"
        file_types[ext] = file_types.get(ext, 0) + 1

    dominant_type = max(file_types, key=file_types.get)

    type_mapping = {
        "py": "Python 代码",
        "js": "JavaScript 代码",
        "md": "文档",
        "json": "配置",
        "yml": "配置",
        "yaml": "配置",
        "sh": "脚本"
    }

    if dominant_type in type_mapping:
        return f"更新{type_mapping[dominant_type]}"

    return None


def generate_change_description(analysis, language, modified_files=None, added_files=None, deleted_files=None):
    """生成变更描述（详细说明变更原因）"""
    if modified_files is None:
        modified_files, added_files, deleted_files = utils.extract_files_from_analysis(analysis)

    if not modified_files and not added_files and not deleted_files:
        return ""

    change_type = analysis.get("type", "")
    scope = analysis.get("scope", "")

    # 统计信息
    lines = []
    if added_files:
        lines.append(i18n.get_text(i18n.FILE_STATS, language, "added", count=len(added_files)))
    if deleted_files:
        lines.append(i18n.get_text(i18n.FILE_STATS, language, "deleted", count=len(deleted_files)))
    if modified_files:
        lines.append(i18n.get_text(i18n.FILE_STATS, language, "modified", count=len(modified_files)))

    # 根据文件内容生成智能描述
    description_lines = generate_smart_description(modified_files, added_files, deleted_files, change_type)
    if description_lines:
        lines.append("")
        lines.extend(description_lines)

    return "\n".join(lines)


def generate_smart_description(modified_files, added_files, deleted_files, change_type):
    """根据文件内容生成智能描述"""
    descriptions = []

    # 分析新增文件
    if added_files:
        for file in added_files:
            desc = utils.describe_file_change(file, "added")
            if desc:
                descriptions.append(f"  + {file} - {desc}")

    # 分析修改文件
    if modified_files:
        for file in modified_files:
            desc = utils.describe_file_change(file, "modified")
            if desc:
                descriptions.append(f"  ~ {file} - {desc}")

    # 分析删除文件
    if deleted_files:
        for file in deleted_files:
            descriptions.append(f"  - {file}")

    # 添加总体变更说明
    change_descriptions = {
        "feat": "添加新功能，增强系统能力",
        "fix": "修复已知问题，提升稳定性",
        "refactor": "重构代码结构，提升可维护性",
        "docs": "更新项目文档",
        "style": "调整代码样式，统一格式",
        "test": "完善测试覆盖",
        "chore": "更新配置和工具",
        "perf": "优化性能，提升响应速度",
        "ci": "更新 CI/CD 配置",
        "build": "更新构建配置"
    }
    if descriptions:
        descriptions.insert(0, "")
        descriptions.insert(0, change_descriptions.get(change_type, "更新代码"))

    return descriptions


def generate_simple_body(analysis, language):
    """
    生成简单格式的 body（当前默认格式）

    Returns:
        body 字符串
    """
    body_parts = []

    # 提取文件列表
    modified_files, added_files, deleted_files = utils.extract_files_from_analysis(analysis)

    # 添加详细变更描述
    change_description = generate_change_description(analysis, language, modified_files, added_files, deleted_files)
    if change_description:
        body_parts.append(change_description)
        body_parts.append("")

    # 如果文件太多，添加提示
    total_files = len(modified_files) + len(added_files) + len(deleted_files)
    if total_files > 15:
        more_text = f"完整变更: 共 {total_files} 个文件"
        body_parts.append(more_text)
        body_parts.append("")

    return "\n".join(body_parts).strip()


def generate_detailed_body(analysis, language, config, show_line_changes, show_emoji_bullets):
    """
    生成详细格式的 body（用户期望的 CHANGELOG 风格）

    结构：
    1. 总体说明（智能生成）
    2. 分类变更列表（**核心改进**：...）
    3. 文件统计（Modified files:、Added files:）

    Returns:
        body 字符串
    """
    body_parts = []

    # 智能分类变更
    categories = categorization.categorize_changes(analysis, language)

    # 生成总体说明
    summary = categorization.generate_smart_summary(analysis, categories, language)
    if summary:
        body_parts.append(summary)
        body_parts.append("")

    # 生成分类变更列表
    category_list = generate_category_list(
        categories, language, show_emoji_bullets
    )
    if category_list:
        body_parts.append(category_list)
        body_parts.append("")

    # 生成文件统计
    file_stats = generate_file_statistics(analysis, language, show_line_changes)
    if file_stats:
        body_parts.append(file_stats)

    return "\n".join(body_parts).strip()


def generate_category_list(categories, language, show_emoji_bullets):
    """
    生成分类变更列表

    格式：
    **核心改进**：
    - 描述 1
    - 描述 2

    **新增功能**：
    ✅ 功能 1
    ✅ 功能 2

    Returns:
        分类列表字符串
    """
    lines = []

    # 类别顺序（按优先级）
    category_order = [
        "breaking_changes",
        "core_improvements",
        "new_features",
        "bug_fixes",
        "documentation",
        "configuration",
        "testing",
        "performance"
    ]

    # 获取类别标题
    titles = i18n.CATEGORY_TITLES.get(language, i18n.CATEGORY_TITLES.get("zh", {}))
    bullet_emoji = i18n.BULLET_EMOJIS.get(language, i18n.BULLET_EMOJIS.get("zh", "✅"))

    for category in category_order:
        items = categories.get(category, [])
        if not items:
            continue

        # 添加类别标题
        title = titles.get(category, category)
        lines.append(f"{title}：")

        # 添加该类别下的所有项目
        for item in items:
            if category == "breaking_changes":
                # 破坏性变更是特殊的，它有 description 和 files
                desc = item.get("description", "")
                lines.append(f"- {desc}")
                files = item.get("files", [])
                if files:
                    lines.append(f"  影响范围：{', '.join(files)}")
            else:
                # 普通项目：显示文件名和描述
                file_path = item.get("file", "")
                desc = item.get("description", "")

                if show_emoji_bullets and category == "new_features":
                    bullet = bullet_emoji
                else:
                    bullet = "-"

                # 如果有描述，显示为：文件名 - 描述
                if desc and desc != file_path:
                    lines.append(f"{bullet} {file_path} - {desc}")
                else:
                    lines.append(f"{bullet} {file_path}")

        lines.append("")  # 类别之间空一行

    return "\n".join(lines).strip()


def generate_file_statistics(analysis, language, show_line_changes):
    """
    生成文件统计部分

    格式：
    Modified files:
      SKILL.md

    Added files:
      README.md
      CHANGELOG.md

    或（带行数变化）：
    Modified files:
      SKILL.md (190 行 → 607 行)

    Returns:
        文件统计字符串
    """
    modified_files, added_files, deleted_files = utils.extract_files_from_analysis(analysis)

    if not modified_files and not added_files and not deleted_files:
        return ""

    lines = []
    titles = i18n.FILE_STATS_TITLES.get(language, i18n.FILE_STATS_TITLES.get("zh", {}))

    # 如果需要显示行数变化，提取行数信息
    line_changes = {}
    if show_line_changes:
        line_changes = categorization.extract_line_changes(analysis)

    # Modified files
    if modified_files:
        lines.append(titles.get("modified", "Modified files:"))
        for filepath in modified_files:
            if show_line_changes and filepath in line_changes:
                added, deleted = line_changes[filepath]
                total = added + deleted
                lines.append(f"  {filepath} ({total} 行)")
            else:
                lines.append(f"  {filepath}")
        lines.append("")

    # Added files
    if added_files:
        lines.append(titles.get("added", "Added files:"))
        for filepath in added_files:
            if show_line_changes and filepath in line_changes:
                added, deleted = line_changes[filepath]
                lines.append(f"  {filepath} (+{added} 行)")
            else:
                lines.append(f"  {filepath}")
        lines.append("")

    # Deleted files
    if deleted_files:
        lines.append(titles.get("deleted", "Deleted files:"))
        for filepath in deleted_files:
            lines.append(f"  {filepath}")

    return "\n".join(lines).strip()


def main():
    """主函数"""
    try:
        analysis = json.load(sys.stdin)
    except json.JSONDecodeError:
        print(json.dumps({"error": "无效的 JSON 输入"}), file=sys.stderr)
        sys.exit(1)

    commit_message = generate_commit_message(analysis)
    print(commit_message)


if __name__ == "__main__":
    main()
