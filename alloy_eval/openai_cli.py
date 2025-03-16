#!/usr/bin/env python3
"""Command-line interface for OpenAI-based Alloy testing."""

import argparse
from enum import Enum

from alloy_eval.openai_tester import OpenAITester


class Mode(Enum):
    """Operation mode for the OpenAI tester."""

    EVALUATE = "evaluate"  # Generate and evaluate solutions
    GENERATE = "generate"  # Only generate solutions

    def __str__(self) -> str:
        return self.value


def main() -> None:
    """Run the OpenAI tester CLI."""
    parser = argparse.ArgumentParser(
        description="Test Alloy specifications using OpenAI models."
    )

    parser.add_argument(
        "--problems",
        type=str,
        required=True,
        help="Path to JSONL file containing problems",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="results.json",
        help="Path to save results JSONL file",
    )
    parser.add_argument(
        "--mode",
        type=Mode,
        choices=list(Mode),
        default=Mode.EVALUATE,
        help="Operation mode: evaluate (generate and test solutions) or generate (only generate solutions)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4o-mini",
        help="OpenAI model to use",
    )
    parser.add_argument(
        "--alloy-path",
        type=str,
        default="alloy",
        help="Path to Alloy analyzer",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.2,
        help="OpenAI temperature parameter",
    )
    parser.add_argument(
        "--debug-dir",
        type=str,
        help="Directory to save debug files",
    )

    args = parser.parse_args()

    # Initialize tester
    tester = OpenAITester(
        problems_file=args.problems,
        model=args.model,
        alloy_path=args.alloy_path,
        temperature=args.temperature,
        debug_dir=args.debug_dir,
    )

    # Run in specified mode
    if args.mode == Mode.EVALUATE:
        tester.run_tests(args.output)
    else:
        tester.generate_solutions(args.output)


if __name__ == "__main__":
    main()
