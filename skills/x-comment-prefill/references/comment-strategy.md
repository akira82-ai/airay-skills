# Comment strategy

## Source gate: raw-material retrieval (资料 first, never 成书)

The X post only supplies a concrete trigger and a relevance check. Material is
sourced from each book's raw `资料/` subdirectory — **never from the finished
book chapter `.md` files**: 成稿已经过提炼和润色，细节密度低，改出来的回复
干瘪。The only book-side file exempt from this ban is `zh/topic-map.md` — it
is a directory routing table, not book content.

Retrieval, per candidate:

1. **主题 + 主旨**: from the post, extract which book it belongs to (主题)
   and what it is really about in one line (主旨).
2. **Routing**: use `zh/topic-map.md` to enter that book's `资料/` directory.
   Books without a `资料/` directory (currently codex, loop-engineering) have
   no eligible source → record `skipped_no_local_match`.
3. **Top-3 candidates**: derive 2–4 discriminative keywords from the 主旨
   (Chinese + English + synonym expansions, e.g. 跑偏 → 漂移 / goal drift),
   then search the book's `资料/` with them. Subdirectory names are semantic
   waypoints (`视频字幕`, `中国本土FDE`, `FDEOps`…) — narrow scope through
   them first. Rank files by hit density × keyword coverage (a file hitting
   two different keywords outranks one hitting the same keyword twice); keep
   the top 3.
