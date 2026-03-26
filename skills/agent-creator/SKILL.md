---
name: agent-creator
description: Create OpenCode agents based on one or more data sources as references. Trigger when users want to build coding assistants, data analysts, or domain expert agents using documentation, code examples, API references, or tutorials.
license: MIT
compatibility: Requires OpenCode >=0.9.0
---

# Overview
This skill helps users create custom OpenCode agents by analyzing data sources and generating agent configurations. The created agents can be invoked when needed for specific tasks.

## Table of Contents
1. [CLI Reference](#cli-reference)
2. [Workflow](#workflow)
3. [Data Sources](#data-sources)
4. [Agent Types](#agent-types)
5. [Agent Configuration Options](#agent-configuration-options)
6. [Agents.md Best Practices](#agents-md-best-practices)
7. [Evaluation](#evaluation)
8. [Quick Start](#quick-start)

---

## CLI Reference
See [references/opencode/agents.mdx](references/opencode/agents.mdx) for detailed information about OpenCode agents.

---

## Workflow
The agent creation process follows these steps:

### 1. **Define Agent Purpose** – clarify what the agent should do
   * What tasks should the agent perform?
   * What domain or technology should it specialize in?
   * What level of expertise is required?
   * Should it be a primary agent (main assistant) or subagent (specialized helper)?

### 2. **Check for Existing Skills** – explore relevant existing skills
   * Search OpenCode skills directory for related functionality
   * Identify skills that could be incorporated or referenced
   * Consider how to leverage existing skills rather than duplicating effort

### 3. **Specify Data Sources** – provide reference materials
   * Documentation files (.md, .txt, .pdf)
   * Code examples and repositories
   * API references and specifications
   * Tutorials and guides
   * Both local files and web URLs supported

### 4. **Choose Agent Configuration** – select output format and mode
   * Skill directory with SKILL.md
   * Configuration files (JSON/YAML)
   * Prompt templates for direct use
   * Primary agent (main conversational agent) or subagent (specialized helper)

### 5. **Generate Agent** – create the agent based on inputs
   * Analyze data sources for patterns and best practices
   * Extract relevant knowledge and examples
   * Structure agent instructions and capabilities
   * Incorporate relevant existing skills when appropriate
   * Package as usable OpenCode agent

### 6. **Test and Refine** – validate the created agent
   * Run test prompts to verify agent behavior
   * Adjust based on performance and accuracy
   * Iterate until satisfactory results

---

## Data Sources
The agent creator accepts various types of data sources:

### Supported Formats
- **Documentation**: Markdown, text files, PDF guides
- **Code Examples**: Source code repositories, snippets, templates
- **API References**: OpenAPI/Swagger specs, function docs
- **Tutorials**: Step-by-step guides, walkthroughs, examples

### Source Specification
- Local file paths: `/path/to/documentation/`
- Web URLs: `https://example.com/docs/`
- Mixed sources: Combine files and URLs
- Interactive selection: Choose during creation process

### Best Practices
- Use authoritative, up-to-date sources
- Include diverse examples covering edge cases
- Prioritize recent versions of documentation
- Ensure sources are legally permissible to use

---

## Agent Types
Based on your requirements, the agent creator focuses on:

### Coding Assistants
- Help with programming tasks in specific languages
- Understand frameworks, libraries, and best practices
- Generate, debug, and explain code
- Follow coding standards and conventions

### Data Analysts
- Process and analyze datasets
- Create visualizations and reports
- Apply statistical methods and ML techniques
- Interpret results and provide insights

### Domain Experts
- Specialize in particular fields (medical, legal, finance, etc.)
- Understand industry-specific terminology and regulations
- Provide domain-specific advice and analysis
- Reference authoritative sources in the field

---

## Agent Configuration Options
When creating agents, use these configuration options from OpenCode (see [references/opencode/agents.mdx](references/opencode/agents.mdx) for full details):

### Mode
- **primary**: Main assistant you interact with directly
- **subagent**: Specialized assistant invoked via @ mention or Task tool
- **all**: Can be used as both (default)

### Permissions
Control what actions the agent can take:
- `"ask"` — Prompt for approval before running
- `"allow"` — Allow all operations without approval
- `"deny"` — Disable the tool

### Tools (deprecated - use permissions instead)
- `read`, `write`, `edit`, `bash`, `webfetch`

### Additional Options
- **model**: Override the default model for this agent
- **temperature**: Control response randomness (0.0-1.0)
- **steps**: Maximum agentic iterations before stopping
- **color**: Visual appearance in the UI
- **hidden**: Hide from @ autocomplete menu

### Example Agent Frontmatter
```markdown
---
description: Expert Python coding assistant
mode: subagent
permission:
  edit: ask
  bash:
    "*": ask
    "pytest *": allow
  webfetch: allow
temperature: 0.3
---

You are an expert Python developer...
```

---

## Agents.md Best Practices
This skill incorporates industry best practices for creating effective AGENTS.md files, which serve as configuration guides for AI agents:

### Core Principles
- **Keep it small and focused**: Ideal AGENTS.md should be under 150 lines
- **Lead with commands**: Put executable commands first for fast feedback
- **Use concrete examples**: Show what good output looks like with real code snippets
- **Set clear boundaries**: Define what agents can and cannot do autonomously
- **Apply progressive disclosure**: Link to detailed documentation instead of duplicating it
- **Avoid sensitive information**: Never include actual secrets, credentials, or private data

### Essential Sections (in priority order)
1. **Development environment setup**: Exact commands for dependency installation and configuration
2. **Build and test commands**: Prefer file-scoped commands for fast iteration
3. **Code style and conventions**: Formatting, naming patterns, architectural decisions
4. **Testing instructions**: Frameworks, locations, coverage expectations
5. **Project structure and key files**: Help agents navigate the codebase
6. **Safety and permission boundaries**: Define autonomous vs. approval-required actions
7. **Pull request and commit guidelines**: Ensure generated code follows team workflows

### Monorepo Support
- Use hierarchical AGENTS.md files: root for org-wide standards, subdirectories for tech-specific details
- Nearest file takes precedence, allowing context-specific guidance

### Common Mistakes to Avoid
- Including sensitive information (credentials, keys, etc.)
- Overly verbose documentation that wastes tokens
- Vague or ambiguous instructions
- Forcing full builds for every small change
- Unclear permission boundaries
- Lack of good/bad code examples
- Letting the file become outdated
- Improper handling of monorepos

See the references/agents_md/ directory for detailed guides on AGENTS.md best practices from industry experts.

---

## Evaluation
To ensure created agents work effectively:

### Testing Approach
1. Create test prompts representing real usage scenarios
2. Vary phrasing, detail level, and complexity
3. Cover edge cases and typical patterns
4. Evaluate agent responses for accuracy and relevance

### Quality Metrics
- **Relevance**: How well responses match the query intent
- **Accuracy**: Correctness of information provided
- **Completeness**: Thoroughness of answers
- **Clarity**: Understandability and organization of responses
- **Usefulness**: Practical applicability of the agent's output

### Iterative Improvement
- Review test results and identify weaknesses
- Refine data sources or agent instructions
- Retest until performance meets expectations
- Document lessons learned for future creations

---

## Quick Start
```bash
# 1. Create a new agent-creator skill instance
opencode run "Create a coding assistant agent for Python using the official Python documentation and popular library examples"

# 2. Specify agent purpose and type when prompted
#    - Tasks: Explain Python concepts, help with debugging, suggest improvements
#    - Type: Coding assistant
#    - Mode: Subagent (specialized helper)

# 3. Check for existing skills when prompted
#    - The skill will automatically search for relevant existing skills
#    - You can approve or deny incorporation of found skills

# 4. Specify data sources when prompted
#    - Local files: /path/to/python/docs/
#    - Web URLs: https://docs.python.org/3/, https://pypi.org/

# 5. Choose agent configuration when prompted
#    - Format: Skill directory
#    - Mode: Subagent

# 6. Test the created agent
opencode run "How do I implement a binary search algorithm in Python?"

# 7. Refine as needed based on results
```

---

## Contributing
Feel free to enhance this skill with:
- Additional data source types
- More agent templates
- Improved evaluation metrics
- Better source analysis algorithms
PRs are welcome.