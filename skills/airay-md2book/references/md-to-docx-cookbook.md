# md → docx Cookbook

> 把 md 加工成出版社级 docx 的全套技巧——基于实战做完《图解 Agent Skills》158 页纸质书审校稿的经验沉淀。

---

## 为什么独立做这个，不直接用 pandoc

`pandoc article.md -o article.docx` 一行就能出 docx，但你打开会发现：

- 默认 Calibri 字体，中文渲染丑（系统宋体兜底）
- 表格无边框无表头底色
- 引用块是单一灰色，分不清「建议 / 警告 / 重点」
- 章节首页平淡——没有章号小标、没有副标题、没有分隔线
- 没有稳定的封面、作者页、目录结构（除非你自己大量定制）
- 配图默认左对齐 + 无图说

**给 AI 看够用，给人类编辑/出版社不够看**。专业出版的版式语言有它自己的细节——这个 cookbook 把这些细节都做成了脚本预设。

---

## 三种使用模式

### 模式 1 · 单文件（最简）

```bash
python3 scripts/md_to_docx.py article.md
```

会自动：
- 同名输出 `article.docx`
- 从 md 同级目录找图片（`./` 或同名 `images/`）
- 应用专业排版预设
- 默认大 32 开页面（176×240mm）

适合：单篇文章投稿、博客转 docx 存档、技术文档归档。

### 模式 2 · 多文件合并（不带封面）

```bash
python3 scripts/md_to_docx.py ch01.md ch02.md ch03.md -o combined.docx
```

每个 md 自动作为一章，章节之间分页。**没有封面、没有目录、没有作者页**——纯内容串接。

适合：把几个章节快速合一份审稿用。

### 模式 3 · 书籍模式（完整出版稿）

```bash
python3 scripts/md_to_docx.py ch*.md postscript.md appendix.md --book \
    --title "图解 Agent Skills" \
    --subtitle "让 AI 记住你的工作方式" \
    --author "花叔" \
    --extra-info "2026 年 · 橙皮书系列" \
    --cover-image ./cover.png \
    --author-page-preset 100qs \
    --chapter-labels "第 1 章,第 2 章,第 3 章,第 4 章,第 5 章,第 6 章,第 7 章,第 8 章,第 9 章,后记,附录" \
    --images-dir ./images-v2 \
    -o book.docx
```

会自动：
- 加封面页（书籍模式必须提供封面图）
- 可选加作者页；版式按样板页渲染，但内容是可复制文本
- 加「关于这本书」介绍页（如果首章前有这段）
- 生成目录；目录只收 `H1/H2/H3`，不包含正文段落，不展开 `H4+`
- 目录页排版固定为：在原字号基础上统一减 2、1.2 倍行距、段前段后为 0
- 作者页排版固定为：在原字号基础上统一减 2、1.2 倍行距、段前段后为 0
- 全书页眉页脚固定留空：不写任何文字、页码、换行或占位内容
- 不再生成独立章标签；目录页和章节首页都不显示 `第一章 / 第五章` 这类单独小标
- 全文中文字体统一为宋体风格，全文英文字体统一为 `Consolas`
- 章节标题、问题标题、引用资料文字统一使用书内红色
- `参考资料` 部分是硬规则：标题与条目统一 1 倍行距、段前段后均为 0
- 每章首页保留大字号章名 + 英文副标题（如果有 `*English*` 这种独立段落）+ 红色底部分隔线

适合：纸质书定稿、出版社审校、投稿完整稿件。

### 封面设计

当前封面默认是这套结构：

- `--cover-image` 是书籍模式必填
- 封面页会直接整页放这张图，不再叠加书名、作者等文字
- 如果不传封面图，脚本会直接报错提示你先提供封面图

调用方式：

```bash
python3 scripts/md_to_docx.py ch01.md --book \
    --title "AI Agent 100 问" \
    --subtitle "第一章测试稿" \
    --author "AIray" \
    --cover-image ./cover.png \
    -o chapter-1.docx
```

### 作者页

如果第二页要像样板图那样排，但内容还能被选择、复制、点击链接，用作者页入口。

内置模板：

```bash
python3 scripts/md_to_docx.py ch01.md --book \
    --title "AI Agent 100 问" \
    --cover-image ./cover.png \
    --author-page-preset 100qs \
    -o chapter-1.docx
```

其中 `100qs` 模板已经固化在技能内：

- [author-page-100qs.md](/Users/agiray/Desktop/github/airay-skills/skills/airay-md2book/references/author-page-100qs.md)
- 后续所有《100 个问题系列》书稿可直接复用这份作者页内容

自定义内容文件：

```bash
python3 scripts/md_to_docx.py ch01.md --book \
    --title "AI Agent 100 问" \
    --cover-image ./cover.png \
    --author-page-file ./author-page.md \
    -o chapter-1.docx
```

作者页内容文件约定：

- `## 标题`：珊瑚色小标题
- 普通段落：黑色正文
- 单独一行 `https://...`：可点击链接

