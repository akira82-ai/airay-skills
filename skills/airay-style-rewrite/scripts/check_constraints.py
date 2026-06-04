#!/usr/bin/env python3
import re
import sys
from pathlib import Path


LITERAL_RULES = [
    ("template_connector", [
        "首先",
        "其次",
        "最后",
        "综上",
        "综上所述",
        "总的来说",
        "总而言之",
        "本质上",
        "核心在于",
        "换句话说",
        "由此可见",
        "值得注意的是",
    ]),
    ("abstract_buzzword", [
        "赋能",
        "提效",
        "优化体验",
        "重塑",
        "范式",
        "生态",
        "闭环",
        "价值沉淀",
        "底层逻辑",
        "长期主义",
        "影响力",
        "认知升级",
    ]),
    ("balanced_formula", [
        "既有优势，也有不足",
        "不能简单地说好或坏",
        "需要辩证看待",
        "在带来机会的同时，也带来了挑战",
    ]),
    ("report_summary", [
        "未来可期",
        "值得持续关注",
        "具有重要意义",
        "具备广阔前景",
        "仍有优化空间",
        "是一个值得思考的问题",
    ]),
]


REGEX_RULES = [
    ("balanced_formula", re.compile(r"一方面[\s\S]{0,80}另一方面")),
]


def snippet_at(text, start, end):
    left = max(0, start - 30)
    right = min(len(text), end + 30)
    return text[left:right].replace("\n", "\\n")


def find_violations(text):
    neg = "不是"
    turn = "而" + "是"
    patterns = [
        ("same_sentence", re.compile(rf"{neg}[^。！？\n]{{0,80}}{turn}")),
        ("comma_sentence", re.compile(rf"{neg}[^。！？\n]{{0,80}}[，,、；;：:][^。！？\n]{{0,80}}{turn}")),
        ("cross_sentence", re.compile(rf"{neg}[\s\S]{{0,120}}{turn}")),
    ]
    violations = []
    for name, pattern in patterns:
        for match in pattern.finditer(text):
            violations.append((
                name,
                match.start(),
                snippet_at(text, match.start(), match.end()),
            ))
    for name, words in LITERAL_RULES:
        for word in words:
            start = text.find(word)
            while start != -1:
                end = start + len(word)
                violations.append((name, start, snippet_at(text, start, end)))
                start = text.find(word, end)
    for name, pattern in REGEX_RULES:
        for match in pattern.finditer(text):
            violations.append((
                name,
                match.start(),
                snippet_at(text, match.start(), match.end()),
            ))
    return violations


def main():
    if len(sys.argv) != 2:
        print("Usage: check_constraints.py <file>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2

    text = path.read_text(encoding="utf-8")
    violations = find_violations(text)
    if violations:
        print("FAILED: AI 味硬规则残留")
        for name, pos, snippet in violations:
            print(f"- {name} at {pos}: {snippet}")
        return 1

    print("PASSED: no hard-rule violations found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
