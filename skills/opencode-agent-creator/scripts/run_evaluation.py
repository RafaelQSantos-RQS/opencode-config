#!/usr/bin/env python3
"""
Evaluation harness for the agent-creator skill.
"""

import json
import subprocess
import time
import pathlib
import sys
import os
import shutil
from datetime import datetime

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
EVALS_PATH = BASE_DIR / "evals" / "evals.json"
WORKSPACE_DIR = BASE_DIR / "agent-creator-workspace"
METRICS_DIR = BASE_DIR / "metrics"


def run_cmd(prompt: str, with_skill: bool, output_dir: pathlib.Path) -> dict:
    """Run opencode run for prompt and capture results."""
    cmd = ["opencode", "run", prompt]
    env = os.environ.copy()

    # For baseline runs, disable skill loading
    if not with_skill:
        env["OPENCODE_DISABLE_CLAUDE_CODE_SKILLS"] = "1"

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    start_time = time.time()
    try:
        # Run the command and capture output
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,  # Increased timeout for complex tasks
            env=env,
        )

        # Save stdout and stderr
        (output_dir / "stdout.txt").write_text(result.stdout)
        (output_dir / "stderr.txt").write_text(result.stderr)

        end_time = time.time()
        duration_ms = int((end_time - start_time) * 1000)

        # Try to extract token usage from stderr if available (this is approximate)
        total_tokens = 0
        stderr_lines = result.stderr.split("\n")
        for line in stderr_lines:
            if "tokens" in line.lower() and "total" in line.lower():
                # Try to extract a number
                import re

                numbers = re.findall(r"\d+", line)
                if numbers:
                    total_tokens = int(numbers[-1])  # Take the last number
                    break

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
            "duration_ms": duration_ms,
            "total_tokens": total_tokens,
            "output_size": len(result.stdout),
        }
    except subprocess.TimeoutExpired:
        end_time = time.time()
        duration_ms = int((end_time - start_time) * 1000)
        return {
            "success": False,
            "stdout": "",
            "stderr": "Command timed out after 120 seconds",
            "returncode": -1,
            "duration_ms": duration_ms,
            "total_tokens": 0,
            "output_size": 0,
        }
    except Exception as e:
        end_time = time.time()
        duration_ms = int((end_time - start_time) * 1000)
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Error running command: {str(e)}",
            "returncode": -2,
            "duration_ms": duration_ms,
            "total_tokens": 0,
            "output_size": 0,
        }


def save_timing_data(run_data: dict, output_dir: pathlib.Path):
    """Save timing data to timing.json."""
    timing_data = {
        "total_tokens": run_data.get("total_tokens", 0),
        "duration_ms": run_data.get("duration_ms", 0),
        "total_duration_seconds": run_data.get("duration_ms", 0) / 1000.0,
    }
    (output_dir / "timing.json").write_text(json.dumps(timing_data, indent=2))


def main():
    """Main evaluation function."""
    print("Starting agent-creator evaluation...")

    # Load test cases
    if not EVALS_PATH.is_file():
        print(f"Missing {EVALS_PATH}", file=sys.stderr)
        sys.exit(1)

    with open(EVALS_PATH) as f:
        evals_data = json.load(f)

    # Handle both old format (list) and new format (dict with skill_name and evals)
    if isinstance(evals_data, list):
        test_cases = evals_data
        skill_name = "agent-creator"
    else:
        test_cases = evals_data.get("evals", [])
        skill_name = evals_data.get("skill_name", "agent-creator")

    if not test_cases:
        print("No test cases found!", file=sys.stderr)
        sys.exit(1)

    # Create workspace directory with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    iteration_dir = WORKSPACE_DIR / f"iteration-{timestamp}"
    iteration_dir.mkdir(parents=True, exist_ok=True)

    print(f"Working in: {iteration_dir}")

    # Process each test case
    all_results = []

    for i, test_case in enumerate(test_cases):
        test_id = test_case.get("id", i + 1)
        prompt = test_case.get("prompt", "")
        expected_output = test_case.get("expected_output", "")

        print(f"\nProcessing test case {test_id}: {prompt[:50]}...")

        # Create test-specific directories
        test_name = f"eval-{test_id}-{prompt[:30].replace(' ', '_').replace('/', '_')}"
        test_dir = iteration_dir / test_name
        test_dir.mkdir(parents=True, exist_ok=True)

        # Run baseline (without skill)
        print("  Running baseline (no skill)...")
        baseline_dir = test_dir / "baseline"
        baseline_result = run_cmd(prompt, with_skill=False, output_dir=baseline_dir)
        save_timing_data(baseline_result, baseline_dir)

        # Run with skill
        print("  Running with skill...")
        skill_dir = test_dir / "with_skill"
        skill_result = run_cmd(prompt, with_skill=True, output_dir=skill_dir)
        save_timing_data(skill_result, skill_dir)

        # Save test metadata
        metadata = {
            "eval_id": test_id,
            "eval_name": test_name,
            "prompt": prompt,
            "expected_output": expected_output,
            "files": test_case.get("files", []),
            "assertions": test_case.get("assertions", []),
        }
        (test_dir / "eval_metadata.json").write_text(json.dumps(metadata, indent=2))

        # Store results for aggregation
        all_results.append(
            {
                "test_id": test_id,
                "prompt": prompt,
                "baseline": baseline_result,
                "with_skill": skill_result,
            }
        )

        print(
            f"  Baseline: {baseline_result['duration_ms']}ms, {baseline_result['total_tokens']} tokens"
        )
        print(
            f"  Skill: {skill_result['duration_ms']}ms, {skill_result['total_tokens']} tokens"
        )

    # Generate benchmark summary
    generate_benchmark(all_results, iteration_dir)

    # Generate human-readable report
    generate_report(all_results, iteration_dir)

    print(f"\nEvaluation complete! Results saved to: {iteration_dir}")
    print("Next steps:")
    print("1. Review the outputs in each test case directory")
    print("2. Draft assertions based on what you see")
    print("3. Update evals/evals.json with your assertions")
    print("4. Run the evaluation again to grade the skill")


