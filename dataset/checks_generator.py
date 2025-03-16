"""
Alloy Check Generator - Creates check commands for Alloy specifications.

This script parses Alloy files and automatically generates check commands for
all predicates, or specific ones based on a pattern.
"""

import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Pattern
import argparse


def parse_predicates(
    content: str, pattern: Optional[Pattern] = None
) -> Dict[str, Tuple[str, str]]:
    """
    Extract predicates from Alloy content, optionally filtering by a pattern.

    Args:
        content: The content of the Alloy file
        pattern: Optional regex pattern to filter predicate names

    Returns:
        A dictionary mapping predicate names to tuples of (full_definition, body)
    """
    predicates: Dict[str, Tuple[str, str]] = {}
    # Use a regex pattern to find predicates and their bodies
    pred_pattern = re.compile(r"(pred\s+(\w+)\s*\{([^}]*)\})", re.DOTALL)

    for match in pred_pattern.finditer(content):
        full_def, pred_name, body = match.groups()

        # If a pattern is provided, only include matching predicates
        if pattern and not pattern.match(pred_name):
            continue

        # Clean up the body (remove comments and excessive whitespace)
        clean_body = re.sub(r"//.*$", "", body, flags=re.MULTILINE)
        clean_body = " ".join(clean_body.split())
        predicates[pred_name] = (full_def, clean_body)

    return predicates


def create_check_command(pred_name: str, body: str, scope: int = 4) -> str:
    """
    Create a check command for a predicate.

    Args:
        pred_name: The name of the predicate
        body: The body of the predicate
        scope: The scope for the check command

    Returns:
        A string containing the check command
    """
    return f"\ncheck {pred_name} {{\n    {pred_name} iff ({body})\n}} for {scope}\n"


def add_checks_to_alloy_file(
    input_file: Path, output_file: Path, pred_pattern: str = None, scope: int = 4
) -> None:
    """
    Parse an Alloy file and add check commands for predicates.

    Args:
        input_file: Path to the input Alloy file
        output_file: Path to save the output Alloy file with added checks
        pred_pattern: Optional regex pattern to filter predicate names
        scope: The scope for the check commands
    """
    try:
        content = input_file.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading input file: {e}")
        sys.exit(1)

    # Compile the pattern if provided
    compiled_pattern = re.compile(pred_pattern) if pred_pattern else None

    # Find all predicates and their bodies
    predicates = parse_predicates(content, compiled_pattern)

    if not predicates:
        print(
            "No predicates found"
            + (f" matching pattern '{pred_pattern}'" if pred_pattern else "")
            + ". Nothing to do."
        )
        return

    # Add check commands for each predicate
    output_content = content
    for pred_name, (full_def, body) in predicates.items():
        check_cmd = create_check_command(pred_name, body, scope)
        # Add the check command after the predicate
        output_content = output_content.replace(full_def, full_def + check_cmd)

    # Write the output file
    try:
        output_file.write_text(output_content, encoding="utf-8")
        print(f"Successfully added {len(predicates)} checks to {output_file}")
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Add check commands to Alloy specifications for predicates."
    )
    parser.add_argument("input_file", type=Path, help="Path to the input Alloy file")
    parser.add_argument(
        "output_file",
        type=Path,
        help="Path to save the output Alloy file with added checks",
    )
    parser.add_argument(
        "--pattern",
        "-p",
        type=str,
        help="Regular expression pattern to filter predicate names (e.g., '^inv')",
    )
    parser.add_argument(
        "--scope",
        "-s",
        type=int,
        default=4,
        help="Scope for the check commands (default: 4)",
    )

    args = parser.parse_args()

    if not args.input_file.exists():
        print(f"Error: Input file '{args.input_file}' does not exist.")
        sys.exit(1)

    if args.input_file.suffix != ".als":
        print("Warning: Input file does not have '.als' extension. Continuing anyway.")

    add_checks_to_alloy_file(
        args.input_file, args.output_file, args.pattern, args.scope
    )


if __name__ == "__main__":
    main()
