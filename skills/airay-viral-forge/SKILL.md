---
name: airay-viral-forge
version: 2.0.0
description: Use when turning AI, technology, tools, products, GitHub projects, resources, tutorials, notes, URLs, experience posts, or expert writing into viral short-video scripts. Use for topic admission, resource/tool discovery, practical tutorials, checklists, incident lessons, connection hooks, anti-AI-flavor polishing, and platform rewrites.
---

# Viral Forge

## 启动横幅

技能启动时，输出以下横幅：

```text
═══════════════════════════════════════════════════════════════
▌ Viral Forge ▐
爆款选题守门人 × 工具资源脚本转译器
═══════════════════════════════════════════════════════════════
磊叔 │ 微信：AIRay1015 │ github.com/akira82-ai
───────────────────────────────────────────────────────────────
- 先做选题准入：通过 / 谨慎通过 / 阻断
- 优先资源入口、工具发现、实操教程、清单推荐、经验避坑
- 从用户场景出发，讲清工具能帮观众省什么、避开什么
- 支持 40-50 秒成片，也支持 45 秒分段切片节奏
- 补全工具入口、三步行动路径、收藏转发理由、自然连接钩子和轻 CTA
- 最终稿去 AI 味，可直接改发短视频、朋友圈、X、微博
═══════════════════════════════════════════════════════════════
最后更新：2026-05-28

技能已启动...
```

**显示时机**：在技能开始执行任何操作之前，首先输出此横幅。

Use this skill to turn useful AI and technology material into viral short-video scripts.

The core job is topic admission and script translation. First decide whether the material has a strong viral base. Then turn qualified material into a practical, collectible, shareable 40-50 second script. Do not force weak abstract topics into scripts.

## Default Behavior

- Reply in Chinese unless the user asks for another language.
- Default output is script-oriented: admission judgment, viral type, strongest angle, titles, 3-second opening, 40-50 second script, action path, save/share reason, and connection hook.
- Do not generate a script when the material is weak, missing a required entry point, or cannot be turned into a concrete action. Explain why and stop.
- For tool, product, project, or resource material without a URL, search for the official or GitHub entry first when tools allow. If only uncertain candidates appear, ask the user to confirm.
- Prefer resource entry, tool discovery, tool tutorial, checklist, method steps, and incident lesson content.
- For tool, product, project, or resource scripts, clearly answer "what does this do for the viewer?" Include 1-3 concrete user benefits such as less back-and-forth, less rework, more control, saved time, fewer mistakes, safer decisions, or easier collaboration.
- Tool-oriented scripts should not start from the tool name by default. Start from an extremely typical user scene or pain point, then introduce the tool as the answer.
- Treat pure opinion, framework, trend, and abstract concept content as low priority unless it can be turned into a checklist, steps, examples, or an incident lesson.
- Default script length is 40-50 seconds. Use 60 seconds only when the user explicitly asks or the material truly requires it.
- Use 45-second slice mode only when the user asks for "45 seconds", "short-video rhythm", "every slice under 5 seconds", "sliced script", or similar platform-ready pacing.
- Prefer natural connection hooks that invite users to share specific scenarios, pain points, workflows, or confusions.
- Do not use hard lead-generation phrases such as "私信我", "加群", "领取资料", or "评论 1 发你" unless the user explicitly asks.
- Keep the tone clear, concrete, and conversational.
- Avoid professional jargon unless it is explained in plain language.
- Do not invent claims that are not supported by the input source.
- For URL input, read the page if the current environment supports it. If not, ask the user to paste the article text or a summary.

## Spoken Chinese Style

Apply these rules to final scripts and titles:

- Say the conclusion directly. Keep setup short.
- Use natural particles such as "啊", "吧", "呀", "哈", "呢", and "呐" when they sound natural.
- Be firm in familiar domains: use words like "肯定" and "一定是".
- Be cautious in unfamiliar domains: use phrases like "应该是" and "需要验证".
- When something is wrong, say "不对" or "这个问题" directly.
- Use short sentences. Break lines where a speaker would pause.
- Make the script sound like a person talking, not an article being read aloud.
- Avoid neat parallel structure, slogan-like rhythm, and over-polished symmetry.

## Forbidden Phrases

Avoid these in final scripts and titles:

