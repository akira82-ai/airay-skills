#!/usr/bin/env python3
"""
自动更新项目版本号
支持多种项目类型：Node.js, Python, Rust, Go
"""

import json
import re
import sys
from pathlib import Path


def parse_version(version_str):
    """解析版本号字符串"""
    match = re.search(r"(\d+)\.(\d+)\.(\d+)", version_str)
    if match:
        return tuple(map(int, match.groups()))
    return None


def bump_version(current_version, bump_type):
    """升级版本号"""
    major, minor, patch = parse_version(current_version) or (0, 0, 0)

    if bump_type == "major":
        return f"{major + 1}.0.0"
    elif bump_type == "minor":
        return f"{major}.{minor + 1}.0"
    else:  # patch
        return f"{major}.{minor}.{patch + 1}"


def read_package_json_version(file_path):
    """读取 package.json 版本号（不修改文件）"""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("version", "0.0.0")


def update_package_json(file_path, new_version):
    """更新 package.json"""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    old_version = data.get("version", "0.0.0")
    data["version"] = new_version

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    return old_version


def read_pyproject_toml_version(file_path):
    """读取 pyproject.toml 版本号（不修改文件）"""
    content = file_path.read_text(encoding="utf-8")
    match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
    return match.group(1) if match else "0.0.0"


def update_pyproject_toml(file_path, new_version):
    """更新 pyproject.toml"""
    content = file_path.read_text(encoding="utf-8")

    # 提取当前版本
    match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
    old_version = match.group(1) if match else "0.0.0"

    # 更新版本
    updated = re.sub(
        r'(version\s*=\s*["\'])[^"\']+(["\'])',
        f"\\g<1>{new_version}\\g<2>",
        content
    )

    file_path.write_text(updated, encoding="utf-8")
    return old_version


def read_cargo_toml_version(file_path):
    """读取 Cargo.toml 版本号（不修改文件）"""
    content = file_path.read_text(encoding="utf-8")
    match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
    return match.group(1) if match else "0.0.0"


def update_cargo_toml(file_path, new_version):
    """更新 Cargo.toml"""
    content = file_path.read_text(encoding="utf-8")

    # 提取当前版本
    match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
    old_version = match.group(1) if match else "0.0.0"

    # 更新版本
    updated = re.sub(
        r'(version\s*=\s*["\'])[^"\']+(["\'])',
        f"\\g<1>{new_version}\\g<2>",
        content
    )

    file_path.write_text(updated, encoding="utf-8")
    return old_version


def read_go_mod_version(file_path):
    """读取 go.mod 版本号（不修改文件）"""
    content = file_path.read_text(encoding="utf-8")
    # Go modules 使用语义化版本，但不在 go.mod 中存储
    # 需要从其他地方获取，这里返回默认值
    match = re.search(r"module\s+\S+\s+v?(\d+\.\d+\.\d+)", content)
    return match.group(1) if match else "0.0.0"


def update_go_mod_version(file_path, new_version):
    """更新 go.mod 版本号"""
    # Go modules 通常不在 go.mod 中存储版本号
    # 这里我们只记录，实际不修改文件
    content = file_path.read_text(encoding="utf-8")
    match = re.search(r"module\s+\S+\s+v?(\d+\.\d+\.\d+)", content)
    old_version = match.group(1) if match else "0.0.0"
    return old_version


def read_gemfile_version(file_path):
    """读取 Gemfile 版本号（不修改文件）"""
    content = file_path.read_text(encoding="utf-8")
    # Gemfile 通常在 .gemspec 中定义版本
    match = re.search(r"s\.version\s*=\s*['\"]([^'\"]+)['\"]", content)
    return match.group(1) if match else "0.0.0"


def update_gemfile_version(file_path, new_version):
    """更新 Gemfile 版本号"""
    content = file_path.read_text(encoding="utf-8")
    match = re.search(r"(s\.version\s*=\s*['\"])([^'\"]+)(['\"])", content)
    if match:
        old_version = match.group(2)
        updated = content[:match.start()] + f"{match.group(1)}{new_version}{match.group(3)}" + content[match.end():]
        file_path.write_text(updated, encoding="utf-8")
        return old_version
    return "0.0.0"


def read_composer_json_version(file_path):
    """读取 composer.json 版本号（不修改文件）"""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("version", "0.0.0")


def update_composer_json(file_path, new_version):
    """更新 composer.json"""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    old_version = data.get("version", "0.0.0")
    data["version"] = new_version

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    return old_version


def read_pom_xml_version(file_path):
    """读取 pom.xml 版本号（不修改文件）"""
    content = file_path.read_text(encoding="utf-8")
    match = re.search(r"<version>([^<]+)</version>", content)
    return match.group(1) if match else "0.0.0"