---

## md 写作约定（书籍模式专用）

### 章节首页结构

为了让脚本能正确生成「大字号章名 + 英文副标题」两层版式，每个章节 md 文件的开头建议这样写：

```markdown
# 01 AI 工具的下一个进化

*The Next Evolution of AI Tools*

---

## 先看一个数字

> ![图 1-1 · 数据曲线 · 女娲37天1.8万star][fig-1-1]

正文从这里开始……
```

脚本会识别：
1. `# 01 AI 工具的下一个进化` → H1 章标题（脚本自动去掉「01」前缀，不再额外生成独立章号小标）
2. 紧跟其后的 `*English*` 段落（独立成行，整段斜体） → 英文副标题，用灰色斜体显示
3. `---` → 不渲染（仅作为视觉分隔，docx 里章标题下已有橙色色边）

### 章号映射

`--chapter-labels` 当前仅保留兼容入口，不再参与目录页和章节页显示。例如：

```bash
--chapter-labels "第 1 章,第 2 章,第 3 章,第 4 章,第 5 章,第 6 章,第 7 章,第 8 章,第 9 章,后记,附录"
```

如果你的 md 文件是 `ch01.md ch02.md ... ch09.md postscript.md appendix.md`，这个参数当前不会再额外生成章号小标。

### 目录展开规则

书籍模式目录按 Markdown 标题层级生成，规则固定如下：

- `H1`：章节级
- `H2`：主目录条目
- `H3`：子目录条目
- `H4` 及以下：不进入目录

同时遵循两条清理规则：

1. 目录不收正文段落、引用、列表、图片图说、表格内容
2. 若 `H1` 已含 `第一章 / 第二章 / 第 N 章 / 附录 / 后记 / 前言 / 序` 等前缀，而 `--chapter-labels` 又提供了章标签，目录展示时要去掉标题里的重复前缀，避免重复显示章名

### 图片自动嵌入

两种语法都支持：

**内联式**（短文章用）：

```markdown
![图说文字](images/cover.png)
```

**引用式**（长书用，集中维护）：

```markdown
正文……

> ![图 1-1 · 数据曲线 · 女娲37天1.8万star][fig-1-1]

正文……

<!-- 文末统一定义 -->
[fig-1-1]: placeholder/ch01-fig01-stars-curve.png "数据曲线 · 女娲37天1.8万star"
```

**约定路径解析**（最方便，做长书时大量用到）：

如果你的图片按 `chNN-figNN.png` 命名（如 `ch01-fig01.png`、`ch08-fig10.png`），ref id 用 `fig-N-X` 形态（如 `fig-1-1`、`fig-8-10`），就算 `[fig-1-1]:` 定义里指向的是占位路径或缺失，脚本会自动到 `--images-dir` 找 `ch01-fig01.png`。

这让你的 md 文件保持纯净——文末定义可以全是 `placeholder/ch01-fig01.png` 这种假路径，实际渲染时脚本会按约定到 `--images-dir` 取真图。

---

## 引用块的自动配色

脚本识别 emoji 前缀，给 callout 自动配色：

| 引用块开头 | 颜色 | 用途 |
|------------|------|------|
| `> **💡 ...**` | 琥珀（黄）| 重点 / 启示 / 类比 |
| `> **✅ ...**` | 青绿 | 建议 / 推荐做法 |
| `> **⚠️ ...**` | 玫红 | 警告 / 注意 / 反面案例 |
| 普通 `>` 引用 | 暖橙 | 一般引用 |

例子：

```markdown
> **💡 重点**
>
> Skills 的真正价值不完全在技术本身。
> 它在于，当你写 SKILL.md 时你会被迫认真审视自己的工作方式。
```

会渲染成琥珀色底 + 玫红左色边的 callout。

---

## 表格

支持标准 markdown 表格，自动应用：
- 表头底色 #F5F5F0
- 全表灰色边框
- 单元格水平居中
- 表头加粗

支持 `<br>` 换行（同一单元格内多行）和 `\|` 转义：

```markdown
| 模式 | 适用 | 案例 |
|---|---|---|
| **流水线** | 端到端工作流 | 阶段 1<br>检查点<br>阶段 2 |
| **API 集成** | 调用 \| 路径外部服务 | huashu-feishu |
```

---

## 代码块

代码块自动用：
- 浅灰底（F5F5F0）
- 橙色左侧 16pt 色边
- JetBrains Mono 等宽字体
- 9.5pt 字号 / 1.4 行距

适合所有语言。语言标签（如 ```python` 的 `python`）目前不渲染高亮——这是有意为之，因为出版社 docx 不需要语法高亮（黑白印刷），但保留底色 + 左色边 让代码块在版式上明显区分于正文。

---

## 页面规格

```bash
--page-size book   # 默认 · 大 32 开 176×240 mm · 适合纸质书
--page-size a4     # A4 · 适合报告 / 论文 / 投稿
```

