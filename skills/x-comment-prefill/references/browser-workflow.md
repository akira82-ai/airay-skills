# Browser workflow (ego lite)

Read the `ego-browser` skill for the full API. Every browser action runs in an
`ego-browser nodejs` heredoc. Keep actions serial and observable. The workflow
has two phases: open all frozen candidates first, then fill them one at a
time.

## Budgets

```text
scan_batch_size: 5-10 unique posts
scan_count: 50 unique posts by default
detail_ready_timeout_ms: 30,000
composer_timeout_ms: 45,000
composer_max_scrolls: 12
composer_scroll_step_px: 500-700
composer_wait_after_scroll_ms: 1,500-2,500
composer_max_consecutive_no_progress: 3
fill_render_wait_ms: about 2,000
```

Every loop has a limit. A timeout ends that action and never authorizes a
second write or a replacement Page.

## Space lifecycle

- Resume the user's named space: `const task = await claimTaskSpace(7);`
  (use the id the user gives; find ids via `listTaskSpaces()`).
- When creating a new space, use a UNIQUE name per run (e.g.
  `taskSpace("x-comment-prefill-" + run_id)`). A generic name like
  `taskSpace("x-comment-prefill")` can resolve to a user-taken-over old space,
  which makes ego hard-stop with "do not retry" — it cannot be retried or
  reclaimed. If a space resolves wrong, create a fresh uniquely-named space;
  never retry the same call.
- After `handOff()`, ego hard-stops agent commands until the user acts. When
  the user explicitly says 继续, reclaim with
  `const task = await takeOverTaskSpace(id);` — `claimTaskSpace` may not work
  for a space the user has taken over.
- One TaskSpace per goal. Every heredoc starts a new Node.js process: variables
  do not persist — persist run state to the state file with
  `await import("node:fs/promises")`. State-file paths must be ABSOLUTE
  (heredoc cwd varies; relative paths fail with ENOENT).
- Page labels (`p1`, `p2`, …) persist across heredocs. After a space has ended
  or been released, `task.tabs()` may return tabs with `label: null` — match
  tabs by URL, never by label or list position.
- An unmanaged tab must be adopted before operating:
  `const page = await task.adopt(tab.page);`
- Never `page.close()` a candidate Page. Never `finish()` a user-owned claimed
  space. If this run created its own space, the only allowed finish is
  `await task.finish({ keep: [filled labels] })` after every candidate
  succeeded; otherwise end with `await task.handOff()` and let the user act.

## Source tab and scan

Locate the user's existing X tab — matched by host and URL, never by position:

```js
const task = await claimTaskSpace(7);
const tab = (await task.tabs()).find(t =>
  /^https?:\/\/(x|twitter)\.com\/(home|profile|search|[A-Za-z0-9_]{1,15})/.test(t.url));
const source = tab.label ? task.page(tab.label) : await task.adopt(tab.page);
```

Extract feed cards in bounded batches with `page.evaluate()`. Capture the
OUTER post's permalink — the `<a>` wrapping the `<time>` element — not a
quoted inner post's link. Normalize every URL to
`https://{x.com|twitter.com}/{username}/status/{id}` (drop `/analytics` and
query params; keep the `/{username}/` segment). Per card record complete
visible text, author handle, timestamp, and metrics from the action buttons
when visible (missing → `unknown`). Pure-image posts whose text cannot be read
are recorded as undecidable, never force-matched.

Persist each batch (observed URLs + facts) to the state file before scrolling.
Merge by normalized URL — the feed is virtualized and cards disappear. Stop at
`scan_count` or a concrete boundary; never pad the candidate count.

## Opening phase (batch open + draft, no typing)

For each frozen candidate, one at a time:

```js
const page = await task.newPage();          // normal visible tab
await page.goto(url);                        // exact candidate URL
await page.waitForSelector('article[data-testid="tweet"]', { timeout: 30_000 });
```

Verify via `page.url()` plus one `page.evaluate()` reading the main article,
author handle, and complete post text; reject login/error/interstitial states
(`detail_not_ready`). Then match the local corpus: grep/sed from the corpus
root to locate the exact file and anchor, and read the verbatim
`source_excerpt`. No accurate match → record `skipped_no_local_match`, do not
open the composer, next candidate.

Draft per `references/comment-strategy.md` (quote-led default, clone-rewrite
fallback, gates, promotion). Store the draft in the state file. Leave the Page
on its post and persist its label, URL, and readiness before opening the next
candidate. A missing or not-ready page is recorded and never replaced; if
`task.newPage()` itself cannot produce a visible tab, stop the phase with
`visible_tab_unavailable`.

## Filling phase (serial, one at a time)

Process prepared candidates in frozen order:

1. **Reacquire by URL**: `const tab = (await task.tabs()).find(t => t.url ===
   url);` If gone → `target_missing`, no replacement, advance the cursor. If
   the live-tab listing itself fails, pause the batch and report the blocker.
2. **Composer discovery** — the first miss is not failure (X renders the box
   lazily; long posts place it below the viewport):

```js
const found = await page.evaluate(() => { /* fill-draft.js xcpReadState() */ });
if (!found.ok) {
  await page.mouse.move(400, 400, { label: "hover feed area" }); // wheel needs the pointer over a scrollable area
  await page.mouse.wheel(0, 600, { label: "scroll to composer" });
  await page.waitForTimeout(2000);
  // re-probe; stop at 45s / 12 scrolls / 3 consecutive no-progress
}
```

   Record probes, scrolls, elapsed ms, and the concrete stop reason
   (`textbox_discovery_timeout` | `..._scroll_limit` | `..._no_progress` |
   `textbox_not_found_at_bottom`). Never use coordinates or stale refs.

3. **Read once, write once.** Before any write, run the length budget from
   `comment-strategy.md` (weighted chars, URL = 23, limit 280); an over-budget
   draft is compressed and re-approved BEFORE touching the box. On a revision
   round, first verify the box still contains the previous approved version —
   if the user has edited or published it, skip. `xcpPrepare(draft)`
   classifies: `empty` → click the real box
   (`page.click('loc=css:div[data-testid="tweetTextarea_0"]')` or a snapshot
   ref), then exactly one `await page.keyboard.paste(draft)` (macOS native
   paste; restores the user's clipboard) or `page.keyboard.insertText(draft)`;
   existing different text → `prefill_conflict`, read-only stop; identical →
   `already_correct`.
4. **Readback.** `await page.waitForTimeout(2000);` then `xcpVerify(draft)` —
   require exact equality after normalizing `\r\n` → `\n`. Never click Send.
   Persist the result before the next candidate.

### Clipboard fallback

On failure, partial, or uncertain fill: set the system clipboard once
(macOS: `await import("node:child_process")` → `spawn('pbcopy')` with the
complete draft), record `clipboard_ready` with the exact URL, and pause the
whole fill phase — a second copy would overwrite the clipboard. On explicit
continuation, verify live tabs and resume with the next unfilled candidate.
Never append, clear, overwrite, switch method, or retry the box.

## Final retention check

Before ending the turn: `await task.tabs()` again, verify every candidate by
normalized URL, and record `tab_closed=false` and `persistence_verified`. Do
not close, discard, navigate, or recycle candidate Pages; a disappeared
candidate is reported as observed, never auto-replaced. Then
`await task.handOff()` so the user reviews and publishes manually.

On "继续": load the state file first, resume the same space by id, verify live
candidate tabs, and continue the saved cursor — no rescan, no reopening filled
candidates, no substitutes.
