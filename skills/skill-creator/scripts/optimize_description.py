#!/usr/bin/env python3
"""
Script to help optimize skill descriptions for better triggering accuracy.

This script implements a simplified version of the description optimization loop
described in the agent-skills documentation.
"""

import json
import subprocess
import time
import pathlib
import sys
import os
from datetime import datetime

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
EVALS_PATH = BASE_DIR / "evals" / "trigger_eval.json"
SKILL_PATH = BASE_DIR
SKILL_MD_PATH = SKILL_PATH / "SKILL.md"

def load_skill_description():
    """Load the current skill description from SKILL.md."""
    if not SKILL_MD_PATH.exists():
        print(f"SKILL.md not found at {SKILL_MD_PATH}", file=sys.stderr)
        return None
    
    content = SKILL_MD_PATH.read_text()
    # Extract description from YAML frontmatter
    lines = content.split('\n')
    in_frontmatter = False
    description_lines = []
    
    for line in lines:
        if line.strip() == '---':
            if not in_frontmatter:
                in_frontmatter = True
                continue
            else:
                break  # End of frontmatter
        elif in_frontmatter and line.startswith('description:'):
            # Handle multiline description
            if '|' in line or '>' in line:
                # Multiline format
                desc_start = line.find('|') + 1 if '|' in line else line.find('>') + 1
                if desc_start > 0:
                    desc_indent = len(line) - len(line.lstrip())
                    description_lines.append(line[desc_start:].rstrip())
                else:
                    description_lines.append('')
            else:
                # Single line format
                description_lines.append(line.split(':', 1)[1].strip())
        elif in_frontmatter and line.startswith(' ') and description_lines:
            # Continuation of multiline description
            description_lines.append(line.rstrip())
        elif in_frontmatter and not line.startswith(' ') and line.strip() and not line.startswith('#'):
            # Another field started
            break
    
    return '\n'.join(description_lines).strip()

def save_skill_description(description):
    """Save a new description to SKILL.md."""
    if not SKILL_MD_PATH.exists():
        print(f"SKILL.md not found at {SKILL_MD_PATH}", file=sys.stderr)
        return False
    
    content = SKILL_MD_PATH.read_text()
    lines = content.split('\n')
    in_frontmatter = False
    frontmatter_end = 0
    description_start = -1
    description_end = -1
    
    for i, line in enumerate(lines):
        if line.strip() == '---':
            if not in_frontmatter:
                in_frontmatter = True
                continue
            else:
                frontmatter_end = i
                break
        elif in_frontmatter and line.startswith('description:'):
            description_start = i
            # Find end of description (next field or end of frontmatter)
            for j in range(i+1, len(lines)):
                if j >= frontmatter_end or (lines[j].strip() and not lines[j].startswith(' ') and ':' in lines[j]):
                    description_end = j
                    break
            if description_end == -1:
                description_end = frontmatter_end
            break
    
    if description_start == -1 or description_end == -1:
        print("Could not find description field in SKILL.md", file=sys.stderr)
        return False
    
    # Build new content
    new_lines = lines[:description_start]
    
    # Add new description
    if '\n' in description:
        # Multiline format
        new_lines.append('description: |')
        for desc_line in description.split('\n'):
            new_lines.append(f'  {desc_line}')
    else:
        # Single line format
        new_lines.append(f'description: {description}')
    
    # Add remaining lines
    new_lines.extend(lines[description_end:])
    
    # Write back
    SKILL_MD_PATH.write_text('\n'.join(new_lines))
    return True

def run_trigger_test(prompt, skill_enabled=True, runs=3):
    """Run a trigger test and return the trigger rate."""
    triggers = 0
    
    for _ in range(runs):
        cmd = ["opencode", "run", prompt]
        env = os.environ.copy()
        
        if not skill_enabled:
            env["OPENCODE_DISABLE_CLAUDE_CODE_SKILLS"] = "1"
        
        try:
            # We'll check if the skill was invoked by looking for skill-specific output
            # In a real implementation, we'd check logs or tool usage
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, env=env)
            
            # Simple heuristic: if the output contains skill-related keywords, assume it triggered
            # This is a simplification - real implementation would be more sophisticated
            output = result.stdout.lower()
            if "skill" in output or "create" in output or "manage" in output:
                triggers += 1
        except Exception:
            pass  # Count as failure to trigger
    
    return triggers / runs if runs > 0 else 0

def main():
    """Main function for description optimization."""
    print("Skill Description Optimization Tool")
    print("=" * 40)
    
    # Load current description
    current_desc = load_skill_description()
    if current_desc is None:
        sys.exit(1)
    
    print(f"Current description:\n{current_desc}\n")
    
    # Load or create trigger evaluation set
    if EVALS_PATH.exists():
        with open(EVALS_PATH) as f:
            trigger_evals = json.load(f)
    else:
        # Create a basic set if none exists
        trigger_evals = [
            {"query": "How do I create a new OpenCode skill?", "should_trigger": True},
            {"query": "Can you help me improve my skill's description?", "should_trigger": True},
            {"query": "I want to automate my OpenCode workflow", "should_trigger": True},
            {"query": "What's the weather today?", "should_trigger": False},
            {"query": "How do I cook pasta?", "should_trigger": False},
            {"query": "Explain machine learning concepts", "should_trigger": False}
        ]
        # Save for future use
        EVALS_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(EVALS_PATH, 'w') as f:
            json.dump(trigger_evals, f, indent=2)
    
    print(f"Testing with {len(trigger_evals)} evaluation queries...")
    
    # Test current description
    print("\nTesting current description:")
    should_trigger_pass = 0
    should_not_trigger_pass = 0
    
    for eval_item in trigger_evals:
        query = eval_item["query"]
        should_trigger = eval_item["should_trigger"]
        
        trigger_rate = run_trigger_test(query, skill_enabled=True)
        
        if should_trigger:
            passed = trigger_rate >= 0.5
            if passed:
                should_trigger_pass += 1
            status = "PASS" if passed else "FAIL"
            print(f"  [SHOULD TRIGGER] '{query}' -> {trigger_rate:.2f} ({status})")
        else:
            passed = trigger_rate < 0.5
            if passed:
                should_not_trigger_pass += 1
            status = "PASS" if passed else "FAIL"
            print(f"  [SHOULD NOT TRIGGER] '{query}' -> {trigger_rate:.2f} ({status})")
    
    total_pass = should_trigger_pass + should_not_trigger_pass
    total_tests = len(trigger_evals)
    print(f"\nCurrent description score: {total_pass}/{total_tests} ({total_pass/total_tests*100:.1f}%)")
    
    # Ask if user wants to optimize
    if total_pass < total_tests:
        response = input("\nWould you like to optimize the description? (y/n): ").lower().strip()
        if response == 'y' or response == 'yes':
            print("\nDescription optimization would normally involve:")
            print("1. Identifying failing queries")
            print("2. Generating improved descriptions using an LLM")
            print("3. Testing each improvement")
            print("4. Selecting the best performing description")
            print("\nFor now, please manually edit the description field in SKILL.md")
            print("based on the failing test cases above.")
        else:
            print("Skipping optimization.")
    else:
        print("\nAll tests passing! Description is well optimized.")

if __name__ == "__main__":
    main()