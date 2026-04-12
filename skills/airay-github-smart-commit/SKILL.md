---
name: airay-github-smart-commit
description: |
  智能 GitHub 提交助手。当用户说"提交 GitHub"、"push to github"、"提交代码"、"commit and push"、"推送到 GitHub"、"上传代码"、"sync to github"时自动触发。

  自动分析代码变更，智能更新 README.md 和版本号，生成美观的 Conventional Commits 格式提交消息（带 emoji），并在用户确认后提交推送。

  核心功能：
  - 加载项目配置（支持 .smart-commit.json）
  - 分析代码变更（调用 analyze_changes.py）
  - 自动更新 README.md（调用 update_readme.py）
  - 自动更新版本号（调用 update_version.py）
  - 生成 commit 消息（调用 generate_commit.py）
  - 使用 AskUserQuestion 请求确认
  - 执行 git add、commit、push
version: 2.0.0
allowed-tools: Bash, Read, AskUserQuestion
author: 磊叔
---

## Script Directory

**Agent Execution Instructions**:
1. Determine this SKILL.md file's directory path as `{baseDir}`
2. Script path = `{baseDir}/scripts/{script-name}`
3. Before running any script, resolve `{baseDir}` first


# 🚀 GitHub 智能提交助手

## 启动横幅

当技能被触发时，首先显示以下横幅信息：

```
═══════════════════════════════════════════════════════════════
▌ GitHub 智能提交助手 ▐
AI 驱动的代码提交自动化工具
═══════════════════════════════════════════════════════════════
磊叔 │ 微信：AIRay1015 │ github.com/akira82-ai
────────────────────────────────────────────────────────────
🤖 智能分析代码变更，自动分类提交类型
📝 自动更新 README.md 版本信息和日期
🔢 智能版本号管理（Semver 规范）
💬 生成 Conventional Commits + Gitmoji 格式消息
✅ 执行前完整预览，确认后安全提交
🌐 支持中英文双语界面
═══════════════════════════════════════════════════════════════
最后更新：2026-03-31

技能已启动...
```

**显示时机**：在技能开始执行任何操作之前，首先输出此横幅，让用户清楚技能已激活并了解即将执行的操作。

## 核心功能

- 🤖 **智能分析** - 自动分析代码变更类型和影响范围
- 📝 **文档更新** - 智能更新 README.md 版本号和日期
- 🔢 **版本管理** - 自动更新项目版本号
- 💬 **美观消息** - 生成 Conventional Commits + Gitmoji 格式
- ✅ **确认流程** - 显示完整预览，用户确认后执行
- 🌐 **多语言** - 支持中英文双语

## 触发短语

**中文**："提交 GitHub"、"提交代码"、"推送到 GitHub"、"上传代码"、"同步到 GitHub"

**英文**："push to github"、"commit and push"、"sync to github"、"upload code"

## 执行流程

### 步骤 1：环境检查与分析

检查 Git 仓库状态并分析代码变更：

```bash
# 检查是否为 git 仓库
git rev-parse --is-inside-work-tree

# 检查是否有待提交的变更
git status --porcelain

# 分析代码变更
analysis=$(python3 {baseDir}/scripts/analyze_changes.py)
```

**错误处理**：
- 非 Git 仓库 → 提示初始化，结束
- 无变更 → 提示工作区干净，结束

**分析输出**（JSON）：
```json
{
  "type": "feat",
  "scope": "auth",
  "emoji": "✨",
  "is_breaking": false,
  "modified_files": ["src/auth/oauth.py"],
  "added_files": ["src/auth/providers/google.py"],
  "deleted_files": []
}
```

### 步骤 2：加载配置

加载项目配置（按优先级）：

```bash
# 查找配置文件
config_file=$(python3 {baseDir}/scripts/config.py --find)
```

**默认配置**：
```json
{
  "language": "zh",
  "readme_style": "auto",
  "version_scheme": "semver"
}
```

**配置优先级**：
1. 项目级配置（`.smart-commit.json`）
2. 全局配置（`~/.smart-commit.json`）
3. 默认配置

### 步骤 3：更新文件（自动执行）

**更新 README.md**（如果存在）：
```bash
if [ -f "README.md" ]; then
    # 获取当前版本号
    if [ -f "package.json" ]; then
        current_version=$(cat package.json | jq -r '.version')
    elif [ -f "pyproject.toml" ]; then
        current_version=$(grep -oP 'version\s*=\s*"\K[^"]+' pyproject.toml)
    else
        current_version="1.0.0"
    fi

    # 更新 README
    python3 {baseDir}/scripts/update_readme.py README.md "$current_version"
fi
```

**更新版本号**：
```bash
# 获取项目根目录
project_dir=$(git rev-parse --show-toplevel)

# 调用更新脚本
version_update=$(python3 {baseDir}/scripts/update_version.py "$project_dir")

new_version=$(echo "$version_update" | jq -r '.new_version')
echo "✓ 版本号已更新: $new_version"
```

### 步骤 4：生成 Commit 消息

使用智能模板生成 commit 消息：

```bash
commit_message=$(echo "$analysis" | python3 {baseDir}/scripts/generate_commit.py)
```

**统一输出格式**：
```
✨ feat(auth): add OAuth authentication

• 新增 2 个文件
• 修改 1 个文件

修改的文件：
  src/auth/oauth.py
  + src/auth/providers/google.py

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

### 步骤 5：确认并提交

**显示预览**：
```bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 变更统计"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "类型: $emoji $change_type"
echo "版本: $new_version"
echo "文件变更: +$added_count ~$modified_count -$deleted_count"
echo ""
echo "📝 Commit 消息"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "$commit_message"
echo ""
```

**使用 AskUserQuestion 请求确认**：
- 确认提交 → 执行 git add、commit、push
- 取消 → 结束流程

**执行 Git 操作**：
```bash
# 添加所有变更
git add .

# 提交
git commit -m "$commit_message"

# 推送
current_branch=$(git branch --show-current)
git push origin "$current_branch"

echo "✅ 提交成功！分支: $current_branch"
```

## 配置文件

### 项目级配置

在项目根目录创建 `.smart-commit.json`：

```json
{
  "language": "zh",
  "readme_style": "auto",
  "version_scheme": "semver"
}
```

### 全局配置

在用户主目录创建 `~/.smart-commit.json`：

```json
{
  "language": "zh",
  "readme_style": "auto",
  "version_scheme": "semver"
}
```

## 错误处理

### 推送失败

```bash
if ! git push origin "$current_branch" 2>&1; then
    echo "⚠️ 推送失败！建议操作："
    echo "  git pull --rebase origin $current_branch"
    echo "  git push origin $current_branch"
    exit 1
fi
```

### 提交失败

```bash
if ! git commit -m "$commit_message" 2>&1; then
    echo "⚠️ 提交失败！pre-commit 钩子检查未通过。"
    exit 1
fi
```

## 技术依赖

- Python 3.7+
- Git 2.0+

## 脚本说明

所有脚本位于：`{baseDir}/scripts/`

- `analyze_changes.py` - 代码变更分析
- `generate_commit.py` - Commit 消息生成
- `update_readme.py` - README 更新
- `update_version.py` - 版本号更新
- `config.py` - 配置管理
- `utils.py` - 工具函数
- `i18n.py` - 国际化支持
