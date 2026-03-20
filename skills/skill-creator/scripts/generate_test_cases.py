#!/usr/bin/env python3
"""
Script to help generate realistic test cases for skill evaluation.

This script guides users through creating effective test prompts that
follow the guidelines from the agent-skills documentation.
"""

import json
import pathlib
import sys

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
EVALS_PATH = BASE_DIR / "evals" / "evals.json"

def load_existing_evals():
    """Load existing evals if they exist."""
    if EVALS_PATH.exists():
        try:
            with open(EVALS_PATH) as f:
                data = json.load(f)
                # Handle both formats
                if isinstance(data, list):
                    return {"skill_name": "unknown", "evals": data}
                else:
                    return data
        except Exception:
            pass
    # Return default structure
    return {"skill_name": "unknown", "evals": []}

def save_evals(data):
    """Save evals to file."""
    EVALS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(EVALS_PATH, 'w') as f:
        json.dump(data, f, indent=2)

def prompt_for_test_case(existing_count):
    """Prompt user for a single test case."""
    print(f"\n--- Test Case {existing_count + 1} ---")
    
    prompt = input("Enter the user prompt (what a real user would ask): ").strip()
    if not prompt:
        return None
    
    expected_output = input("Describe what success looks like (expected output): ").strip()
    if not expected_output:
        expected_output = "A successful completion of the requested task"
    
    # Ask about input files (optional)
    files_input = input("List any input files needed (comma-separated, or leave empty): ").strip()
    files = []
    if files_input:
        files = [f.strip() for f in files_input.split(',') if f.strip()]
    
    return {
        "id": existing_count + 1,
        "prompt": prompt,
        "expected_output": expected_output,
        "files": files,
        "assertions": []  # Will be added later after seeing outputs
    }

def main():
    """Main function to generate test cases."""
    print("Skill Test Case Generator")
    print("=" * 30)
    print("This script helps you create realistic test cases for skill evaluation.")
    print("Follow the guidelines:")
    print("- Start with 2-3 test cases")
    print("- Vary phrasing, detail level, and formality")
    print("- Cover edge cases and typical usage")
    print("- Use realistic context (file paths, column names, etc.)")
    print()
    
    # Load existing evals
    data = load_existing_evals()
    existing_count = len(data.get("evals", []))
    print(f"Found {existing_count} existing test cases.")
    
    # Ask how many to add
    try:
        to_add = int(input("How many test cases would you like to add? "))
    except ValueError:
        print("Please enter a valid number.")
        return
    
    if to_add <= 0:
        print("No test cases added.")
        return
    
    # Generate test cases
    new_test_cases = []
    for i in range(to_add):
        test_case = prompt_for_test_case(existing_count + i)
        if test_case is None:
            print("Test case creation cancelled.")
            break
        new_test_cases.append(test_case)
        print(f"Added test case {test_case['id']}")
    
    if not new_test_cases:
        print("No test cases were added.")
        return
    
    # Combine with existing
    all_test_cases = data.get("evals", []) + new_test_cases
    
    # Update data
    data["evals"] = all_test_cases
    # Update skill name if it was unknown
    if data.get("skill_name") == "unknown":
        # Try to infer from directory name or ask
        skill_name = input("What is the name of the skill being tested? ").strip()
        if skill_name:
            data["skill_name"] = skill_name
    
    # Save
    save_evals(data)
    
    print(f"\nSuccessfully saved {len(all_test_cases)} test cases to {EVALS_PATH}")
    print("\nNext steps:")
    print("1. Run the evaluation to see initial outputs")
    print("2. Review the outputs and draft assertions")
    print("3. Update the test cases with your assertions")
    print("4. Run the evaluation again to grade the skill")

if __name__ == "__main__":
    main()