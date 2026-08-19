---
name: x-comment-prefill
description: >-
  Run a stateful, human-in-the-loop X comment-prefill workflow in the user's
  already connected Chrome or Edge session. Use whenever the user asks to scan
  X posts, read the first 50, find posts worth replying to, draft replies,
  fill reply boxes without publishing, continue a prior X batch, recover target
  tabs, revise one prefilled comment, or only optimize comment text without
  opening a browser. The skill screens and freezes candidates, matches local
  Chinese material,   and hands off in the form the run needs. By default it drafts and hands off as
  copy-ready text plus links (text-handoff), opening the browser only to read
  the timeline; it fills reply boxes only when the user explicitly opts into
  browser-prefill. It never publishes, likes, reposts, follows, or silently
  changes browsers.
---

# X comment prefill

This skill owns the workflow and its safety gates. It does not own the user's
temporary campaign choices or local browser implementation. Load only the
reference needed for the current stage:

- `references/browser-workflow.md` for browser discovery, DOM checks, tab
  lifecycle, and final handoff.
- `references/comment-strategy.md` before drafting or revising any reply.
- `references/topic-map.md` when matching an X post to local `zh` material.
- `references/report-template.md` when reporting results or writing run state.

## Run parameters

At the start of a new run, capture the temporary parameters without changing
the skill:

```text
run_id: generated unique identifier
mode: content-only | text-handoff | browser-prefill   # default text-handoff
browser: chrome | edge | unspecified
goal: followers | engagement | traffic | discussion | user supplied
topics: all | user supplied topic set
allow_links: never | natural-match-only | user supplied
promotion_level: no_link | book_mention | book_mention_plus_link
scan_count: default 50
```

Capture `promotion_level` and `allow_links` at run start, not after drafts
exist. Setting `promotion_level` late (e.g. "make it stronger / add the link"
after comments are written) forces a full re-draft, which was the main rework
driver in prior runs.

`promotion_level` is a per-candidate **upper bound**, not a uniform switch.
Even when the run sets `book_mention_plus_link`, a candidate may resolve to
`book_mention` or `no_link` if the natural-match test fails or the
delete-book-title test in `comment-strategy.md` would be violated. Re-evaluate
the actual level for each candidate after its draft exists.

The run's `goal` sets the default promotion ceiling: when the goal is
`followers` or `engagement`, cap `promotion_level` at `book_mention` unless the
user explicitly asks for links; only `goal: traffic` justifies
`book_mention_plus_link` by default. Rationale: opening an off-platform link
contributes almost nothing to the reply's distribution and pulls engaged
readers out of the thread — links trade away the in-thread interaction that
drives follower growth. A book mention alone keeps the memory signal that
leads readers to visit the profile.

Route the request before any browser action:

- Use `content-only` when the user provides the post text or asks to optimize,
  compare, or draft a comment without opening the post/link or touching X.
  Read only the supplied post and the relevant local `zh` material. Do not
  inspect tabs, scan, open URLs, fill textboxes, or call `finalize`.
- Use `text-handoff` (the DEFAULT) when the user asks to scan X, find posts
  worth replying to, or wants ready-to-post comments. Open the browser only to
  read the timeline and verify posts; then draft from local material and hand
  off copy-ready text plus the post link. Do NOT fill any reply box. This avoids
  the borrow / session-timeout / locked-window constraints of in-browser filling.
- Use `browser-prefill` ONLY when the user explicitly asks to fill the reply
  box (e.g. "填进回复框"). Load `browser-workflow.md` and run the browser stages
  below. Treat any request to publish as outside this skill.
- If the user says “不必打开链接” while supplying the post text, interpret it
  as `content-only`; it does not authorize opening the URL merely to verify
  context. A link may still be included in the draft only when the separate
  link policy permits it.

If the mode is ambiguous, default to `text-handoff` and ask one consolidated
question at run start: confirm `mode` (text-handoff vs browser-prefill),
`promotion_level`, and `allow_links` together so drafts are not reworked later.

In `content-only`, the state record is optional and must not contain browser
claims. The output is a draft plus its evidence card and promotion decision;
when no accurate local match exists, output `skipped: no_accurate_local_match`
instead of a fallback comment. In `browser-prefill`, follow the full stateful
workflow and handoff gates below.

If the user names a browser, use only that browser. If they do not, choose one
already connected to the requested X session and state the choice. Never switch
silently. The default external-action boundary is: fill for review, never
submit. A user request to publish is outside this skill and requires a separate
explicit confirmation and workflow.

## State is part of the workflow

