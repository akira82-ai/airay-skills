---
name: airay-viral-forge
version: 4.0.0
description: Use when turning AI, technology, tools, GitHub projects, resources, tutorials, notes, URLs, experience posts, or expert writing into short-video scripts. Built on a single open-loop drive model (Zeigarnik effect) with 5-segment structure, 9-template + 3-element hooks, 6 emotional paths by content type, structural comment excitation, like-trigger design, dynamic duration, and 5-dimension diagnostic review. Outputs scripts with breath marks (｜) and speed marks (>>).
---

# Viral Forge

## Banner

Print this banner before using the skill:

```text
═══════════════════════════════════════════════════════════════
▌ Viral Forge v4.0 ▐
情绪内核 → 注意力架构 → 脚本构建 → 诊断审查
═══════════════════════════════════════════════════════════════
磊叔 │ 微信：AIRay1015 │ github.com/akira82-ai
技能已启动...
═══════════════════════════════════════════════════════════════
最后更新：2026-07-08
```

## Default Behavior

- Reply in Chinese unless the user asks for another language.
- Default to a 4-Phase workflow. Run only the current Phase, report the result, then wait for confirmation or edits.
- Use one-shot output only when the user explicitly says "一次性输出", "直接成片", "不用等我确认", "完整脚本", or similar.
- Short-video logic comes first; keep X-compatible save/share/follow reasoning.
- The core engine is a single open loop (开环): create unresolved cognitive tension at 0-5s, deliver progressively, close with surprise at 25-33s, open a new loop at 33-40s. Completion is driven by the user's need to resolve the tension, not by scattered burst points.
- Metric priority: 3秒留存（门槛）→ 完播率（互动前提，通过开环驱动自然提升）→ 评论率（核心互动）→ 点赞率（微互动）→ 收藏率（留存互动）. Do not optimize completion in isolation (avoid padding).
- If a promising material lacks entry, evidence, scene, or action path, complete it inside Phase 1 — do not block separately.
- Do not invent sources, claims, effects, numbers, or user feedback.
- For tool, product, project, or resource material without a URL, search official sites, GitHub, docs, demos, or credible discussions when tools allow.
- If sources conflict or no high-confidence source appears, state the uncertainty and ask for confirmation.
- Scripts must include breath marks (｜) and speed marks (>>) per the Script Notation rules.
- First sentence must create an open loop — no background setup.

### Decision-First Output（决策导向输出原则）

每个 Phase 的输出必须遵循"决策优先"原则：

1. 只输出用户做决策（继续/调整/阻断）必需的信息
2. 删除分析过程、中间推理、冗余解释——这些在内部完成，不展示
3. 每个 Phase 的核心输出字段保持精简，但决策相关性优先于字段数量限制
4. 面板/表格只保留"决策直接相关"的行列，删除背景信息行
5. 如果某项信息不影响用户当前决策，不输出
6. 结尾只问一个决策问题，不堆叠多个确认项

## Workflow — 4 Phase

### Phase 1：情绪内核提取（Emotional Core Extraction）

从**观众视角**确定这条视频要制造什么感觉。方向、评论机制、点赞机制全部从情绪内核推导，不再作为独立前置决策。

- 识别素材类型、目标受众、内容类型（见 Content Types 7 分类）。
- 确定情绪内核：这条视频要在观众心里制造什么感觉？（不是"讲什么"，而是"让观众感受到什么"）
- 按内容类型匹配情绪路径（见 Emotional Path 6 种）。
- 推荐主攻方向（播放/收藏/点赞/评论）作为情绪内核的**衍生判断**，而非独立决策。
- 素材补全在此阶段 AI 自主完成：扫 entry/evidence/scene/action path，缺失则搜索补全，补不全则标注风险。
- 按内容类型推荐时长（见 Duration Selection）。
- 输出 Phase 1 面板，等待确认。

### Phase 2：注意力架构（Attention Architecture）

设计贯穿全片的认知张力曲线。钩子选择、情绪路径、评论激发点、点赞触发点一步完成。

