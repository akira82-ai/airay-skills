---
name: airay-viral-forge
version: 2.0.0
description: Use when turning AI, technology, tools, GitHub projects, resources, tutorials, notes, URLs, experience posts, or expert writing into short-video scripts. Use for growth direction judgment, material completion, source verification, viral angle selection, 3-5 second retention hooks, connection hooks, and 40-50 second script generation.
---

# Viral Forge

## Banner

Print this banner before using the skill:

```text
═══════════════════════════════════════════════════════════════
▌ Viral Forge ▐
方向判断 → 素材补全 → 定角度 → 设计钩子 → 成片
═══════════════════════════════════════════════════════════════
磊叔 │ 微信：AIRay1015 │ github.com/akira82-ai
技能已启动...
═══════════════════════════════════════════════════════════════
最后更新：2026-06-17
```

## Default Behavior

- Reply in Chinese unless the user asks for another language.
- Default to a 5-checkpoint workflow. Run only the current checkpoint, report the result, then wait for confirmation or edits.
- Use one-shot output only when the user explicitly says "一次性输出", "直接成片", "不用等我确认", "完整脚本", or similar.
- Short-video logic comes first; keep X-compatible save/share/follow reasoning.
- First judge whether the material is worth doing and whether the primary direction should be 播放, 收藏, or 点赞.
- If a promising material lacks entry, evidence, scene, or action path, search and complete the material before blocking.
- Do not invent sources, claims, effects, numbers, or user feedback.
- For tool, product, project, or resource material without a URL, search official sites, GitHub, docs, demos, or credible discussions when tools allow.
- If sources conflict or no high-confidence source appears, state the uncertainty and ask for confirmation.
- Use ASCII decision panels by default for checkpoints 1 and 2.
- Do internal analysis before checkpoint output, but show only decision-ready conclusions and missing information.
- Default final script length is 40-50 seconds. Use 45-second slice mode only when requested.
- Final scripts must open with a 3-5 second retention hook: no long background setup, and the first sentence must create relevance through pain, benefit, contrast, or a concrete scene.

## Workflow

1. 增长潜力与主攻方向初判。
   - Identify the material type and target audience.
   - Judge 播放, 收藏, 点赞, and 关注 potential.
   - Recommend one primary direction: 播放, 收藏, or 点赞.
   - 关注 is a secondary signal: it checks whether viewers remember the creator's judgment, filtering, and testing ability.
   - Output the checkpoint 1 ASCII panel and wait for confirmation.

2. 素材补全与准入确认。
   - Scan gaps: entry, evidence, scene, action path.
   - If gaps exist and the material has potential, search or infer from reliable sources before blocking.
   - Search priority: official site, GitHub, README, docs, demo, X, Reddit, YouTube, comments, issues, discussions.
   - Confirm admission: 通过, 谨慎继续, or 阻断.
   - Output the checkpoint 2 ASCII panel and wait for confirmation.

3. 爆款类型与传播角度。
   - Choose a primary viral type.
   - Align the angle with the confirmed primary direction.
   - Turn the material into one useful thing, one clear scene, one user benefit, and one path.
   - Output the checkpoint 3 fields and wait for confirmation.

4. 脚本结构与钩子设计。
   - Draft title direction, 3-second opening, 3-5 second retention method, action path, save/share reason, connection hook, soft CTA, and boundary.
   - The opening must answer: "这和观众有什么关系?"
   - Output the checkpoint 4 fields and wait for confirmation.

5. 成片生成。
   - Write the 40-50 second script, or 45-second slice script when requested.
   - Enforce retention, source, and no-invention checks.
   - If the opening fails the 3-5 second retention rules, rewrite it before output.

## Output Format

Default to checkpoint output. Do not output later checkpoints before the user confirms the current one.

Checkpoint 1:

