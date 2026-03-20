#!/usr/bin/env python3
"""
Script to generate a starter skill template based on best practices.

This script creates a basic skill structure that follows the guidelines
from the agent-skills documentation.
"""

import json
import os
import pathlib
import sys
from datetime import datetime

def prompt_for_skill_info():
    """Prompt user for skill information."""
    print("Skill Template Generator")
    print("=" * 25)
    print("This script will help you create a new OpenCode skill.")
    print()
    
    # Get skill name
    while True:
        name = input("Skill name (lowercase, hyphens only, e.g., 'docker-manager'): ").strip()
        if not name:
            print("Please provide a skill name.")
            continue
        # Validate name format
        if not name.replace('-', '').isalnum():
            print("Skill name must contain only lowercase letters, numbers, and hyphens.")
            continue
        if name.startswith('-') or name.endswith('-'):
            print("Skill name cannot start or end with a hyphen.")
            continue
        if '--' in name:
            print("Skill name cannot contain consecutive hyphens.")
            continue
        break
    
    # Get skill description
    print("\nDescribe what your skill does and when to use it.")
    print("Be specific and 'pushy' to avoid under-triggering.")
    print("Example: 'Extract PDF text, fill forms, merge files. Use when handling PDFs.'")
    description = input("Skill description: ").strip()
    if not description:
        description = f"A skill for {name.replace('-', ' ')} tasks."
    
    # Get compatibility info (optional)
    print("\nCompatibility information (optional, press Enter to skip):")
    compatibility_input = input("Requirements (e.g., 'python >=3.10, node >=18'): ").strip()
    
    compatibility = []
    if compatibility_input:
        # Parse simple format
        for part in compatibility_input.split(','):
            part = part.strip()
            if part:
                compatibility.append(part)
    
    # Ask about optional fields
    print("\nOptional fields (press Enter to skip):")
    license_input = input("License (e.g., 'MIT', 'Apache-2.0'): ").strip()
    license_field = license_input if license_input else None
    
    return {
        "name": name,
        "description": description,
        "compatibility": compatibility if compatibility else None,
        "license": license_field
    }

def create_skill_directory(skill_info, base_path=None):
    """Create the skill directory structure."""
    if base_path is None:
        base_path = pathlib.Path.cwd()
    
    skill_dir = base_path / skill_info["name"]
    
    # Check if directory already exists
    if skill_dir.exists():
        overwrite = input(f"Directory {skill_dir} already exists. Overwrite? (y/n): ").lower().strip()
        if overwrite != 'y' and overwrite != 'yes':
            print("Operation cancelled.")
            return None
        # Remove existing directory
        import shutil
        shutil.rmtree(skill_dir)
    
    # Create directory structure
    skill_dir.mkdir(parents=True)
    (skill_dir / "scripts").mkdir()
    (skill_dir / "references").mkdir()
    (skill_dir / "assets").mkdir()
    (skill_dir / "evals").mkdir()
    
    print(f"Created skill directory: {skill_dir}")
    
    # Create SKILL.md
    create_skill_md(skill_dir, skill_info)
    
    # Create basic evals file
    create_evals_template(skill_dir / "evals" / "evals.json")
    
    # Create basic scripts directory placeholder
    create_scripts_placeholder(skill_dir / "scripts")
    
    # Create references directory placeholder
    create_references_placeholder(skill_dir / "references")
    
    # Create assets directory placeholder
    create_assets_placeholder(skill_dir / "assets")
    
    return skill_dir

