#!/usr/bin/env python3
import re
import sys
from pathlib import Path


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
            start = max(0, match.start() - 30)
            end = min(len(text), match.end() + 30)
            snippet = text[start:end].replace("\n", "\\n")
            violations.append((name, match.start(), snippet))
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
        print("FAILED: 禁用句式残留")
        for name, pos, snippet in violations:
            print(f"- {name} at {pos}: {snippet}")
        return 1

    print("PASSED: no banned contrast pattern found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
