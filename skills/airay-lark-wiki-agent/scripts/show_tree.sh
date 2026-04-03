#!/bin/bash
# 树形展示知识库节点结构
# 用法: ./show_tree.sh [parent_token] [depth] [space_id]

SPACE_ID="${3:-7472294423981064194}"
PARENT_TOKEN="${1:-}"
DEPTH="${2:-0}"

# 生成缩进
indent() {
    local d="$1"
    local result=""
    for ((i=0; i<d; i++)); do
        result+="  "
    done
    echo "$result"
}

# 递归展示节点
show_tree_recursive() {
    local parent="$1"
    local depth="$2"

    local current_indent
    current_indent=$(indent "$depth")

    # 获取子节点列表
    local params
    if [ -z "$parent" ]; then
        params='{}'
    else
        params="{\"parent_node_token\": \"$parent\"}"
    fi

    local nodes
    nodes=$(lark-cli api GET "/open-apis/wiki/v2/spaces/$SPACE_ID/nodes" \
        --params "$params" 2>/dev/null)

    # 解析并显示节点
    echo "$nodes" | jq -r '.data.items[]? | "\(.node_token)|\(.title)|\(.has_child)"' 2>/dev/null | while IFS='|' read -r token title has_child; do
        if [ -n "$token" ]; then
            local marker="├─"
            if [ "$has_child" = "true" ]; then
                marker="┬─"
            fi
            echo "${current_indent}${marker} ${title} (${token})"

            # 递归显示子节点
            if [ "$has_child" = "true" ]; then
                show_tree_recursive "$token" $((depth + 1))
            fi
        fi
    done
}

# 主入口
echo "📚 知识库树形结构 (Space: $SPACE_ID)"
show_tree_recursive "$PARENT_TOKEN" "$DEPTH"
