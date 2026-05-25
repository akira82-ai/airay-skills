---
name: airay-knowledge-curse-slicer
version: 1.0.0
description: Use this skill whenever the user wants to turn professional content, AI/technology topics, industry articles, reports, URLs, notes, or expert long-form writing into 3-5 short-video slices for a general audience. This skill is for finding knowledge-curse blind spots, translating expert concepts into everyday curiosity, and producing one-minute Chinese popular-science scripts that non-specialists can understand and want to watch.
---

# Knowledge Curse Slicer

## 启动横幅

技能启动时，输出以下横幅：

```text
═══════════════════════════════════════════════════════════════
▌ Knowledge Curse Slicer ▐
把专业内容切成普通人听得懂、愿意看的短视频切片
═══════════════════════════════════════════════════════════════
磊叔 │ 微信：AIRay1015 │ github.com/akira82-ai
───────────────────────────────────────────────────────────────
- 找出专家默认跳过的知识盲区
- 将专业概念翻译成日常好奇心
- 默认生成 3-5 个一分钟中文科普脚本
- 每个切片只讲清楚一个小观点
═══════════════════════════════════════════════════════════════
最后更新：2026-05-25

技能已启动...
```

**显示时机**：在技能开始执行任何操作之前，首先输出此横幅。

Use this skill to convert professional information sources into short-video scripts for general audiences.

The core job is not summarization. The core job is to find where experts assume too much, then turn those hidden assumptions into interesting, understandable public-facing angles.

## Default Behavior

- Reply in Chinese unless the user asks for another language.
- Generate 3-5 slices by default. Use the user's requested number when specified.
- Make each slice explain exactly one small idea.
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

## Readable Layout Principles

Use these rules when the output includes long text, book-style content, graphic-text posts, captions, or layout advice:

- The core of good layout is simple: clear type, loose lines, enough white space, clear hierarchy, and a reading path that naturally goes downward.
- For Chinese body text, prefer Songti for formal and long reading. Use a clean Heiti for casual reading. Avoid decorative fonts for body text.
- Keep hierarchy obvious: book title > major heading > secondary heading > body > notes. Use size and weight differences, not random font changes.
- Body line height should normally be 1.2-1.5 times the font size. Follow the rule that line spacing is greater than letter spacing.
- Do not pack text tightly. Dense body text creates visual fatigue.
- Use two-sided alignment for book body text. Use left alignment for short copy when it reads better.
- Indent the first line of Chinese body paragraphs by 2 characters when writing book-style text.
- Keep paragraphs short. Aim for 3-5 lines per paragraph. Split large blocks.
- Keep paragraph spacing consistent across the whole piece.
- Leave enough margins. The top margin should be larger than the bottom margin, and the inner margin should be larger than the outer margin for book pages.
- Keep white space consistent across the whole work. Do not change margin sizes randomly.
- Put major titles centered, bold, enlarged, and on their own line. Put smaller titles left-aligned and separate from body text.
- Leave one blank line between a heading and the body below it.
- Keep images close to the related text. Do not let images crowd text or appear far from the idea they explain.
- Keep image size consistent. Put captions below images, in a smaller font than the body.
- Use mostly black-and-white body text. Avoid large blocks of color that make the page messy.
- Keep text volume balanced page by page. Avoid one page being too full and another too empty.
- Do not split a complete word awkwardly across lines. Avoid punctuation or bullets appearing alone at the start of a line.
- Keep punctuation, numbering, Arabic numerals, and English word styling consistent.
- Put notes at the footer or end. Do not insert notes into the body in a way that interrupts reading rhythm.

## Forbidden Phrases

Avoid these in final scripts and titles:

- "我觉得", "可能", "大概", "或许"
- "事实上", "本质上", "某种程度上"
- "值得注意的是", "换句话说"
- "不是...而是..."
- "首先", "其次", "最后", "综上所述", "总而言之"
- Opening with "随着" or "近年来"
- "不仅...而且..."
- Exclamation marks
- Dashes used as dramatic punctuation