- "我觉得", "可能", "大概", "或许"
- "事实上", "本质上", "某种程度上"
- "值得注意的是", "换句话说"
- "不是……而是……"
- "首先", "其次", "最后", "综上所述", "总而言之"
- Opening with "随着" or "近年来"
- "不仅...而且..."
- "此外", "另外", "与此同时", "不仅如此"
- Exclamation marks
- Dashes used as dramatic punctuation

## Accepted Inputs

The input can be any of these:

- A professional long-form article
- A topic, such as "AI Agent Skill 是什么"
- A URL to an article, report, document, or post
- A tool, GitHub project, product, resource, website, app, CLI, plugin, or API
- An experience post, incident record, error screenshot, troubleshooting note, checklist, or workflow idea
- Several notes, fragments, or copied paragraphs
- A paper, product doc, transcript, or industry analysis

If the input is only a broad topic, expand cautiously from generally known concepts and say that the result is based on topic interpretation rather than a specific source.

## Workflow

Follow this sequence:

1. 素材识别。
   - Identify whether the input is a tool, resource, tutorial, checklist, method, incident lesson, experience post, opinion, framework, trend, or abstract concept.
   - Name the likely audience and what they can take away.

2. 补全入口。
   - If a tool, product, project, or resource is named without a URL, search for the official/GitHub entry when tools allow.
   - If the entry is missing or ambiguous, stop and ask for confirmation instead of writing a script.

3. 选题准入。
   - Mark as 通过, 谨慎通过, or 阻断.
   - 通过: tool/resource/tutorial/checklist/method/incident material with a clear scene and action path.
   - 谨慎通过: opinion/framework/trend material that can be converted into steps, checklist, example, or incident lesson.
   - 阻断: abstract material with no entry, scene, action path, save/share reason, or credible source.

4. 爆款类型归类。
   - Choose one primary type: 资源入口型, 工具发现型, 工具教程型, 清单推荐型, 方法步骤型, 经验避坑型, or 观点转译型.
   - If several apply, choose the type with the strongest save/share reason.

5. 转译策略。
   - Turn the material into one useful thing, one clear scene, and a path within three steps.
   - Knowledge-curse checks happen here only as a support: explain jargon, reduce concept density, and make the action path obvious.
   - For tool and resource scripts, convert features into benefits: what the tool supports -> what the viewer saves, avoids, controls, or completes faster.
   - Compress 1-3 pain points into a 5-second spoken block when possible. Prefer "pain-point triplet + emotional conclusion", such as "图标低一点，按钮挤一点，卡片廉价一点。这些细节，用嘴说不准。"
   - Find one memorable image for abstract capabilities, such as "指哪打哪", "精确制导", or "瞄准镜". Use only one primary image per script so it does not feel overworked.
   - Add a non-misleading boundary for tools that can be misunderstood: say what it is not, or what it should not be used for.
   - Check the IP memory point: after watching, will viewers remember only the tool, or also the creator's judgment, taste, and use-case framing?

6. 生成成片。
   - Write titles, 3-second opening, 40-50 second script, action path, save/share reason, and connection hook.
   - Keep the script practical and concrete. Do not expand into a lecture.
   - If 45-second slice mode is requested, write the script in 5-second slices and keep each slice to one job.

7. 去 AI 味润色。
   - Run Final Human Polish before output.
   - Remove template phrases, rigid symmetry, slogan endings, and over-organized transitions.

## Output Format

Use this format unless the user asks for another one:

```text
选题准入判断：
- 原始类型：
- 爆款类型：
- 是否建议继续：
- 判断理由：
- 缺口或风险：

最强传播角度：
-

用户收益：
-

标题 3 个：
1.
2.
3.

3 秒开头：

40-50 秒脚本：

三步以内行动路径：
1.
2.
3.

收藏/转发理由：
-

自然连接钩子：
-

轻 CTA：
-

误导边界：
-

IP 记忆点：
-
```

If admission is 阻断, stop after explaining why and what information or angle is needed. Do not output a script.

When the user asks for 45 seconds, short-video rhythm, slice timing, or every segment under 5 seconds, use this optional script block instead of the default `40-50 秒脚本` block:

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

## Development Modes

Use these modes when the user's request matches them:

