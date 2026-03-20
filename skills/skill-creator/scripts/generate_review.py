#!/usr/bin/env python3
"""
Simple evaluation harness for the OpenCode *skill‑creator* meta‑skill.

The harness reads ``evals/evals.json`` which must contain a list of objects:
{
  "id": <int>,
  "prompt": "<text>",
  "expected": "<optional description>"
}

For each entry it runs two commands:
* **Baseline** – ``opencode run "<prompt>"`` with skills disabled.
* **With skill** – ``opencode run "<prompt>"`` with normal settings (the
  skill is triggered automatically via its description; no ``--agent`` flag is
  needed because ``skill‑creator`` is a *skill*, not an agent.

The script records execution time and the size of stdout, then writes a markdown
report to ``metrics/report.md``.
"""

import json, subprocess, time, pathlib, sys, os

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
EVALS_PATH = BASE_DIR / "evals" / "evals.json"
REPORT_PATH = BASE_DIR / "metrics" / "report.md"

def run_cmd(prompt: str, with_skill: bool) -> tuple[float, int]:
    """Run ``opencode run`` for *prompt*.

    *If* ``with_skill`` is ``False`` we explicitly disable skill loading via the
    ``OPENCODE_DISABLE_CLAUDE_CODE_SKILLS`` environment variable so the model
    behaves as the raw CLI. When ``with_skill`` is ``True`` we keep the default
    environment, allowing the meta‑skill to be triggered if its description matches
    the prompt.
    """
    cmd = ["opencode", "run", prompt]
    env = os.environ.copy()
    if not with_skill:
        env["OPENCODE_DISABLE_CLAUDE_CODE_SKILLS"] = "1"
    start = time.time()
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, env=env)
    except Exception:
        return (time.time() - start, 0)
    duration = time.time() - start
    size = len(result.stdout)
    return duration, size

def main():
    if not EVALS_PATH.is_file():
        print(f"Missing {EVALS_PATH}", file=sys.stderr)
        sys.exit(1)
    with open(EVALS_PATH) as f:
        data = json.load(f)
    lines = ["# Skill‑creator evaluation report", ""]
    lines.append("| ID | Prompt | Baseline time (s) | Skill time (s) | Baseline out size | Skill out size |")
    lines.append("|----|--------|-------------------|----------------|-------------------|----------------|")
    for entry in data:
        pid = entry.get("id")
        prompt = entry.get("prompt", "")
        bt, bs = run_cmd(prompt, with_skill=False)
        st, ss = run_cmd(prompt, with_skill=True)
        rows = f"| {pid} | {prompt.replace('|','\\|')} | {bt:.2f} | {st:.2f} | {bs} | {ss} |"
        lines.append(rows)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines))
    print(f"Report written to {REPORT_PATH}")

if __name__ == "__main__":
    main()
