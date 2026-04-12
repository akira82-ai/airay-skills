---
name: airay-skill-backup
version: 1.0.0
description: |
  Backup and restore installed Claude Code global skills (~/.claude/skills/).
  TRIGGER when: user says "备份技能", "backup skills", "恢复技能", "restore skills",
  "列出备份", "list backup", "/skill-backup", or mentions exporting/importing/syncing skills.
---

## Script Directory

**Agent Execution Instructions**:
1. Determine this SKILL.md file's directory path as `{baseDir}`
2. Script path = `{baseDir}/scripts/{script-name}`
3. Before running any script, resolve `{baseDir}` first


**重要**：技能加载后，必须先将下方 banner 以纯文本形式输出给用户，然后再执行任何操作。

```
═══════════════════════════════════════════════════════════════
▌ Skill Backup ▐
备份和恢复已安装的 Claude Code 全局技能 (~/.claude/skills/)
═══════════════════════════════════════════════════════════════
磊叔 │ 微信：AIRay1015 │ github.com/akira82-ai
────────────────────────────────────────────────────────────
  备份    将技能打包为 .tar.gz 归档
  恢复    从备份文件还原技能到 ~/.claude/skills/
  列表    查看备份文件中包含的技能清单
═══════════════════════════════════════════════════════════════
最后更新：2026-03-31

## 子命令

### 创建备份

```bash
bash {baseDir}/scripts/backup.sh <输出路径> [选项]
```

选项：
- `--skills skill1 skill2 ...` — 只备份指定技能（默认备份全部）
- `--note "备注"` — 添加备注信息

示例：
```bash
# 备份全部技能
bash {baseDir}/scripts/backup.sh ~/backups/skills-2026-03-27.tar.gz

# 只备份指定技能
bash {baseDir}/scripts/backup.sh ~/backups/partial.tar.gz --skills skill-creator skill-usage

# 带备注
bash {baseDir}/scripts/backup.sh ~/backups/test.tar.gz --note "实验前备份"
```

### 列出备份内容

```bash
bash {baseDir}/scripts/list.sh <备份文件>
```

### 恢复备份

```bash
bash {baseDir}/scripts/restore.sh <备份文件> [--target <目标路径>]
```

默认恢复到 `~/.claude/skills/`，会覆盖已有同名技能。

## 执行流程

当用户请求备份/恢复技能时：

1. 确定用户意图（备份/恢复/列出）

### 备份流程

2. 用 Bash 列出当前已安装的技能（`ls ~/.claude/skills/`）
3. 使用 AskUserQuestion 让用户选择备份范围：
   - 选项 1：备份全部技能
   - 选项 2：备份指定技能（用户在 Other 中输入技能名，空格分隔）
   - question: "要备份哪些技能？"
   - header: "备份范围"
4. 使用 AskUserQuestion 让用户选择/输入备份路径：
   - 选项 1：`~/backups/` — 默认备份目录
   - 选项 2：桌面 `~/Desktop/`
   - question: "备份文件保存到哪里？"
   - header: "备份路径"
   - 用户可在 Other 中输入自定义路径
5. 根据用户选择构建命令并执行 backup.sh
6. 向用户报告结果

### 恢复流程

2. 用 Bash 列出 ~/backups/ 目录下已有的备份文件（`ls -lt ~/backups/*.tar.gz 2>/dev/null`）
3. 使用 AskUserQuestion 让用户选择要恢复的备份文件，列出找到的文件供选择，用户可在 Other 中输入其他路径
   - question: "要恢复哪个备份？"
   - header: "选择备份"
4. 执行 restore.sh
5. 向用户报告结果

### 列表流程

2. 用 Bash 列出 ~/backups/ 目录下已有的备份文件
3. 使用 AskUserQuestion 让用户选择要查看的备份文件
   - question: "要查看哪个备份的内容？"
   - header: "选择备份"
4. 执行 list.sh
5. 向用户报告结果