Maintain one state record for the active run. By default write it to
`.x-comment-prefill/runs/{run_id}.json` under the current project; if that
location is not writable, use the task workspace and report the fallback path.
Create the directory only when the workflow actually starts. Do not hide state
only in conversation memory. Use the schema in `references/report-template.md`. Candidate status values are:
`discovered | drafted | opened | filled | handed_off | skipped | failed`.
Never collapse these into a single "done" field.

For every drafted candidate, also persist the material evidence card and the
promotion level:

```text
evidence_card:
  trigger: exact post detail used only as a topic or context clue
  material_file: exact local zh file path
  material_anchor: heading, paragraph, or stable text anchor
  material_point: one concrete case, method, judgment, or lesson used
  ownership: user-provided | source-derived
promotion_level: no_link | book_mention | book_mention_plus_link
```

The evidence card is a gate, not just report metadata. A topic label, keyword,
or directory match without a concrete file and anchor is not sufficient to
draft. `content-only` may keep this card in the response instead of writing a
run file; `browser-prefill` must persist it in candidate state.

Persist state after each stage and after each candidate. A state write must not
contain credentials, cookies, or unrelated page content. If the runtime cannot
write state, report that limitation and keep a compact state summary in the
response; do not pretend that “continue” recovery is reliable.

## Continuation router

Interpret a follow-up against the active state before doing browser work:

1. **“继续” / “再来”**: if an active run exists, resume its recorded stage and
   reuse its exclusion set. Do not rescan or reinterpret completed candidates.
   If the previous run is complete or the user clearly requests a new batch,
   create a new `run_id` and exclude all historical status URLs.
2. **“改一下评论”**: identify the requested candidate by exact status URL,
   stable candidate record, or uniquely visible target tab. Modify only that
   draft, then re-run the comment and exact-readback gates for that tab. Do not
   rescan, open a replacement tab, or alter other candidates.
3. **Conflicting new parameters**: apply them only to the not-yet-completed
   stage. Do not rewrite completed facts. If a change would invalidate the
   frozen candidate list, say so and ask whether to start a new run.

## State-machine stages and gates

Run these stages in order. Each stage has one job; do not jump ahead because a
later action would be convenient.

### 1. Preflight browser

This stage applies to `browser-prefill` and `text-handoff`. `content-only`
stops before this stage and must not inspect or change browser state. In
`text-handoff`, locate the source tab to read the timeline but do not open any
target tab or fill boxes.

Read `browser-workflow.md`. Locate the user's connected browser and inspect
live tabs. Require exactly one usable X source tab for collection, unless the
active state already names a live source tab that can be reacquired by exact
URL. Do not open a new X source tab. If the requested browser is unavailable,
stop with the concrete blocker.

Contract: input is the browser choice and active state; allowed actions are
live-tab listing and exact-URL reacquisition; forbidden actions are browser
switching, opening a source tab, scrolling, and creating target tabs.
Success means the source tab URL and browser are recorded. Failure means no
scrolling, no candidate tabs, and no guessed tab IDs.

### 2. Collect and deduplicate

This stage applies to `browser-prefill` and `text-handoff`.

Read the requested number of timeline posts from the source tab. Normalize each
main-post URL to its status URL, remove tracking parameters and `/analytics`,
and count unique URLs rather than cards. Record author, full visible post text,
language, and visible reading/reply metrics. Unknown metrics stay unknown.

Exclude both the current run's scanned URLs and the persisted historical set.
Stop at `scan_count`; report the actual count if the feed contains fewer.

Contract: input is the verified source tab and exclusion sets; allowed actions
are bounded visible extraction, URL normalization, and bounded scrolling;
forbidden actions are opening detail tabs, opening reply boxes, and external
engagement actions.
Success means a deduplicated scan record exists. Failure means preserve the
partial scan and stop collection; do not invent missing metrics.

### 3. Screen and freeze candidates

This stage applies to `browser-prefill` and `text-handoff`.

Apply the current run parameters and the thresholds in `comment-strategy.md`.
Select only concrete, discussable, topic-matched posts with confirmed metrics.
Prefer quality over quota. Rank passing candidates by the golden-window
signals in `comment-strategy.md`: post freshness (prefer under 24h; the
timestamp sits on the permalink anchor already collected in stage 2),
mutual-follow authors (top priority when determinable), and small/mid-size
authors whose reply the comment can realistically earn. These are ranking
signals, not hard gates — an unknown timestamp or relationship must not drop
an otherwise passing candidate. Once this stage succeeds, freeze the candidate list:
later “continue” actions cannot silently add substitutes to the same run.

