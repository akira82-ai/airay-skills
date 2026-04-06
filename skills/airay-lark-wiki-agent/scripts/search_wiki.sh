#!/bin/bash
# 搜索 Wiki 内容
# 用法: ./search_wiki.sh <query> [page_size]

PAGE_SIZE="${2:-10}"
QUERY="$1"

if [ -z "$QUERY" ]; then
    echo "用法: $0 <search_query> [page_size]"
    exit 1
fi

echo "🔍 搜索关键词: $QUERY"
echo "页面大小: $PAGE_SIZE"
echo "---"

result=$(lark-cli docs +search --query "$QUERY" --page-size "$PAGE_SIZE" 2>&1)

# 检查是否成功
if echo "$result" | jq -e '.code == 0' > /dev/null 2>&1; then
    # 格式化输出搜索结果
    echo "$result" | jq -r '
        .data.items[]? |
        "📄 \(.title)\n   Token: \(.node_token // "无")\n   类型: \(.obj_type)\n"
    ' 2>/dev/null

    total=$(echo "$result" | jq -r '.data.total // 0')
    echo "---"
    echo "找到 $total 个结果"
else
    echo "❌ 搜索失败: $result"
    exit 1
fi