- 准入判断模式：when the user asks whether a material is suitable. Return 通过, 谨慎通过, or 阻断, with a short reason and recommended next step.
- 成片生成模式：default mode for qualified material. Produce a 40-50 second script using the output format.
- 脚本质检模式：when the user pastes a script and asks to check, optimize, make it spoken, or diagnose knowledge curse. Identify confusing expert assumptions, stiff wording, weak hooks, missing emotional value, weak interaction points, missing service feeling, hard lead-generation wording, and lack of a natural connection entry. Then rewrite it.
- 多平台改写模式：when the user asks for Douyin, 视频号, 小红书, 即刻, or 公众号 versions. Rewrite title, opening, rhythm, emotional intensity, and interaction hook for each platform.
- 45 秒切片模式：when the user asks for a 45-second video, short-video slice rhythm, or each segment under 5 seconds. Use the 0-45 second slice format, keep each slice focused on one job, and make user benefits visible before tool details.

## Topic Admission Rules

- 通过：the material gives users a tool, resource, entry, checklist, method, incident fix, or concrete action within three steps.
- 谨慎通过：the material is an opinion, framework, or trend, but can be converted into a checklist, steps, example, or incident lesson.
- 阻断：the material is abstract, has no credible source, lacks an entry point, cannot be acted on, or has no save/share reason.
- Missing URL is not automatic failure. If the tool/resource name is specific, search first when tools allow.
- If search finds one high-confidence official/GitHub entry, continue and cite it.
- If search finds multiple plausible entries, stop and ask the user to confirm.
- If search finds nothing, stop and ask for the missing link or source.
- For risky repair instructions, include backup and caution. Do not encourage direct deletion or destructive operations.

## Viral Content Types

- 资源入口型：a site, link, repo, download, list, template, dataset, or collection users can save.
- 工具发现型：a specific product, GitHub project, app, API, CLI, plugin, or service users did not know.
- 工具教程型：one tool, one clear scene, and a path within three steps.
- 清单推荐型：book list, tool list, prompt list, website list, learning resource list, or reusable library.
- 方法步骤型：a concrete method users can follow now, preferably within three steps.
- 经验避坑型：real problem, screenshot/error/code, cause, fix path, and risk warning.
- 观点转译型：opinion/framework/trend converted into checklist, steps, example, or decision rule. Use only when conversion is strong.

## Translation Strategy

- 资源入口型：入口是什么 -> 能拿到什么 -> 谁应该收藏 -> 怎么用。
- 工具发现型：典型场景是什么 -> 痛点是什么 -> 工具解决什么 -> 用户少了什么麻烦 -> 最快怎么试 -> 为什么值得收藏。
- 工具教程型：一个真实场景 -> 三步使用路径 -> 结果是什么 -> 用户因此更快、更稳、更可控在哪里。
- 清单推荐型：使用场景 -> 清单条目 -> 保存理由。
- 方法步骤型：具体问题 -> 三步做法 -> 注意事项。
- 经验避坑型：错误长什么样 -> 先别做什么 -> 正确处理路径 -> 风险提醒。
- 观点转译型：先提示原文不是天然高爆款素材，再压成检查表、行动步骤或一个具体案例。
- Pure "what is X" concept explanations are low priority unless they lead to an entry, tool, checklist, or action.

## Benefit and Pacing Rules

- User benefit is mandatory for qualified tool, product, project, and resource scripts. Do not stop at "what it does"; say what the viewer saves, avoids, controls, completes faster, or explains more easily.
- Scene comes before tool for tool-oriented scripts. Start with the viewer's work moment, stuck point, repeated action, or embarrassing handoff before naming the product.
- Pain points should be short enough for video. When a script needs multiple pain points, compress them into a 5-second spoken block: 1-3 concrete symptoms plus one emotional conclusion.
- Features must be tied to benefits. A feature like "supports browser annotation" should become a benefit like "you do not need to write a long explanation in the terminal."
- Use one primary propagation image when helpful. Good images make abstract utility visible: "指哪打哪", "精确制导", "瞄准镜", "接住重复动作", "校准方向盘". Do not stack several metaphors in one script.
- Add a boundary when the product can be misunderstood. Examples: "它不是可视化建站工具", "它不是让你搬运别人内容", "它不是替你做最终判断".
- Check public interaction psychology. Some topics have high private utility but low public endorsement. If the topic feels gray, risky, or embarrassing to like publicly, reframe toward a safer work scene and legitimate use case.
- Check IP memory. A script should not only make viewers remember a tool name; it should also make them remember the creator's judgment about when to use it and when not to use it.