页边距：
- book：上下 2.2cm，左右 2.0cm
- a4：上下左右 2.5cm

---

## 字体回退链

中文字体默认 `思源宋体 CN`，回退到系统的 `Songti SC`（macOS）/ `SimSun`（Windows）/ `Noto Serif CJK`（Linux）。如果你电脑没装思源宋体，docx 在花叔/出版社编辑那里打开还是会用他们装的字体——这是 docx 的优点，**字体是「指定 + 系统兜底」**，不像 html 需要你自己解决。

如果你要给特定出版社做交付，可以问对方常用字体（如方正书宋、方正兰亭黑），改 `scripts/md_to_docx.py` 顶部的：

```python
FONT_CN_BODY = "方正书宋 GBK"      # 改这一行
FONT_CN_HEAD = "方正兰亭黑 GBK"    # 改这一行
```

---

## 实战经验（来自 158 页橙皮书）

**1. 图位先用占位定义，后期统一替换**

写书的时候图还没画，但 md 里要预留图位。用引用式 + 约定路径解析最方便：

```markdown
> ![图 8-3 · 女娲三阶段架构图][fig-8-3]
<!-- 文末 -->
[fig-8-3]: placeholder/ch08-fig03.png "三阶段架构图"
```

实际生成 docx 时，只要 `--images-dir ./images-v2` 里有 `ch08-fig03.png`，脚本就会自动用真图替换 placeholder 引用。md 里那一行 `placeholder/` 不用改。

**2. 章节末尾不要手动加分页**

书籍模式会自动在每个 md 文件之间插分页。你只需要在 md 里正常用 `---` 做语义分隔（章节内的子节分隔）。脚本不会把 `---` 渲染成分页符。

**3. 「关于这本书」放第一个 md**

如果你想要「封面 → 关于这本书 → 目录 → 正文」的版式，把「关于这本书」内容写进 `ch00-intro.md` 或直接做成第一个 md 文件。封面是脚本自动生成的（来自 `--title / --subtitle / --author / --extra-info`），目录是从每个 md 的 H1 自动生成。

**4. 后记和附录的 H1 不要用「后记」「附录」前缀**

因为 `--chapter-labels` 已经提供了「后记」「附录」这类章号标签，md 里的 H1 写实际内容标题就行。脚本会自动去掉前缀「第 N 章」「附录」「后记」（如果有），避免章号重复。

例如：

```markdown
# 后记

*写不进 Skill 的部分*

---

写到这里我得说一句真话……
```

`--chapter-labels "...,后记,附录"` 已经提供「后记」标签——脚本会把 H1「后记」清成空（因为完全匹配前缀），用副标题「写不进 Skill 的部分」作为主标题。

---

## 异常处理

| 场景 | 处理 |
|------|------|
| `python-docx` 未安装 | 脚本提示 `python3 -m pip install python-docx Pillow` |
| 找不到图片 | 在该位置插入红字 `[未找到图片：path]` 占位，不报错继续 |
| H1 自动识别错 | 检查 md 里 H1 文本是否包含「第 N 章 / 附录 / 后记」前缀——脚本会去掉这些前缀 |
| 目录章名不对 | 检查 md 第一个 H1 的清理结果（脚本去掉 `^第N章\s*` / `^\d{2}\s+` / `^附录\s*` / `^后记\s*`） |
| 表格列对不齐 | 检查 markdown 表格 separator 行的 `|` 数量必须和表头一致 |
| docx 在 Word 打开字体不对 | docx 字体是「指定 + 系统兜底」，不同电脑会用不同字体；要彻底统一需要嵌字（出版社一般不需要） |

---

## 投稿场景速查

**给文学/科技类出版社的纸质书审校稿**：用书籍模式 + 大 32 开 + 完整封面/目录/页眉。例：

```bash
python3 scripts/md_to_docx.py ch*.md --book \
    --title "书名" --author "作者" --page-size book \
    --images-dir ./images -o 出版社审校版.docx
```

**给科研期刊/会议的投稿稿件**：A4 单文件，不需要封面/目录。

```bash
python3 scripts/md_to_docx.py paper.md --page-size a4 -o paper.docx
```

**给客户做的咨询报告**：A4 + 书籍模式（要封面但不要花哨章号）。

```bash
python3 scripts/md_to_docx.py report.md --book \
    --title "XX 产品咨询报告" --author "花叔咨询" \
    --page-size a4 -o report.docx
```

**给编辑改稿的工作稿**：不需要书籍模式，直接转就行。让编辑用 Word 的「修订模式」批注，比给 html 方便十倍。

```bash
python3 scripts/md_to_docx.py article.md -o article_draft.docx
```

---

## 一句话总结

**docx 不是给 LLM 看的，是给人看的。** 凡是「需要编辑做批注 / 出版社审校 / 投稿系统接收 / 客户需要 .docx 格式」的场景，用能力 4。其他场景继续用能力 2 的 html。
