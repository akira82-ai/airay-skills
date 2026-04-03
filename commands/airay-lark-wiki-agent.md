---
description: 飞书知识库完整 CRUD 操作。当用户需要创建、查询、更新、删除 wiki 节点，或进行批量操作、成员管理时使用。
allowed-tools: Bash, AskUserQuestion
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
  创建    创建新节点/文档
  查询    列出节点、搜索内容、获取详情
  更新    修改标题、移动节点、复制节点
  删除    删除节点
  高级    批量操作、成员管理、空间设置
═══════════════════════════════════════════════════════════════

技能已启动...
```

## 触发关键词

- **创建**: 创建wiki节点、新建文档、添加wiki页面、新建知识库页面
- **查询**: 查看wiki节点、列出子节点、搜索wiki、获取节点信息、wiki目录树
- **更新**: 修改节点标题、移动wiki节点、复制节点、重命名
- **删除**: 删除wiki节点
- **高级**: 批量操作、成员管理、空间设置

## 默认配置

- **知识空间 ID**: `7472294423981064194`
- **知识库 URL**: `https://my.feishu.cn/wiki/QWQHwA9uYibmtzkZLJBccaEhnNd`

## 快速操作

### 列出顶级节点
```bash
lark-cli api GET "/open-apis/wiki/v2/spaces/7472294423981064194/nodes" \
  --params '{"parent_node_token": "", "page_size": 50}'
```

### 创建新文档
```bash
lark-cli api POST "/open-apis/wiki/v2/spaces/7472294423981064194/nodes" \
  --data '{"parent_node_token": "", "obj_type": "docx", "title": "新文档标题"}'
```

### 更新节点标题
```bash
lark-cli api POST "/open-apis/wiki/v2/spaces/7472294423981064194/nodes/<node_token>/title" \
  --data '{"title": "新标题"}'
```

### 移动节点
```bash
lark-cli api POST "/open-apis/wiki/v2/spaces/7472294423981064194/nodes/<node_token>/move" \
  --data '{"target_parent_token": "<目标父节点token>"}'
```

### 删除节点
```bash
lark-cli api DELETE "/open-apis/wiki/v2/spaces/7472294423981064194/nodes/<node_token>"
```

### 显示节点树
```bash
{baseDir}/scripts/show_tree.sh
```

### 搜索内容
```bash
{baseDir}/scripts/search_wiki.sh "<搜索关键词>"
```

## 节点类型

| obj_type | 说明 |
|----------|------|
| `docx` | 新版文档（推荐） |
| `doc` | 旧版文档 |
| `sheet` | 电子表格 |
| `mindnote` | 思维导图 |
| `bitable` | 多维表格 |
| `slides` | 演示文稿 |

## 前置要求

1. **安装 lark-cli**: 用户需单独安装
2. **登录认证**: `lark-cli auth login`
3. **权限检查**: 确保有相应的 wiki scope