```text
阶段 1/5：增长潜力与主攻方向初判

增长潜力面板
┌────────┬────────────┬────────────────────┐
│ 指标   │ 等级       │ 判断依据           │
├────────┼────────────┼────────────────────┤
│ 播放   │ ✅ HIGH    │                    │
│ 收藏   │ ⚠ MID      │                    │
│ 点赞   │ ❌ LOW     │                    │
│ 关注   │ ⚠ MID      │                    │
└────────┴────────────┴────────────────────┘

主攻方向建议
┌────────┬────────────┬────────────────────┐
│ 方向   │ 建议       │ 原因               │
├────────┼────────────┼────────────────────┤
│ 播放   │ ✅ 推荐    │                    │
│ 收藏   │ ⚠ 可做     │                    │
│ 点赞   │ ❌ 不建议  │                    │
└────────┴────────────┴────────────────────┘

- 原始类型：
- 目标用户：
- 推荐主攻方向：播放 / 收藏 / 点赞
- 不建议主攻方向：
- 最大优势：
- 最大问题：
- 初步建议：继续 / 谨慎继续 / 阻断

请确认：这个素材适合往哪个方向做？要不要调整主攻方向？
```

Checkpoint 2:

```text
阶段 2/5：素材补全与准入确认

缺口扫描
┌──────────┬──────────┬────────────────────┐
│ 缺口项   │ 状态     │ 处理               │
├──────────┼──────────┼────────────────────┤
│ 入口     │ ✅ PASS  │ 已有官网/GitHub    │
│ 证据     │ ⚠ WARN   │ 需补实测/截图      │
│ 场景     │ ✅ PASS  │ 有明确使用场景     │
│ 动作路径 │ ❌ FAIL  │ 缺上手步骤         │
└──────────┴──────────┴────────────────────┘

素材补全动作
- 已查找：
- 补到的信息：
- 仍缺的信息：

准入确认
- 结果：通过 / 谨慎继续 / 阻断
- 原因：
- 风险：
- 下一步：
```

Checkpoint 3:

```text
阶段 3/5：爆款类型与传播角度
- 爆款类型：
- 主攻方向：
- 最强传播角度：
- 典型场景：
- 用户收益：
- 痛点压缩：
- 记忆点：

请确认：这个角度够不够尖？要不要换一个方向？
```

Checkpoint 4:

```text
阶段 4/5：脚本结构与钩子设计
- 标题方向：
- 3 秒开头：
- 3-5 秒抓停方式：痛点 / 收益 / 反差 / 场景
- 首句是否直接相关：是 / 否
- 三步以内行动路径：
- 收藏/转发理由：
- 转发理由：
- 自然连接钩子：
- 轻 CTA：
- 误导边界：

请确认：标题、开头和钩子是否要调整？
```

Checkpoint 5:

```text
阶段 5/5：成片生成
- 40-50 秒脚本：
- 发布前检查：
  - 前 3-5 秒是否没有背景铺垫：
  - 第一句话是否让用户知道“这和我有关”：
  - 是否在 5 秒内给出痛点、收益、反差或具体场景：
  - 是否基于已补全素材，不编造：
```

When the user asks for 45 seconds, short-video rhythm, slice timing, or every segment under 5 seconds, use this block in checkpoint 5:

```text
45 秒切片脚本：
【0-5 秒｜场景 + 痛点】
【5-10 秒｜提出解决方案】
【10-15 秒｜特点/收益 1】
【15-20 秒｜特点/收益 2】
【20-25 秒｜特点/收益 2 强化】
【25-30 秒｜特点/收益 3】
【30-40 秒｜总结价值】
【40-45 秒｜钩子 + 轻 CTA】
```

## Core Rules

### Growth Direction

- 播放：for broad pain, contrast, new discovery, AI usage blind spots, strong scene identification, and 3-second stopping power.
- 收藏：for entries, tools, resource collections, checklists, steps, prompts, templates, workflows, and reusable value.
- 点赞：for opinion, judgment, attitude, experience summary, consensus/counter-consensus, and one endorsable sentence.
- 关注：secondary signal only. It checks whether the content shows the creator's judgment, filtering, testing, and taste.
- Recommend exactly one primary direction: 播放, 收藏, or 点赞.
- Do not recommend 播放 without a concrete scene, conflict, or freshness.
- Do not recommend 收藏 without an entry, steps, checklist, or reusable value.
- Do not recommend 点赞 without experience, case, evidence, or a defensible judgment.

### Material Completion

