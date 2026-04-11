---
name: airay-lark-wiki-agent
version: 1.0.0
description: |
  飞书知识库完整 CRUD 操作。当用户需要创建、查询、更新、删除 wiki 节点，或进行批量操作、成员管理时使用。
allowed-tools: Bash, AskUserQuestion
author: 磊叔
metadata:
  requires:
    bins: ["lark-cli"]
---

## Script Directory

**Agent Execution Instructions**:
1. Determine this SKILL.md file's directory path as `{baseDir}`
2. Script path = `{baseDir}/scripts/{script-name}`
3. Before running any script, resolve `{baseDir}` first


# 📘 飞书知识库 CRUD 工具

## 启动横幅

当技能被触发时，首先显示以下横幅信息：

```
═══════════════════════════════════════════════════════════════
▌ Lark Wiki CRUD ▐
飞书知识库完整 CRUD 操作工具
═══════════════════════════════════════════════════════════════
磊叔 │ 微信：AIRay1015 │ github.com/akira82-ai
────────────────────────────────────────────────────────────
最后修改：20260406
────────────────────────────────────────────────────────────
  创建    创建新节点/文档
  查询    列出节点、搜索内容、获取详情
  更新    修改标题、移动节点、复制节点
  删除    删除节点
  高级    批量操作、成员管理、空间设置
═══════════════════════════════════════════════════════════════

技能已启动...
```

完备的飞书知识库 CRUD 操作技能，支持节点的增删改查、批量操作、成员管理等。

## 默认配置

- **知识空间 ID**: `7472294423981064194`
- **知识库 URL**: `https://my.feishu.cn/wiki/QWQHwA9uYibmtzkZLJBccaEhnNd`

## 中文 JSON 数据处理最佳实践

**问题**：lark-cli 在处理包含中文字符的 JSON 数据时存在编码问题。直接在 Bash 中调用容易失败。

**解决方案**：使用 Python subprocess 包装调用

```python
import subprocess
import json

data = {
    "obj_type": "docx",
    "parent_node_token": "xxx",
    "title": "每日复盘 - 2026-04-06"  # 中文内容
}

result = subprocess.run([
    "lark-cli", "api", "POST",
    "/open-apis/wiki/v2/spaces/7472294423981064194/nodes",
    "--data", json.dumps(data, ensure_ascii=False)  # 关键
], capture_output=True, text=True, encoding='utf-8')
```

**关键点**：
- `ensure_ascii=False` 确保中文正确编码
- `encoding='utf-8'` 确保正确的编码处理
- 通过 subprocess 传递参数列表，避免 Shell 解析问题

**辅助脚本**：使用 `{baseDir}/scripts/lark_api_helper.py` 提供的 `lark_api()` 函数简化调用。

## 触发关键词

- **创建**: 创建wiki节点、新建文档、添加wiki页面、新建知识库页面
- **查询**: 查看wiki节点、列出子节点、搜索wiki、获取节点信息、wiki目录树
- **更新**: 修改节点标题、移动wiki节点、复制节点、重命名
- **删除**: 删除wiki节点
- **高级**: 批量操作、成员管理、空间设置

## 命令选择原则

| 操作类型 | 推荐命令 | 说明 |
|----------|----------|------|
| 创建文档 | `docs +create` | 支持直接填充 Markdown 内容 |
| 更新文档 | `docs +update` | 支持多种更新模式 |
| 读取文档 | `docs +fetch` | 获取文档内容 |
| 搜索文档 | `docs +search` | 搜索 Wiki 中的文档 |
| 插入文件 | `docs +media-insert` | 插入图片或文件到文档 |
| 创建文件夹 | `api POST` | 无 Shortcut，必须用 API |
| 移动/复制/删除 | `api POST/DELETE` | 无 Shortcut，必须用 API |

**核心原则**：能用 Shortcut 就用 Shortcut，API POST 仅用于无 Shortcut 的操作。

---

## CRUD 操作

### Create - 创建节点

#### 创建文档（推荐）

使用 `docs +create` 创建包含内容的 Wiki 文档：

```bash
lark-cli docs +create \
  --title "文档标题" \
  --wiki-node "<父节点token，空字符串表示顶级>" \
  --markdown "# Markdown 内容"
```

**优点**：
- 一步完成：创建节点 + 填充内容
- 支持直接传入 Markdown
- 错误信息友好
- 自动处理权限

#### 创建文件夹/其他类型节点

