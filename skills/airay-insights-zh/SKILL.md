---
name: airay-insights-zh
version: 1.0.0
description: |
  翻译或生成 Claude Code 的 insights 中文报告。当用户说以下任一内容时自动触发：
  - "翻译 insights"、"翻译报告"、"中文版 insights"
  - "/insights-zh"、"生成中文报告"、"insights 中文翻译"
  - "把 insights 报告翻译成中文"、"生成中文的 insights HTML"
  - "中文 insights"、"生成 insights 中文版"、"我的 insights"
  - 提到将 ~/.claude/usage-data/report.html 翻译为中文

  功能说明：
  - 智能判断：如果 report.html 不存在则提示用户先运行 /insights
  - 自动检查报告年龄（3 天内为新鲜，过期则提示用户）
  - 使用 TSV 格式提取文本，避免 JSON 转义问题
  - 使用 Task 工具启动独立子代理翻译，避免嵌套会话问题
  - 保留所有 HTML 标签、CSS 样式、JavaScript 代码
  - 只翻译用户可见的文本内容
  - 生成 report-zh.html 并在浏览器中打开
disable-model-invocation: false
allowed-tools: Bash, Read, Write, Task, Skill
---

## Script Directory

**Agent Execution Instructions**:
1. Determine this SKILL.md file's directory path as `{baseDir}`
2. Script path = `{baseDir}/scripts/{script-name}`
3. Before running any script, resolve `{baseDir}` first


# Insights 中文报告生成器

生成或翻译 Claude Code 的 insights HTML 报告为中文。

## 启动横幅

技能触发时，请先显示以下横幅：

```
═══════════════════════════════════════════════════════════════
▌ Insights 中文翻译 ▐
Claude Code 报告汉化工具
═══════════════════════════════════════════════════════════════
磊叔 │ 微信：AIRay1015 │ github.com/akira82-ai
────────────────────────────────────────────────────────────
📄 TSV 格式提取文本，避免 JSON 转义问题
🤖 Task 子代理翻译，避免嵌套会话错误
🎨 保留完整 HTML 结构、CSS 样式、JS 代码
✨ 自动检查报告年龄，智能提示更新
🌐 翻译用户可见文本，保留技术术语
═══════════════════════════════════════════════════════════════

技能已启动...
```

## 核心优势

- ✅ **避免嵌套会话问题**：使用 Task 工具而非 subprocess 调用 claude 命令
- ✅ **避免 JSON 转义问题**：使用 TSV 格式而非 JSON 存储翻译
- ✅ **修复索引不一致问题**：统一使用 BeautifulSoup，通过原文匹配而非索引
- ✅ **简化流程**：单一脚本完成提取、合并流程
- ✅ **自动清理**：翻译完成后自动删除临时 TSV 文件
- ✅ **自动检查**：检测报告年龄，过期时提示用户

## 执行流程

### 步骤 0: 智能判断与报告检查

1. **检查源文件**：
   ```bash
   ls -lh ~/.claude/usage-data/report.html
   ```

2. **检查报告年龄**：
   - 自动检查报告是否在 3 天内生成
   - **如果报告过期**：提示用户运行 `/insights` 生成新报告，**结束技能**

3. **判断用户意图**：
   - 如果用户说"生成"、"新建"或文件不存在 → 提示运行 `/insights`
   - 如果用户说"翻译"、"转换"且文件存在且新鲜 → 继续翻译步骤

### 步骤 1: 提取文本块

运行提取脚本：
```bash
python3 {baseDir}/scripts/translate.py
```

脚本会：
1. ✅ 检查报告年龄（3 天内为新鲜）
2. ✅ 提取 HTML 中的所有文本块
3. ✅ 保存为 TSV 格式到 `/tmp/insights_blocks.tsv`
4. ✅ 显示翻译提示

输出示例：
```
============================================================
Insights 报告翻译工具
============================================================

[1/4] 检查报告状态...
✅ 报告新鲜（0 天前生成）

[2/4] 提取文本块...
✅ 提取了 311 个文本块，共 15756 字符
✅ 已保存到 /tmp/insights_blocks.tsv

[3/4] 等待翻译...
请使用 Task 工具翻译 /tmp/insights_blocks.tsv
```

### 步骤 2: 批量翻译（显示进度）

使用批量翻译模式，在主会话中实时显示进度：

1. **启动批量翻译**：
   ```bash
   python3 {baseDir}/scripts/auto_batch.py
   ```

2. **查看进度和待翻译内容**：
   输出示例：
   ```
   [██████░░░] 50.3% (140/309)

   待翻译批次：15 行
   ═══════════════════════════════════════════════════════════

   1. Conversation Insights
   2. Dashboard Overview
   3. Time Period
   ...
   ```

3. **提供翻译**：
   - 翻译显示的 15 行内容
   - 每行一个翻译
   - 保持专有名词和技术术语不变

4. **更新 TSV 文件**：
   使用以下命令更新翻译：
   ```bash
   python3 {baseDir}/scripts/auto_batch.py --update <start_idx> <trans1> <trans2> ...
   ```

   或者直接编辑 TSV 文件：
   ```bash
   open /tmp/insights_blocks.tsv
   ```

