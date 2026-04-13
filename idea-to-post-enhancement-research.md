# idea-to-post 技能增强：融入外部精华

> 日期：2026-04-13
> 目标：将外部技能的精华融入 airay-idea-to-post，补强"输出阶段"（审稿→打磨→格式适配），实现 70-80 分 → 90+ 分

---

## 一、现有技能分析

**强项（输入阶段，已成熟）：**
- 7-10 轮渐进式追问 + 框架内化
- 双阶段智能搜索（背景搜索 + 精准验证）
- 信息完备度判断标准
- 多平台输出结构

**短板（输出阶段，需增强）：**
- 初稿生成后的"反思与优化"只有一句话，缺少系统化机制
- 没有审稿评分体系
- 没有去 AI 味的具体规则
- 没有中文排版规范
- 公众号/X article 格式适配不够深入

---

## 二、外部技能精华提取

### 1. zhy-wechat-writing（zhylq/yuan-skills，94 installs/周，35 stars）

**来源:** https://skills.sh/zhylq/yuan-skills/zhy-wechat-writing

**可借鉴：**

#### 四维审稿机制
- 逻辑（30%）：论点清晰、论据充分、推理合理
- 表达（25%）：语言流畅、无 AI 痕迹、口语化适度
- 数据（25%）：数据准确、案例恰当、引用规范
- 结构（20%）：标题吸引、段落分明、首尾呼应
- 评分标准：90-100 优秀可直接发布 / 80-89 良好小幅优化 / 70-79 合格需修改 / <70 需重写

#### AI 痕迹词汇替换表
| 原词 | 替换为 |
|------|--------|
| 综上所述 | 总的来说 |
| 总而言之 | 说到底 |
| 由此可见 | 所以说 |
| 不难看出 | 我们能发现 |
| 众所周知 | 大家都知道 |

#### 润色规则
- 去除 AI 味：删除僵硬连接词（此外、另外），简化啰嗦从句
- 增强口语化：适当添加 其实、说实话、不得不说
- 优化节奏：长短句结合、适当使用感叹句/反问句
- 段落控制：不超过 5 行

#### 公众号 HTML 主题
- 6 套主题样式（apple/blue/dark/green/notion/vibrant）
- 可直接发布到公众号草稿箱

---

### 2. copy-editing（borghei/claude-skills，48 installs/周，85 stars）

**来源:** https://skills.sh/borghei/claude-skills/copy-editing

**可借鉴：**

#### Seven Sweeps 七轮编辑框架
1. Sweep 1 - 清晰度：句子可一次读懂、消除歧义引用
2. Sweep 2 - 语气一致性：避免正式/随意混用
3. Sweep 3 - So What 检验：每个论断都回答"为什么我该关心"
4. Sweep 4 - 证据支撑：每个主张都有数据/案例/引用
5. Sweep 5 - 具体性：模糊词汇替换为具体数字/场景
6. Sweep 6 - 情感共鸣：痛点具象化、用微故事
7. Sweep 7 - 零风险：消除行动障碍、添加信任信号

#### Filler 词清单（必须删除）
very, really, extremely, incredibly, quite, rather, somewhat, just, actually, basically, essentially, literally, in order to, the fact that, it should be noted that

#### 弱动词替换表
| 弱 | 强 |
|----|-----|
| utilize | use |
| implement | set up, build, create |
| leverage | use, apply |
| facilitate | help, enable |
| innovative | new, original |
| robust | strong, thorough |
| seamless | smooth, easy |
| cutting-edge | modern, latest |

#### 具体性升级
| 模糊 | 具体 |
|------|------|
| 节省时间 | 每周节省 4 小时 |
| 很多用户 | 2,847 个团队 |
| 效果很快 | 14 天见效 |
| 简单易用 | 10 分钟完成配置 |

---

### 3. essay-polish（clyderankin/essay-skills，46 installs/周）

**来源:** https://skills.sh/clyderankin/essay-skills/essay-polish

**可借鉴：**

