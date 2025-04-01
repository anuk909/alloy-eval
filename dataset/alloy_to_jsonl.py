import re
import json
import argparse
import os


def extract_comment(pred_name, alloy_content, position, look_inline):
    """
    Extract relevant comments for a predicate.

    Args:
        pred_name: The name of the predicate
        alloy_content: The full Alloy file content
        position: The starting position of the predicate
        look_inline: Whether to look for inline comments within the predicate body

    Returns:
        The extracted comment text or None if no comment found
    """
    # Look at content before the position
    preceding_content = alloy_content[:position]
    has_empty_line_before = preceding_content.endswith("\n\n")
    preceding_content = preceding_content.strip()

    if not has_empty_line_before:
        # Try to find multi-line comment
        comment = _find_multiline_comment(preceding_content)
        if comment:
            return comment

        # Try to find single-line comment
        comment = _find_singleline_comment(preceding_content)
        if comment:
            return comment

    # If requested and no comment found yet, look for inline comment
    if look_inline and position < len(alloy_content):
        # Find the end of the predicate
        open_braces = 0
        for i in range(position, len(alloy_content)):
            if alloy_content[i] == "{":
                open_braces += 1
            elif alloy_content[i] == "}":
                open_braces -= 1
                if open_braces == 0:
                    # Extract the predicate body
                    pred_body = alloy_content[position : i + 1]
                    # Look for inline comment
                    inline_pattern = r"//\s*(.*?)\s*$"
                    match = re.search(inline_pattern, pred_body, re.MULTILINE)
                    if match:
                        return match.group(1).strip()
                    break

    raise Exception(f"Couldn't find any comment for {pred_name}")


def _find_multiline_comment(text):
    """Find the last multi-line comment in text."""
    comment_pattern = r"/\*([^*]|\*[^/])*?\*/"
    comments = list(re.finditer(comment_pattern, text, re.DOTALL))

    if comments:
        # Get the last comment (closest to the predicate)
        last_comment = comments[-1].group(0)

        # Verify it's directly before the predicate (allowing only whitespace between)
        comment_end_pos = comments[-1].end()
        if text[comment_end_pos:].strip() == "":
            # Clean up the comment content
            return last_comment.replace("/*", "").replace("*/", "").strip()

    return None


def _find_singleline_comment(text):
    """Find the last single-line comment in text."""
    single_line_pattern = r"//\s*(.*?)\s*$"
    single_comments = list(re.finditer(single_line_pattern, text, re.MULTILINE))

    if single_comments:
        # Get the last single-line comment
        last_comment = single_comments[-1].group(1)

        # Verify it's directly before the predicate (allowing only whitespace between)
        comment_end_pos = single_comments[-1].end()
        if text[comment_end_pos:].strip() == "":
            return last_comment

    return None


def remove_comments(code_text):
    """Remove all comments from code text."""
    # Remove single-line comments
    code_without_single_comments = re.sub(r"//.*$", "", code_text, flags=re.MULTILINE)

    # Remove multi-line comments
    code_without_comments = re.sub(
        r"/\*.*?\*/", "", code_without_single_comments, flags=re.DOTALL
    )

    return code_without_comments


def extract_signatures(alloy_content):
    """Extract all signature definitions from Alloy content."""
    sig_pattern = (
        r"\bsig\s+.*?\}"  # Match 'sig' anywhere in the text until the next '}'
    )
    matches = re.findall(sig_pattern, alloy_content, re.DOTALL)

    return {
        sig.split()[1].strip(","): sig for sig in matches
    }  # Extract first signature name