创建非文档类型节点（文件夹、表格等）：

```bash
# 创建文件夹
lark-cli api POST "/open-apis/wiki/v2/spaces/7472294423981064194/nodes" \
  --data '{
    "parent_node_token": "<父节点token>",
    "obj_type": "wiki",
    "title": "文件夹名称"
  }'

# 创建其他类型节点（需要先创建，再填充内容）
lark-cli api POST "/open-apis/wiki/v2/spaces/7472294423981064194/nodes" \
  --data '{
    "parent_node_token": "<父节点token>",
    "obj_type": "docx",
    "title": "节点标题"
  }'
```

**节点类型**：
- `wiki`: 文件夹
- `docx`: 新版文档（推荐使用 `docs +create`）
- `doc`: 旧版文档
- `sheet`: 电子表格（推荐使用 `sheets +create`）
- `bitable`: 多维表格（推荐使用 `base +base-create`）
- `mindnote`: 思维导图
- `slides`: 演示文稿
- `file`: 文件

**返回字段**：
- `node_token`: 新创建节点的 token
- `space_id`: 知识空间 ID
- `obj_token`: 实际文档的 token

### Read - 读取节点

```bash
# 列出子节点
lark-cli api GET "/open-apis/wiki/v2/spaces/7472294423981064194/nodes" \
  --params '{
    "parent_node_token": "<父节点token，空表示顶级>",
    "page_size": 50
  }'

# 获取单个节点详情
lark-cli api GET "/open-apis/wiki/v2/spaces/7472294423981064194/nodes/<node_token>"

# 获取文档内容（推荐）

使用 `docs +fetch` 获取文档的 Markdown 内容：

```bash
lark-cli docs +fetch --doc "<文档URL或token>"

# 输出为表格格式
lark-cli docs +fetch --doc "<文档URL或token>" --format table
```

# 搜索内容

使用 `docs +search` 搜索 Wiki 中的文档：

```bash
lark-cli docs +search --query "搜索关键词" --page-size 10
```

**支持的过滤选项**：
```bash
# 按文档类型过滤
lark-cli docs +search --query "关键词" --filter '{"doc_type": "docx"}'

# 按时间过滤
lark-cli docs +search --query "关键词" --filter '{"create_time": ">=2024-01-01"}'
```
```

### Update - 更新节点

#### 方式一：仅更新节点标题

```bash
lark-cli api POST "/open-apis/wiki/v2/spaces/7472294423981064194/nodes/<node_token>/title" \
  --data '{"title": "新标题"}'
```

#### 方式二：更新文档内容（推荐）

使用 `docs +update` 更新文档内容和标题：

```bash
# 覆盖整个文档
lark-cli docs +update \
  --doc "<文档URL或token>" \
  --new-title "新标题" \
  --markdown "新的 Markdown 内容"

# 追加内容
lark-cli docs +update \
  --doc "<文档URL或token>" \
  --mode append \
  --markdown "追加的内容"
```

**支持的模式**：
- `overwrite`: 覆盖整个文档（默认）
- `append`: 追加到文档末尾
- `insert_before`: 在指定位置前插入
- `insert_after`: 在指定位置后插入
- `replace_range`: 替换指定范围

#### 方式三：插入文件到文档

使用 `docs +media-insert` 将本地文件插入到文档中：

```bash
# 插入图片
lark-cli docs +media-insert \
  --file "/path/to/image.png" \
  --doc "<文档URL或token>" \
  --type image \
  --caption "图片说明"

# 插入文件
lark-cli docs +media-insert \
  --file "/path/to/file.pdf" \
  --doc "<文档URL或token>" \
  --type file
```

**支持的文件类型**：
- 图片：PNG, JPG, GIF, WebP 等（最大 20MB）
- 文件：PDF, Word, Excel, PPT 等（最大 20MB）

```bash
# 移动节点（同空间内）
lark-cli api POST "/open-apis/wiki/v2/spaces/7472294423981064194/nodes/<node_token>/move" \
  --data '{"target_parent_token": "<目标父节点token>"}'

# 移动节点（跨空间）
lark-cli api POST "/open-apis/wiki/v2/spaces/7472294423981064194/nodes/<node_token>/move" \
  --data '{
    "target_parent_token": "<目标父节点token>",
    "target_space_id": "<目标空间ID>"
  }'

# 复制节点
lark-cli api POST "/open-apis/wiki/v2/spaces/7472294423981064194/nodes/<node_token>/copy" \
  --data '{
    "target_parent_token": "<目标父节点token>",
    "target_space_id": "<目标空间ID，可选>",
    "title": "副本标题"
  }'
```

