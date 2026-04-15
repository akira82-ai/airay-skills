---
name: airay-chat-export
version: 1.0.0
description: |
  对话导出工具。完整保存 Claude Code 对话 session 记录到本地 JSON 文件。
  支持日期范围筛选（今天、昨天、近 3 天、近 7 天、自定义）和项目路径筛选。
  当用户说"导出对话"、"export chat"、"对话导出"、"/chat-export"、"保存对话记录"时触发。

author: 磊叔
---

# 对话导出工具

## 启动横幅

技能启动时，输出以下横幅：

```
═══════════════════════════════════════════════════════════════
▌ 对话导出工具 ▐
完整保存 Claude Code 对话 session 记录到本地 JSON 文件
═══════════════════════════════════════════════════════════════
磊叔 │ 微信：AIRay1015 │ github.com/akira82-ai
────────────────────────────────────────────────────────────
• 支持日期范围筛选（今天 / 昨天 / 近 3 天 / 近 7 天 / 自定义）
• 支持项目路径筛选（可选）
• 完整对话内容保存（用户消息、AI 响应、工具调用）
• JSON 格式输出，便于后续分析
• 自动保存到当前工作目录
═══════════════════════════════════════════════════════════════
最后更新：2026-04-15
```

## 参数处理

### 日期范围选择

如果用户没有指定时间范围，用 AskUserQuestion 询问，选项为：
- 今天
- 昨天
- 近 3 天
- 近 7 天
- 自定义日期范围

根据用户选择，计算对应的日期范围（当天、前 1 天、前 3 天、前 7 天、或自定义），时间戳使用 UTC 时区。

### 项目路径筛选

使用 AskUserQuestion 询问是否需要筛选特定项目：
- 是 - 询问项目路径
- 否 - 导出所有项目的对话记录

如果选择筛选，用户可以输入完整项目路径或部分路径匹配。

## 数据提取步骤

### 第 1 步：从 history.jsonl 获取消息列表

用 Bash 执行 Python 脚本，读取 ~/.claude/history.jsonl，按时间戳筛选指定日期范围内的所有记录。

### 第 2 步：获取涉及的 session 列表

从第 1 步中提取不重复的 sessionId 和对应的项目路径。如果指定了项目路径筛选，则只保留匹配的 session。

### 第 3 步：从项目 JSONL 文件中提取完整内容

使用技能自带的 export.py 脚本提取完整对话数据。

**调用脚本**：
```bash
python ~/.claude/plugins/marketplaces/airay-skills/skills/airay-chat-export/scripts/export.py --start_ms <start_ms> --end_ms <end_ms> [--project "<project_path>"] [--output <output_file>]
```

**时间戳格式说明**：
两个数据源的时间戳格式不同，脚本中会统一处理：
1. `history.jsonl` 的 timestamp 字段是 int（Unix 毫秒），如 `1770288337219`
2. 项目 JSONL 文件的 timestamp 字段是 ISO 8601 字符串，如 `"2026-03-31T04:24:20.514Z"`

### 第 4 步：生成 JSON 文件

将提取的对话数据保存为 JSON 文件到当前工作目录。

**文件命名规则**：
- 单天范围：`chat-export-YYYY-MM-DD.json`
- 多天范围：`chat-export-YYYY-MM-DD~YYYY-MM-DD.json`

## JSON 输出结构

```json
{
  "export_metadata": {
    "export_timestamp": "2026-04-15T20:46:56.337Z",
    "date_range": {
      "start_ms": 1776182400000,
      "end_ms": 1776268800000,
      "label": "今天"
    },
    "project_filter": "/Users/agiray/Desktop/GitHub/airay-skills",
    "total_sessions": 5,
    "total_messages": 127
  },
  "sessions": [
    {
      "session_id": "2cfb601c-a434-4647-870b-d9e148dcb231",
      "project_path": "/Users/agiray/Desktop/GitHub/airay-skills",
      "start_time": "2026-04-15T10:30:45.123Z",
      "end_time": "2026-04-15T11:45:30.456Z",
      "message_count": 25,
      "messages": [
        {
          "type": "user",
          "timestamp": "2026-04-15T10:30:45.123Z",
          "content": "用户的消息内容",
          "role": "user",
          "cwd": "/current/working/directory"
        },
        {
          "type": "assistant",
          "timestamp": "2026-04-15T10:30:46.234Z",
          "content": [
            {
              "type": "text",
              "text": "AI 的响应内容"
            },
            {
              "type": "tool_use",
              "id": "tool_use_id",
              "name": "Bash",
              "input": {"command": "echo hello"}
            }
          ],
          "role": "assistant"
        },
        {
          "type": "tool_result",
          "timestamp": "2026-04-15T10:30:47.345Z",
          "tool_use_id": "tool_use_id",
          "content": "命令输出结果",
          "is_error": false,
          "role": "tool"
        }
      ]
    }
  ],
  "statistics": {
    "total_tool_calls": 45,
    "tool_breakdown": {
      "Bash": 20,
      "Read": 15,
      "Write": 5,
      "Edit": 5
    },
    "projects_involved": [
      "/Users/agiray/Desktop/GitHub/airay-skills"
    ],
    "time_span_hours": 1.25
  }
}
```

## 输出

导出完成后，显示以下信息：

```
✅ 对话导出完成！

导出范围：今天 (2026-04-15)
项目：/Users/agiray/Desktop/GitHub/airay-skills
会话数：5
消息数：127

保存位置：./chat-export-2026-04-15.json
文件大小：245 KB

💡 提示：使用 jq 或 Python 脚本进一步分析导出的数据
```

## 格式规则
- 所有统计数字必须精确，不允许"约"、"大概"
- 输出 JSON 使用 UTF-8 编码
- 保留原始消息内容结构，不做摘要或省略
- 使用中文
- 不使用 emoji
