#!/usr/bin/env bash
# skill-backup 共享工具函数

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$HOME/.claude/skills"
TMP_DIR=""

# 日志函数
log_info()  { echo -e "\033[0;34m[INFO]\033[0m  $*"; }
log_error() { echo -e "\033[0;31m[ERROR]\033[0m $*" >&2; }
log_success() { echo -e "\033[0;32m[OK]\033[0m    $*"; }

# 清理临时目录
cleanup() {
  if [[ -n "$TMP_DIR" && -d "$TMP_DIR" ]]; then
    rm -rf "$TMP_DIR"
  fi
}
trap cleanup EXIT INT TERM

# 获取主机名
get_machine_info() {
  hostname -f 2>/dev/null || hostname
}

# 生成 ISO 8601 时间戳
get_timestamp() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

# 验证技能目录完整性（SKILL.md 存在且含 YAML frontmatter）
validate_skill() {
  local skill_dir="$1"
  local skill_file="$skill_dir/SKILL.md"

  if [[ ! -f "$skill_file" ]]; then
    return 1
  fi

  # 检查是否有 name 和 description 字段（在 YAML frontmatter 中）
  local has_name has_desc
  has_name=$(awk '/^---/{n++; next} n==1 && /^name:/{print; exit}' "$skill_file")
  has_desc=$(awk '/^---/{n++; next} n==1 && /^description:/{print; exit}' "$skill_file")

  if [[ -z "$has_name" || -z "$has_desc" ]]; then
    return 1
  fi

  return 0
}

# 检查 jq 是否可用
ensure_jq() {
  if ! command -v jq &>/dev/null; then
    log_error "需要 jq 但未找到，请先安装：brew install jq"
    exit 1
  fi
}
