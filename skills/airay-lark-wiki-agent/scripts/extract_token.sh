#!/bin/bash
# 从飞书 Wiki URL 提取 node_token
# URL 格式: https://my.feishu.cn/wiki/<node_token>?...

extract_token() {
    local url="$1"
    echo "$url" | sed -E 's|.*wiki/([a-zA-Z0-9]+).*|\1|'
}

# 如果直接执行此脚本
if [ "${BASH_SOURCE[0]}" = "$0" ] && [ -n "$1" ]; then
    extract_token "$1"
fi
