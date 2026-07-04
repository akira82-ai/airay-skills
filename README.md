# airay-skills

AI 磊叔 开发或二创的技能仓库。

## 项目状态

- 技能数量：15
- 最近更新：2026-07-04

## 安装

```bash
# 将整仓安装到 Claude skills 目录
git clone https://github.com/akira82-ai/airay-skills.git ~/.claude/skills/airay-skills

# 后续更新
cd ~/.claude/skills/airay-skills && git pull
```

### 仅安装单个技能（以`airay-html-ppt-skill`为例）

```bash
# 1) 克隆统一仓库
git clone https://github.com/akira82-ai/airay-skills.git ~/.claude/skills/airay-skills

# 2) 仅暴露该技能为直接技能路径
ln -sfn ~/.claude/skills/airay-skills/skills/airay-html-ppt-skill ~/.claude/skills/airay-html-ppt-skill
```

## 技能列表

| 技能 | 说明 |
|------|------|
| airay-100-questions | 围绕技术与产品主题生成六章式 100 问问题清单 |
| airay-agent-review | 基于本地对话与工具记录生成每日工作复盘 |
| airay-chat-export | 导出 Claude Code 对话 session 到本地 JSON |
| airay-file-organizer | 基于语义分析进行文件分类整理（Johnny Decimal） |
| airay-github-smart-commit | 分析变更并生成规范化提交信息 |
| airay-html-ppt-skill | 生成杂志风横向翻页 Web PPT（含导出能力） |
| airay-idea-to-post | 通过多轮引导将灵感扩展为深度文章 |
| airay-insights-zh | 生成/翻译 Claude Code insights 中文报告 |
| airay-viral-forge | 将工具、资源、经验和专业内容锻造成高传播短视频脚本 |
| airay-lark-wiki-agent | 飞书知识库 Wiki 节点 CRUD 与批量操作 |
| airay-md2book | 将一份或多份 Markdown 加工成书籍级 docx |
| airay-prompt-optimizer | 诊断并优化提示词，输出可直接复制的改写版本 |
| airay-skill-backup | 备份和恢复已安装的 Claude Code 全局技能 |
| airay-skill-usage | 统计指定时间段内的技能使用情况 |
| airay-style-rewrite | 个人语气风格迁移与去 AI 味改写 |

## 运行依赖

按技能按需安装：

- Python 3.7+
- Git 2.0+
- jq（用于 `airay-skill-backup` 与部分 `airay-lark-wiki-agent` 脚本）
- beautifulsoup4（用于 `airay-insights-zh`）：`pip3 install beautifulsoup4`
- lark-cli（用于 `airay-lark-wiki-agent`）：需单独安装并完成认证
- `airay-style-rewrite` 使用 Python 3 脚本，无额外第三方依赖

## 许可证

MIT
