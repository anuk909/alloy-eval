import argparse
from enum import Enum

from alloy_eval.openai.openai_tester import OpenAITester
from alloy_eval.openai.multi_solution_tester import (
    SinglePromptMultiSolutionTester,
    MultiplePromptMultiSolutionTester,
)


class Mode(Enum):
    """Operation mode for the OpenAI tester."""

    EVALUATE = "evaluate"  # Generate and evaluate solutions
    GENERATE = "generate"  # Only generate solutions

    def __str__(self) -> str:
        return self.value


class GenerationStrategy(Enum):
    """Strategy for generating multiple solutions."""

    SINGLE_PROMPT = "single"  # Generate all solutions in a single prompt
    MULTIPLE_PROMPTS = "multiple"  # Generate solutions using multiple prompts

    def __str__(self) -> str:
        return self.value


class GenerationStrategy(Enum):
    """Strategy for generating multiple solutions."""

    SINGLE_PROMPT = "single"  # Generate all solutions in a single prompt
    MULTIPLE_PROMPTS = "multiple"  # Generate solutions using multiple prompts

    def __str__(self) -> str:
        return self.value


def get_tester_class(strategy: GenerationStrategy, total_solutions: int):
    """
    Get the appropriate tester class based on the generation strategy.

    Args:
        strategy: The generation strategy to use
        total_solutions: Total number of solutions to generate

    Returns:
        The appropriate tester class
    """
    if total_solutions == 1:
        return OpenAITester
    elif strategy == GenerationStrategy.SINGLE_PROMPT:
        return SinglePromptMultiSolutionTester
    else:
        return MultiplePromptMultiSolutionTester


def main() -> None:
    """Run the OpenAI tester CLI."""
    parser = argparse.ArgumentParser(
        description="Test Alloy specifications using OpenAI models."
    )

    # Required arguments
    parser.add_argument(
        "--problems",
        type=str,
        required=True,
        help="Path to JSONL file containing problems",
    )

    # Optional arguments
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

    # Solution generation arguments
    solution_group = parser.add_argument_group("Solution Generation")
    solution_group.add_argument(
        "--total-solutions",
        type=int,
        default=1,
        help="Total number of solutions to generate per problem",
    )
    solution_group.add_argument(
        "--generation-strategy",
        type=GenerationStrategy,
        choices=list(GenerationStrategy),
        default=GenerationStrategy.SINGLE_PROMPT,
        help="Strategy for generating multiple solutions: single (all in one prompt) or multiple (separate prompts)",
    )
    solution_group.add_argument(
        "--k-values",
        type=int,
        nargs="+",
        help="List of k values to calculate pass@k for. If not specified, only pass@1 is calculated.",
    )

    args = parser.parse_args()

    # Get the appropriate tester class
    tester_class = get_tester_class(args.generation_strategy, args.total_solutions)

    # Initialize tester with common arguments
    common_args = {
        "problems_file": args.problems,
        "model": args.model,
        "alloy_path": args.alloy_path,
        "temperature": args.temperature,
        "debug_dir": args.debug_dir,
    }

    # Add multi-solution specific arguments only if needed
    if args.total_solutions > 1:
        common_args.update(
            {
                "total_solutions": args.total_solutions,
                "k_values": args.k_values,
            }
        )

    # Initialize tester
    tester = tester_class(**common_args)

    # Run in specified mode
    if args.mode == Mode.EVALUATE:
        tester.run_tests(args.output)
    else:
        tester.generate_solutions(args.output)


if __name__ == "__main__":
    main()
