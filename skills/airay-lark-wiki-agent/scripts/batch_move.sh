#!/bin/bash
# 批量移动 Wiki 节点
# 用法: ./batch_move.sh <token1,token2,...> <target_parent_token> [space_id]

SPACE_ID="${3:-7472294423981064194}"
TARGET_PARENT="$2"
TOKENS="$1"

if [ -z "$TOKENS" ] || [ -z "$TARGET_PARENT" ]; then
    echo "用法: $0 <token1,token2,...> <target_parent_token> [space_id]"
    exit 1
fi

echo "🔄 批量移动节点到: $TARGET_PARENT"
echo "空间 ID: $SPACE_ID"
echo "---"

# 将逗号分隔的 token 转为数组
IFS=',' read -ra TOKEN_ARRAY <<< "$TOKENS"

success_count=0
fail_count=0

for token in "${TOKEN_ARRAY[@]}"; do
    token=$(echo "$token" | xargs) # 去除空格
    echo "移动节点: $token"

    result=$(lark-cli api POST "/open-apis/wiki/v2/spaces/$SPACE_ID/nodes/$token/move" \
        --data "{\"target_parent_token\": \"$TARGET_PARENT\"}" 2>&1)

    if echo "$result" | jq -e '.code == 0' > /dev/null 2>&1; then
        echo "  ✅ 成功"
        ((success_count++))
    else
        echo "  ❌ 失败: $result"
        ((fail_count++))
    fi
done

echo "---"
echo "完成: 成功 $success_count, 失败 $fail_count"
