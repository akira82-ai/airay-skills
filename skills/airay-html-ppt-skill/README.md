# Magazine Web PPT · 你的 AI 演示稿生产力工具

> 🌏 **English version: [README.en.md](./README.en.md)**

你不是来“学模板”的。  
你是来**更快做出一份能讲、能看、能交付的演示稿**。

这个 Skill 帮你把 PPT 这件事变成一条清晰流程：  
**输入需求 → 自动成稿 → 浏览器预览 → 一键导出 PDF**。

![Magazine Web PPT 效果展示](https://github.com/user-attachments/assets/5dc316a2-401c-4e37-9123-ea081b6ae470)

## 你能得到什么

- 更快起稿：给出 0-5 输入项，直接进入结构化产出
- 更稳呈现：杂志风视觉、节奏清晰、信息层级明确
- 更少返工：内置验收逻辑，先把可读性和可交付做对
- 更强复用：单文件 HTML，适合演讲、评审、分享的重复生产

## 新增能力（本项目增强）

- ✅ **24 页能力导览 Demo**：不只看效果，还能边看边学怎么用
- ✅ **启动即引导**：首屏给你 0-5 输入模板，降低沟通成本
- ✅ **ESC 索引可读性修复**：缩略图显示为可读态，不再关键内容空白
- ✅ **图片全屏预览**：任意 `<img>` 点击可全屏查看
- ✅ **当前页内循环切图**：全屏态支持左右切换，仅在当前 slide 图片集合内循环
- ✅ **键盘翻页收敛**：仅 `Space / ArrowLeft / ArrowRight` 翻页，滚轮不触发翻页
- ✅ **导出文件名优化**：PDF 默认取第一页标题（如：`杂志风 Web PPT.pdf`）
- ✅ **HTTP 预览强制规则**：查看 demo 与预览成稿都要求本地 HTTP 访问

## 快速开始（3 步）

### 1）安装

```bash
npx skills add https://github.com/akira82-ai/airay-html-ppt-skill --skill airay-html-ppt-skill
```

### 2）首次输入（照这个填）

```text
0）查看demo
1）主题
2）受众
3）时长
4）目的
5）页数要求
```

### 3）预览（必须走 HTTP）

```bash
python3 -m http.server 4173
```

打开 `http://localhost:4173/assets/demo.html` 查看 Demo，或打开你的成稿 HTML 进行预览与验收。

## 交互与导出

- 翻页：`Space` / `←` / `→`
- 索引：`ESC` 打开/关闭
- 图片：点击全屏，`ESC` 关闭，左右键仅在当前页内切图
- 导出：右下角 `导出 PDF` 按钮
- 文件名：默认取第一页标题

## 适合 / 不适合

**✅ 合适**

- 线下分享 / 行业演讲 / 私享会
- AI 产品发布 / demo day / 方案汇报
- 希望兼顾审美、效率与交付稳定性的个人或团队

**❌ 不合适**

- 复杂财务建模页
- 超大表格培训课件
- 多人实时协作编辑型文档

## 安装（完整方式）

### 方式一：一行命令安装（推荐）

```bash
npx skills add https://github.com/akira82-ai/airay-html-ppt-skill --skill airay-html-ppt-skill
```

### 方式二：把下面这段话直接发给 AI

> 帮我安装 `airay-html-ppt-skill` 这个 Claude Code skill。请按下面步骤做：
>
> 1. 确保 `~/.claude/skills/` 目录存在（不存在就创建）
> 2. 执行 `git clone https://github.com/akira82-ai/airay-html-ppt-skill.git ~/.claude/skills/airay-html-ppt-skill`
> 3. 验证：`ls ~/.claude/skills/airay-html-ppt-skill/` 应该看到 `SKILL.md`、`assets/`、`references/` 三项
> 4. 告诉我安装好了，之后我说“做一份杂志风 PPT”之类的话就会触发这个 skill

把这段话复制粘贴给 Claude Code / Cursor / 任何有 shell 权限的 AI Agent，它会自动完成安装。

### 方式三：手动命令行

```bash
git clone https://github.com/akira82-ai/airay-html-ppt-skill.git ~/.claude/skills/airay-html-ppt-skill
```

## 触发方式

装好后，Claude Code 会在对话里自动发现并调用这个 skill。触发关键词：

- “帮我做一份杂志风 PPT”
- “生成一个 horizontal swipe deck”
- “editorial magazine style presentation”
- “electronic ink 风格演讲 slides”

## 使用流程

Skill 本身是结构化工作流，Agent 会逐步引导：

1. **查看 Demo（可选）** — 打开 `assets/demo.html`，快速体验 24 页能力样例
2. **需求澄清** — 输入 0-5：主题、受众、时长、目的、页数（或先查看 demo）
3. **拷贝模板** — `assets/template.html` → 项目目录，改 `<title>`，换主题色
4. **填充内容** — 从布局骨架里挑、粘、改文案（先做类名预检 + 主题节奏规划）
5. **可选配图** — 可询问是否生成配图，再按页面比例插入
6. **自检** — 对照 `references/checklist.md`，P0 级问题必须全过
7. **预览** — 启动本地 HTTP 后在浏览器查看
8. **迭代** — inline style 改字号/高度/间距

详细说明见 [`SKILL.md`](./SKILL.md)。

## Codex 配图能力

在 Codex 环境中，完成 deck 初稿后可以主动询问用户是否需要生成配图。用户确认后，再选择图片类型或风格，常用类型包括：

- 人文纪实照片：富士 / 徕卡感的真实场景，增加人文表现力
- 信息图 / 流程图 / 对比图 / 系统关系图：用于解释无法用实拍照片说明的概念
- 截图再设计 / UI 情景图：把原始截图统一成适合 PPT 的比例和视觉密度

生成图片时要遵守两个关键规则：

- 图片是 PPT 中的嵌入素材，不要自带页脚、页底、标题、角标、页码或装饰边框
- 图片比例必须先匹配落位：主图常用 16:9 / 16:10，截图再设计常用 16:10，多图网格统一高度

## 目录结构

```text
airay-html-ppt-skill/
├── package.json          ← 项目配置
├── SKILL.md              ← Skill 主文件：工作流、原则、常见错误
├── README.md             ← 本文件
├── assets/
│   ├── template.html     ← 完整可运行的种子 HTML（CSS + WebGL + 翻页 JS 全配好）
│   ├── demo.html         ← 官方 24 页 Demo Deck（能力导览/回归基线）
│   └── demo-images/      ← Demo 使用的本地占位图（离线可用）
└── references/
    ├── components.md     ← 组件手册（字体、色、网格、图标、callout、stat、pipeline）
    ├── layouts.md        ← 页面布局骨架（可直接粘贴）
    ├── themes.md         ← 主题色预设
    ├── image-prompts.md  ← 配图类型、比例和基础提示词
    └── checklist.md      ← 质量检查清单（P0 / P1 / P2 / P3 分级）
```

## 快速查看 Demo

打开 `assets/demo.html` 即可看到 24 页能力导览示例，覆盖输入模板、结构布局、配图规则、交互能力、导出与验收、边界说明。

## 导出图片 PDF

页面右下角「导出 PDF」按钮会执行前端图片导出（`html2canvas + jsPDF`）：

- 导出前自动冻结动画、显示全部内容，并临时隐藏导航与提示区
- 逐页截图后合成为 PDF（图片版，非文字版）
- 默认文件名：`<第一页标题>.pdf`
- 输出页尺寸：16:9（`160mm x 90mm`）

说明：

- 这是纯前端导出，不需要本地 Node 服务
- 建议在本地 HTTP 页面中使用（避免 `file://` 造成资源限制）

## 主题色预设

从 `references/themes.md` 里选一套。保持主题系统统一，能显著降低返工成本。

| 主题 | 适合场景 |
|------|---------|
| 🖋 墨水经典 | 通用默认、商业发布、不知道选啥 |
| 🌊 靛蓝瓷 | 科技 / 研究 / AI / 技术发布会 |
| 🌿 森林墨 | 自然 / 可持续 / 文化 / 非虚构 |
| 🍂 牛皮纸 | 怀旧 / 人文 / 文学 / 独立杂志 |
| 🌙 沙丘 | 艺术 / 设计 / 创意 / 画廊 |

切换主题只需替换 `template.html` 开头 `:root{}` 里的变量。

## 核心设计原则

1. **克制优于炫技** — WebGL 背景只在 hero 页透出
2. **结构优于装饰** — 信息靠字号 + 字体对比 + 网格留白
3. **图片是第一公民** — 比例稳定，裁切可控
4. **配图只做素材** — 不把页脚、标题、角标画进图片
5. **节奏靠 hero 页** — hero / non-hero 交替，阅读更轻松
6. **术语统一** — 输入、预览、导出、验收口径一致

## 致谢（Acknowledgement）

本项目核心能力与方法论 **fork 自 [guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill)**。  
感谢 [歸藏（op7418）](https://github.com/op7418) 在真实线下分享中的长期沉淀：模板体系、流程经验与质量清单，都为这个方向打下了高质量基础。

## 贡献

Bug、排版问题、新布局需求——欢迎开 Issue 或 PR。改动请优先：

- 在 `template.html` 里补类，不要让 layouts 使用未定义类
- 把踩过的坑写到 `checklist.md` 对应级别
- 新主题色进入 `themes.md` 并给出适用场景

## License

MIT © 2026 [op7418](https://github.com/op7418)
