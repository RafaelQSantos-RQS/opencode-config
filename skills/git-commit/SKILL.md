---
name: git-commit
description: Execute git commit with conventional commit message analysis, intelligent staging, and message generation. Use when user asks to commit changes, create a git commit, or mentions "/commit". Supports: (1) Auto-detecting type and scope from changes, (2) Generating conventional commit messages from diff, (3) Interactive commit with optional type/scope/description overrides, (4) Intelligent file staging for logical grouping.
license: MIT
allowed-tools: Bash, Read, Glob, Grep
---

# Git Commit (Conventional Commits 1.0.0)

## Overview
This skill automates the creation of semantic git commits by analyzing codebase changes and strictly adhering to the **Conventional Commits 1.0.0** specification. It ensures project history is structured, machine-readable, and aligned with Semantic Versioning (SemVer).

## Reference Material
For the full technical specification of Conventional Commits 1.0.0, refer to:
- `references/conventional-commits.md`

## Workflow (Required: Create a Todo List for the User)
Before executing any changes, you MUST create a structured todo list using the `todowrite` tool to track the following steps:
1.  **Analyze**: Run `git status` and `git diff` to understand changes.
2.  **Stage**: Add relevant files using `git add`.
3.  **Draft**: Generate a Conventional Commit message.
4.  **Commit**: Execute `git commit`.

### 1. Analyze Changes
Examine the current state of the repository to understand the context of the work.
```bash
git status --porcelain
git diff              # Unstaged changes
git diff --staged     # Staged changes
```

### 2. Determine Intent & Category
Based on the diff, categorize the change according to the specification:
- **feat**: New feature (correlates with SemVer MINOR).
- **fix**: Bug fix (correlates with SemVer PATCH).
- **docs**: Documentation changes only.
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc).
- **refactor**: A code change that neither fixes a bug nor adds a feature.
- **perf**: A code change that improves performance.
- **test**: Adding missing tests or correcting existing tests.
- **build**: Changes that affect the build system or external dependencies.
- **ci**: Changes to CI configuration files and scripts.
- **chore**: Other changes that don't modify src or test files.
- **revert**: Reverts a previous commit.

### 3. Handle Breaking Changes
A breaking change MUST be indicated by:
1.  Appending a `!` after the type/scope (e.g., `feat(api)!: drop support for v1`).
2.  AND/OR including a `BREAKING CHANGE:` footer.
*Preference: Use `!` for visibility in the summary and a footer for detailed explanation.*

### 4. Construct the Message
- **Type**: Noun (feat, fix, etc.).
- **Scope (Optional)**: Noun describing a section of the codebase (e.g., `fix(parser):`).
- **Description**: Short summary in the **imperative, present tense** ("add", not "added").
- **Body (Optional)**: Detailed explanation, separated by a blank line.
- **Footer (Optional)**: External references (e.g., `Refs: #123`) or Breaking Change notes.

### 5. Execution
Stage relevant files and execute the commit.
```bash
git add <files>
git commit -m "<message>"
```

## Safety Protocol
- **Secrets**: NEVER commit files like `.env`, `credentials.json`, or private keys.
- **Force**: NEVER run destructive commands (`--force`, `hard reset`) unless explicitly requested.
- **Hooks**: If a commit fails due to a pre-commit hook, fix the issue and create a **NEW** commit. NEVER use `--no-verify` or `--amend` unless instructed.
- **Main Branch**: Warn the user before committing directly to `main` or `master`.
