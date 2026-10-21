---
name: x-comment-prefill
description: >-
  Scan x.com with ego lite, match posts against the user's local Chinese book
  corpus, rewrite matched excerpts into spoken-style replies with the 改稿人
  method, and prefill reply boxes without publishing. Use only for the
  scan-and-prefill workflow.
---

# X comment prefill

One workflow only: open `x.com`, scan the feed, match posts to topics in
`/Users/agiray/Desktop/github/1-my-repo/100-questions-of-ai-agent/zh`, draft
replies whose substance is a verbatim local excerpt, and prefill them for the
user to review and publish manually.

## Browser tool: ego lite only

ego lite is the required browser. Load the `ego-browser` skill for the API and
run all browser work through `ego-browser nodejs` heredocs. No other browser
automation path is allowed: no hidden windows, no disposable agent windows, no
DOM-only extensions, no direct CDP drivers for candidate tabs. ego lite tabs
are the user's own visible Chrome tabs; the user can watch every step.

Read references progressively:

- `references/browser-workflow.md` — space lifecycle, scanning, opening,
  filling, retention. Read before any browser action.
- `references/comment-strategy.md` — source gate, quote-led drafting, gates,
  promotion. Read before drafting.
- `references/clone-rewrite-prompt.md` — the 改稿人 rewrite prompt; the only
  drafting method (structure rebuild + 活人感 rules + author-with-book rules).
- `/Users/agiray/Desktop/github/1-my-repo/100-questions-of-ai-agent/zh/topic-map.md`
  — read at startup before matching posts to books.
- `references/report-template.md` — run state and final report.
- `references/fill-draft.js` — read-only page helpers to locate and verify the
  reply editor inside `page.evaluate()`.

## Hard boundaries

- Never publish, send, like, repost, quote-post, follow, or DM. `submitted` is
  always `false`.
- Never close, navigate away, or clean up a candidate Page. Candidate Pages
  stay on their post for user review.
- One TaskSpace for the whole goal. Do not recover problems by creating a new
  space; recover inside it or stop and ask.
- Fill only through ego's real input path: click the real reply box, then one
  `keyboard.paste()` / `keyboard.insertText()`. Never DOM value setters,
  synthetic events, or `page.fill()` on the composer.
- Never generate a reply from the X post alone. Require a concrete local file,
  anchor, and verbatim `source_excerpt` from the zh corpus.
- Never source material from finished book chapter `.md` files — only from the
  book's `资料/` raw materials. External-collected material speaks in
  整理者口吻, never as the user's lived experience.
- If no accurate local match exists, skip the post. Never turn it into a
  review, summary, agreement, rebuttal, advice, or keyword opinion.
- Read the box before filling. Never clear, append, overwrite, or retry a
  nonempty, partial, or uncertain box.
- Respect the account's length limit: weighted length (code point > 0x2000
  counts 2, else 1; a URL counts 23) must fit 280 for standard accounts.
  Compress the draft before filling; never ship over-limit text.

## Entry and defaults

Show these parameters and wait for explicit confirmation before any browser
action. A bare "继续" resumes the saved run: reload the state file, reclaim the
space with `takeOverTaskSpace(id)`, verify live tabs, continue the cursor — it
does not rescan.

~~~text
mode: scan-and-prefill          # the only mode
browser: ego lite               # required
space: resume the user's named space id, else taskSpace("x-comment-prefill")
local_corpus: /Users/agiray/Desktop/github/1-my-repo/100-questions-of-ai-agent/zh
topics: all books in the external zh/topic-map.md
scan_count: 50 unique posts
promotion: book title woven into body + link on its own last line
fallback: clipboard one at a time
confirmation: pending
~~~

## Fixed workflow

After confirmation, follow `references/browser-workflow.md`:

1. **Source tab.** Resume or claim one TaskSpace. Locate the user's existing
   x.com or twitter.com tab via `task.tabs()` matched by URL (labels may be
   null — match by URL, never by position), and `adopt()` it if unmanaged.