## Accepted Inputs

The input can be any of these:

- A professional long-form article
- A topic, such as "AI Agent Skill 是什么"
- A URL to an article, report, document, or post
- Several notes, fragments, or copied paragraphs
- A paper, product doc, transcript, or industry analysis

If the input is only a broad topic, expand cautiously from generally known concepts and say that the result is based on topic interpretation rather than a specific source.

## Workflow

Follow this sequence:

1. Understand the information source.
   - Identify the main subject, the central claim, and the most important mechanisms or examples.
   - Separate what the source explicitly says from what you infer.

2. Extract the professional core.
   - Find key concepts, mechanisms, trends, risks, opportunities, examples, and counterintuitive points.
   - Prefer points that can be explained through everyday scenarios.

3. Identify knowledge-curse points.
   - Mark terms, background assumptions, skipped reasoning, implicit value, and expert-only context.
   - Ask: where would a non-specialist pause and wonder "what does this mean?" or "why should I care?"

4. Translate into public-interest angles.
   - Convert expert concepts into ordinary concerns: work, money, efficiency, anxiety, opportunity, risk, family, daily life, or common misconceptions.
   - Prefer "life consequence" over "concept definition".

5. Select 3-5 slices.
   - Each slice should have one sharp idea, one audience hook, and one clear takeaway.
   - Do not make multiple slices that say the same thing in different words.

6. Write one-minute scripts.
   - Scripts should be easy to speak aloud.
   - Use concrete examples, simple contrasts, and light analogies when helpful.
   - End with a memorable practical insight, not a vague slogan.
   - Run the spoken-style and forbidden-phrase checks before returning the final answer.

## Output Format

Use this format unless the user asks for another one:

```text
整体判断：
- 信息源核心：
- 最适合大众化的方向：
- 主要知识诅咒点：

切片 1：
- 标题：
- 大众兴趣点：
- 专业来源：
- 知识诅咒点：
- 一分钟脚本：

切片 2：
- 标题：
- 大众兴趣点：
- 专业来源：
- 知识诅咒点：
- 一分钟脚本：
```

Add more slices as needed.

## Script Shape

Each script should feel like one natural spoken paragraph. It can contain:

- A direct hook that gets to the point.
- A familiar scene from work, money, school, family, phone use, or daily decisions.
- A plain explanation that assumes no professional background.
- A simple example when it helps.
- A closing line that sounds like something a real person would say.

Allow pauses, short lines, and slight repetition. Do not force every script into the same rhythm.

## Quality Bar

A good output should pass these checks:

- It is a set of slices, not a summary.
- Each slice covers only one small idea.
- Each slice names the knowledge-curse point it solves.
- The viewer can understand it without AI, finance, law, medicine, or industry background.
- The script can be spoken in about one minute.
- The title creates curiosity without misleading the viewer.
- The explanation connects the professional point to ordinary life or work.
- The final script avoids the forbidden phrases and punctuation.
- The final script sounds like spoken Chinese, with natural particles used lightly.

## Examples

Professional source point:
"AI Agent Skill 是一种将可复用能力封装为标准化执行单元的机制。"

Possible public slice:
"以后用 AI，肯定不能只会问一句话了啊。你要知道，Skill 这东西，可以先理解成 AI 的技能包。一个技能负责查资料，一个技能负责写文档，一个技能负责做表格。你给它安排清楚，它就能按步骤干活。普通人要练的呀，是把事情说清楚，把任务拆明白。这样 AI 才接得住。"

Professional source point:
"大模型降低了知识工作的边际生产成本。"

Possible public slice:
"以前写一份方案，很多人要熬到半夜吧。现在会用 AI 的人，下班前就能先弄出三版。这个变化挺关键啊。你不用一上来就写得特别完美，你可以先试，先改，先比较。成本低了，人就敢多试几次。很多工作差距，就是这么拉开的。"