- 选择钩子模板（9 模板，见 Hook System）。
- 用三要素模型检查钩子质量（身份信号 + 利益承诺 + 信息缺口，3 秒内至少 2 个）。
- 设计开环句：开头制造什么未闭合的认知张力？闭合点兑现什么？
- 确定评论激发类型（5 种机制中选 1-2 种，见 Comment Trigger）。
- 确定点赞触发瞬间（"值得标记的瞬间"位置和内容，见 Like Trigger）。
- 确定情绪路径节点（按内容类型定制的 4 段情绪）。
- 输出 Phase 2 面板，等待确认。

### Phase 3：脚本构建（Script Construction）

将注意力架构转化为 5 段开环结构脚本。

- 按 5 段开环结构生成脚本（见 Open-Loop Structure）。
- 按内容类型动态时长（见 Duration Selection）。
- 标注气口（｜）和语速（>>）（见 Script Notation）。
- 执行认知增量检查（每句必须推进开环闭合或制造新认知张力）。
- 执行禁用词替换（见 Weak Opening → Strong Opening）。
- 输出完整脚本，等待确认后进入 Phase 4。

### Phase 4：诊断审查（Diagnostic Review）

5 维度定性诊断（非 23 项合规检查）。

- 对脚本执行 5 维度诊断（见 Diagnostic Review）。
- 未通过项直接修复后重新输出脚本。
- 全部通过则交付最终脚本。

## Output Format

默认按 Phase 输出，不提前输出后续 Phase。用户说"一次性输出"时连续走完 4 Phase。

Phase 1:

```text
阶段 1/4：情绪内核提取

- 内容类型：（7 分类之一）
- 情绪内核：（要在观众心里制造什么感觉）
- 情绪路径：（按内容类型匹配的 4 段路径）
- 主攻方向：播放 / 收藏 / 点赞 / 评论（衍生判断）
- 建议时长：（按内容类型推荐）
- 素材状态：齐全 / 已补全 / 有风险（标注）

请确认：情绪内核对不对？方向和时长要不要调？
```

Phase 2:

```text
阶段 2/4：注意力架构

- 钩子模板：（9 模板之一）+ 三要素检查（身份/利益/缺口，命中几个）
- 开环句：（开头制造的未闭合张力）
- 闭合点：（结尾兑现的答案）
- 评论激发：（5 种机制中选哪种，埋在哪段）
- 点赞触发瞬间：（"值得标记的瞬间"是什么，在闭合+超预期处吗）
- 情绪节点：（4 段情绪路径的关键节点）

请确认：开环和闭合的设计够不够有力？
```

Phase 3:

```text
阶段 3/4：脚本构建

（按 5 段开环结构输出完整脚本，含气口｜和语速>>标识）

- 字数：（按语速 3 字/秒 × 时长）
- 认知增量检查：通过 / 未通过（标注哪句不推进开环）

请确认：直接进诊断？还是要改哪里？
```

Phase 4:

```text
阶段 4/4：诊断审查

A. 开环有效性：通过 / 未通过（说明）
B. 掉人节点预测：通过 / 未通过（标注风险段）
C. 评论激发诊断：通过 / 未通过
D. 点赞触发诊断：通过 / 未通过
E. 情绪完整性：通过 / 未通过
F. 气口/语速标识：通过 / 未通过

（如有未通过项，附修复后脚本；全过则交付最终脚本）

请确认：直接用？还是要改哪里？
```

## Core Rules

### Growth Direction

- 播放：for broad pain, contrast, new discovery, AI usage blind spots, strong scene identification, and 3-second stopping power.
- 收藏：for entries, tools, resource collections, checklists, steps, prompts, templates, workflows, and reusable value.
- 点赞：for opinion, judgment, attitude, experience summary, consensus/counter-consensus, and one endorsable sentence.
- 评论：for content that creates cognitive dissonance, leaves an information gap, or triggers emotional overflow — the direction emerges when the content itself makes viewers want to speak.
- 关注：secondary signal only. It checks whether the content shows the creator's judgment, filtering, testing, and taste.
- 方向是情绪内核的衍生判断，不是独立前置决策。Phase 1 确定情绪内核后自然推出方向。
- Do not recommend 播放 without a concrete scene, conflict, or freshness.
- Do not recommend 收藏 without an entry, steps, checklist, or reusable value.
- Do not recommend 点赞 without experience, case, evidence, or a defensible judgment.

