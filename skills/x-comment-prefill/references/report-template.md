# State and report template

## Run state (browser-prefill and text-handoff)

Persist one JSON or Markdown record for the active run. By default use
`.x-comment-prefill/runs/{run_id}.json` under the current project; if that path
is unavailable, use the task workspace and report the fallback path. Use this
minimum shape:

```json
{
  "run_id": "xcp-YYYYMMDD-HHMMSS-unique",
  "mode": "content-only|text-handoff|browser-prefill",
  "current_stage": "awaiting_confirmation|preflight|collect|freeze|detail|delivery|complete|blocked",
  "browser": "chrome|edge",
  "run_intent": "new_scan|resume",
  "goal": "followers|engagement|traffic|discussion|custom",
  "topics": ["topic"],
  "allow_links": "never|natural-match-only|custom",
  "scan_count": 50,
  "source_tab_url": "https://x.com/...",
  "scanned_status_urls": [],
  "historical_status_urls": [],
  "frozen_candidates": [],
  "candidate_results": [],
  "tab_marking": "not_attempted|partial|complete",
  "persistence_verified": false,
  "confirmation": "pending|confirmed",
  "delivered_as": "text|browser",
  "submitted": false
}
```

For `content-only`, do not create a browser run record. Return only the
supplied post, the evidence card, the draft or skip reason, and the promotion
level. Do not invent browser fields or a tab-marking result. When no accurate
local match exists, return `skipped: no_accurate_local_match` without a draft.

For `browser-prefill`, each candidate result should include `status_url`,
  `status`, `opened`, `filled`, `tab_mark`, `persistence_verified`, `submitted`, `material_file`,
`material_anchor`, `material_point`, `trigger`, `ownership`,
`promotion_level`, `textbox_discovery`, `failure_reason`, and, when filled, the
exact draft or a safe hash plus the exact-readback result. For browser-prefill,
`textbox_discovery` records `probe_count`, `scroll_count`, `elapsed_ms`, and
`stop_reason`; use `stop_reason: success` before filling. When no accurate local match exists,
set `status: skipped`, `reason: no_accurate_local_match`, and `filled=false`.

For `text-handoff`, use `status: drafted`, set `delivered_as: text`, include
  the copy-ready `draft` and `post_link`, and omit `opened`/`filled`/`tab_mark`
(nothing was filled).

Do not store cookies, tokens, or unnecessary private page content.

## User-facing report (`browser-prefill`)

```markdown
## X 评论预填结果

- run_id: `{run_id}`
- run_intent: `{new_scan|resume}`
- mode: `{content-only|text-handoff|browser-prefill}`
- confirmation: `{pending|confirmed}`
- delivered_as: `{text|browser}`
- 浏览器: `{browser}`
- 扫描: `{unique_count}/{scan_count}` 条去重 status URL
- 冻结候选: `{candidate_count}`
- tab marking: `{success|failed|not attempted}`
- persistence verified: `{true|false}`
- submitted: `false`

| # | 作者 | status URL | 主题 | 阅读量 | 回复量 | opened | filled | tab_mark | persistence_verified | 失败原因 |
|---|---|---|---|---:|---:|---|---|---|---|---|
| 1 | … | … | … | … | … | … | … | … | … |

### 评论草稿

1. `{status_url}`
   > {draft}

   - material: `{material_file}` — `{material_anchor}`
   - point: `{material_point}`
   - ownership: `{user-provided|source-derived}`
   - promotion: `{no_link|book_mention|book_mention_plus_link}`
   - textbox discovery: `{probe_count}` probes, `{scroll_count}` scrolls,
     `{elapsed_ms}` ms, stop=`{stop_reason}`

### 原创灵感（最多两条）

| # | 标题 | 来自的具体问题 | 读者可拿走什么 | 建议如何验证 |
|---|---|---|---|---|
```

Never collapse `opened`, `filled`, `tab_mark`, `persistence_verified`, and
`submitted` into one “完成” field. If a candidate vanished, say
`opened_but_not_filled`; if no local material matched, say
`skipped: no_accurate_local_match`; if tab marking was not possible because a
gate failed, say so explicitly.

For `text-handoff`, the table columns `opened`/`filled`/`tab_mark` do not
apply — leave them blank and add a `delivered_as: text` line plus a copy-ready
block (post link + comment + promotion note) per candidate. Never claim a box
was filled or a browser tab was delivered; `submitted` stays `false`.
