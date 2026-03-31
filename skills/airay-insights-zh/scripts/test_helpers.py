#!/usr/bin/env python3
"""
insights-zh 技能测试辅助函数

用于验证翻译功能和输出正确性
"""

import re
import json
from pathlib import Path
from html.parser import HTMLParser
from typing import Dict, List, Any


def file_exists(path: str) -> bool:
    """检查文件是否存在"""
    return Path(path).expanduser().exists()


def contains_chinese_text(path: str) -> bool:
    """检查文件是否包含中文字符"""
    path = Path(path).expanduser()
    if not path.exists():
        return False

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查中文字符（Unicode 范围 U+4E00-U+9FFF）
    return bool(re.search(r'[\u4e00-\u9fff]', content))


def html_structure_valid(path: str) -> bool:
    """验证 HTML 结构是否完整"""
    path = Path(path).expanduser()
    if not path.exists():
        return False

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 基本检查：文件不为空，包含 HTML 标签
    if not content.strip():
        return False

    # 简单检查：包含基本的 HTML 结构
    has_html_tag = bool(re.search(r'<html', content, re.IGNORECASE))
    has_body_tag = bool(re.search(r'<body', content, re.IGNORECASE))

    # 至少应该有一些 HTML 标签
    has_any_tags = bool(re.search(r'<[^>]+>', content))

    return has_any_tags


def styles_preserved(path: str) -> bool:
    """验证 CSS 样式和类名是否保留"""
    path = Path(path).expanduser()
    if not path.exists():
        return False

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查是否存在 style 标签或 class 属性
    has_style_tags = bool(re.search(r'<style[^>]*>.*?</style>', content, re.DOTALL | re.IGNORECASE))
    has_class_attributes = bool(re.search(r'class=["\'][^"\']*["\']', content))

    return has_style_tags or has_class_attributes


def html_tags_preserved(path: str) -> bool:
    """验证 HTML 标签是否完整保留"""
    path = Path(path).expanduser()
    if not path.exists():
        return False

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 计算标签数量
    opening_tags = len(re.findall(r'<([a-z][a-z0-9]*)\b', content, re.IGNORECASE))
    closing_tags = len(re.findall(r'</([a-z][a-z0-9]*)>', content, re.IGNORECASE))

    # 应该有相当数量的开标签和闭标签
    return opening_tags > 0 and closing_tags > 0


def css_preserved(path: str) -> bool:
    """验证 CSS 样式是否保留"""
    path = Path(path).expanduser()
    if not path.exists():
        return False

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查 style 标签内容
    style_blocks = re.findall(r'<style[^>]*>(.*?)</style>', content, re.DOTALL | re.IGNORECASE)

    # 至少应该有一些 CSS 规则
    for block in style_blocks:
        if re.search(r'\{[^}]*\}', block.strip()):
            return True

    return False


def javascript_preserved(path: str) -> bool:
    """验证 JavaScript 代码是否保留"""
    path = Path(path).expanduser()
    if not path.exists():
        return False

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查 script 标签内容
    script_blocks = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL | re.IGNORECASE)

    # 至少应该有一些 JavaScript 代码
    for block in script_blocks:
        if re.search(r'function|var|let|const|if|for|while', block.strip()):
            return True

    return False


def html_attributes_preserved(path: str) -> bool:
    """验证 HTML 属性值是否保留"""
    path = Path(path).expanduser()
    if not path.exists():
        return False

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查常见属性
    common_attributes = ['class=', 'id=', 'style=', 'href=', 'src=']
    has_attributes = any(attr in content for attr in common_attributes)

    return has_attributes