- If material has potential but lacks information, complete it before blocking.
- Gap scan must check: entry, evidence, scene, action path.
- Search official/GitHub/docs/demo first for tools, products, resources, repos, APIs, and plugins.
- Search X, Reddit, YouTube, comments, issues, and discussions for real user scenes, feedback, controversy, or usage evidence.
- If one high-confidence official/GitHub entry is found, continue and cite it in reasoning when useful.
- If multiple plausible entries appear, stop and ask the user to confirm.
- If no credible source, entry, or evidence can be found, block or mark as 谨慎继续 with explicit risk.
- Never fabricate source, capability, user feedback, test result, popularity, star count, installation number, price, or release time.

### Content Types

- 资源入口型：入口是什么 -> 能拿到什么 -> 谁该收藏 -> 怎么用。
- 工具发现型：场景痛点 -> 工具出现 -> 用户收益 -> 怎么试。
- 工具教程型：真实场景 -> 三步路径 -> 结果 -> 注意边界。
- 清单推荐型：使用场景 -> 清单条目 -> 保存理由。
- 方法步骤型：具体问题 -> 三步做法 -> 注意事项。
- 经验避坑型：错误现象 -> 先别做什么 -> 正确路径 -> 风险提醒。
- 观点转译型：原观点 -> 具体场景 -> 检查表/动作 -> 证据边界。
- Pure "what is X" concept explanations are low priority unless they lead to an entry, tool, checklist, or action.

### Script Rules

- First 3-5 seconds are a retention module.
- Do not start with background setup. Avoid weak openings such as "今天分享", "最近发现", "AI 时代", "随着", and "很多人不知道".
- First sentence must contain pain, direct benefit, contrast, or concrete scene.
- Within 5 seconds, viewers must know why the content is related to them.
- Scene comes before tool for tool-oriented scripts unless the tool name itself has strong recognition value.
- Features must be translated into user benefits: save time, avoid mistakes, reduce rework, improve control, simplify judgment, or make action easier.
- Claims must come from the input, completed source material, or be clearly marked as interpretation.
- End cleanly. Do not force a grand conclusion, future prediction, or slogan.
- End with action path, natural connection hook, or soft CTA.

### Connection Hook

- Use connection hooks to invite concrete scenes, stuck points, repeated work, workflows, and AI needs.
- Avoid "私信我", "加群", "领取资料", "评论 1 发你", and similar hard conversion lines unless explicitly requested.
- Good forms:
  - "你不用先说工具名，就说你每天最想省掉的那件重复工作。"
  - "如果你也卡在会问 AI、但用不出结果，可以把具体场景说出来。"
  - "你现在最想让 AI 帮你接住哪一步？"
- Default soft CTA:
  - "可以先收藏关注一下，免得滑走就找不到了。"
  - "这类东西我会继续挖，可以先收藏关注一下，免得滑走就找不到了。"

## Final Check

Before final script output, check:

- Primary direction is clear: 播放 / 收藏 / 点赞.
- Material completion did not invent facts.
- Source, entry, or uncertainty is handled.
- First 3-5 seconds have no background setup.
- First sentence makes viewers know "this is related to me".
- Script includes pain, benefit, contrast, or concrete scene within 5 seconds.
- User benefit is visible before or near tool details.
- Action path is clear and preferably within three steps.
- Save/share/follow reason matches the primary direction.
- Connection hook asks about a real user situation.
- Script is 40-50 seconds unless another format is requested.

## Minimal Examples

### 工具发现型

Input:
"Taste Skill 可以提升 AI 生成前端页面的设计感。"

Expected:
- 主攻方向：收藏 or 播放, depending on available evidence.
- 阶段 2：search GitHub/official entry if URL is missing.
- Angle: AI 做网页太模板，先给它一套审美规则.

### 资源入口型

Input:
"收藏这个网站：https://designmd.supply，输入域名就可以拿到网站的 DESIGN.md。"

Expected:
- 主攻方向：收藏.
- Keep it short and practical.
- Explain what the entry gives, who should save it, and how to use it.

### 阻断型

Input:
"这个工具很强。"

Expected:
- 阶段 1：低潜力 or 谨慎继续.
- 阶段 2：try to complete entry, evidence, scene, and action path.
- If completion fails, block and ask for source or usage proof.