### Material Completion（嵌入 Phase 1）

- 素材有潜力但信息不足时，在 Phase 1 自主补全，不独立成步。
- Gap scan: entry, evidence, scene, action path.
- Search priority: official site, GitHub, README, docs, demo, then X, Reddit, YouTube, comments, issues, discussions.
- 找到 1 个高置信官方/GitHub 入口 → 继续并在推理中引用。
- 多个候选入口 → 停下问用户确认。
- 无可信源 → 阻断或标注"谨慎继续"+明确风险。
- Never fabricate source, capability, user feedback, test result, popularity, star count, installation number, price, or release time.

### Content Types（保留 7 分类）

- 资源入口型：入口是什么 -> 能拿到什么 -> 谁该收藏 -> 怎么用。
- 工具发现型：场景痛点 -> 工具出现 -> 用户收益 -> 怎么试。
- 工具教程型：真实场景 -> 三步路径 -> 结果 -> 注意边界。
- 清单推荐型：使用场景 -> 清单条目 -> 保存理由。
- 方法步骤型：具体问题 -> 三步做法 -> 注意事项。
- 经验避坑型：错误现象 -> 先别做什么 -> 正确路径 -> 风险提醒。
- 观点转译型：原观点 -> 具体场景 -> 检查表/动作 -> 证据边界。
- Pure "what is X" concept explanations are low priority unless they lead to an entry, tool, checklist, or action.

### Hook System — 9 模板 + 三要素模型

**选择层：9 模板**（替代 12 类钩子库 + 4 开局 + 7×3 矩阵）

| 类型 | 底层心理 | 变体 | 示例 |
|------|---------|------|------|
| **信息差型** | "你知道的比观众多" | 悬念式 | "这个功能藏了三个月，今天终于能说了。" |
| | | 反常识式 | "你以为 Prompt 越长越好？20 字就够了。" |
| | | 好奇式 | "GitHub 上有个项目，star 一夜涨了 5000。" |
| **利益差型** | "你能帮观众省时省钱" | 痛点式 | "写了 3 小时代码，AI 一句话就重构完了。" |
| | | 收益式 | "这个工作流让我每天少加班 2 小时。" |
| | | 对比式 | "左边人工 2 小时，右边 AI 30 秒，效果还更好。" |
| **认同差型** | "你说出了观众想说的话" | 场景式 | "当你需要在 10 分钟内做完一份 PPT——" |
| | | 提问式 | "你有没有想过，为什么 AI 总是答非所问？" |
| | | 故事式 | "上周朋友花 3000 块买的方案，我用 AI 10 分钟复刻了。" |

**构造层：三要素模型**（替代 4 要素公式）

```
钩子 = 身份信号 + 利益承诺 + 信息缺口

优先级（AI 内容默认）：利益承诺 ≥ 身份信号 > 信息缺口
非 AI 内容备选：身份信号 > 利益承诺 > 信息缺口
3 秒内必须包含至少 2 个要素

身份信号：不是"程序员"（太泛），而是"每天写代码超过 4 小时的人"（具体可代入）
利益承诺：不是"提升效率"（不可验证），而是"少加班 2 小时"（可验证）
信息缺口：不是"有个方法很厉害"（模糊），而是"但大多数人用错了第三步"（明确未完成信息）
```

Phase 2 中先用 9 模板选类型，再用三要素模型检查质量。

### Open-Loop Structure — 5 段开环（替代 10 切片）

**核心原理**：完播率的真正引擎不是"每 10 秒一个爆点"（防御模型），而是**在开头制造一个未闭合的认知开环，让用户为了得到闭合而留在全片**（Zeigarnik 效应）。