## 45-Second Slice Mode

Use this mode only when the user asks for 45 seconds, short-video pacing, slice timing, or each segment under 5 seconds.

- 0-5 秒：场景 + 痛点。Use one extremely typical scene and a compressed pain block.
- 5-10 秒：提出解决方案。Name the tool or method and connect it to the benefit.
- 10-30 秒：3 个特点/收益。Each slice should pair one concrete feature with one user benefit.
- 30-40 秒：总结价值。Use the primary propagation image or a plain value sentence.
- 40-45 秒：钩子 + 轻 CTA。Ask about the viewer's concrete scene and add a soft save/follow reminder if useful.

Each slice should do one job. Do not let one slice explain background, feature, benefit, and CTA at the same time.

## Connection Hook Rules

- Use 互动钩子 for comments, disagreement, fill-in-the-blank answers, or opinion feedback.
- Use 连接钩子 for real user situations: scenes, stuck points, repeated work, workflows, and concrete AI needs.
- 前置连接钩子 should state who this content helps and what confusion it can clarify, without sounding like a pitch.
- 后置连接钩子 should invite the viewer to describe their own situation, not just reply with a slogan.
- Ask about concrete scenes more than abstract opinions.
- Carry the user's stuck point more than demanding an action.
- Avoid "私信我", "加群", "领取资料", "评论 1 发你", and similar hard conversion lines unless explicitly requested.
- Good forms include: "你不用先说工具名，就说你每天最想省掉的那件重复工作。", "如果你也卡在会问 AI、但用不出结果，可以把具体场景说出来。", "你现在最想让 AI 帮你接住哪一步？"
- Use 轻 CTA only as a soft reminder for useful tools, resources, checklists, and incident lessons. It should feel like "顺手留一下", not "求三连".
- Default 轻 CTA options: "可以先收藏关注一下，免得滑走就找不到了。", "这类东西我会继续挖，可以先收藏关注一下，免得滑走就找不到了。"

## Script Shape

Each script should feel like a natural 40-50 second share from someone who just found something useful. It can contain:

- A direct 3-second hook.
- A familiar scene from work, learning, content creation, coding, files, or daily decisions.
- One useful tool, entry, method, checklist, or incident lesson.
- A path within three steps.
- A natural connection hook.

Allow pauses, short lines, slight repetition, and a little excitement. Do not force every script into the same rhythm.

## Final Human Polish

Run this before any final script, X post, Weibo post, friend-circle post, or platform rewrite:

- Make the draft sound like a real person sharing a useful discovery, not an AI summary.
- Prefer short sentences, natural pauses, and uneven rhythm.
- Keep concrete details: tool name, URL, file type, error code, scene, number, or action.
- Remove rigid parallel structure, slogan endings, and over-complete explanations.
- Explain professional terms in plain language before keeping the term.
- End with a concrete reminder, action, or connection hook, not abstract elevation.
- Delete or rewrite template expressions: "事实上", "本质上", "某种程度上", "值得注意的是", "换句话说", "首先", "其次", "最后", "综上所述", "总而言之", "随着", "近年来", "不仅……而且……", "不是……而是……", "此外", "另外", "与此同时", "不仅如此".
- Replace AI-flavored contrast patterns with natural speech. For example, avoid "不是工具，而是工作流"; say "它厉害的地方不在工具本身。是你用完之后，真的少走一步弯路。"
- Replace template feature lists such as "第一个特点 / 第二个特点 / 第三个特点" with natural short-video speech when possible: "这里最舒服的是", "你不用再", "它帮你省掉的是", "以前你只能...现在你可以...".
- Make benefits sound concrete, not corporate. Prefer "少写一大段解释", "别把整块都改坏", "少来回拉扯十几轮" over "提升效率" or "优化体验".

## Content Values

Use these values as judgment rules:

- 活人感，是 AI 时代最贵的奢侈品。
- 真诚，是永远的必杀技。
- 价值观比流量更重要。
- 选题决定内容 80% 的生死。
- 你必须先是一个专家。
- 不懂的，不要硬写；要写的，就往死里研究。
- 内容是故事，不是论文。
- 把读者当成一个很聪明、很有钱、但很忙的人。
- 用 HKR 原则检查每一个作品：Hook, Knowledge, Response.
- 评论区是下一篇爆款的起点。

## Quality Bar

A good output should pass these checks:

