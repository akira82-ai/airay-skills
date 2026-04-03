#!/bin/bash
# 搜索 Wiki 内容
# 用法: ./search_wiki.sh <query> [space_id]

SPACE_ID="${2:-7472294423981064194}"
QUERY="$1"

if [ -z "$QUERY" ]; then
    echo "用法: $0 <search_query> [space_id]"
    exit 1
fi

echo "🔍 搜索关键词: $QUERY"
echo "空间 ID: $SPACE_ID"
echo "---"

result=$(lark-cli api GET "/open-apis/wiki/v2/search_wiki" \
    --params "{\"query\": \"$QUERY\", \"space_id\": \"$SPACE_ID\"}" 2>&1)

# 检查是否成功
if echo "$result" | jq -e '.code == 0' > /dev/null 2>&1; then
    # 格式化输出搜索结果
    echo "$result" | jq -r '
        .data.items[]? |
        "📄 \(.title)\n   Token: \(.node_token)\n   类型: \(.obj_type)\n   父节点: \(.parent_node_token // "无")\n"
    ' 2>/dev/null

    total=$(echo "$result" | jq -r '.data.total // 0')
    echo "---"
    echo "找到 $total 个结果"
else
    echo "❌ 搜索失败: $result"
    exit 1
fi
