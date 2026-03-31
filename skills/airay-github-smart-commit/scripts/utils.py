#!/usr/bin/env python3
"""
通用工具函数
"""

import re
from datetime import datetime
from typing import Dict, List, Tuple
from pathlib import Path


# 常用目录和忽略的文件名
COMMON_ROOTS = ["src", "lib", "app", "dist", "build", "test", "tests"]
IGNORED_PARTS = ["src", "lib", "app", "index", "main"]
CONFIG_EXTENSIONS = (".json", ".yaml", ".yml", ".toml", ".md")


# 预编译的正则表达式
class Patterns:
    """常用正则表达式模式（预编译以提高性能）"""

    # 版本号模式
    VERSION_PATTERNS = [
        re.compile(r"(Version\s*[：:]\s*)v?([\d.]+)", re.IGNORECASE),
        re.compile(r"(##?\s*Version\s*[：:]\s*)v?([\d.]+)", re.IGNORECASE),
        re.compile(r"(##?\s*Current\s+Version\s*[：:]\s*)v?([\d.]+)", re.IGNORECASE),
        re.compile(r"(##?\s*当前版本\s*[：:]\s*)v?([\d.]+)", re.IGNORECASE),
        re.compile(r"(\*\*Version:\*\*)\s*v?([\d.]+)", re.IGNORECASE),
        re.compile(r"(\*\*版本:\*\*)\s*v?([\d.]+)", re.IGNORECASE),
        re.compile(r"(版本[：:]\s*)v?([\d.]+)", re.IGNORECASE),
        re.compile(r"(https://img\.shields\.io/badge/version-)([\d.]+)", re.IGNORECASE),
        re.compile(r"(badge\.fury\.io/[^/]+/)([\d.]+)", re.IGNORECASE),
    ]

    # 日期模式
    DATE_PATTERNS = [
        re.compile(r"(##?\s*Last\s+Updated?\s*[：:]\s*)(\d{4}-\d{2}-\d{2})", re.IGNORECASE),
        re.compile(r"(##?\s*最后更新\s*[：:]\s*)(\d{4}-\d{2}-\d{2})", re.IGNORECASE),
        re.compile(r"(\*\*Last\s+Updated?:\*\*)\s*(\d{4}-\d{2}-\d{2})", re.IGNORECASE),
        re.compile(r"(\*\*最后更新:\*\*)\s*(\d{4}-\d{2}-\d{2})", re.IGNORECASE),
        re.compile(r"(最后更新[：:]\s*)(\d{4}-\d{2}-\d{2})", re.IGNORECASE),
        re.compile(r"(Last Updated[：:]\s*)(\d{4}-\d{2}-\d{2})", re.IGNORECASE),
    ]

    # README 风格检测（预编译）
    CYBERPUNK_PATTERNS = [
        re.compile(r"╔═+╗"),
        re.compile(r"║.*║"),
        re.compile(r"╚═+╝"),
        re.compile(r"系统状态："),
        re.compile(r"System Status:"),
        re.compile(r"版本：v\d+\.\d+\.\d+"),
        re.compile(r"Version: v\d+\.\d+\.\d+")
    ]

    STANDARD_PATTERNS = [
        re.compile(r"^# \w+"),
        re.compile(r"##\s+Version"),
        re.compile(r"##\s+版本"),
        re.compile(r"##\s+Installation"),
        re.compile(r"##\s+安装")
    ]

    BADGES_PATTERNS = [
        re.compile(r"!\[.*\]\(https://img\.shields\.io"),
        re.compile(r"!\[.*\]\(https://badge\.fury\.io"),
        re.compile(r"version.*badge"),
        re.compile(r"badge.*version")
    ]


def get_today() -> str:
    """获取今天的日期字符串 (YYYY-MM-DD)"""
    return datetime.now().strftime("%Y-%m-%d")


def get_build_date() -> str:
    """获取构建日期字符串 (YYYYMMDD)"""
    return datetime.now().strftime("%Y%m%d")


def extract_files_from_analysis(analysis: Dict) -> Tuple[List[str], List[str], List[str]]:
    """
    从分析结果中提取文件列表

    Args:
        analysis: 分析结果字典

    Returns:
        (modified_files, added_files, deleted_files)
    """
    return (
        analysis.get("modified_files", []),
        analysis.get("added_files", []),
        analysis.get("deleted_files", [])
    )


def replace_version(content: str, new_version: str) -> str:
    """
    在文本中替换版本号

    Args:
        content: 原始内容
        new_version: 新版本号

    Returns:
        替换后的内容
    """
    updated = content

    for pattern in Patterns.VERSION_PATTERNS:
        updated = pattern.sub(
            lambda m: f"{m.group(1)}{new_version}",
            updated
        )

    return updated