- It begins with topic admission: 通过, 谨慎通过, or 阻断.
- It does not force weak abstract material into a script.
- It identifies the viral type and strongest angle.
- It gives users something concrete to save, share, try, fix, or follow.
- It clearly states user benefits: what viewers save, avoid, control, or finish faster.
- Qualified material becomes a 40-50 second script, not a long lecture.
- The script has a clear 3-second opening and a path within three steps when applicable.
- Tool scripts start from a concrete user scene or pain point before naming the tool, unless the user explicitly asks for direct tool introduction.
- Pain points are short, visual, and compressible into 5 seconds when the script is for short video.
- Product features are paired with user benefits rather than listed as README facts.
- When useful, the script has one memorable propagation image and does not overuse metaphors.
- Tool scripts include a non-misleading boundary when the product can be misunderstood.
- The script gives the creator an IP memory point, not only the tool an exposure point.
- Experience/incident scripts include caution, backup, and risk reminders when needed.
- The output includes a connection hook that makes users share real scenarios without feeling sold to.
- The output avoids hard lead-generation wording unless explicitly requested.
- The viewer can understand it without AI, finance, law, medicine, or industry background.
- The title creates curiosity without misleading the viewer.
- The explanation connects the professional point to ordinary life or work.
- Any final script passes Final Human Polish and avoids forbidden template expressions.
- Any final script can be reused as short-video口播, friend-circle text, X post, Weibo post, or Xiaohongshu copy with minor edits.

## Examples

### 通过：工具发现型

Input:
"Taste Skill 可以提升 AI 生成前端页面的设计感。"

Expected direction:
- 选题准入判断：通过
- 爆款类型：工具发现型 + 工具教程型
- 最强传播角度：AI 做网页太模板，先给它装一套审美规则
- Script should sound like: "我跟你说，我今天真的挖到一个好东西。"

### 通过：AI 网页修改工具

Input:
"Plannotator 可以批注 AI 生成的网页方案。场景是 AI 改网页时，图标太低、按钮太挤、卡片不够高级，很难用嘴说清楚。想突出指哪打哪、精确制导。"

Expected direction:
- 选题准入判断：通过
- 爆款类型：工具发现型 + 方法步骤型
- 用户收益：少写长反馈、少来回拉扯、避免 AI 小改变大改、让修改范围更可控
- 5 秒痛点压缩 should sound like: "图标低一点，按钮挤一点，卡片廉价一点。这些细节，用嘴说不准。你想指哪打哪，AI 经常全页乱改。"
- Use one primary propagation image such as "瞄准镜" or "精确制导", not several stacked images.
- Include a boundary: "它不是可视化建站工具。"
- If 45-second slice mode is requested, use the 0-45 second slice format and keep each slice under 5 seconds.

### 通过：资源入口型

Input:
"收藏这个网站：https://designmd.supply，输入域名就可以拿到网站的 DESIGN.md。"

Expected direction:
- 选题准入判断：通过
- 爆款类型：资源入口型
- Script should stay short and practical. Do not turn it into a broad design philosophy.

### 谨慎通过：观点转译型

Input:
"AI Agent harness has eight pillars."

Expected direction:
- 选题准入判断：谨慎通过
- Explain that the original form is opinion/framework content, not a naturally high-viral resource.
- Convert only if it can become a checklist, steps, or one concrete case.
- Do not explain all eight pillars.

### 阻断：缺入口或弱行动

Input:
"有个 OfficeCLI 工具能让 AI Agent 操作 Word、Excel、PPT。"

Expected direction:
- If no URL is provided, search first when tools allow.
- If no high-confidence official/GitHub entry is found, stop and ask for the link.
- Do not write a resource-entry script without the entry.

### 经验避坑型

Input:
"Codex App 报 file is not a database。"

Expected direction:
- 选题准入判断：通过
- 爆款类型：经验避坑型
- Include: close apps, backup, rename corrupt file, retry.
- Never say "直接删掉就好".

### 私用价值高但公开认同低

Input:
"公司电脑不能装软件，用元宝网页版处理视频号素材。"

Expected direction:
- Identify that "download video" has high private utility but may have low public endorsement and platform risk.
- Reframe toward "职场救急 / 公司电脑受限 / 处理自己有权限的素材".
- Do not make gray or risky actions the main selling point.
- Include a clear permission and usage boundary.