4. **Rank and pick**: read the 3 candidates and rank them against the post's
   FULL text (not just the keywords — this fixes grep's lexical misses). The
   winner becomes the verbatim `source_excerpt`. Record its source type:
   - `own-draft` — the user's own notes/drafts → 亲历口吻 allowed;
   - `external-collect` — collected articles, video subtitles, interviews →
     **整理者口吻 only**（“我整理书的时候看到过一个说法”“有人这么干过”）;
     never dress external material as the user's own lived experience.
5. **Miss = skip**: if keyword expansion finds nothing, or no candidate
   actually answers the trigger, record `skipped_no_local_match`. 宁缺毋滥 —
   a weak hit is worse than no hit.

Evidence card (persist with the candidate):

```text
trigger: exact post detail that made the material relevant
material_file: file under the book's 资料/ directory
material_anchor: heading or stable paragraph anchor
source_excerpt: sufficiently complete verbatim passage
material_point: one method, experience, case, judgment, or lesson
ownership: own-draft | external-collect
```

A topic name, keyword, memory, or the X post itself is not a substitute.
Respect negative topic boundaries: when the topic map explicitly excludes a
meaning (e.g. the Graph book is not about knowledge graphs), a keyword hit on
the excluded meaning does not match. If the local passage cannot answer the
trigger naturally, skip the candidate.

## Reply direction: exactly three stances

The reply always speaks from own material, but it must take one of exactly
three stances toward the post. The post's shape × the material's relation
decide the direction — never rotate or pick by taste. If none of the three is
supported by the material, skip the candidate.

| direction | stance | looks like |
| --- | --- | --- |
| **共鸣** | same experience | “诶呦卧槽，我也这样” + a bit of the user's own parallel experience |
| **扩展** | complementary half | the post covered half; own material supplies the other half |
| **交流** | opposing view | “你说的不对，我认为是……” + own judgment and grounds |

Three bans apply to every direction — they are the ways a reply goes wrong by
talking AT the post instead of FROM own material:

- **禁评价**: no judging the post or author (“你说得太对了”“写得太好”“这个判断
  很准”). Agreement is expressed only by laying out own parallel experience,
  never by praising the other side.
- **禁解释**: no restating or explaining the post back (“你的意思是…”“其实你在
  说的是…”). In 扩展, the added half must come from own material — never
  complete or clarify the author's half for them.
- **禁科普**: no lecturing at the author (“你之所以这么想是因为没理解X原理”).
  In 交流, challenge the CLAIM, not the person: blunt is fine, condescending
  teaching is not.

## Voice profile: chosen by the post's temperature

Direction is the stance; voice is the register it is spoken in. Pick one
voice per candidate from the post's tone — never rotate, never mix registers
in one reply:

- **乔木体 (calm-judgment, default):** 结论先行、短句、结构干净、收尾给一个
  可带走的判断。For posts that reason calmly about method, technology, or
  tradeoffs. Example shape: “Agent 框架用到最后，常常回到自己手写的那几百行。
  ……分水岭在最后一步：没有检查，跑得越快，假完成越多。”
- **Clarkson 体 (satirical-metaphor):** 一本正经的胡说、夸张比喻、先绕后扎
  的 punchline。For posts that rant, meme, or carry strong emotion — match
  their energy, pick up their combative wording, and borrow the post's own
  words as connection points. Example shape: “供养 agent 框架两周，最后滚回
  自己那 300 行，这不叫失败，这叫成年。框架像位管家，制服笔挺……少检查那步，
  跑得越快，假完成得越体面。”

Clarkson guardrails: exaggeration lands ONLY on rhetoric (metaphors,
comparisons), never on facts — no invented experiences, numbers, or
credentials; borrowing the post's own words as hooks is allowed; the satire
targets the claim or the situation, never the person; the post's vulgar words
may be echoed, not escalated.

Invariants across both voices: same thesis, same corpus anchor, book title +
link rules unchanged, weighted-length budget unchanged, hard bans unchanged.

## Drafting: the 改稿人 rewrite (single mandatory method)

Run `references/clone-rewrite-prompt.md` on the `source_excerpt` — input
mapping is at the top of that file. It owns the whole 活人感 methodology:
structure rebuild (re-derive from a one-line thesis with a different entry,
never sentence-by-sentence 精装修), the six entry strategies (场景 / 例子冷开场 /
引言署名 / 倒叙 / 动作建议先行 / 规则先行), emotion rules, hard bans, and the
author-with-book rules. No separate humanize pass and no other rewriting
method exists.

The rewrite's own output checks are part of drafting:

- **重构自查:** if the new draft's opening and information order can be found
  in the original, it is 精装修 — discard and rebuild.
- **语气自查:** read it aloud; if it reads as carefully composed copy rather
  than typed-off words, rewrite.
- Book attribution follows the 作者带书 rules: 内容先行书名后置, verbs 写/收/
  拆/整理/给过 (never 发现/首创/提出), 语气是熟不是吹, no advertising bridge.

## Gates

Reject or rewrite the draft if any check fails:

1. **Fidelity:** every concrete fact, number, and first-person claim is
   supported by `source_excerpt` (or is the post's own detail used as shared
   ground). 落点必须长在原文语境能推出的范围内.
2. **Direction:** it takes exactly one of the three stances (共鸣 / 扩展 /
   交流) toward the post, and commits none of the three bans (评价 / 解释 /
   科普). Evaluating, restating, or lecturing the post or author fails here.
3. **Hard bans clean:** no 翻案腔, no 三项以上同构排比, no 破折号, no 路标词,
   no 黑话, no 假细节, no 表演性口语 — per the 改稿人 硬禁令 list.

Do not fix a failed gate by adding detail. Shorten the body or skip it.

## Length budget (before filling)

X weighted length: a character with `code point > 0x2000` counts as 2, else 1;
a URL counts as 23. Standard accounts: whole reply ≤ 280 weighted. The link
alone costs 23 — budget the body accordingly. If the draft is over, compress
the draft first (drop a clause, tighten particles) and re-run the 语气自查;
never truncate mid-sentence and never ship an over-limit draft.

## Promotion

Decide promotion only after the gates pass. Use the exact book title and URL
from `/Users/agiray/Desktop/github/1-my-repo/100-questions-of-ai-agent/zh/topic-map.md`.
A strong local match generally means: book title woven into the body per the
作者带书 rules (署名不是推荐), with the link on its own last line. The body
must still make sense after removing both.

- Never place the book mention in the final sentence, and never let it become
  a restate-and-mount tail — a closing line that only compresses what the body
  already said. The mention must sit in a sentence that adds local material
  the body has not already delivered.
- No advertising bridge: “这类问题我整理进了”“欢迎看看”“相关内容见下方” are
  banned. If the book cannot be mentioned without such a bridge, omit the
  mention or link.