Contract: input is the deduplicated scan; allowed actions are metric/topic
screening and local-material lookup; forbidden actions are opening target tabs,
filling replies, and changing the frozen list after this gate.
Success means every candidate has a reason, topic/material match status, and
screening facts. A candidate with missing required metrics is not final.

### 4. Process detail tabs serially

This stage applies to `browser-prefill` and `text-handoff`; in `text-handoff`
skip the in-browser steps (1, 4, 5) and produce copy-ready text instead.

Read `browser-workflow.md` and `comment-strategy.md`. For each frozen candidate,
one at a time:

1. Reacquire an existing exact-URL target tab, or open one target tab only
   after selection. The first opened target tab is a deliverable, not a
   temporary inspection page.
2. Verify exact URL, target main article, author, and nonempty complete post
   text. Do not rely on the timeline excerpt.
3. Use the post only as a topic or context clue to locate a specific
   local-material passage before drafting. Apply the drafting rules, the three
   pre-draft questions, and the delete-book-title test in
   `comment-strategy.md`. If no accurate local match exists, record
   `skipped: no_accurate_local_match`, do not draft, and do not fill that
   tab.
4. Read back the visible text and require exact equality with the draft.
5. Persist `opened`, `filled`, `submitted=false`, the material anchor, and any
   failure or skip reason before
   moving to the next candidate.

In `text-handoff`, do not open a target tab, do not fill, and do not read back
in the browser. After drafting (step 3), record the candidate as `drafted`
with its evidence card and promotion level. Copy-ready text delivery happens
in Stage 5.

Contract: input is one frozen candidate at a time; allowed actions are exact-tab
reacquisition, detail verification, draft generation, textbox filling, and
readback; forbidden actions are parallel candidate processing, replacement tabs,
and submission or other engagement actions.
If a target tab disappears, record `opened_but_not_filled` and do not open a
replacement for that URL. A failed candidate does not authorize cleanup.

### 5. Live-tab handoff

This stage applies to `browser-prefill` and `text-handoff`; in `text-handoff`
it is a text delivery, not a browser `finalize`.

After all candidates are processed, reacquire live tabs and verify every kept
target by exact URL and exact readback. Merge live-tab sources and deduplicate
by URL so stale handles cannot become evidence. Call `finalize({keep})` at most
once, only with verified target tabs. Never use it as cleanup. Whether it
succeeds or fails, stop browser actions immediately after this attempt.

Contract: input is the completed candidate state and live-tab listings; allowed
actions are final verification and one handoff call; forbidden actions are
cleanup, a second finalize call, and any browser action after finalize.

In `text-handoff`, do not call `finalize` and do not do browser work. Deliver
one block per kept candidate: post link, copy-ready comment, promotion level,
and evidence card. Mark `delivered_as: text` and `submitted: false`. Stop after
delivery.

Success means the report distinguishes `opened`, `filled`, `handed_off`, and
`submitted=false`. Failure means report the actual live-tab state; never claim
that a stale handle was handed off.

## Non-negotiable boundaries

- Never click the final reply/send/publish button.
- Never like, repost, quote-post, follow, DM, or publish.
- Never close, discard, recycle, or clean up tabs, including failed target tabs.
- Never guess a URL, metric, author, tab ID, selector, or readback.
- Never use a keyword alone as evidence for a topic match or a link.
- Never generate a comment from the original post alone. Without an accurate
  local-material match, skip the candidate; do not write a summary, evaluation,
  agreement, disagreement, rebuttal, advice, or generic opinion about the
  original author or post.
- In `content-only`, never open the supplied post URL or any alternative URL;
  the supplied text is the only post evidence.
- When linking, make the comment body complete first. The book/source mention
  may be woven into the experience, and the hyperlink may stand on its own
  line; never use an abrupt “这类问题我整理进了……” transition or append an
  unexplained promotional tail.
- Never call `finalize` more than once, and never do browser work after it.
- Never present `opened` or `filled` as `submitted` or `published`.
- Never bait engagement with hollow rhetorical questions or manufactured
  controversy. A reply earns replies through a specific, positioned judgment
  others can join — not through bait.

## Final response

Use `references/report-template.md`. State the run ID, browser, scan count,
frozen candidate count, per-candidate status, finalize result, and the explicit
boundary `submitted: false`. If the user asked for original-post ideas, add at
most two ideas grounded in posts actually read; do not open a composer for
them. Do not claim a local state file, browser handoff, or publication unless
the corresponding gate was verified.

For `text-handoff`, the deliverable is copy-ready text per candidate (post link
+ comment + promotion note + evidence card), not a browser handoff. Never claim
a reply box was filled or handed off; always state `delivered_as: text` and
`submitted: false`.