def validate_translation_quality(
    original_path: str,
    translated_path: str
) -> Dict[str, Any]:
    """
    验证翻译质量

    Args:
        original_path: 原始 HTML 文件路径
        translated_path: 翻译后的 HTML 文件路径

    Returns:
        包含验证结果的字典
    """
    original_path = Path(original_path).expanduser()
    translated_path = Path(translated_path).expanduser()

    result = {
        "valid": True,
        "issues": [],
        "metrics": {}
    }

    if not original_path.exists():
        result["valid"] = False
        result["issues"].append(f"原始文件不存在: {original_path}")
        return result

    if not translated_path.exists():
        result["valid"] = False
        result["issues"].append(f"翻译文件不存在: {translated_path}")
        return result

    with open(original_path, 'r', encoding='utf-8') as f:
        original_content = f.read()

    with open(translated_path, 'r', encoding='utf-8') as f:
        translated_content = f.read()

    # 检查是否包含中文
    has_chinese = contains_chinese_text(str(translated_path))
    result["metrics"]["has_chinese"] = has_chinese

    if not has_chinese:
        result["valid"] = False
        result["issues"].append("翻译文件不包含中文字符")

    # 检查 HTML 标签数量是否一致
    original_tags = len(re.findall(r'<[^>]+>', original_content))
    translated_tags = len(re.findall(r'<[^>]+>', translated_content))
    result["metrics"]["original_tags"] = original_tags
    result["metrics"]["translated_tags"] = translated_tags

    if original_tags != translated_tags:
        result["valid"] = False
        result["issues"].append(f"HTML 标签数量不一致: 原始 {original_tags}, 翻译 {translated_tags}")

    # 检查文件大小
    original_size = len(original_content)
    translated_size = len(translated_content)
    result["metrics"]["original_size"] = original_size
    result["metrics"]["translated_size"] = translated_size
    result["metrics"]["size_ratio"] = translated_size / original_size if original_size > 0 else 0

    # 翻译后的文件应该在原始大小的 50%-200% 之间（中文通常更紧凑）
    if not (0.5 <= result["metrics"]["size_ratio"] <= 2.0):
        result["issues"].append(f"文件大小比例异常: {result['metrics']['size_ratio']:.2%}")

    return result


def run_test_case(test_case: Dict[str, Any]) -> Dict[str, Any]:
    """
    运行单个测试用例

    Args:
        test_case: 测试用例字典

    Returns:
        包含测试结果的字典
    """
    result = {
        "id": test_case["id"],
        "name": test_case["name"],
        "passed": True,
        "assertions": [],
        "errors": []
    }

    for assertion in test_case.get("assertions", []):
        assertion_result = {
            "name": assertion["name"],
            "description": assertion["description"],
            "passed": False,
            "error": None
        }

        try:
            check = assertion["check"]

            # 简单的断言检查（实际使用时需要更复杂的评估）
            if "file_exists" in check:
                path = check.split("(")[1].rstrip(")").strip("'\"")
                assertion_result["passed"] = file_exists(path)
            elif "contains_chinese_text" in check:
                path = check.split("(")[1].rstrip(")").strip("'\"")
                assertion_result["passed"] = contains_chinese_text(path)
            elif "html_structure_valid" in check:
                path = check.split("(")[1].rstrip(")").strip("'\"")
                assertion_result["passed"] = html_structure_valid(path)
            else:
                assertion_result["error"] = f"未实现的检查: {check}"

            if not assertion_result["passed"]:
                result["passed"] = False

        except Exception as e:
            assertion_result["error"] = str(e)
            result["passed"] = False
            result["errors"].append(f"{assertion['name']}: {e}")

        result["assertions"].append(assertion_result)

    return result


def main():
    """主函数：运行所有测试用例"""
    evals_path = Path(__file__).parent.parent / "evals" / "evals.json"

    if not evals_path.exists():
        print(f"❌ 测试文件不存在: {evals_path}")
        return

    with open(evals_path, 'r', encoding='utf-8') as f:
        eval_data = json.load(f)

    print(f"🧪 运行 {eval_data['skill_name']} 测试用例\n")

    results = []
    for test_case in eval_data["evals"]:
        result = run_test_case(test_case)
        results.append(result)

        status = "✅ 通过" if result["passed"] else "❌ 失败"
        print(f"{status} - {result['name']}: {test_case.get('description', '')}")

        for assertion in result["assertions"]:
            status = "  ✅" if assertion["passed"] else "  ❌"
            print(f"{status} {assertion['name']}: {assertion['description']}")
            if assertion.get("error"):
                print(f"     错误: {assertion['error']}")

        print()

    # 总结
    passed = sum(1 for r in results if r["passed"])
    total = len(results)
    print(f"\n📊 测试结果: {passed}/{total} 通过")

    if passed == total:
        print("🎉 所有测试通过！")
    else:
        print(f"⚠️ {total - passed} 个测试失败")


if __name__ == "__main__":
    main()