#### 最终打磨检查项
- 节奏感：读起来顺口，句子不拖沓、不零碎
- 用词精确：替换弱动词、删除 filler 词、消除冗余
- 一致性：格式/人称/时态/术语统一
- 过渡自然：首尾衔接、段落过渡不生硬

#### 诚实评估输出
- 好在哪（2-3 点）
- 弱在哪（可接受范围内）
- 整体判断：能否在目标平台发表

---

### 4. article-polish（daqi/daqi-skills，24 installs/周）

**来源:** https://skills.sh/daqi/daqi-skills/article-polish

**可借鉴：**

#### 中文排版规范
- 中英文之间必须加空格（AI Agent 而非 AIAgent，2024 年 而非 2024年）
- 中文语境用全角标点（，。！？：；）
- 英文/代码周围用半角标点
- 省略号应为 ……
- 术语统一（Token、AI Agent、LLM、大模型）

---

### 5. ArticleSkill（TanShilongMario/ArticleSkill，93 stars）

**来源:** https://github.com/TanShilongMario/ArticleSkill

**可借鉴：**

#### 风格适配
- 亲和力强：第一人称、情绪化表达、适度自嘲
- 专业严谨：数据支撑、客观分析、逻辑严密
- 幽默风趣：轻松调侃、生动比喻、口语化
- 极简干货：话少干货多、直击要害

#### 去AI化处理
- 删除僵硬连接词
- 增加人性化细节和场景化描述
- 让文本更像真人手笔

#### 爆款要素检查
- 4 种标题公式（数字型/提问型/对比型/悬念型）
- 减少条目式输出，用叙述性文字替代

---

### 6. social-media（langchain-ai/deepagents，810 installs/周，20.4K stars）

**来源:** https://skills.sh/langchain-ai/deepagents/social-media

**可借鉴：**

#### X/Twitter Thread 格式
- 280 字符/条，用 1/🧵 格式
- 每条不超过 2 个 hashtag
- 结构：Hook → 支撑点 → 案例/证据 → 结论 + CTA

#### LinkedIn 格式
- 1,300 字符，前 210 字符可见
- 专业但个人化
- 用 "I" 分享经历

---

## 三、融合方案

### 不推翻现有流程，在初稿生成后增加三阶段后处理：

```
现有流程（追问 → 搜索 → 初稿生成）不变
        ↓
[新增] Stage 1: 四维审稿 + 评分（借鉴 zhy-wechat-writing）
        ↓
[新增] Stage 2: 深度打磨（借鉴 copy-editing + essay-polish + article-polish）
        ↓
[新增] Stage 3: 平台格式适配（借鉴 social-media + zhy-wechat-writing）
        ↓
最终输出
```

### 具体实施

1. **新建 `references/post-polish.md`** — 整合所有打磨规则：
   - 四维审稿标准 + 评分体系
   - AI 痕迹词汇替换表
   - Filler 词 + 弱动词替换表
   - 具体性升级规则
   - 中文排版规范（中英文空格、标点）
   - 节奏优化规则
   - 诚实评估输出格式

2. **修改 `SKILL.md`** — 扩展"反思与优化"部分：
   - 引用 `references/post-polish.md`
   - 加入审稿→打磨→格式适配的三阶段流程

3. **更新 `references/post-structures.md`** — 增强 X article 和公众号格式适配

---

## 四、预期效果

| 维度 | 融入前 | 融入后 |
|------|--------|--------|
| 初稿审稿 | 无系统化机制 | 四维评分，90+ 标准量化 |
| 去 AI 味 | 无 | 具体词汇替换表 + 口语化规则 |
| 语言精准度 | 无 | Filler 词/弱动词替换 + 具体性升级 |
| 排版规范 | 无 | 中英文空格 + 标点 + 术语一致性 |
| 节奏感 | 无 | 长短句 + 段落控制 + 过渡优化 |
| 公众号格式 | 基础 Markdown | 可选 HTML 主题样式 |
| X article 格式 | 简单 thread | 完整 thread 结构 + 字符控制 |