def update_pom_xml(file_path, new_version):
    """更新 pom.xml"""
    content = file_path.read_text(encoding="utf-8")
    match = re.search(r"<version>([^<]+)</version>", content)
    old_version = match.group(1) if match else "0.0.0"

    # 替换所有版本号（可能有多个）
    updated = re.sub(
        r"<version>[^<]+</version>",
        f"<version>{new_version}</version>",
        content,
        count=1  # 只替换第一个（项目版本）
    )

    file_path.write_text(updated, encoding="utf-8")
    return old_version


def read_setup_py_version(file_path):
    """读取 setup.py 版本号（不修改文件）"""
    content = file_path.read_text(encoding="utf-8")
    match = re.search(r"version\s*=\s*['\"]([^'\"]+)['\"]", content)
    return match.group(1) if match else "0.0.0"


def update_setup_py(file_path, new_version):
    """更新 setup.py"""
    content = file_path.read_text(encoding="utf-8")
    match = re.search(r"(version\s*=\s*['\"])([^'\"]+)(['\"])", content)
    if match:
        old_version = match.group(2)
        updated = content[:match.start()] + f"{match.group(1)}{new_version}{match.group(3)}" + content[match.end():]
        file_path.write_text(updated, encoding="utf-8")
        return old_version
    return "0.0.0"


def detect_project_type(project_dir):
    """检测项目类型"""
    project_dir = Path(project_dir)

    # 按优先级检测
    if (project_dir / "package.json").exists():
        return "nodejs", project_dir / "package.json"
    elif (project_dir / "pyproject.toml").exists():
        return "python", project_dir / "pyproject.toml"
    elif (project_dir / "setup.py").exists():
        return "python-setup", project_dir / "setup.py"
    elif (project_dir / "Cargo.toml").exists():
        return "rust", project_dir / "Cargo.toml"
    elif (project_dir / "go.mod").exists():
        return "go", project_dir / "go.mod"
    elif (project_dir / "Gemfile").exists() or (project_dir / "*.gemspec").exists():
        gemspec = list(project_dir.glob("*.gemspec"))
        if gemspec:
            return "ruby", gemspec[0]
        return "ruby", project_dir / "Gemfile"
    elif (project_dir / "composer.json").exists():
        return "php", project_dir / "composer.json"
    elif (project_dir / "pom.xml").exists():
        return "java", project_dir / "pom.xml"

    return None, None


def main():
    """主函数"""
    if len(sys.argv) < 3:
        print("Usage: update_version.py <project_dir> <bump_type>", file=sys.stderr)
        sys.exit(1)

    project_dir = Path(sys.argv[1])
    bump_type = sys.argv[2]  # major, minor, patch

    # 检测项目类型
    project_type, config_file = detect_project_type(project_dir)

    if not project_type:
        print("警告：无法识别项目类型，跳过版本号更新", file=sys.stderr)
        sys.exit(0)

    # 更新版本号
    try:
        # 第一步：读取当前版本（不修改文件）
        if project_type == "nodejs":
            old_version = read_package_json_version(config_file)
        elif project_type == "python":
            old_version = read_pyproject_toml_version(config_file)
        elif project_type == "python-setup":
            old_version = read_setup_py_version(config_file)
        elif project_type == "rust":
            old_version = read_cargo_toml_version(config_file)
        elif project_type == "go":
            old_version = read_go_mod_version(config_file)
        elif project_type == "ruby":
            old_version = read_gemfile_version(config_file)
        elif project_type == "php":
            old_version = read_composer_json_version(config_file)
        elif project_type == "java":
            old_version = read_pom_xml_version(config_file)
        else:
            old_version = "0.0.0"

        # 第二步：计算新版本
        new_version = bump_version(old_version, bump_type)

        # 第三步：更新文件
        if project_type == "nodejs":
            update_package_json(config_file, new_version)
        elif project_type == "python":
            update_pyproject_toml(config_file, new_version)
        elif project_type == "python-setup":
            update_setup_py(config_file, new_version)
        elif project_type == "rust":
            update_cargo_toml(config_file, new_version)
        elif project_type == "go":
            update_go_mod_version(config_file, new_version)
        elif project_type == "ruby":
            update_gemfile_version(config_file, new_version)
        elif project_type == "php":
            update_composer_json(config_file, new_version)
        elif project_type == "java":
            update_pom_xml(config_file, new_version)

        print(json.dumps({
            "old_version": old_version,
            "new_version": new_version,
            "project_type": project_type,
            "config_file": str(config_file)
        }))

    except Exception as e:
        print(f"错误：更新版本号失败：{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