### Delete - 删除节点

```bash
lark-cli api DELETE "/open-apis/wiki/v2/spaces/7472294423981064194/nodes/<node_token>"
```

---

## 高级功能

### 批量操作

```bash
# 批量移动节点（遍历 token 数组）
for token in token1 token2 token3; do
  lark-cli api POST "/open-apis/wiki/v2/spaces/7472294423981064194/nodes/$token/move" \
    --data '{"target_parent_token": "<目标父节点token>"}'
done

# 批量复制节点
for token in token1 token2 token3; do
  lark-cli api POST "/open-apis/wiki/v2/spaces/7472294423981064194/nodes/$token/copy" \
    --data '{
      "target_parent_token": "<目标父节点token>",
      "title": "副本 - $token"
    }'
done
```

### 成员管理

```bash
# 列出空间成员
lark-cli api GET "/open-apis/wiki/v2/spaces/7472294423981064194/members"

# 添加成员
lark-cli api POST "/open-apis/wiki/v2/spaces/7472294423981064194/members" \
  --data '{
    "member_type": "user",
    "member_id": "<用户open_id>",
    "perm": "view"
  }'
# perm 权限值: view(查看), edit(编辑), admin(管理)

# 删除成员
lark-cli api DELETE "/open-apis/wiki/v2/spaces/7472294423981064194/members/<member_id>"
```

### 空间设置

```bash
# 更新空间设置
lark-cli api PATCH "/open-apis/wiki/v2/spaces/7472294423981064194/settings" \
  --data '{
    "indexable": true
  }'
```

### 获取知识空间列表

```bash
lark-cli api GET "/open-apis/wiki/v2/spaces"
```

---

## 辅助脚本

所有脚本位于：`{baseDir}/scripts/`

### 从 URL 提取 Token

```bash
# 从飞书 Wiki URL 提取 node_token
# URL 格式: https://my.feishu.cn/wiki/<node_token>
{baseDir}/scripts/extract_token.sh "<wiki_url>"
```

### 树形展示节点

```bash
# 递归展示节点树
{baseDir}/scripts/show_tree.sh "[parent_node_token]"
```

### 搜索 Wiki 内容

```bash
# 搜索知识库内容
{baseDir}/scripts/search_wiki.sh "<query>"
```

### 批量移动节点

```bash
# 批量移动节点到指定父节点
{baseDir}/scripts/batch_move.sh <target_parent_token> <node_token1> <node_token2> ...
```

### 批量复制节点

```bash
# 批量复制节点到指定父节点
{baseDir}/scripts/batch_copy.sh <target_parent_token> <node_token1> <node_token2> ...
```

---

## 权限要求

| 操作 | 所需 Scope |
|------|-----------|
| 创建节点 | `wiki:node:create` 或 `wiki:wiki` |
| 读取节点 | `wiki:node:read` 或 `wiki:wiki:readonly` |
| 更新节点 | `wiki:node:update` 或 `wiki:wiki` |
| 删除节点 | `wiki:node:delete` 或 `wiki:wiki` |
| 移动节点 | `wiki:node:move` 或 `wiki:wiki` |
| 复制节点 | `wiki:node:copy` 或 `wiki:wiki` |
| 搜索内容 | `wiki:wiki:readonly` |
| 成员管理 | `wiki:space:member:manage` 或 `wiki:wiki` |

## 使用说明

1. **确保已登录**: `lark-cli auth login`
2. **确保有权限**: 检查当前身份是否有所需 scope
3. **写操作前确认**: 使用 `AskUserQuestion` 让用户确认后再执行
4. **处理错误**: 遇到权限错误时，引导用户运行 `lark-cli auth login` 或检查 scope 配置

## 节点类型说明

| obj_type | 说明 |
|----------|------|
| `doc` | 旧版文档 |
| `docx` | 新版文档（推荐） |
| `sheet` | 电子表格 |
| `mindnote` | 思维导图 |
| `bitable` | 多维表格 |
| `file` | 文件 |
| `slides` | 演示文稿 |
| `wiki` | 知识库页面 |

## 限制说明

- 移动节点：原/目标空间总节点数不超过 40 万
- 目录树：不超过 50 层
- 单层节点数：不超过 2000
- 单次移动节点数：不超过 2000
