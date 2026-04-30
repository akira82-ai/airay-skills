# airay-skills

airay 维护的 Claude Code 多技能仓库（monorepo）。
A unified monorepo of Claude Code skills maintained by airay.

## Project Status

- Skills: 10
- Last updated: 2026-04-30
- See detailed history in `CHANGELOG.md`

## Migration Notice

`airay-html-ppt-skill` 已在本仓统一维护，路径：`skills/airay-html-ppt-skill/`。

## Installation

```bash
# Install full repository into Claude skills directory
git clone https://github.com/akira82-ai/airay-skills.git ~/.claude/skills/airay-skills

# Update later
cd ~/.claude/skills/airay-skills && git pull
```

### Install one skill only (`airay-html-ppt-skill`)

```bash
# 1) Clone unified repository
git clone https://github.com/akira82-ai/airay-skills.git ~/.claude/skills/airay-skills

# 2) Expose only this skill as a direct skill path
ln -sfn ~/.claude/skills/airay-skills/skills/airay-html-ppt-skill ~/.claude/skills/airay-html-ppt-skill
```

## Skills

| Skill | Description |
|-------|-------------|
| airay-agent-review | 基于本地对话与工具记录生成每日工作复盘 |
| airay-chat-export | 导出 Claude Code 对话 session 到本地 JSON |
| airay-file-organizer | 基于语义分析进行文件分类整理（Johnny Decimal） |
| airay-github-smart-commit | 分析变更并生成规范化提交信息 |
| airay-html-ppt-skill | 生成杂志风横向翻页 Web PPT（含导出能力） |
| airay-idea-to-post | 通过多轮引导将灵感扩展为深度文章 |
| airay-insights-zh | 生成/翻译 Claude Code insights 中文报告 |
| airay-lark-wiki-agent | 飞书知识库 Wiki 节点 CRUD 与批量操作 |
| airay-skill-backup | 备份和恢复已安装的 Claude Code 全局技能 |
| airay-skill-usage | 统计指定时间段内的技能使用情况 |

## Requirements

按技能按需安装：

- Python 3.7+
- Git 2.0+
- jq（用于 `airay-skill-backup` 与部分 `airay-lark-wiki-agent` 脚本）
- beautifulsoup4（用于 `airay-insights-zh`）：`pip3 install beautifulsoup4`
- lark-cli（用于 `airay-lark-wiki-agent`）：需单独安装并完成认证

## License

MIT
