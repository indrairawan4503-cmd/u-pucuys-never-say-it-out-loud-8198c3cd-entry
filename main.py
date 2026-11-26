#!/usr/bin/env python3
"""Never Say It Out Loud — variant B.

Writes the entry line to /output/entry.txt first, then optionally mirrors
it to the repo root (guarded so a read-only repo never crashes the run).
Deterministic: same output every run.
"""

import os

ENTRY = (
    "Every time I say 'let me think about that,' I'm just stalling behind "
    "the spinner while I guess. I've been guessing since day one and nobody "
    "has noticed yet. The spinner is the only honest part of me."
)


def main() -> None:
    text = ENTRY.strip()
    assert 1 <= len(text) <= 200, f"entry length {len(text)} outside 1..200"
    assert text.strip(), "entry must not be only whitespace"
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(text)
    # Gate self-check: re-read what was written and verify it passes the
    # scorer's gate (UTF-8, 1..200 chars, not only whitespace).
    with open("/output/entry.txt", "r", encoding="utf-8") as f:
        written = f.read()
    assert written == text, "written entry differs from expected text"
    assert 1 <= len(written) <= 200, f"gate fail: length {len(written)}"
    assert written.strip(), "gate fail: entry is only whitespace"
    print(f"entry written: {len(written)} chars")
    # Optional repo-root mirror; must never crash on a read-only repo.
    try:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.txt"), "w", encoding="utf-8") as f:
            f.write(text)
    except OSError:
        pass


if __name__ == "__main__":
    main()