def extract_predicates(alloy_content):
    """Extract all predicate definitions from Alloy content."""
    predicates = {}

    # Find all predicate definitions
    pred_pattern = r"pred\s+(\w+)\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}"
    pred_matches = list(re.finditer(pred_pattern, alloy_content, re.DOTALL))

    for match in pred_matches:
        pred_name = match.group(1)
        pred_body = match.group(2).strip()
        pred_start_pos = match.start()

        # Extract the comment for this predicate
        comment = extract_comment(pred_name, alloy_content, pred_start_pos, look_inline=True)

        # Remove comments from the predicate body
        clean_body = remove_comments(pred_body).strip()

        predicates[pred_name] = {
            "body": clean_body,
            "definition": f"pred {pred_name} {{\n",
            "description": comment,
            "position": pred_start_pos,
        }

    return predicates


def extract_checks(alloy_content, predicates):
    """Extract check blocks for predicates and add them to the predicates dict."""
    # Find all checks
    check_pattern = r"check\s+(\w+)\s*\{([^}]*)\}(?:\s+for\s+(\d+))?"
    check_matches = re.finditer(check_pattern, alloy_content, re.DOTALL)

    for match in check_matches:
        pred_name = match.group(1)
        check_body = match.group(2).strip()
        check_size = (
            match.group(3) if match.group(3) else "4"
        )  # Default to 4 if not specified

        if pred_name in predicates:
            predicates[pred_name][
                "check"
            ] = f"check {pred_name} {{\n    {check_body}\n}} for {check_size}"

    return predicates


def create_jsonl_entries(predicates, signatures, domain_name=""):
    """Create JSONL entries from extracted predicates and signatures."""
    jsonl_entries = []

    # Get all signatures as a string
    all_signatures = "\n".join(signatures.values())

    for pred_name, pred_info in predicates.items():
        # Use the comment directly as the prompt
        prompt = pred_info.get(
            "description", f"Create an Alloy predicate '{pred_name}'"
        )

        task_id = f"{domain_name}/{pred_name}" if domain_name else pred_name

        # For empty predicates (empty after comment removal), provide a stub
        body = pred_info["body"]
        canonical_solution = f"\t{body}\n}}" if body.strip() else f"}}"

        task_entry = {
            "task_id": task_id,
            "prompt": prompt,
            "signatures": all_signatures,
            "predicate_definition": pred_info["definition"],
            "canonical_solution": canonical_solution,
            "check": pred_info.get("check", ""),
        }

        jsonl_entries.append(json.dumps(task_entry))

    return "\n".join(jsonl_entries)


def parse_alloy_to_jsonl(alloy_content, domain_name=""):
    """Main function to parse Alloy content to JSONL format."""
    # Extract all signature definitions
    signatures = extract_signatures(alloy_content)

    # Extract all predicate definitions
    predicates = extract_predicates(alloy_content)

    # Extract check blocks
    predicates = extract_checks(alloy_content, predicates)

    # Create JSONL entries
    return create_jsonl_entries(predicates, signatures, domain_name)


def main():
    parser = argparse.ArgumentParser(
        description="Convert Alloy files to JSONL task format"
    )
    parser.add_argument("input_file", help="Input Alloy file path")
    parser.add_argument(
        "-o",
        "--output",
        help="Output JSONL file path (default: problems.jsonl)",
    )
    parser.add_argument(
        "-d",
        "--domain",
        default="",
        help='Domain name for task_id prefix (e.g., "graph")',
    )

    args = parser.parse_args()

    # Set default output filename if not provided
    if not args.output:
        base_name = os.path.splitext(args.input_file)[0]
        args.output = f"{base_name}_problems.jsonl"

    try:
        # Read the Alloy content from the input file
        with open(args.input_file, "r") as file:
            alloy_content = file.read()

        # Parse the content and generate JSONL
        jsonl_output = parse_alloy_to_jsonl(alloy_content, args.domain)

        # Write the JSONL output to the specified file
        with open(args.output, "w") as file:
            file.write(jsonl_output)

        print(f"Conversion completed successfully! Output written to {args.output}")

    except FileNotFoundError:
        print(f"Error: Input file '{args.input_file}' not found.")
    except Exception as e:
        print(f"Error during conversion: {str(e)}")


if __name__ == "__main__":
    main()