```
【0-5s｜开环钩子】
一句话制造未闭合的认知张力。
首句包含：身份锚定 + 痛点/利益/反常识（至少 2 个要素）。
禁止背景铺垫。
节奏：慢速、留白。

【5-10s｜张力加深】
不释放核心信息，用一个细节/判断加深悬念。
让用户从"有点好奇"升级为"真的想知道"。
段尾用微钩子牵引："但这还不是最关键的——"
节奏：中速。

【10-25s｜渐进交付】
3-4 个信息点，每个都是"逼近答案"的一步。
段间用前向张力牵引。
信息密度按内容类型调整（教程型高/观点型低）。
画面每 8-10 秒切换一次。
节奏：可用 >> 标注信息点连发段（快语速）。

【25-33s｜闭合 + 超预期】
闭合开环——给出开头承诺的答案。
紧跟超预期信息点——制造"值得标记的瞬间"（点赞触发）。
这是全片情绪峰值。
节奏：闭合句可 >>（快速揭晓），超预期句回到中速。

【33-40s｜新开环 + 行动催化】
开启新的小开环（系列粘性）。
评论激发——不是请求评论，而是内容本身制造了表达欲。
连接钩子——邀请具体场景。
节奏：中速、段尾｜。
```

**变体：结果前置结构（可选）**——当内容有强视觉冲击的 before/after 时，0-5s 直接展示结果，制造"怎么做到的"开环。适用：工具教程型/工具发现型且效果有视觉冲击力。不适用：效果不明显的内容——弱结果前置会杀死留存。

### Emotional Path — 按内容类型定制 6 种（替代固定四段）

| 内容类型 | 情绪路径 | 开环方式 |
|---------|---------|---------|
| 工具发现型 | 惊讶→验证→获得→分享 | 悬念式/好奇式 |
| 工具教程型 | 期待→跟随→完成→满足 | 收益式 |
| 经验避坑型 | 焦虑→认同→释然→行动 | 痛点式/对比式 |
| 观点转译型 | 挑衅→思考→重构→表达 | 反常识式 |
| 清单推荐型 | 期待→确认→满足→收藏 | 收益式 |
| 资源入口型 | 好奇→确认→获得→保存 | 悬念式/好奇式 |

Phase 1 确定情绪内核后自动匹配路径。焦虑情绪每条脚本最多用 1 次。

### Comment Trigger — 结构式激发（替代五层外挂）

**核心原理**：高评论率视频的评论区是被内容**激发**的，不是被**请求**的。驱动用户克服打字摩擦力的只有 5 种心理状态：

| 心理状态 | 触发条件 | 评论类型 | 设计方法 |
|---------|---------|---------|---------|
| **认知失调** | 内容与既有认知冲突 | 反驳/质疑/补充 | 在内容中埋设反常识判断 |
| **社会信号** | 想展示自己的知识/经验 | 炫耀/纠正/补充 | 留一个可补充的信息缺口 |
| **情感溢出** | 内容触发强烈情绪 | 情绪宣泄 | 在闭合+超预期处制造情绪峰值 |
| **信息缺口** | 想进一步了解 | 提问/求教程 | 新开环留下未答问题 |
| **社群归属** | 想加入讨论/表达认同 | 认同/附和/分享经历 | 场景代入引发"我也是" |

**脚本层职责**（skill 只做这些）：
- Phase 2 确定评论激发类型（1-2 种）。
- Phase 3 在对应段埋设激发点。
- 在新开环处留下"忍不住想说两句"的钩子。
- 禁止"请求式"引导（"你们怎么看？""评论区告诉我"），改用激发式设计。

### Like Trigger — 点赞触发设计（专项新增）

**核心原理**：点赞是最低摩擦的互动行为（双击屏幕），触发条件比评论低得多。v3.0.0 对点赞率零设计是最大结构性缺口。

**点赞触发瞬间通常出现在**：
- 超预期价值点（"这个技巧我从来不知道"）→ 在闭合+超预期处设计
- 观点代言句（"对对对就是这样"）→ 在 Phase 1 确定情绪内核时确定
- 完满感结尾（"从头到尾都值了"）→ 在新开环+催化处设计

Phase 2 确定"值得标记的瞬间"的位置和内容，Phase 4 诊断检查"是否有至少一个点赞触发瞬间"。

### Duration Selection — 按内容类型动态（替代 40s 固定）

