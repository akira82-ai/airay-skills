#!/usr/bin/env python3
"""
国际化模块
统一管理所有中英文文本映射
"""

# 变更类型描述（符合 Conventional Commits 规范）
TYPE_DESCRIPTIONS = {
    "en": {
        "feat": "Add",
        "fix": "Fix",
        "refactor": "Refactor",
        "docs": "Update",
        "style": "Fix style in",
        "test": "Add tests for",
        "chore": "Update",
        "perf": "Optimize",
        "ci": "Update CI",
        "build": "Update build"
    },
    "zh": {
        "feat": "添加",
        "fix": "修复",
        "refactor": "重构",
        "docs": "更新",
        "style": "调整样式",
        "test": "添加测试",
        "chore": "更新",
        "perf": "优化",
        "ci": "更新 CI",
        "build": "更新构建"
    }
}

# 文件统计描述（简洁格式）
FILE_STATS = {
    "en": {
        "added": "• Add {count} new files",
        "deleted": "• Remove {count} files",
        "modified": "• Modify {count} files",
        "more_files": "  ... and {count} more files",
        "modified_files_header": "Modified files:"
    },
    "zh": {
        "added": "• 新增 {count} 个文件",
        "deleted": "• 删除 {count} 个文件",
        "modified": "• 修改 {count} 个文件",
        "more_files": "  ... 以及其他 {count} 个文件",
        "modified_files_header": "修改的文件："
    }
}

# 破坏性变更警告
BREAKING_WARNING = {
    "en": "BREAKING CHANGE: This update contains breaking changes",
    "zh": "⚠️ 破坏性变更：此更新包含不兼容的 API 变更"
}

# 分类标题（详细格式使用）
CATEGORY_TITLES = {
    "zh": {
        "core_improvements": "**核心改进**",
        "new_features": "**新增功能**",
        "bug_fixes": "**修复问题**",
        "documentation": "**新增文档**",
        "configuration": "**配置变更**",
        "testing": "**测试完善**",
        "performance": "**性能优化**",
        "breaking_changes": "**破坏性变更**",
    },
    "en": {
        "core_improvements": "**Core Improvements**",
        "new_features": "**New Features**",
        "bug_fixes": "**Bug Fixes**",
        "documentation": "**Documentation**",
        "configuration": "**Configuration**",
        "testing": "**Testing**",
        "performance": "**Performance**",
        "breaking_changes": "**Breaking Changes**",
    }
}

# emoji 列表符号
BULLET_EMOJIS = {
    "zh": "✅",
    "en": "✓"
}

# 文件统计标题（详细格式）
FILE_STATS_TITLES = {
    "zh": {
        "modified": "修改的文件：",
        "added": "新增的文件：",
        "deleted": "删除的文件：",
    },
    "en": {
        "modified": "Modified files:",
        "added": "Added files:",
        "deleted": "Deleted files:",
    }
}


def get_text(mapping, language, key, fallback=None, **kwargs):
    """
    获取本地化文本

    Args:
        mapping: 文本映射字典
        language: "en" 或 "zh"
        key: 键名
        fallback: 如果键不存在时的回退值
        **kwargs: 格式化参数

    Returns:
        本地化文本字符串
    """
    lang_mapping = mapping.get(language, mapping.get("en", {}))
    text = lang_mapping.get(key, fallback or key)

    if kwargs:
        return text.format(**kwargs)
    return text
