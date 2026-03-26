---
name: skill-creator
description: Build, refine and evaluate OpenCode skills. Trigger this skill whenever the user talks about "skill", "opencode", "cli", "agent", "mcp", "model", "serve", "web", "github", "plugin" or wants to automate OpenCode workflows. This description is intentionally "pushy" to avoid under‑triggering.
license: MIT
compatibility: Requires Python >=3.10, Node >=18, and OpenCode >=0.9.0
---

# Overview
This skill provides a **plug‑and‑play** package that, once copied into your `~/.config/opencode/skills/` directory, works out‑of‑the‑box. No extra registration commands are required.

## Table of Contents
1. [CLI Reference](#cli-reference)
2. [Agents, MCP & Models](#agents-mcp-models)
3. [Servers (serve / web)](#servers-serve-web)
4. [GitHub & Plugins](#github-plugins)
5. [Evaluation Workflow](#evaluation-workflow)
6. [Quick Start (copy & use)](#quick-start)

---

## CLI Reference
See [references/opencode/cli.mdx](references/opencode/cli.mdx) for detailed CLI reference information.

---

## Agents, MCP & Models
See the following references for detailed information:
- [references/opencode/agents.mdx](references/opencode/agents.mdx)
- [references/opencode/mcp-servers.mdx](references/opencode/mcp-servers.mdx)
- [references/opencode/models.mdx](references/opencode/models.mdx)

---

## Servers (serve / web)
See the following references for detailed information:
- [references/opencode/serve.mdx](references/opencode/serve.mdx)
- [references/opencode/web.mdx](references/opencode/web.mdx)

---

## GitHub & Plugins
See the following references for detailed information:
- [references/opencode/github.mdx](references/opencode/github.mdx)
- [references/opencode/plugins.mdx](references/opencode/plugins.mdx)

---

## Meta‑skill Workflow (R&D Loop)
The purpose of this skill is to **guide the user through creating, improving, and evaluating OpenCode skills**. Follow the loop below:

### 1. **Capture Intent** – ask the user:
   * What capability should the new skill provide?
   * When should it trigger? (keywords, context)
   * Desired output format?
   * Should we set up test cases to verify the skill works? (Objective outputs benefit from test cases; subjective ones may not need them)
   * **Update References**: Do you want to update the reference documentation now? (Run `scripts/update-references.sh`)

### 2. **Interview & Research** – probe edge‑cases, dependencies, and reference materials:
   * Check available reference files in `references/opencode/` for technical details
   * Ask about input/output formats, example files, success criteria
   * Research similar skills or best practices if needed

### 3. **Draft SKILL.md Structure** – generate a skeleton with:
   * Front‑matter (name, description, compatibility)
   * Section outline based on skill complexity
   * Follow progressive disclosure: keep main SKILL.md under 500 lines
   * Reference external documentation when needed

### 4. **Create Test Prompts** – build 2‑3 realistic prompts:
   * Start with what a real user would actually say
   * Vary phrasing (formal/casual), detail level, and complexity
   * Cover edge cases and typical usage patterns
   * Save to `evals/evals.json` without assertions initially

### 5. **Run Evaluation Harness**:
   ```bash
   python scripts/run_evaluation.py
   ```
   * Runs baseline (no skill) and with-skill versions in parallel
   * Captures timing data and output metrics
   * Prepares for human review and assertion drafting

### 6. **While runs are in progress, draft assertions**:
   * Review outputs to determine what "good" looks like
   * Create objectively verifiable checks for each test case
   * Update `evals/evals.json` with assertions
   * Explain what each assertion validates to the user

### 7. **Grade, aggregate, and launch viewer**:
   * Grade each run against assertions (save to grading.json)
   * Aggregate results into benchmark.json with pass rates, timing, tokens
   * Run analyst pass to identify patterns in the data
   * Launch evaluation viewer for qualitative and quantitative review

### 8. **Read feedback and improve**:
   * Focus on test cases with specific complaints
   * Generalize from feedback rather than overfitting to examples
   * Keep skill lean by removing unproductive steps
   * Explain the reasoning behind instructions
   * Bundle repeated work into scripts/ directory

### 9. **Iterate**:
   * Apply improvements to the skill
   * Rerun all test cases in a new iteration directory
   * Review with human feedback
   * Repeat until satisfied or no meaningful progress

When the loop converges, the user can **copy the generated folder** into their OpenCode `skills/` directory and start using the new skill immediately.

---

## Quick Start (copy‑and‑use)
```bash
# 1. Copy the skill folder into your OpenCode skills directory
cp -r /path/to/skill-creator ~/.config/opencode/skills/

# 2. Run a test prompt using the skill
opencode run "Explain closures in JavaScript"

# 3. Run the evaluation suite (optional)
python scripts/generate_review.py
```
No `opencode skill add` command is necessary – the skill is discovered automatically when placed in the skills folder.

---

## Contributing
Feel free to add more scripts, update the reference docs, or improve the evaluation harness. PRs are welcome.

---
*Following Agent Skills specification for proper progressive disclosure and best practices*