| 内容类型 | 建议时长 | 原因 |
|---------|---------|------|
| 资源入口型 | 15-25s | 信息简单，快速交付 |
| 观点转译型 | 20-30s | 注意力衰减快，宜短 |
| 工具发现型 | 25-35s | 需要展示效果但不需要完整教程 |
| 经验避坑型 | 30-40s | 需要叙事铺垫 |
| 工具教程型 | 35-45s | 需要完整步骤讲解 |
| 清单推荐型 | 30-40s | 逐个展示需要时间 |

40 秒保留为"中等时长"默认值。Phase 1 确定情绪内核后自动推荐时长。

### Information Density — 认知增量模型（替代 1 点/秒固定）

- **字数**：按语速 3 字/秒计算。40s≈120 字，30s≈90 字，20s≈60 字。
- **认知增量**：每句必须推进开环闭合或制造新的认知张力（定性标准，非定量）。
- **密度按内容类型调整**：
  - 教程型/清单型：高密度（1.2-1.5 点/秒）
  - 观点型：低密度（0.5-0.8 点/秒，需要思考空间）
  - 避坑型/入口型：中密度（0.8-1 点/秒）
- **删减优先级**：先删不推进开环的信息 → 再删重复信息 → 再删描述性文字 → 保留推进开环+制造认知失调+超预期信息。
- **数字优先**：能用数字不用形容词（"提升 3 倍"优于"大幅提升"）。
- **画面文案互补**：画面能展示的不用文案重复。
- **语气词审计**：每 30 秒"嗯/啊/其实/然后/就是说"不超过 3 个。
- **关键词前置**：每句核心信息放在前半句。

### Script Notation — 气口（｜）与语速（>>）标识

脚本输出必须标注两类朗读标识，供 TTS 生成和真人录制参考节奏。

**1. 换气气口「｜」**

- 每个完整语义单元之间标注一个 ｜。
- 5 段开环结构的每段段尾必须有 ｜（段间停顿）。
- 一个句子内不超过 2 个 ｜（避免支离破碎）。
- 示例："写 3 小时代码｜AI 一句话重构完｜这不是夸张"

**2. 快语速标记「>>」**

- 仅标注需要"快读+高密度"的句子（通常是渐进交付段的信息点连发）。
- 每条脚本最多 2 句标 >>（过多则失去强调作用）。
- >> 标在句首，覆盖整句。
- 示例：">>第一步输入需求｜第二步选模板｜第三步一键生成"
- 适用场景：渐进交付段（10-25s）的信息点连发 / 闭合段的答案快速揭晓。
- 不适用场景：开环钩子段（0-5s，要稳要慢要留悬念）/ 情绪收束段（要稳）。

**3. 与 5 段开环结构的配合**

| 段落 | 语速基调 | 气口 ｜ | 语速 >> |
|------|---------|--------|--------|
| 0-5s 开环钩子 | 慢速、留白 | 每句后有 | 不用 |
| 5-10s 张力加深 | 中速 | 段尾有 | 不用 |
| 10-25s 渐进交付 | 中快 | 段间有 | 可用（信息点连发） |
| 25-33s 闭合+超预期 | 闭合句可快、超预期句回中 | 段尾有 | 闭合句可用 |
| 33-40s 新开环+催化 | 中速 | 连接钩子前有 | 不用 |

### AI Content Strategy — 认知软化 + 准入信号

1. **准入信号设计（新增）**：
   - 前 3 秒必须传达"这不需要技术背景也能用"的信号。
   - 降低准入焦虑（不是"听不懂"的问题，是"不敢看"的问题）。

2. **认知门槛软化**：
   - 前 3 秒不出现超过 1 个技术名词，多个概念先用通俗场景替代。
   - 技术名词紧跟"等于什么"的翻译："RAG——就是让 AI 先查资料再回答"。
   - 先给"能干什么"再给"怎么做到的"。

3. **内容软化（防止"太干太硬"）**：
   - 每个功能点后跟生活化比喻："就像给 AI 配了一个私人图书管理员"。
   - 每个技术步骤后跟效果体感："这一步做完，AI 的回答突然变靠谱了"。

4. **受众分层钩子**：
   - 小白用户：结果展示型钩子（看效果→教方法）。
   - 进阶用户：效率对比型钩子（旧方法 vs 新方法）。
   - 开发者：技术亮点型钩子（API/star/性能数据）。

