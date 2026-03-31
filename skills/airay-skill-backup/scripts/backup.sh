#!/usr/bin/env bash
# 创建技能备份
# 用法: backup.sh <output-path> [--skills skill1 skill2 ...] [--note "备注"]

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/utils.sh"

OUTPUT_PATH=""
SELECTED_SKILLS=()
NOTE=""

# 解析参数
parse_args() {
  OUTPUT_PATH="$1"
  if [[ -z "$OUTPUT_PATH" ]]; then
    log_error "请指定输出路径"
    echo "用法: backup.sh <output-path> [--skills skill1 skill2 ...] [--note \"备注\"]"
    exit 1
  fi

  shift
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --skills)
        shift
        while [[ $# -gt 0 && ! "$1" =~ ^-- ]]; do
          SELECTED_SKILLS+=("$1")
          shift
        done
        ;;
      --note)
        shift
        NOTE="$1"
        shift
        ;;
      *)
        log_error "未知参数: $1"
        exit 1
        ;;
    esac
  done
}

parse_args "$@"

# 确定备份范围
SKILLS_TO_BACKUP=()

if [[ ${#SELECTED_SKILLS[@]} -gt 0 ]]; then
  # 指定技能模式
  for skill in "${SELECTED_SKILLS[@]}"; do
    if [[ -d "$SKILLS_DIR/$skill" ]]; then
      SKILLS_TO_BACKUP+=("$skill")
    else
      log_error "技能 '$skill' 不存在，跳过"
    fi
  done
  if [[ ${#SKILLS_TO_BACKUP[@]} -eq 0 ]]; then
    log_error "没有找到任何可备份的技能"
    exit 1
  fi
else
  # 全部备份模式
  for dir in "$SKILLS_DIR"/*/; do
    [[ ! -d "$dir" ]] && continue
    dir="${dir%/}"
    name="$(basename "$dir")"
    # 跳过隐藏目录
    [[ "$name" =~ ^\. ]] && continue
    SKILLS_TO_BACKUP+=("$name")
  done
fi

log_info "准备备份 ${#SKILLS_TO_BACKUP[@]} 个技能: ${SKILLS_TO_BACKUP[*]}"

# 创建临时目录
TMP_DIR="$(mktemp -d)"
BACKUP_DIR="$TMP_DIR/skills"

mkdir -p "$BACKUP_DIR"

# 复制技能到临时目录（排除 .git 目录）
for skill in "${SKILLS_TO_BACKUP[@]}"; do
  rsync -a --exclude='.git' "$SKILLS_DIR/$skill/" "$BACKUP_DIR/$skill/"
done

# 生成 metadata.json
ensure_jq

METADATA_FILE="$TMP_DIR/metadata.json"

jq -n \
  --arg timestamp "$(get_timestamp)" \
  --arg hostname "$(get_machine_info)" \
  --argjson skills "$(printf '%s\n' "${SKILLS_TO_BACKUP[@]}" | jq -R . | jq -s .)" \
  --argjson count "${#SKILLS_TO_BACKUP[@]}" \
  --arg note "$NOTE" \
  '{
    timestamp: $timestamp,
    hostname: $hostname,
    skills: $skills,
    count: $count,
    note: $note
  }' > "$METADATA_FILE"

# 打包为 tar.gz
# 确保输出目录存在
mkdir -p "$(dirname "$OUTPUT_PATH")"
tar -czf "$OUTPUT_PATH" -C "$TMP_DIR" metadata.json skills

# 显示备份摘要
FILE_SIZE=$(du -h "$OUTPUT_PATH" | cut -f1)
log_success "备份完成"
echo ""
echo "  文件路径: $OUTPUT_PATH"
echo "  技能数量: ${#SKILLS_TO_BACKUP[@]}"
echo "  文件大小: $FILE_SIZE"
if [[ -n "$NOTE" ]]; then
  echo "  备注:     $NOTE"
fi