def generate_benchmark(results: list, output_dir: pathlib.Path):
    """Generate benchmark.json summarizing the results."""
    if not results:
        return

    # Calculate statistics
    baseline_times = [
        r["baseline"]["duration_ms"] for r in results if r["baseline"]["success"]
    ]
    skill_times = [
        r["with_skill"]["duration_ms"] for r in results if r["with_skill"]["success"]
    ]
    baseline_tokens = [
        r["baseline"]["total_tokens"] for r in results if r["baseline"]["success"]
    ]
    skill_tokens = [
        r["with_skill"]["total_tokens"] for r in results if r["with_skill"]["success"]
    ]

    # Simple pass/fail based on success (would be replaced with assertion grading later)
    baseline_passes = sum(1 for r in results if r["baseline"]["success"])
    skill_passes = sum(1 for r in results if r["with_skill"]["success"])
    total_tests = len(results)

    benchmark = {
        "run_summary": {
            "baseline": {
                "pass_rate": {
                    "mean": baseline_passes / total_tests if total_tests > 0 else 0,
                    "stddev": 0,  # Would calculate properly with multiple runs
                },
                "time_seconds": {
                    "mean": sum(baseline_times) / len(baseline_times) / 1000.0
                    if baseline_times
                    else 0,
                    "stddev": 0,
                },
                "tokens": {
                    "mean": sum(baseline_tokens) / len(baseline_tokens)
                    if baseline_tokens
                    else 0,
                    "stddev": 0,
                },
            },
            "with_skill": {
                "pass_rate": {
                    "mean": skill_passes / total_tests if total_tests > 0 else 0,
                    "stddev": 0,
                },
                "time_seconds": {
                    "mean": sum(skill_times) / len(skill_times) / 1000.0
                    if skill_times
                    else 0,
                    "stddev": 0,
                },
                "tokens": {
                    "mean": sum(skill_tokens) / len(skill_tokens)
                    if skill_tokens
                    else 0,
                    "stddev": 0,
                },
            },
            "delta": {
                "pass_rate": (skill_passes / total_tests if total_tests > 0 else 0)
                - (baseline_passes / total_tests if total_tests > 0 else 0),
                "time_seconds": (
                    sum(skill_times) / len(skill_times) / 1000.0 if skill_times else 0
                )
                - (
                    sum(baseline_times) / len(baseline_times) / 1000.0
                    if baseline_times
                    else 0
                ),
                "tokens": (sum(skill_tokens) / len(skill_tokens) if skill_tokens else 0)
                - (
                    sum(baseline_tokens) / len(baseline_tokens)
                    if baseline_tokens
                    else 0
                ),
            },
        }
    }

    (output_dir / "benchmark.json").write_text(json.dumps(benchmark, indent=2))
    print(f"Benchmark saved to: {output_dir / 'benchmark.json'}")


def generate_report(results: list, output_dir: pathlib.Path):
    """Generate a human-readable markdown report."""
    lines = ["# Agent Creator Evaluation Report", ""]
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    lines.append("## Summary")
    lines.append("")
    lines.append(
        "| Test ID | Prompt | Baseline Time (s) | Skill Time (s) | Baseline Success | Skill Success |"
    )
    lines.append(
        "|---------|--------|-------------------|----------------|------------------|---------------|"
    )

    for result in results:
        baseline_time = result["baseline"]["duration_ms"] / 1000.0
        skill_time = result["with_skill"]["duration_ms"] / 1000.0
        baseline_success = "✓" if result["baseline"]["success"] else "✗"
        skill_success = "✓" if result["with_skill"]["success"] else "✗"

        # Truncate prompt for display
        prompt_display = (
            result["prompt"][:50] + "..."
            if len(result["prompt"]) > 50
            else result["prompt"]
        )

        lines.append(
            f"| {result['test_id']} | {prompt_display} | {baseline_time:.2f} | {skill_time:.2f} | {baseline_success} | {skill_success} |"
        )

    lines.append("")
    lines.append("## Details")
    lines.append("")

    for result in results:
        lines.append(f"### Test Case {result['test_id']}: {result['prompt']}")
        lines.append("")
        lines.append("**Baseline (No Skill):**")
        lines.append(
            f"- Status: {'Success' if result['baseline']['success'] else 'Failed'}"
        )
        lines.append(f"- Time: {result['baseline']['duration_ms']}ms")
        lines.append(f"- Tokens: {result['baseline']['total_tokens']}")
        lines.append(f"- Output size: {result['baseline']['output_size']} chars")
        if not result["baseline"]["success"]:
            lines.append(f"- Error: {result['baseline']['stderr'][:200]}...")
        lines.append("")
        lines.append("**With Skill:**")
        lines.append(
            f"- Status: {'Success' if result['with_skill']['success'] else 'Failed'}"
        )
        lines.append(f"- Time: {result['with_skill']['duration_ms']}ms")
        lines.append(f"- Tokens: {result['with_skill']['total_tokens']}")
        lines.append(f"- Output size: {result['with_skill']['output_size']} chars")
        if not result["with_skill"]["success"]:
            lines.append(f"- Error: {result['with_skill']['stderr'][:200]}...")
        lines.append("")
        lines.append("--")
        lines.append("")

    (output_dir / "report.md").write_text("\n".join(lines))
    print(f"Report saved to: {output_dir / 'report.md'}")


if __name__ == "__main__":
    main()
