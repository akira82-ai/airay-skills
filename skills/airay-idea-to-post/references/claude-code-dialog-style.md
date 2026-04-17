# Claude Code 对话风格规范

本文档定义如何将原始对话素材（如 JSON 文件）转换为 Claude Code 风格的展示格式。

## 使用场景

当文章中需要展示真实的对话片段、开发过程、Bug修复记录时，使用本规范将原始数据格式化为 Claude Code 风格，增强真实感和可信度。

---

## 基本元素

```markdown
❯ <用户命令>
⏺ <工具调用>(<参数>)
  ⎿ <输出内容>
✻ Crunched for <执行时间>
```

---

## 核心规则

### 1. 用户输入

**格式**：`❯` 开头，多行自动缩进

```markdown
❯ /airay-chat-export

或

❯ OK，我们在这个项目里面创建一个新的skill，
   这个skill的名字等会再起，但我希望它能够完成任务...
```

### 2. 横幅（技能启动时）

**格式**：特殊边框 + 居中标题 + 功能列表

```markdown
⏺ ══════════════════════════════════════════════════
  ▌ 技能名称 ▐
  技能描述
  ══════════════════════════════════════════════════
  作者 │ 联系方式 │ github
  ─────────────────────────────────────────────────
  • 功能点1
  • 功能点2
  ══════════════════════════════════════════════════
  最后更新：YYYY-MM-DD

  技能已启动...

  让我<后续操作描述>：
```

**注意**：
- 边框使用 `═` 和 `─`
- 标题用 `▌` 包裹居中
- 功能列表用 `•` 开头
- 最后更新日期单独一行

### 3. AI 思考过程

**格式**：`⏺` 开头，纯文本描述，不加工具调用符号

```markdown
⏺ 用户希望创建一个新的 skill，功能是获取指定日期和关键字/项目的
  对话 session 记录并保存到本地。

  这是一个规划任务，我需要：
  1. 先了解 airay-agent-review 的实现逻辑
  2. 探索项目中对话 session 记录的存储位置和格式
```

### 4. Bash 工具调用（成功）

**格式**：`⏺ Bash(命令)` + `⎿` 输出

```markdown
⏺ Bash(python3 ~/.claude/skills/airay-chat-export/scripts/export.py \
     --start_ms 1776211200000 \
     --end_ms 1776297599999)
  ⎿ ✅ 对话导出完成！

     导出范围：今天 (2026-04-15)
     会话数：2
     消息数：207

     保存位置：./chat-export-2026-04-15.json
     文件大小：112 KB
```

### 5. Bash 工具调用（失败）

**格式**：`⏺ Bash(命令)` + `⎿ Error:`

```markdown
⏺ Bash(python3 ~/.claude/skills/airay-chat-export/scripts/config.py --find)
  ⎿ Error: Exit code 1
     未知命令：--find
```

### 6. 长内容输出

**格式**：显示关键内容 + `+X lines (ctrl+o to expand)`

```markdown
⏺ Read(skills/airay-agent-review/SKILL.md)
  ⎿ 1	---
     2	name: airay-agent-review
     3	version: 1.0.0
     … +160 lines (ctrl+o to expand)
```

### 7. 用户回答问题

**格式**：`⏺ User answered Claude's questions:` + `⎿` 列表

```markdown
⏺ User answered Claude's questions:
  ⎿ · 请选择要导出的日期范围？ → 近 3 天
     · 是否要筛选特定项目？ → 是，查看完整列表
```

### 8. 执行时间

**格式**：`✻ Crunched for Xs`

```markdown
✻ Crunched for 3s
```

### 9. JSON 输出展示

**格式**：使用标准 Markdown 代码块

```markdown
⏺ jq '.sessions[0].messages[0]' chat-export-2026-04-15.json
  ⎿ {
       "type": "user",
       "timestamp": "2026-04-15T12:41:40.135Z",
       "role": "user",
       "content": "OK，我们在这个项目里面创建一个新的skill...",
       "cwd": "/Users/agiray/Desktop/github/airay-skills"
     }
```

---

## 完整示例

### 示例1：Bug发现与修复过程

```markdown
❯ 哎我发现为什么用户发起的信息都是空的呢？你没有找到吗？

  "type": "user",
  "timestamp": "2026-04-15T12:41:40.135Z",
  "role": "user",
  "content": [],  // ← 空的！
  "cwd": "/Users/agiray/Desktop/GitHub/airay-skills"

⏺ 您发现了一个重要问题！让我检查一下原始数据结构，看看用户消息的内容
  实际存储在哪个字段。

⏺ Bash(cat ~/.claude/history.jsonl | head -1 | python3 -m json.tool)
  ⎿ {
       "display": "/model ",
       "pastedContents": {},
       "timestamp": 1767413522397,
       "project": "/Users/agiray/Desktop/test",
       "sessionId": "2cfb601c-a434-4647-870b-d9e148dcb231"
     }

⏺ 这个 history.jsonl 文件的结构看起来不太一样，没有 content 字段。
  让我检查一下项目的 JSONL 文件，看看 session 数据的实际结构。

⏺ Bash(cat ~/.claude/projects/-Users-agiray-Desktop-GitHub-airay-skills/*.jsonl | \
     head -1 | python3 -m json.tool | head -30)
  ⎿ {
       "type": "user",
       "message": {
         "role": "user",
         "content": "OK，我们在这个项目里面创建一个新的skill..."
       }
     }

⏺ 找到问题了！用户消息的内容实际存储在 `message.content` 字段中，而不是顶层的
  `content`。让我修复这个 bug：

✻ Crunched for 12s

⏺ Edit(skills/airay-chat-export/scripts/export.py)
  ⎿ ✅ 已修复！用户消息内容实际存储在 `message.content` 字段中。
     让我重新导出：
```

---

## 应用场景建议

**适用的文章位置**：
1. **技术细节部分**（如"开发踩坑"）- 展示真实的bug发现和修复过程
2. **功能展示部分** - 展示工具使用流程
3. **情感/故事部分** - 展示有价值的对话片段

**不适用的场景**：
- 纯理论阐述
- 抽象概念解释
- 非技术类内容

---

## 转换步骤

从原始 JSON 文件转换为 Claude Code 风格的步骤：

1. **提取关键片段**：从 JSON 中提取相关的对话片段
2. **识别消息类型**：判断是 user、assistant、tool_use 还是 tool_result
3. **应用格式规则**：根据消息类型选择对应的格式模板
4. **用代码块包裹**：使用 Markdown 代码块（`````）包裹整个对话片段
5. **验证真实性**：确保内容真实，不虚构细节

---

## 注意事项

1. **真实性优先**：只使用真实的对话记录，不虚构
2. **适度简化**：长输出可以截断，但保留关键信息
3. **格式一致**：严格遵循格式规则，保持风格统一
4. **可读性平衡**：技术真实感和读者可读性之间找到平衡
5. **用代码块包裹**：所有对话片段都必须用 Markdown 代码块（`````）包裹

---

## 版本历史

- 2026-04-17: 初始版本，基于 Claude Code 真实对话风格提炼