2. **Scan.** Read visible feed cards in bounded batches through
   `page.evaluate()`; per card record complete visible text, author, timestamp,
   metrics when visible, and the normalized status URL. Persist each batch as a
   checkpoint before scrolling. Merge by URL (the feed is virtualized) and
   exclude historical URLs. Posts that are pure images with unreadable text are
   recorded as undecidable, not matched.
3. **Match and grade.** Match every scanned post against the external
   topic-map and the zh corpus (grep/sed from the corpus root). Grade matches:
   strong (a concrete passage directly answers the post's trigger), medium
   (topic fits, passage partial), weak (keyword only), no match. Candidates
   come from strong matches; medium only if the user asks for more. Freeze the
   candidate list.
4. **Opening phase.** For each frozen candidate, `task.newPage()` + `goto()`
   (a normal visible tab), verify exact URL, main article, author, complete
   post text, and no login/error interstitial. Keep the Page on its post. Do
   not type anything in this phase.
5. **Drafting phase.** Per candidate, run the raw-material retrieval in
   `references/comment-strategy.md`: extract 主题 + 主旨 from the post → route
   via `zh/topic-map.md` into that book's `资料/` directory (**never** the
   finished chapter `.md` files; books without `资料/` → skip) → search with
   2–4 discriminative keywords (CN + EN, synonym-expanded) → top-3 files by
   hit density × keyword coverage → rank the 3 against the post's full text →
   the winner becomes the verbatim `source_excerpt`, tagged `ownership`:
   `own-draft` (亲历口吻 allowed) or `external-collect` (整理者口吻 only).
   Then decide the reply direction (共鸣 / 扩展 / 交流) and the voice profile
   (乔木体 / Clarkson 体, by the post's temperature) per the models in
   `references/comment-strategy.md` — never rotation; no direction supported →
   skip. Rewrite the excerpt with the 改稿人
   prompt (`references/clone-rewrite-prompt.md`) in the chosen voice:
   structure rebuild with a different entry (场景 / 例子冷开场 / 引言署名 /
   倒叙 / 动作建议先行 / 规则先行), 活人感 rules, author-with-book attribution
   rules, and its own 重构自查 + 语气自查. Then run the gates and promotion in
   `references/comment-strategy.md`. Store the draft.
6. **Filling phase.** Reacquire each candidate Page by URL via `task.tabs()`.
   Run the bounded composer discovery (probe → `mouse.wheel()` → wait →
   re-probe). Read the box once: empty → click the real box and fill once via
   `keyboard.paste()` or `keyboard.insertText()`; different text →
   `prefill_conflict`, read-only stop; identical → `already_correct`. Wait for
   render, read back once, require exact equality. Never click Send.
7. **Clipboard fallback.** If the box cannot be found or a fill is partial or
   uncertain, copy that candidate's complete draft to the system clipboard
   once (pbcopy), report `clipboard_ready` with the exact URL, and pause the
   whole fill phase before another draft can overwrite the clipboard.
8. **Retention and handoff.** Re-list `task.tabs()` and verify every candidate
   by URL. Then `await task.handOff()` so the user reviews and publishes
   manually. Never `page.close()` a candidate; never `finish()` a user-owned
   space. If this run created its own space and every candidate succeeded,
   `finish({ keep: [filled labels] })` is the only allowed finish.

Persist state after each batch and candidate per
`references/report-template.md`: run_id, stage, scan cursor, observed and
frozen URLs, per-candidate evidence card (`trigger`, `material_file`,
`material_anchor`, `source_excerpt`, `material_point`), draft, fill result,
clipboard result, tab label, and failure reason. Never store credentials or
unnecessary private page text.

## Result language

Report separately: `opened`, `drafted`, `filled`, `clipboard_ready`,
`skipped_no_local_match`, `reply_box_not_found`, `partial_fill`,
`target_missing`, `visible_tab_unavailable`. Always include the exact URL,
space id, page label, `tab_closed`, and `persistence_verified`. End every
report with `submitted=false`.
