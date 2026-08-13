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

If no user X tab is open to borrow (e.g. the user's Chrome only shows
`chrome://newtab`), the Agent Window shares the browser profile, so
`bsk tab create --session <sid> --url https://x.com/home` opens a *logged-in*
source tab for collection — same idea as the borrow-blocked fallback for
target tabs. Verify the tab title shows the home feed (e.g. `(n) 主页 / X`)
before collecting. This avoids the `tab borrow` auto-cancel that some
harnesses trigger.

## URL normalization

Normalize only URLs that can be proven to identify the main post:

1. Keep the `x.com` or `twitter.com` host and `/status/<id>` path.
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

## Detail-page readiness

For each selected URL, serially use an existing exact-URL target tab or create
one target tab. Check at most three times for all of the following:

- the current URL exactly equals the normalized target URL;
- the target main `article[data-testid="tweet"]` is present;
- the target author is visible;
- the complete main-post text is nonempty.

The target tab becomes a deliverable as soon as it is opened. If readiness
fails, retain it, record the reason, and do not create a replacement.

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
tweet region finishes rendering — the first `querySelector` returns null even
though the box exists. If the first probe is null, **scroll the page (or the
reply area) into view and wait 2–4s, then re-probe**; do not immediately fall
back to the reply dialog or skip the candidate. Verified in run
`xcp-20260813-1350-lfvj`: the first probe was null on two of three tabs, and a
re-probe after a short wait succeeded.

Ambiguous or hidden controls are a skip, not an invitation to use coordinates
or positional guesses. Fill only after the complete main post is verified.
Read back `innerText` or equivalent visible DOM text and require exact equality
with the draft. A Draft.js `value` or an enabled submit button is not proof of
successful fill.

### Filling X's Draft.js composer (verified method)

`bsk fill` does **not** register on X's `contenteditable` reply box (the
`value` is set but React/Draft.js ignores it, so readback comes back empty).

**Never use `document.execCommand('insertText')` here.** It desyncs Draft.js:

| tab state | result |
| --- | --- |
| tab not focused | text lands in the DOM only, Draft.js `editorState` stays empty → placeholder renders **on top of** the text (looks like overlapping glyphs), the reply button stays **gray/disabled**, and the user cannot edit, select, or paste |
| tab focused | the string is committed **twice** (native DOM insert + Draft.js state insert) |

Working procedure — clear with real input, insert through Draft.js only:

```bash
bsk tab select <tab> --session <sid>
bsk click --session <sid> --tab-id <tab> --selector 'div[data-testid="tweetTextarea_0"]'
```

1. **Select all via the Range API** (`Meta+a` / `Ctrl+a` through `bsk press`
   does *not* select inside Draft.js):

```js
var el = document.querySelector('div[data-testid="tweetTextarea_0"]');
el.focus();
var r = document.createRange(); r.selectNodeContents(el);
var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
```

2. **Delete with a real key** so Draft.js sees it: `bsk press 'Backspace'`.

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

### Sandbox limits and session lifetime

- `bsk evaluate` / `bsk click` only work on tabs **inside the Agent Window**.
  User-window tabs need `bsk tab borrow`, which some harnesses auto-cancel
  (`tab_borrow cancelled by user`). When borrow is blocked, open fresh Agent
  Window tabs for the same URLs, fix them there, hand those off, and tell the
  user to close the stale tabs — do not report the run as unfixable.
- Sessions die after roughly five minutes idle. Chain
  `session start` → `tab create` → fill → verify inside one command run, and
  re-check `bsk session list` at the start of every user turn instead of
  assuming a stored session id is alive.
- `bsk session stop <sid>` promotes the Agent Window into a normal user window
  and keeps its tabs; that is the handoff. There is no `--keep` flag.
- **The Agent Window blocks human input while the session is live** (the
  "agent is controlling" banner). The user cannot click, scroll, edit, or
  publish until the session stops. So stop the session as soon as readback
  passes — never leave a session open "just in case" — and if a turn ends
  without a handoff, say explicitly that the browser is still locked and how
  to release it. Verify release with `bsk browsers` (`SESSIONS` column) or
  `bsk session list`.

## Handoff and stopping

Before handoff, merge the current live-tab listing with the user-visible tab
listing and deduplicate by normalized URL. Keep only target tabs whose exact
URL and draft readback were verified. Run one `finalize({keep})` at most once;
do not include source, home, or inspection tabs. After the attempt, stop all
browser interaction, even if the result is an error. Never close tabs as part
of handoff.

**After content is written, do not close the filled reply tabs.** The handoff
is `bsk session stop <sid>`, which promotes the Agent Window into a normal
user window and **keeps** the filled tabs so the user can review and publish
manually. A filled box that shows empty after promotion means re-fill that one
tab — never treat it as a cleanup cue. Recycle/close only happens on the user's
explicit request.

The report must separate:

```text
opened: true/false
filled: true/false
handed_off: true/false
submitted: false
```