def create_skill_md(skill_dir, skill_info):
    """Create the SKILL.md file."""
    skill_md_path = skill_dir / "SKILL.md"
    
    # Build frontmatter
    frontmatter_lines = ["---"]
    frontmatter_lines.append(f"name: {skill_info['name']}")
    frontmatter_lines.append(f"description: |")
    
    # Format description as multiline
    desc_lines = skill_info['description'].split('. ')
    for i, line in enumerate(desc_lines):
        if line and not line.endswith('.'):
            line += '.'
        if i == 0:
            frontmatter_lines.append(f"  {line}")
        else:
            frontmatter_lines.append(f"  {line}")
    
    # Add license if provided
    if skill_info['license']:
        frontmatter_lines.append(f"license: {skill_info['license']}")
    
    # Add compatibility if provided
    if skill_info['compatibility']:
        frontmatter_lines.append("compatibility:")
        for compat in skill_info['compatibility']:
            frontmatter_lines.append(f"  - {compat}")
    
    frontmatter_lines.append("---")
    
    # Build skill content
    content_lines = []
    content_lines.append("")
    content_lines.append("# " + skill_info['name'].replace('-', ' ').title())
    content_lines.append("")
    content_lines.append("## Overview")
    content_lines.append("")
    content_lines.append("This skill provides capabilities for " + skill_info['name'].replace('-', ' ') + ". ")
    content_lines.append("Follow the workflow below to use this skill effectively.")
    content_lines.append("")
    content_lines.append("## When to Use This Skill")
    content_lines.append("")
    content_lines.append("Use this skill when you need to " + skill_info['description'].lower() + "")
    content_lines.append("")
    content_lines.append("## Workflow")
    content_lines.append("")
    content_lines.append("1. **Step 1**: Describe what you want to accomplish")
    content_lines.append("2. **Step 2**: Provide any necessary input files or context")
    content_lines.append("3. **Step 3**: Let the skill guide you through the process")
    content_lines.append("4. **Step 4**: Review the output and provide feedback for improvement")
    content_lines.append("")
    content_lines.append("## Quick Start")
    content_lines.append("")
    content_lines.append("```bash")
    content_lines.append("# 1. Use the skill with a prompt")
    content_lines.append(f'opencode run "Your task here" --agent {skill_info["name"]}')
    content_lines.append("```")
    content_lines.append("")
    content_lines.append("## Available Scripts")
    content_lines.append("")
    content_lines.append("This skill includes helpful scripts in the `scripts/` directory.")
    content_lines.append("Check the individual script files for usage instructions.")
    content_lines.append("")
    content_lines.append("## References")
    content_lines.append("")
    content_lines.append("Additional reference materials are available in the `references/` directory.")
    content_lines.append("These are loaded on demand when needed for specific tasks.")
    content_lines.append("")
    content_lines.append("## Evaluation")
    content_lines.append("")
    content_lines.append("To evaluate this skill, test cases are provided in the `evals/` directory.")
    content_lines.append("Run the evaluation suite to see how the skill performs.")
    content_lines.append("")
    
    # Combine frontmatter and content
    full_content = "\n".join(frontmatter_lines) + "\n" + "\n".join(content_lines)
    
    # Write file
    skill_md_path.write_text(full_content)
    print(f"Created SKILL.md at {skill_md_path}")

def create_evals_template(evals_path):
    """Create a basic evals template."""
    evals_template = {
        "skill_name": "REPLACE_WITH_SKILL_NAME",
        "evals": [
            {
                "id": 1,
                "prompt": "REPLACE_WITH_YOUR_TEST_PROMPT",
                "expected_output": "DESCRIBE_WHAT_SUCCESS_LOOKS_LIKE",
                "files": [],
                "assertions": []
            }
        ]
    }
    
    evals_path.write_text(json.dumps(evals_template, indent=2))
    print(f"Created evals template at {evals_path}")

def create_scripts_placeholder(scripts_dir):
    """Create a placeholder for scripts directory."""
    readme_path = scripts_dir / "README.md"
    readme_path.write_text("# Scripts Directory\n\nThis directory contains executable scripts that the skill can run.\n\nAdd your scripts here and reference them from SKILL.md.\n")
    print(f"Created scripts placeholder at {readme_path}")

def create_references_placeholder(refs_dir):
    """Create a placeholder for references directory."""
    readme_path = refs_dir / "README.md"
    readme_path.write_text("# References Directory\n\nThis directory contains reference documentation that the skill can load on demand.\n\nAdd reference files here and reference them from SKILL.md when needed.\n")
    print(f"Created references placeholder at {readme_path}")

def create_assets_placeholder(assets_dir):
    """Create a placeholder for assets directory."""
    readme_path = assets_dir / "README.md"
    readme_path.write_text("# Assets Directory\n\nThis directory contains static resources like templates, images, and data files.\n\nAdd assets here and reference them from SKILL.md when needed.\n")
    print(f"Created assets placeholder at {readme_path}")

def main():
    """Main function."""
    # Get skill information from user
    skill_info = prompt_for_skill_info()
    
    # Ask where to create the skill
    print("\nWhere would you like to create the skill?")
    print("1. Current directory")
    print("2. Specify a path")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    base_path = None
    if choice == "2":
        path_input = input("Enter the base directory path: ").strip()
        if path_input:
            base_path = pathlib.Path(path_input)
            if not base_path.exists():
                print(f"Directory {base_path} does not exist.")
                create_anyway = input("Create it anyway? (y/n): ").lower().strip()
                if create_anyway != 'y' and create_anyway != 'yes':
                    print("Operation cancelled.")
                    return
                base_path.mkdir(parents=True)
    
    # Create the skill
    skill_dir = create_skill_directory(skill_info, base_path)
    
    if skill_dir:
        print(f"\nSkill '{skill_info['name']}' created successfully at: {skill_dir}")
        print("\nNext steps:")
        print("1. Review and customize the generated SKILL.md")
        print("2. Add your specific instructions and workflows")
        print("3. Create useful scripts in the scripts/ directory")
        print("4. Add reference materials to the references/ directory")
        print("5. Create realistic test cases in the evals/ directory")
        print("6. Test your skill with the evaluation workflow")
        print("\nTo use your skill:")
        print(f'  opencode run "Your task here" --agent {skill_info["name"]}')

if __name__ == "__main__":
    main()