---
name: airay-md2book
description: 把一份或多份 Markdown 加工成书籍级 docx，适用于出版社审校、投稿、纸质书定稿和正式交付。支持单文件转换，也支持书籍模式：自动生成封面、目录、作者页、章节分页，并自动嵌入图片。触发词：md 转 docx、markdown 转 word、做一本书、出版社审校稿、投稿稿、纸质书定稿、book docx、目录页、作者页、章节分页、生成 word 稿件。
---

# airay-md2book

> 这个技能现在只做一件事：把 Markdown 变成书籍级 docx。

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
  --subtitle "让 AI 记住你的工作方式" \
  --author "花叔" \
  --extra-info "2026 年 · 橙皮书系列" \
  --cover-image ./cover.png \
  --author-page-preset 100qs \
  --chapter-labels "第 1 章,第 2 章,第 3 章,后记,附录" \
  --images-dir ./images \
  -o book.docx
```

## 参数说明

- `--book`：开启书籍模式，自动加封面、目录、作者页、章节分页
- `--title`：书名，书籍模式必填
- `--subtitle`：副标题
- `--author`：作者名
- `--extra-info`：封面顶部小字
- `--cover-image`：封面图路径；书籍模式必填，封面页只放这张图，不再额外叠加文字
- `--author-page-file`：作者页内容文件，生成可复制文本页
- `--author-page-preset`：内置作者页模板，当前支持 `100qs`
  - `100qs` 已固化为技能内置模板，后续所有《100 个问题系列》书稿可直接复用
- `--chapter-labels`：章号标签，逗号分隔
- `--images-dir`：图片目录
- `--page-size`：`book` 或 `a4`
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

如果 `H1` 本身已经带有 `第一章`、`第二章`、`附录`、`后记`、`前言`、`序` 等前缀，而书籍模式又通过 `--chapter-labels` 提供了章标签，目录展示时应去掉标题里的重复前缀，避免出现：

- `第一章 第一章 基础认知与定位`

正确效果应为：

- `第一章 基础认知与定位`

### 章节标题

每个章节文件建议以 H1 开头：

```markdown
# 第一章 基础认知与定位
```

如果书籍模式需要章号小标，优先使用 `--chapter-labels`，不要把章号逻辑硬编码在正文里。

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

或者传你自己的内容文件：

```bash
python3 "$SKILL_DIR/scripts/md_to_docx.py" ch01.md --book \
  --title "AI Agent 100 问" \
  --cover-image ./cover.png \
  --author-page-file ./author-page.md \
  -o book.docx
```

## 依赖

先确保安装：

```bash
python3 -m pip install python-docx Pillow
```

脚本缺依赖时会直接报错并提示安装命令。

## 输出结果

成功后告诉用户：

- docx 的绝对路径
- 文件是否成功生成
- 如果是书籍模式，可顺带说明包含了封面、作者页和目录

## 参考

完整 cookbook：

- `references/md-to-docx-cookbook.md`
