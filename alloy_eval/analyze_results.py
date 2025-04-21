import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track

console = Console()


def load_results(file_path: str | Path) -> dict[str, Any]:
    """Load results from a JSON file."""
    with open(file_path, "r") as f:
        return json.load(f)


def get_predicate_type(task_id: str) -> str:
    """Extract predicate type from task ID."""
    # Extract the predicate name from task_id (e.g., "Antisymmetric_sol0" -> "Antisymmetric")
    return task_id.split("_")[0]


def get_error_type(error_message: str | None) -> str:
    """Determine the error type from the error message."""
    if error_message is None:
        return "Success"
    elif "Counterexample found" in error_message:
        return "CounterExample"
    else:
        return "Other Failure"


def analyze_results(results: dict[str, Any]) -> None:
    """Analyze and display results in a visual format."""
    # Display header
    console.print(
        Panel.fit(
            f"[bold blue]Results Analysis[/bold blue]\n"
            f"Model: [green]{results['model']}[/green]"
        )
    )

    # Group results by predicate type
    predicate_results = defaultdict(
        lambda: {
            "total": 0,
            "success": 0,
            "counterexample": 0,
            "other_failure": 0,
            "error_types": defaultdict(int),
        }
    )

    # Process each result
    for result in track(results["results"], description="Analyzing results"):
        task_id = result["task_id"]
        pred_type = get_predicate_type(task_id)
        passed = result.get("passed", False)
        error_message = result.get("error_message", None)
        error = result.get("error", None)

        # Skip entries with no solution
        if error == "No solution generated":
            continue

        # Update counters for this predicate type
        predicate_results[pred_type]["total"] += 1

        if passed:
            predicate_results[pred_type]["success"] += 1
        else:
            error_type = get_error_type(error_message)
            if error_type == "CounterExample":
                predicate_results[pred_type]["counterexample"] += 1
            else:
                predicate_results[pred_type]["other_failure"] += 1

            # Track specific error types
            if error_message:
                predicate_results[pred_type]["error_types"][error_message] += 1

    # Create a table for all statistics
    table = Table(
        show_header=True,
        header_style="bold magenta",
        title="[bold]Results Statistics[/bold]",
    )
    table.add_column("Predicate Type")
    table.add_column("Total")
    table.add_column("Success")
    table.add_column("CounterExample")
    table.add_column("Other Failure")

    # Add rows for each predicate type
    for pred_type in sorted(predicate_results.keys()):
        stats = predicate_results[pred_type]
        total = stats["total"]
        if total == 0:
            continue

        table.add_row(
            pred_type,
            str(total),
            f"{stats['success']} ({stats['success']/total*100:.1f}%)",
            f"{stats['counterexample']} ({stats['counterexample']/total*100:.1f}%)",
            f"{stats['other_failure']} ({stats['other_failure']/total*100:.1f}%)",
        )

    # Display table
    console.print(table)
    console.print()

    # Display error type breakdown for each predicate
    for pred_type in sorted(predicate_results.keys()):
        stats = predicate_results[pred_type]
        if not stats["error_types"]:
            continue

        console.print(f"[bold]{pred_type} Error Types:[/bold]")
        error_table = Table(show_header=True, header_style="bold yellow")
        error_table.add_column("Error Type")
        error_table.add_column("Count")

        for error_type, count in sorted(
            stats["error_types"].items(), key=lambda x: x[1], reverse=True
        ):
            error_table.add_row(error_type, str(count))

        console.print(error_table)
        console.print()

    # Display overall summary
    total_results = sum(stats["total"] for stats in predicate_results.values())
    total_success = sum(stats["success"] for stats in predicate_results.values())
    total_counterexample = sum(
        stats["counterexample"] for stats in predicate_results.values()
    )
    total_other_failure = sum(
        stats["other_failure"] for stats in predicate_results.values()
    )

    console.print(
        Panel.fit(
            "[bold]Overall Summary[/bold]\n"
            f"Total tasks: [blue]{total_results}[/blue]\n"
            f"Successful: [green]{total_success}[/green] ({total_success/total_results*100:.1f}%)\n"
            f"Counterexamples: [red]{total_counterexample}[/red] ({total_counterexample/total_results*100:.1f}%)\n"
            f"Other failures: [yellow]{total_other_failure}[/yellow] ({total_other_failure/total_results*100:.1f}%)"
        )
    )


def main() -> None:
    """Main function to run the analyzer."""
    import argparse

    parser = argparse.ArgumentParser(description="Analyze Alloy evaluation results")
    parser.add_argument("results_file", type=str, help="Path to results.json file")
    args = parser.parse_args()

    try:
        results = load_results(args.results_file)
        analyze_results(results)
    except Exception as e:
        console.print(f"[red]Error analyzing results: {e}[/red]")


if __name__ == "__main__":
    main()
