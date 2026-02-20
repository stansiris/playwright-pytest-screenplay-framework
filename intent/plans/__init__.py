"""Utilities for extracting actionable steps from user documentation."""

from __future__ import annotations

import re

_STEP_PREFIX = re.compile(r"^\s*(?:[-*]\s+|\d+[.)]\s+)?(?P<step>.+?)\s*$")


def extract_documented_steps(documentation: str) -> list[str]:
    """
    Extract non-empty user steps from free-form documentation.

    Supports markdown bullets/numbering and raw code snippets. Non-step lines
    like imports/function declarations are ignored.
    """

    if not documentation or not documentation.strip():
        raise ValueError("Documentation cannot be empty.")

    steps: list[str] = []
    for raw_line in documentation.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        if line.startswith("```"):
            continue
        if line.startswith("import ") or line.startswith("from "):
            continue
        if re.match(r"^def\s+\w+\(", line):
            continue

        match = _STEP_PREFIX.match(line)
        if not match:
            continue

        step = match.group("step").strip()
        if step:
            steps.append(step)

    if not steps:
        raise ValueError("No actionable steps were found in documentation.")

    return steps
