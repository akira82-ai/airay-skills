# Browser workflow

## Browser choice and preflight

Use the user's already connected Chrome or Edge session. “Chrome/Edge
compatible” means the procedure is browser-neutral; it does not authorize
switching browsers during a run. Reacquire live tabs from the browser's tab
listing by complete URL after every user turn because tab handles can expire.

For collection, require exactly one X source tab whose host is `x.com` or
`twitter.com`. A source tab may be home, a recommendation feed, or search
results. Do not open an X home tab when the preflight condition fails; report
the actual tab count and stop.

If no usable X source tab is connected, use the selected browser adapter's
documented way to create or connect one, or stop with the concrete blocker.
Do not invent a browser-specific fallback. Verify the tab is on the X home or
requested feed before collecting.

## URL normalization

Normalize only URLs that can be proven to identify the main post:

1. Keep the `x.com` or `twitter.com` host and the FULL path `/{username}/status/<id>`. The `/{username}/` segment is part of the canonical URL and MUST be preserved — a URL without it (`x.com/status/<id>`) returns "该页面不存在" (404). Only strip `/analytics` and query/tracking parameters.
2. Remove `/analytics` and tracking/query parameters.
3. Treat the normalized status URL as the identity for deduplication,
   historical exclusions, candidate records, and handoff verification.

Do not merge URLs merely because their visible text looks similar.

## Collection DOM rules

Use bounded extraction from visible `article[data-testid="tweet"]` elements.
For each article, find the canonical status link and normalize it. Extract the
article's full visible text, author, and metrics. A visible card is not a post
until it has a unique normalized status URL. Ads, quoted-post cards, and
duplicate renders do not increase the count.

Scroll in bounded increments only until the requested unique count is reached
or the feed is exhausted. If metrics are absent, record `unknown`; do not infer
them from likes, reposts, account size, or neighboring cards.

### Collection pitfalls (verified)

- **Metrics are not in the article `aria-label`.** Live X DOM does not expose
  reply/like/view counts on the `article` element's accessible name. Extract
  them from the interactive buttons inside the article
  (`[data-testid^="reply"]`, `[data-testid^="like"]`,
  `[data-testid^="retweet"]`) by reading each button's own accessible name /
  `aria-label`; if a count is missing, record `unknown`.
- **The timeline is DOM-virtualized.** After scrolling, only ~8 cards stay in
  the DOM. To collect a stable set, scroll to top (`scrollTo(0,0)`), then scroll
  in small increments, reading on each step and **merging by normalized status
  id** (dedupe), rather than assuming all cards persist. Stop when the requested
  unique count is reached or the feed is exhausted.

- **Quoted/embedded tweets swap the permalink.** The first `a[href*="/status/"]`
  inside an article may be the QUOTED (inner) post's permalink, not the outer
  tweet's. Capturing it makes the frozen status ID and the visible author
  disagree (e.g. the candidate ends up pointing at the wrong post). Capture the
  outer tweet's own permalink — the `<a>` wrapping the timestamp (`time`
  element) — and verify the resolved author matches the article's visible
  author before freezing.

## Detail-page readiness

For each selected URL, serially use an existing exact-URL target tab or create
one target tab. Check at most three times for all of the following:

- the current URL exactly equals the normalized target URL;
- the target main `article[data-testid="tweet"]` is present;
- the target author is visible;
- the complete main-post text is nonempty.

An Agent-created target tab must be marked as `handoff` as soon as it is opened
and while it is unfinished. If readiness fails, retain the mark, record the
reason, and do not create a replacement.

## Reply textbox and readback

Prefer the visible unique inline textbox:

```css
div[data-testid="tweetTextarea_0"][role="textbox"]
```

If it is unavailable, scope a newly opened reply dialog to a visible unique
textbox:

```css
div[role="dialog"] div[role="textbox"]
```

A null first probe is usually **lazy-load, not absence**. On a status detail
page the inline composer (`tweetTextarea_0`) may not be in the DOM until the
tweet region finishes rendering. Long posts can also place it below the
viewport. Therefore, a missing first probe is never enough to skip a candidate.

### Dynamic composer discovery loop

Before filling, run this bounded loop on the already verified detail tab. These
are defaults for one candidate and may be tightened when the browser session is
near its lifetime limit:

```text
max_discovery_ms: 45,000
max_scrolls: 12
scroll_step_px: 500–700
wait_after_scroll_ms: 1,500–2,500
max_consecutive_no_progress: 3
```

For every iteration:

1. Probe the inline selector and any visible, unique reply-dialog textbox.
   Require exactly one visible usable textbox. If found, stop discovery and
   proceed to the fill gate.
2. If none is found, scroll the detail page downward by one bounded step. Do
   not use a guessed coordinate to fill the box. The scroll is only to expose
   X's lazily rendered composer.
3. Wait for the dynamic render, then probe the DOM again. Record the scroll
   position, document height, probe count, and scroll count.
4. Stop with a concrete failure only when one of these gates fires:
   `textbox_discovery_timeout`, `textbox_discovery_scroll_limit`,
   `textbox_discovery_no_progress`, or `textbox_not_found_at_bottom`.

`no_progress` means the scroll position and document height do not advance for
three consecutive attempts, or the page is already at its bottom boundary.
Do not label the first null result, a single unchanged scroll, or a still
rendering page as `textbox_not_found`. If the loop stops, retain the tab and
persist:

```text
textbox_discovery:
  probe_count: number
  scroll_count: number
  elapsed_ms: number
  stop_reason: success | textbox_discovery_timeout |
    textbox_discovery_scroll_limit | textbox_discovery_no_progress |
    textbox_not_found_at_bottom
```

