---
name: airay-md2book
description: 把一份或多份 Markdown 加工成书籍级 docx，适用于出版社审校、投稿、纸质书定稿和正式交付。支持单文件转换，也支持书籍模式：自动生成封面、目录、作者页、章节分页，并自动嵌入图片。触发词：md 转 docx、markdown 转 word、做一本书、出版社审校稿、投稿稿、纸质书定稿、book docx、目录页、作者页、章节分页、生成 word 稿件。
---

# airay-md2book

> 这个技能现在只做一件事：把 Markdown 变成书籍级 docx。

## 启动横幅

技能启动时，先输出以下横幅：

```text
═══════════════════════════════════════════════════════════════
▌ airay-md2book ▐
Markdown 书稿整理 → 书籍级 docx 生成
═══════════════════════════════════════════════════════════════
磊叔 │ 微信：AIRay1015 │ github.com/akira82-ai
───────────────────────────────────────────────────────────────
- 单篇 Markdown 转标准 Word 稿件
- 多篇 Markdown 合并成书籍 docx
- 自动生成封面、目录、作者页、章节分页
- 面向出版社审校、投稿和正式交付
═══════════════════════════════════════════════════════════════
最后更新：2026-07-04
```

## 什么时候用

以下场景直接触发：

- 把单篇 md 生成 Word 稿件
- 把多篇 md 合成一本书
- 生成出版社审校稿 / 投稿稿 / 纸质书定稿
- 需要封面、目录、作者页、章节分页的 Word 文档

不再负责：

- PDF 生成
- HTML 生成
- 封面图采样排版

## 调用方式

### 单文件

```bash
python3 "$SKILL_DIR/scripts/md_to_docx.py" article.md
python3 "$SKILL_DIR/scripts/md_to_docx.py" article.md -o article.docx
python3 "$SKILL_DIR/scripts/md_to_docx.py" article.md --images-dir ./images
```

### 多文件合并

```bash
python3 "$SKILL_DIR/scripts/md_to_docx.py" ch01.md ch02.md ch03.md -o combined.docx
```

### 书籍模式

```bash
python3 "$SKILL_DIR/scripts/md_to_docx.py" ch*.md postscript.md appendix.md --book \
  --title "图解 Agent Skills" \
  --cover-image ./cover.png \
  --author-page-preset 100qs \
  --images-dir ./images \
  -o book.docx
```

## 参数说明

- `--book`：开启书籍模式，自动加封面、目录、作者页、章节分页
- `--title`：书名，书籍模式必填
- `--cover-image`：封面图路径；书籍模式必填，封面页只放这张图，不再额外叠加文字
- `--author-page-preset`：内置作者页模板，当前支持 `100qs`
  - `100qs` 已固化为技能内置模板，后续所有《100 个问题系列》书稿可直接复用
- `--images-dir`：图片目录
- `-o/--output`：输出 docx 路径

## 输入约定

### 目录规则

书籍模式下，目录遵循以下硬约束：

- 目录只展示 Markdown 原文中的 `H1`、`H2`、`H3`
- 不展示正文段落、引用块、列表、图片说明、表格正文
- 不向下展开 `H4` 及更深层级
- `H1` 用于章节级目录
- `H2` 用于主条目
- `H3` 用于轻量子条目
- 目录页排版已固化：在原字号基础上统一减 2、1.2 倍行距、段前段后均为 0
- 全书页眉页脚强制留空：不得写任何文字、页码、换行或占位内容

- 不再生成独立章标签，不再单独显示 `第一章 / 第五章` 这类小标

### 章节标题

每个章节文件建议以 H1 开头：

```markdown
# 第一章 基础认知与定位
```

章节首页不再额外生成章号小标，只显示 H1 标题本身。

### 全局样式

- 全文中文字体统一为微软雅黑（正文英文同字体），代码块/行内代码用 `Consolas`
- 章节标题、问题标题、引用资料文字统一使用书内红色
- H1-H3 默认挂内置 Heading 样式与大纲级别（`docx-theme.yaml` 的 `headings.use_builtin_styles` 可关），供 Word 导航窗格与自动目录识别
- `参考资料` 部分是硬规则：标题与条目统一 1 倍行距、段前段后均为 0

### 图片

支持两种写法：

```markdown
![图说](images/cover.png)
```

```markdown
![图 1-1 · 数据曲线][fig-1-1]

[fig-1-1]: images/ch01-fig01.png "数据曲线"
```

### 作者页

如果你要第二页做成“按图排版，但内容可选择和复制”，用：

```bash
python3 "$SKILL_DIR/scripts/md_to_docx.py" ch01.md --book \
  --title "AI Agent 100 问" \
  --cover-image ./cover.png \
  --author-page-preset 100qs \
  -o book.docx
```

作者页排版已固化：

- 在原字号基础上统一减 2
- 1.2 倍行距
- 段前段后均为 0
- 全书页眉页脚强制留空：不得写任何文字、页码、换行或占位内容

### 参考资料

`参考资料` 这一节的识别和样式入口已经统一放到：

- [docx-theme.yaml](/Users/agiray/Desktop/github/airay-skills/skills/airay-md2book/docx-theme.yaml)

重点看：

- `reference_section.title_text`
- `reference_section.title_texts`
- `reference_section.title`
- `reference_section.item`

## 依赖

先确保安装：

```bash
python3 -m pip install python-docx Pillow PyYAML
```

脚本缺依赖时会直接报错并提示安装命令。

## 输出结果

成功后告诉用户：

- docx 的绝对路径
- 文件是否成功生成
- 如果是书籍模式，可顺带说明包含了封面、作者页和目录