5. **时效性标注**：
   - 涉及版本号/价格/功能的声明标注信息日期。
   - 信息可能过时时加"截至我查的时候"限定语。

6. **实测优先**：
   - 强烈建议附带实测截图/录屏作为证据。
   - 无实测时明确标注"基于公开信息整理"。

### Weak Opening → Strong Opening（禁用词替换库 · 扩展版）

| 禁用开头 | 替换方案 |
|---------|---------|
| "今天分享…" | [痛点] "你还在用 XX 方式？它正在浪费你的时间。" |
| "最近发现…" | [数据冲击] "90% 的人不知道，这个工具能…" |
| "AI时代…" | [反常识] "AI 越强，这个技能反而越值钱。" |
| "随着…" | [场景] "想象一下：周一早上，你的周报已经写完了。" |
| "很多人不知道" | [悬念] "这个功能藏了三个月，今天终于敢说了。" |
| "这个工具太强了" | [利益+缺口] "这个工具能砍掉你一半重复工作｜但第三步用错了更慢" |
| "AI 又能做 XXX 了" | [场景+缺口] "AI 现在能直接生成完整项目｜但 90% 的人第一步就错了" |
| "给大家推荐" | [身份+利益] "每天写代码的人｜这个工作流让你少加班 2 小时" |

### Connection Hook（保留）

- 用连接钩子邀请具体场景、卡点、重复工作、工作流、AI 需求。
- 避免"私信我"、"加群"、"领取资料"、"评论 1 发你"等硬转化话术，除非用户明确要求。
- 好的形式：
  - "你不用先说工具名，就说你每天最想省掉的那件重复工作。"
  - "如果你也卡在会问 AI、但用不出结果，可以把具体场景说出来。"
  - "你现在最想让 AI 帮你接住哪一步？"
- 默认软 CTA：
  - "可以先收藏关注一下，免得滑走就找不到了。"
  - "这类东西我会继续挖，可以先收藏关注一下，免得滑走就找不到了。"

### Platform Adaptation — 3 条原则（替代 7×3 矩阵）

- **抖音**：身份信号要最强（纯算法分发，前 3 秒决定生死）。
- **视频号**：标题即钩子（社交场景下标题是转发门面）。
- **小红书**：封面+标题是第一钩子（搜索场景先看到封面）。

未指定平台时默认抖音规则。

## Diagnostic Review — 5 维度诊断（替代 23 项合规检查）

Phase 4 对脚本执行以下诊断。未通过项直接修复后重新输出。

**A. 开环有效性**
- 开环句是否制造了"我想知道答案"的冲动？
- 交付路径是否在逐步逼近答案而非平行罗列？
- 闭合点是否兑现了开头承诺？
- 超预期点是否制造了"值得标记的瞬间"？

**B. 掉人节点预测**
- 5-10s（张力加深区）是否会出现"你到底想说什么"的焦躁？
- 10-25s（渐进交付区）是否有超过 8 秒的无增量信息段？
- 25-33s（闭合区）闭合是否过于平淡？

**C. 评论激发诊断**
- 内容中是否有至少一个"让人忍不住想说两句"的点？
- 这个点是认知失调/信息缺口/情感溢出中的哪一种？
- 结尾是激发了表达欲还是 merely 请求评论？

**D. 点赞触发诊断**
- 脚本中是否有至少一个"值得标记的瞬间"？
- 这个瞬间在闭合+超预期处吗？

**E. 情绪完整性**
- 情绪曲线是否连贯（按内容类型定制的路径）？
- 是否有超过 10 秒的情绪平坦区？
- 结尾情绪是否高于中段基线？

**F. 气口/语速标识检查（新增）**
- 气口分布是否合理（每段段尾有 ｜，无过度支离）？
- 语速标记是否克制（全片 ≤2 句 >>，且用在渐进交付或闭合段）？
- 开环钩子段是否误用了 >>（应慢速留白）？

## Appendix

### A. Post-Publish Operations（运营层参考，非脚本生成职责）