5. **重复步骤 1-4**，直到显示：
   ```
   ✅ 所有行已翻译完成！
   ```

6. **继续到步骤 3**：合并翻译结果

### 步骤 3: 合并翻译结果

翻译完成后，再次运行脚本：
```bash
python3 {baseDir}/scripts/translate.py
```

脚本会自动：
1. ✅ 加载 TSV 中的翻译
2. ✅ 使用 BeautifulSoup 合并到 HTML
3. ✅ 保存为 `report-zh.html`
4. ✅ 在浏览器中打开

输出示例：
```
[4/4] 合并翻译...
✅ 生成完成: ./report-zh.html
   替换了 305 个文本节点

============================================================
✅ 翻译完成！
输出文件: /path/to/report-zh.html
============================================================
```

## 翻译规则

**必须保留不翻译：**
- HTML 标签和属性名（`class`、`id`、`data-*`、`style`、`href` 等）
- HTML 属性值（`class="container"`、`id="header"` 等）
- CSS 类名和 ID
- 代码块中的技术术语和代码片段
- 专有名词：Claude Code、GitHub、Twitter、Python、Rust 等
- 技术术语：TUI、API、HTML、CSS、JSON、SSH 等

**需要翻译：**
- 所有用户可见的文本内容
- 页面标题、标题、段落文本
- 按钮文本、链接文本（href 保留，链接文本翻译）
- 表格内容、列表项文本

**翻译原则：**
- 保持 HTML 结构完全不变
- 保持所有标签和属性完整
- 只翻译文本节点内容
- 确保翻译后的 HTML 语法正确
- 技术术语保持一致性
- **避免使用引号**：TSV 格式下，中文引号会破坏解析，用其他表达方式

## 错误处理

### 报告不存在

如果 `~/.claude/usage-data/report.html` 不存在：
1. 提示用户运行 `/insights` 命令生成报告
2. 支持指定自定义路径：`--path <your-report.html>`

### 报告过期

如果报告超过 3 天未更新：
1. 提示用户报告已过期及过期天数
2. 建议运行 `/insights` 生成最新报告
3. 可使用 `--force` 参数强制翻译过期报告

### 嵌套会话错误

如果看到错误：
```
Error: Claude Code cannot be launched inside another Claude Code session
```

**原因**：使用了 `subprocess.run(['claude', 'prompt', ...])`
**解决**：使用 Task 工具启动独立子代理

### TSV 格式问题

如果 TSV 解析失败：
1. 检查是否有未转义的制表符
2. 检查是否有中文引号（应该避免使用）
3. 确保每行都有两列：原文\t译文

## 依赖问题

脚本需要 `beautifulsoup4` 库：
```bash
pip3 install beautifulsoup4
```

## 可选参数

```bash
# 翻译指定报告
python3 {baseDir}/scripts/translate.py --path <your-report.html>

# 指定输出文件
python3 {baseDir}/scripts/translate.py --output result.html

# 强制翻译过期报告（不推荐）
python3 {baseDir}/scripts/translate.py --force
```

## 完成提示

```
✅ Insights 中文报告生成完成！

生成的文件：
- report-zh.html (当前目录)

原始报告：~/.claude/usage-data/report.html (未修改)

已在浏览器中打开翻译后的报告。
```

## 架构说明

### 新架构（推荐）

**流程**：
```
检查报告 → 提取文本 → TSV 格式 → Task 子代理翻译 → 合并 HTML
```

**优势**：
- **避免嵌套会话**：Task 工具启动独立子代理
- **避免 JSON 转义**：TSV 格式天然支持中文引号
- **易于维护**：单一脚本，逻辑清晰
- **进度可控**：每个步骤独立执行，可中断恢复

### 旧架构问题（已废弃）

旧方案 `translate_report.py` 存在以下问题：

1. **嵌套会话失败**：
   ```python
   subprocess.run(['claude', 'prompt', '--model', 'haiku', ...])
   # Error: Claude Code cannot be launched inside another Claude Code session
   ```

2. **JSON 转义问题**：
   ```python
   # 子代理生成的 JSON
   {"translation": "例如，你多次用"算了，clear"这样的短语"}
   # 中文引号导致解析失败
   ```

3. **修复困难**：
   - 多次尝试正则替换、行级修复均失败
   - 最终改用 TSV 格式才解决

## 详见

- 技术细节记录：`~/memory/insights-translation-fix.md`

## 索引问题修复

### 问题描述

早期版本的 translate.py 存在索引不一致问题：

1. **提取阶段**使用 `HTMLParser`，提取了 311 个文本块
2. **合并阶段**使用 `BeautifulSoup.find_all(string=True)`，找到 315 个文本节点
3. 两者的遍历顺序和节点计数不同，导致索引错位

### 解决方案

统一使用 BeautifulSoup 进行文本提取和合并：

- **提取阶段**：保存 `(NavigableString 对象, 文本)` 元组
- **存储格式**：TSV 改为 `原文 | 译文` 两列
- **合并阶段**：重新提取节点，按原文内容匹配翻译

### 优势

- 彻底解决索引不一致问题
- 不依赖索引，使用内容匹配
- 代码更简洁（不需要索引管理）
