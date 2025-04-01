import argparse
import json
from pathlib import Path

from alloy_eval.evaluation import evaluate_functional_correctness
from alloy_eval.data_utils import read_jsonl


def evaluate_samples(
    samples_path: str | Path,
    alloy_path: str | Path,
    problems_file: str | Path | None = None,
) -> dict:
    """
    Evaluate a collection of samples from a JSONL file.

    Args:
        samples_path: Path to JSONL file containing samples
        alloy_path: Path to Alloy analyzer executable
        problems_file: Optional path to problems file

    Returns:
        Dictionary with results and metrics in standardized format
    """
    samples = read_jsonl(samples_path)
    results = []

    for sample in samples:
        result = evaluate_functional_correctness(
            solution=sample["completion"],
            problem_id=sample["task_id"],
            alloy_path=alloy_path,
            problems_file=problems_file,
        )
        results.append(result)

    # Calculate metrics
    passed = sum(1 for r in results if r.passed)
    total = len(results)
    success_rate = passed / total if total > 0 else 0.0

    # Create standardized output format
    return {
        "results": results,
        "report": {
            "total_problems": total,
            "total_success": passed,
            "success_rate": success_rate,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Evaluate Alloy formal specifications."
    )
    parser.add_argument("samples_file", help="Path to samples JSONL file")
    parser.add_argument(
        "--alloy-path", required=True, help="Path to Alloy analyzer executable"
    )
    parser.add_argument("--problems-file", help="Path to problems file (JSON or JSONL)")

    args = parser.parse_args()

    samples_path = Path(args.samples_file)
    results = evaluate_samples(
        samples_path=samples_path,
        alloy_path=args.alloy_path,
        problems_file=args.problems_file,
    )

    # Write detailed results
    results_file = Path(str(samples_path) + "_results.json")
    with open(results_file, "w") as f:
        json.dump(results, f, indent=2)

    # Print success rate from the report
    print(f"Success rate: {results['report']['success_rate']:.2%}")


if __name__ == "__main__":
    main()
