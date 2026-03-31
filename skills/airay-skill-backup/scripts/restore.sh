#!/usr/bin/env bash
# 恢复技能备份
# 用法: restore.sh <backup-file> [--target <path>]

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/utils.sh"

BACKUP_FILE=""
TARGET=""

# 解析参数
parse_args() {
  BACKUP_FILE="$1"
  if [[ -z "$BACKUP_FILE" ]]; then
    log_error "请指定备份文件"
    echo "用法: restore.sh <backup-file> [--target <path>]"
    exit 1
  fi

  if [[ ! -f "$BACKUP_FILE" ]]; then
    log_error "备份文件不存在: $BACKUP_FILE"
    exit 1
  fi

  shift
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --target)
        shift
        TARGET="$1"
        shift
        ;;
      *)
        log_error "未知参数: $1"
        exit 1
        ;;
    esac
  done

  TARGET="${TARGET:-$SKILLS_DIR}"
}

parse_args "$@"

ensure_jq

# 从 tar.gz 中提取 metadata.json
TMP_DIR="$(mktemp -d)"
EXTRACT_DIR="$TMP_DIR/extract"
mkdir -p "$EXTRACT_DIR"

tar -xzf "$BACKUP_FILE" -C "$EXTRACT_DIR"

if [[ ! -f "$EXTRACT_DIR/metadata.json" ]]; then
  log_error "备份文件中未找到 metadata.json，可能不是有效的技能备份"
  exit 1
fi

# 显示备份信息
METADATA="$EXTRACT_DIR/metadata.json"
BACKUP_TIMESTAMP=$(jq -r '.timestamp' "$METADATA")
BACKUP_HOSTNAME=$(jq -r '.hostname' "$METADATA")
SKILL_COUNT=$(jq -r '.count' "$METADATA")
BACKUP_NOTE=$(jq -r '.note' "$METADATA")

log_info "备份信息:"
echo "  时间: $BACKUP_TIMESTAMP"
echo "  主机: $BACKUP_HOSTNAME"
echo "  技能数量: $SKILL_COUNT"
if [[ "$BACKUP_NOTE" != "null" && -n "$BACKUP_NOTE" ]]; then
  echo "  备注: $BACKUP_NOTE"
fi
echo ""

# 验证技能完整性并复制
RESTORED=0
CORRUPTED=()

for skill_dir in "$EXTRACT_DIR/skills"/*/; do
  [[ ! -d "$skill_dir" ]] && continue
  skill_name="$(basename "${skill_dir%/}")"

  if validate_skill "$skill_dir"; then
    mkdir -p "$TARGET"
    cp -r "$skill_dir" "$TARGET/$skill_name"
    RESTORED=$((RESTORED + 1))
  else
    log_error "技能 '$skill_name' 损坏或缺少 SKILL.md，跳过"
    CORRUPTED+=("$skill_name")
  fi
done

# 后验证
if [[ $RESTORED -ne $SKILL_COUNT ]]; then
  log_error "预期恢复 $SKILL_COUNT 个技能，实际恢复 $RESTORED 个"
fi

# 显示恢复摘要
echo ""
log_success "恢复完成"
echo "  目标路径: $TARGET"
echo "  已恢复:   $RESTORED 个技能"
if [[ ${#CORRUPTED[@]} -gt 0 ]]; then
  echo "  已跳过:   ${#CORRUPTED[@]} 个损坏技能 (${CORRUPTED[*]})"
fi