def replace_date(content: str, new_date: str = None) -> str:
    """
    在文本中替换日期

    Args:
        content: 原始内容
        new_date: 新日期字符串，默认为今天

    Returns:
        替换后的内容
    """
    if new_date is None:
        new_date = get_today()

    updated = content

    for pattern in Patterns.DATE_PATTERNS:
        updated = pattern.sub(
            lambda m: f"{m.group(1)}{new_date}",
            updated
        )

    return updated


def sanitize_filename(filename: str) -> str:
    """
    清理文件名：移除扩展名（除非是配置文件）

    Args:
        filename: 文件名

    Returns:
        清理后的文件名
    """
    if "." in filename and not filename.endswith(CONFIG_EXTENSIONS):
        return filename.rsplit(".", 1)[0]
    return filename


def extract_target_from_files(files: List[str]) -> str:
    """
    从文件列表中提取主要目标

    Args:
        files: 文件路径列表

    Returns:
        提取的目标名称
    """
    if not files:
        return ""

    main_file = files[0]

    # 如果路径中包含目录
    if "/" in main_file:
        parts = main_file.split("/")
        # 从后往前找第一个有意义的部分
        for part in reversed(parts):
            if part and part not in IGNORED_PARTS:
                return sanitize_filename(part)
        # 如果没找到，使用最后一部分
        return sanitize_filename(parts[-1])

    # 如果只是文件名，直接返回
    return sanitize_filename(main_file)


def describe_file_change(filepath: str, change_status: str = "") -> str:
    filename = Path(filepath).name.lower()
    path_lower = filepath.lower()

    # 特殊文件的描述
    special_files = {
        "readme.md": "项目说明文档",
        "changelog.md": "变更日志",
        "package.json": "项目配置和依赖",
        "tsconfig.json": "TypeScript 配置",
        "webpack.config.js": "构建配置",
        ".gitignore": "Git 忽略规则",
        ".env.example": "环境变量示例",
        "dockerfile": "Docker 配置",
        "docker-compose.yml": "Docker Compose 配置"
    }

    if filename in special_files:
        return special_files[filename]

    # 根据脚本文件名判断
    script_descriptions = {
        "config.py": "配置管理系统",
        "i18n.py": "国际化文本映射",
        "generate_commit.py": "Commit 消息生成器",
        "analyze_changes.py": "代码变更分析器",
        "categorization.py": "智能分类模块",
        "update_readme.py": "README 更新器",
        "update_version.py": "版本号更新器",
        "utils.py": "工具函数库"
    }

    if filename in script_descriptions:
        return script_descriptions[filename]

    # 认证相关
    if "auth" in path_lower or "login" in path_lower or "oauth" in path_lower:
        if "provider" in path_lower:
            return "OAuth 提供商"
        elif "session" in path_lower:
            return "会话管理"
        return "认证模块"

    # API 相关
    if "api" in path_lower:
        if "user" in path_lower:
            return "用户 API"
        return "API 接口"

    # 数据库相关
    if "db" in path_lower or "database" in path_lower or "query" in path_lower:
        return "数据库操作"

    # UI 相关
    if "ui" in path_lower or "component" in path_lower or "view" in path_lower:
        return "UI 组件"

    # 工具类
    if "util" in path_lower or "helper" in path_lower or "tool" in path_lower:
        return "工具函数"

    # 生成器、分析器类
    if "generate" in path_lower or "gen" in path_lower or "builder" in path_lower:
        return "生成器"
    if "analyze" in path_lower or "analysis" in path_lower or "parser" in path_lower:
        return "分析器"
    if "manager" in path_lower:
        return "管理器"

    # 测试相关
    if "test" in path_lower:
        return "测试用例" if change_status == "added" else "测试代码"

    # 配置相关
    if "config" in path_lower or "setting" in path_lower:
        return "配置管理"

    # 文档类
    if any(doc in path_lower for doc in ["readme", "contributing", "changelog", "license"]):
        if change_status == "added":
            return "添加项目文档"
        if change_status == "modified":
            return "更新文档说明"

    # Git 配置
    if ".gitmessage" in path_lower or "gitignore" in path_lower:
        return "Git 模板"

    # 脚本类
    if filename.endswith(".sh"):
        if "install" in path_lower:
            return "安装脚本"
        if "build" in path_lower:
            return "构建脚本"
        return "Shell 脚本"

    # Python 脚本
    if filename.endswith(".py"):
        return "脚本模块" if "scripts" in path_lower else "Python 模块"

    # 配置文件
    if any(ext in filename for ext in [".json", ".yaml", ".yml", ".toml", ".xml"]):
        return "配置示例" if "example" in path_lower or "sample" in path_lower else "配置文件"

    # 示例/模板文件
    if "example" in path_lower or "template" in path_lower or "sample" in path_lower:
        return "示例文件"

    # 默认返回
    if change_status == "added":
        return "新文件"
    if change_status == "modified":
        return "更新"
    return "变更"