Only after the loop has found a unique visible textbox may the agent fill it.
Do not open a replacement tab merely because discovery hit its limit. A later
manual retry is a new action and must re-check the live tab first.

Verified behavior: the first probe can be null on multiple tabs, while a
scroll followed by a short wait exposes the composer. The wait is part of the
discovery operation, not an optional delay.

Ambiguous or hidden controls are a skip, not an invitation to use coordinates
or positional guesses. Fill only after the complete main post is verified.
Read back `innerText` or equivalent visible DOM text and require exact equality
with the draft. A Draft.js `value` or an enabled submit button is not proof of
successful fill.

### Filling X's Draft.js composer (verified method)

`references/fill-draft.js` packages the select-all, insert, and verify steps
below into reusable page-context functions (`xcpSelectAll`, `xcpInsert`,
`xcpFill`, `xcpVerify`). Use it through the selected browser adapter when it
supports page evaluation. The steps below explain the same logic inline for
contexts where the file cannot be loaded.

Value-only filling does **not** register on X's `contenteditable` reply box (the
value may be set while React/Draft.js ignores it, so readback comes back
empty).

**Never use `document.execCommand('insertText')` here.** It desyncs Draft.js:

| tab state | result |
| --- | --- |
| tab not focused | text lands in the DOM only, Draft.js `editorState` stays empty → placeholder renders **on top of** the text (looks like overlapping glyphs), the reply button stays **gray/disabled**, and the user cannot edit, select, or paste |
| tab focused | the string is committed **twice** (native DOM insert + Draft.js state insert) |

Working procedure — focus the editor through the browser adapter, clear with
real input, and insert through Draft.js only. Do not rely on a value setter or
an unverified coordinate.

1. **Select all via the Range API** (generic keyboard select-all actions may
   not select inside Draft.js):

```js
var el = document.querySelector('div[data-testid="tweetTextarea_0"]');
el.focus();
var r = document.createRange(); r.selectNodeContents(el);
var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
```

2. **Delete with a real key** through the browser adapter so Draft.js sees it.

3. **Insert with a synthetic `textInput` event plus a capture-phase
   `preventDefault` guard**, so React/Draft.js applies the edit and the native
   DOM insertion is cancelled (this is what prevents the double insert):

```js
var el = document.querySelector('div[data-testid="tweetTextarea_0"]');
var guard = function(e){ e.preventDefault(); };
el.addEventListener('textInput', guard, true);
var ev = document.createEvent('TextEvent');
ev.initTextEvent('textInput', true, true, window, DRAFT, 0, 'en-US');
el.dispatchEvent(ev);
el.removeEventListener('textInput', guard, true);
```

Dispatching a synthetic `ClipboardEvent('paste')` with a `DataTransfer` does
**not** work on X — Draft.js ignores it.

Verification (wait ~2s for the React re-render, then read once):
- `innerText.rstrip('\n')` exactly equals the draft;
- `document.querySelectorAll('.public-DraftEditorPlaceholder-root').length === 0`;
- `button[data-testid="tweetButtonInline"].disabled === false`.

An enabled button alone is not proof; require all three. Reading `innerText`
immediately after dispatch is misleading — the double-insert only shows up
after the re-render.

#### Idempotent fill guard

A filled box must never be refilled blindly — re-dispatching into an already
populated Draft.js editor is what produced the duplicated/overlapping text in
earlier runs.

- **Before any fill**, read back the box. If `innerText` (trimmed) already
  equals the draft, `placeholderCount === 0`, and the reply button is enabled,
  **skip the fill** — the candidate is already correct.
- **During handoff re-verification, READ ONLY.** Never re-run the fill against a
  candidate that was already processed. If readback mismatches the draft, do not
  silently refill; record `filled=false` with the mismatch and surface it to the
  user (ask whether to clear and refill) instead of looping.
- **One fill per candidate per run.** The frozen-candidate gate forbids changing
  the list after screening; extend the same discipline to the textbox: a
  candidate's textbox is written once, then only ever read.

Never click the send/reply button. Leave the tab open for the user to review
and publish manually.

### Tab retention and handoff

Agent-created tabs may be ephemeral and can be cleaned up when the current
turn ends unless they are marked. The browser adapter must provide the
following semantic operations, using its own supported API:

- `markHandoff`: mark an unfinished target tab that must remain available for
  diagnosis or a later turn.
- `markDeliverable`: mark a successfully filled and verified target tab for
  the user to review and publish manually.

Mark every Agent-created target tab immediately after opening it as
`handoff`. After exact readback succeeds, replace that mark with
`deliverable`; the latest mark wins. Reapply the appropriate mark in every
later turn in which the tab must survive. Do not mark source, search,
inspection, duplicate, or blank tabs. A failed target tab remains marked as
`handoff` when it must stay open for diagnosis or a later turn.

`requestManualHandoff` is a separate control-transfer operation. It does not
replace tab marking and should be used only when the user explicitly needs to
take control and the selected browser supports it.

Before ending the turn, re-list live tabs and verify every marked target by
normalized URL. Record the mark result and persistence check. Never call a
close, discard, recycle, cleanup, or keep-list operation as a substitute for
marking. If the browser runtime has a separate control-release operation, use
its documented handoff only after marking and verification; it must preserve
the marked tabs.

Runtime session expiry, user-control locks, and tab-handle lifetime are
adapter-specific. Persist the URL and state before a possible expiry and
reacquire the tab by exact URL in a later turn; do not infer that an expired
handle means the tab was closed.

The report must separate:

```text
opened: true/false
filled: true/false
tab_mark: handoff|deliverable|none
persistence_verified: true/false
submitted: false
```