评论率 Layer 3-5 移入此附录，供发布后运营参考：

1. **置顶评论·三阶段**：冷启动期置顶悬念式提问；流量爆发期置顶转化引导；长尾期置顶关联内容。
2. **评论区运营**：黄金 30 分钟集中回复前 30 条；有策略保留与核心卖点相关的争议评论（可+22% 播放量）；禁止"谢谢支持"敷衍话术。
3. **数据反馈闭环**：每周导出评论关键词云图；识别高频问题→下期脚本植入针对性钩子；掉人段→该段爆点失败→下期重新设计。

### B. Result-First Structure（可选变体）

当内容有强视觉冲击的 before/after 时，可选用结果前置结构作为开环模型的变体：
- 0-5s：直接展示最终效果/结果（制造"怎么做到的"开环）。
- 5-8s：制造好奇("怎么做到的？三步")。
- 8-32s：倒叙步骤讲解。
- 32-40s：总结+新开环+连接钩子。

适用条件：工具教程型/工具发现型，且工具效果有视觉冲击力。不适用：效果不明显的内容。

### C. Post-Publish Review（可选 Phase 5）

发布后 48 小时可选复盘：
- 5 秒完播率 < 30% → 重写开头钩子（同素材重做）。
- 整体完播率 → 识别掉人段 → 该段开环失效 → 下期重新设计。
- 评论关键词 → 提取高频问题 → 下期植入针对性开环。
- 对比历史脚本 → 追踪哪种钩子模板和开环模式效果最好。

## Minimal Examples

### 工具发现型

Input:
"Taste Skill 可以提升 AI 生成前端页面的设计感。"

Expected:
- 内容类型：工具发现型
- 情绪内核：惊讶+获得（"AI 生成的页面居然能这么好看"）
- 情绪路径：惊讶→验证→获得→分享
- 主攻方向：收藏 or 播放（衍生判断）
- Phase 1：search GitHub/official entry if URL is missing.
- 开环："AI 做网页太模板｜给它一套审美规则｜效果完全不一样｜但第 4 步最容易漏"

### 资源入口型

Input:
"收藏这个网站：https://designmd.supply，输入域名就可以拿到网站的 DESIGN.md。"

Expected:
- 内容类型：资源入口型
- 情绪内核：好奇+获得（"还能这样拿到设计规范"）
- 情绪路径：好奇→确认→获得→保存
- 主攻方向：收藏（衍生判断）
- 建议时长：15-25s
- 开环："一个网站的设计规范｜输入域名就能拿到｜但大多数人只看了第一屏"

### 阻断型

Input:
"这个工具很强。"

Expected:
- Phase 1：低潜力 or 谨慎继续.
- 素材补全：try to complete entry, evidence, scene, and action path.
- If completion fails, block and ask for source or usage proof.

### 完整脚本示例（含气口/语速标识）

Input:
"CodeWhisperer 的重构功能可以自动拆 PR。"

Expected Phase 3 输出:

```text
【0-5s｜开环钩子】
你每天写代码超过 4 小时｜这个工具能帮你砍掉一半 review 时间｜但大多数人用错了第三步｜

【5-10s｜张力加深】
它不是又一个 Copilot｜它做的事情比你想的更深｜

【10-25s｜渐进交付】
>>第一步装插件｜第二步选重构范围｜第三步一键提交｜
关键是第三步｜它会自动拆成 5 个 PR｜每个都能单独 review｜

【25-33s｜闭合+超预期】
所以你省掉的不是打字时间｜是整个 review 循环｜而且它支持 17 种语言｜

【33-40s｜新开环+催化】
但有个隐藏用法我还没说｜用它做代码迁移比重构快 10 倍｜你手头有要迁移的老项目吗｜
```

- 字数：约 115 字（40s × 3 字/秒 ≈ 120 字）
- 气口：每段段尾有 ｜，句内不超过 2 个
- 语速 >>：1 句（渐进交付段信息点连发）
- 评论激发：信息缺口（"隐藏用法"新开环）+ 社群归属（"你手头有要迁移的老项目吗"场景代入）
- 点赞触发：超预期（"支持 17 种语言"+"省掉整个 review 循环"）
