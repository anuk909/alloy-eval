import json
from pathlib import Path
from typing import Any

from alloy_eval.models import EvaluationResult
from alloy_eval.ui_utils import console, generate_report


class ResultHandler:
    """Handles the processing and saving of results."""

    def __init__(self, model: str):
        """
        Initialize the result handler.

        Args:
            model: The OpenAI model name
        """
        self.model = model

    def create_result_with_index(
        self,
        task_id: str,
        index: int,
        solution: str | None = None,
        error: str | None = None,
        passed: bool = False,
    ) -> EvaluationResult | dict[str, Any]:
        """
        Create a result with the solution index in the task_id.

        Args:
            task_id: The task ID
            index: The solution index
            solution: The solution text
            error: Error message if any
            passed: Whether the solution passed

        Returns:
            An EvaluationResult or dictionary
        """
        task_id_with_index = f"{task_id}_sol{index}"

        if isinstance(solution, str):
            # For evaluation results
            return EvaluationResult(
                task_id=task_id_with_index,
                passed=passed,
                solution=solution,
                error_message=error,
            )
        else:
            # For generation results
            return {
                "task_id": task_id_with_index,
                "solution": solution,
                "error": error,
            }

    def save_results(
        self,
        output_file: str | Path,
        all_results: list[dict[str, Any]],
        title: str,
        include_report: bool = False,
    ) -> None:
        """
        Save results to a file and generate a report.

        Args:
            output_file: Path to save results to
            all_results: List of result dictionaries
            title: Report title
            include_report: Whether to include a report in the output
        """
        # Prepare data for saving
        data = {
            "model": self.model,
            "results": all_results,
        }

        # Add report if needed
        if include_report:
            total = len(all_results)
            successful = sum(1 for r in all_results if r.get("passed"))
            success_rate = f"{successful/total*100:.2f}%"

            data["report"] = {
                "total_problems": total,
                "total_success": successful,
                "success_rate": success_rate,
            }

        # Save results
        with open(output_file, "w") as f:
            json.dump(data, f, indent=2)

        # Generate report for console output
        generate_report(
            title=title,
            model=self.model,
            results=all_results,
            success_key="passed" if include_report else "solution",
            success_label="Tests passed" if include_report else "Solutions generated",
        )

        # Display summary
        if include_report:
            console.print(
                f"\n[green]Total solutions tested: {len(all_results)}[/green]"
            )
            console.print(
                f"[green]Successful solutions: {successful} ({success_rate})[/green]"
            )
        else:
            successful = sum(1 for r in all_results if r.get("solution") is not None)
            console.print(f"\n[green]Total solutions generated: {successful}[/green]")
