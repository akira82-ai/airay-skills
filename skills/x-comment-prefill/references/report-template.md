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
  "current_stage": "preflight|collect|freeze|detail|handoff|complete|blocked",
  "browser": "chrome|edge",
  "goal": "engagement|traffic|discussion|custom",
  "topics": ["topic"],
  "allow_links": "never|natural-match-only|custom",
  "scan_count": 50,
  "source_tab_url": "https://x.com/...",
  "scanned_status_urls": [],
  "historical_status_urls": [],
  "frozen_candidates": [],
  "candidate_results": [],
  "finalize_attempted": false,
  "finalize_result": null,
  "delivered_as": "text|browser",
  "submitted": false
}
```

For `content-only`, do not create a browser run record. Return only the
supplied post, the evidence card, the draft or skip reason, and the promotion
level. Do not invent browser fields or a `finalize` result.

For `browser-prefill`, each candidate result should include `status_url`, `opened`, `filled`,
`handed_off`, `submitted`, `material_file`, `material_anchor`, `material_point`,
`trigger`, `ownership`, `promotion_level`, `failure_reason`, and, when filled`,
the exact draft or a safe hash plus the exact-readback result. For
`text-handoff`, use `status` of `drafted`, set `delivered_as: text`, include the
copy-ready `draft` and `post_link`, and omit `opened`/`filled`/`handed_off`
(nothing was filled). For `content-only`, return the evidence card and
draft/skip result directly; do not add browser state fields. When no accurate
match exists, use
For `browser-prefill`, use `skipped: no_accurate_local_match` and leave
`filled=false`. Do not store
cookies, tokens, or unnecessary private page content.

## User-facing report (`browser-prefill`)

```markdown
## X 评论预填结果

- run_id: `{run_id}`
- mode: `{content-only|text-handoff|browser-prefill}`
- delivered_as: `{text|browser}`
- 浏览器: `{browser}`
- 扫描: `{unique_count}/{scan_count}` 条去重 status URL
- 冻结候选: `{candidate_count}`
- finalize: `{success|failed|not attempted}`
- submitted: `false`

| # | 作者 | status URL | 主题 | 阅读量 | 回复量 | opened | filled | handed_off | 失败原因 |
|---|---|---|---|---:|---:|---|---|---|---|
| 1 | … | … | … | … | … | … | … | … | … |

### 评论草稿

1. `{status_url}`
   > {draft}

   - material: `{material_file}` — `{material_anchor}`
   - point: `{material_point}`
   - ownership: `{user-provided|source-derived}`
   - promotion: `{no_link|book_mention|book_mention_plus_link}`

### 原创灵感（最多两条）

| # | 标题 | 来自的具体问题 | 读者可拿走什么 | 建议如何验证 |
|---|---|---|---|---|
```

Never collapse `opened`, `filled`, `handed_off`, and `submitted` into one
“完成” field. If a candidate vanished, say `opened_but_not_filled`; if no local
material matched, say `skipped: no_accurate_local_match`; if a finalize call was
not allowed because a gate failed, say so explicitly.

For `text-handoff`, the table columns `opened`/`filled`/`handed_off` do not
apply — leave them blank and add a `delivered_as: text` line plus a copy-ready
block (post link + comment + promotion note) per candidate. Never claim a box
was filled or handed off; `submitted` stays `false`.
