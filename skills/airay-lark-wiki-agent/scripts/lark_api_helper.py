#!/usr/bin/env python3
"""
lark-cli API 调用辅助函数

解决 lark-cli 在处理包含中文字符的 JSON 数据时的编码问题。
"""

import subprocess
import json
from typing import Optional, Dict, Any


def lark_api(method: str,
             path: str,
             data: Optional[Dict[str, Any]] = None,
             params: Optional[Dict[str, Any]] = None) -> Optional[Dict]:
    """
    统一的 lark-cli API 调用封装

    Args:
        method: HTTP 方法 (GET, POST, PUT, DELETE, PATCH)
        path: API 路径 (如 "/open-apis/wiki/v2/spaces/xxx/nodes")
        data: 请求体数据 (字典)
        params: 查询参数 (字典)

    Returns:
        响应数据字典，失败返回 None

    Example:
        # 创建 Wiki 节点
        result = lark_api(
            "POST",
            "/open-apis/wiki/v2/spaces/7472294423981064194/nodes",
            data={
                "obj_type": "docx",
                "parent_node_token": "xxx",
                "node_type": "origin",
                "title": "每日复盘 - 2026-04-06"
            }
        )

        # 获取节点列表
        result = lark_api(
            "GET",
            "/open-apis/wiki/v2/spaces/7472294423981064194/nodes",
            params={"parent_node_token": "", "page_size": 50}
        )
    """
    cmd = ["lark-cli", "api", method, path]

    if params:
        cmd.extend(["--params", json.dumps(params, ensure_ascii=False)])
    if data:
        cmd.extend(["--data", json.dumps(data, ensure_ascii=False)])

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding='utf-8'
    )

    if result.returncode != 0:
        print(f"Error (exit code {result.returncode}):")
        if result.stderr:
            print(f"  Stderr: {result.stderr}")
        if result.stdout:
            print(f"  Stdout: {result.stdout}")
        return None

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        print(f"  Raw response: {result.stdout}")
        return None


if __name__ == "__main__":
    # 测试示例
    print("测试 lark_api_helper.py")
    print("=" * 50)

    # 测试获取节点列表
    print("\n1. 测试获取节点列表...")
    result = lark_api(
        "GET",
        "/open-apis/wiki/v2/spaces/7472294423981064194/nodes",
        params={"parent_node_token": "", "page_size": 5}
    )

    if result and result.get("code") == 0:
        items = result.get("data", {}).get("items", [])
        print(f"✓ 成功获取 {len(items)} 个顶级节点")
        for item in items[:3]:
            print(f"  - {item.get('title', 'Untitled')}")
    else:
        print("✗ 获取节点列表失败")

    print("\n辅助脚本测试完成！")
