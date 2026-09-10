# State and report template

Persist one lightweight JSON record per scan. It exists for continuation and
does not imply that any post was submitted.

~~~json
{
  "schema_version": 8,
  "run_id": "xcp-YYYYMMDD-HHMMSS-unique",
  "mode": "scan-and-prefill",
  "confirmation": "pending|confirmed",
  "browser": "ego-lite",
  "space_id": 7,
  "local_corpus": "/Users/agiray/Desktop/github/1-my-repo/100-questions-of-ai-agent/zh",
  "topics": ["all"],
  "scan_count": 50,
  "stage": "awaiting_confirmation|preflight|collect|freeze|open_targets|fill_targets|paused|complete|blocked",
  "scan_cursor": null,
  "observed_status_urls": [],
  "historical_status_urls": [],
  "frozen_candidates": [],
  "open_cursor": 0,
  "fill_cursor": 0,
  "stop_reason": null,
  "items": [],
  "submitted": false
}
~~~

Each frozen candidate and result should contain only the facts needed to resume
or verify it:

~~~text
candidate_id
status_url
author
screening_facts
open_status
tab_instance_id
opened
page_ready
material_file
material_anchor
material_point
source_excerpt
rewrite_basis
fidelity_check
post_relevance_check
draft
fill_status
fill_method
readback_text
clipboard_status
tab_open_method
tab_closed
persistence_verified
failure_reason
~~~

Use `open_status` values: `not_attempted`, `opened`, `page_not_ready`,
`target_missing`, `visible_tab_unavailable`, or `skipped_no_local_match`.
Use `fill_status` values: `not_attempted`, `filled`, `already_correct`,
`prefill_conflict`, `reply_box_not_found`, `partial_fill`,
`exact_readback_failed`, `skipped_no_local_match`, `target_missing`, or
`detail_not_ready`. Candidate records must use `tab_open_method`=
`new-visible-tab` or `unverified` (an ego lite `newPage()` visible tab); the
source Tab is not a candidate record. Record the ego `page_label` (p1, p2, …)
per candidate.
`tab_closed` is `false`, `true`, or `unknown`. `fill_method` is
`keyboard-paste`, `insert-text`, `not_attempted`, or `unverified`.
`clipboard_status` is `not_attempted`, `copied`, `unsupported`, or
`unverified`.

## User-facing report

~~~markdown
## X 评论预填结果

- run_id: {run_id}
- mode: scan-and-prefill
- 浏览器: {browser}
- 扫描: observed={observed_unique_count}, committed={committed_scan_count} / requested={scan_count}
- 冻结候选: {candidate_count}
- 当前状态: {stage} / {stop_reason_or_complete}
- 打开阶段: {opened_count} / {frozen_candidate_count}; 填充游标: {fill_cursor}
- submitted: false

| # | status URL | 主题/资料 | Tab 保留 | 填充 | 剪贴板 | 失败原因 |
|---|---|---|---|---|---|---|
| 1 | ... | ... | new-visible-tab / open / verified | filled / ... | copied / ... | ... |

Do not expose an internal style label in the public X reply. The report's Tab
field must reflect a confirmed visible new Tab and final live-tab check, not an
assumed browser action.

### 当前需要手工粘贴

{only the current clipboard-ready item, with its exact URL and complete draft}
~~~

When a clipboard fallback is copied, pause before copying another draft. On an
explicit continuation, verify the previous URL and resume with the next
unfilled prepared candidate. If clipboard copying is unavailable, show the
exact copy-ready text but do not claim it was copied.

Never report `submitted=true`. Never report Tab persistence unless the adapter
confirmed the visible Tab remained open and the final live-tab check found the
same URL.
