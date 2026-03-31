#!/usr/bin/env bash
# 列出备份内容
# 用法: list.sh <backup-file>

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/utils.sh"

BACKUP_FILE="$1"

if [[ -z "$BACKUP_FILE" ]]; then
  log_error "请指定备份文件"
  echo "用法: list.sh <backup-file>"
  exit 1
fi

if [[ ! -f "$BACKUP_FILE" ]]; then
  log_error "备份文件不存在: $BACKUP_FILE"
  exit 1
fi

ensure_jq

# 从 tar.gz 中提取 metadata.json（不解压全部）
METADATA=$(tar -xOzf "$BACKUP_FILE" metadata.json 2>/dev/null)

if [[ -z "$METADATA" ]]; then
  log_error "无法从备份文件中读取 metadata.json"
  exit 1
fi

# 格式化输出
echo ""
jq -r '
  "  \u001b[0;34m备份信息\u001b[0m",
  "  ─────────────────────────",
  "  时间:     \(.timestamp)",
  "  主机:     \(.hostname)",
  "  技能数量: \(.count)",
  (if .note != null and .note != "" then "  备注:     \(.note)" else empty end),
  "",
  "  \u001b[0;34m技能列表\u001b[0m",
  "  ─────────────────────────",
  (.skills[] | "  • \(. + " ")")
' <<< "$METADATA"

echo ""
FILE_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
echo "  文件大小: $FILE_SIZE"
echo ""
