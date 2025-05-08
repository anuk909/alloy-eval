import json
from pathlib import Path
from typing import Any
import numpy as np

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
        pass_at_k: dict[str, float] | None = None,
    ) -> None:
        """
        Save results to a file and generate a report.

        Args:
            output_file: Path to save results to
            all_results: List of result dictionaries
            title: Report title
            include_report: Whether to include a report in the output
            pass_at_k: Dictionary with Pass@K values for different k (optional)
        """
        # Group results by problem
        problem_results = {}
        for r in all_results:
            base_id = r["task_id"].rsplit("_sol", 1)[0]
            if base_id not in problem_results:
                problem_results[base_id] = []
            problem_results[base_id].append(r)

        # Calculate pass@k for each problem
        problem_pass_at_k = {}
        for problem_id, results in problem_results.items():
            num_correct = sum(1 for r in results if r.get("passed", False))
            num_samples = len(results)

            # Calculate pass@k for each k value
            problem_k_values = {}
            if pass_at_k:
                for k_str, _ in pass_at_k.items():
                    k = int(k_str.split("@")[1])
                    if k <= num_samples:
                        # Calculate pass@k for this problem
                        if num_samples - num_correct < k:
                            pass_rate = 1.0
                        else:
                            pass_rate = 1.0 - np.prod(
                                1.0
                                - k
                                / np.arange(
                                    num_samples - num_correct + 1, num_samples + 1
                                )
                            )
                        problem_k_values[f"pass@{k}"] = f"{pass_rate*100:.1f}%"

            problem_pass_at_k[problem_id] = {
                "solutions": results,
                "pass_at_k": problem_k_values,
                "summary": {
                    "total_solutions": num_samples,
                    "successful_solutions": num_correct,
                    "success_rate": f"{num_correct/num_samples*100:.1f}%",
                },
            }

        # Prepare data for saving
        data = {
            "model": self.model,
            "problems": problem_pass_at_k,
        }

        # Add overall report if needed
        if include_report:
            total = len(all_results)
            successful = sum(1 for r in all_results if r.get("passed"))
            success_rate = f"{successful/total*100:.2f}%"

            report = {
                "total_problems": len(problem_results),
                "total_solutions": total,
                "total_success": successful,
                "success_rate": success_rate,
            }

            # Add overall Pass@K metrics if provided
            if pass_at_k:
                report["pass_at_k"] = {k: f"{v*100:.1f}%" for k, v in pass_at_k.items()}

            data["report"] = report

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
            if pass_at_k:
                for k, value in pass_at_k.items():
                    console.print(f"[cyan]{k} = {value*100:.1f}%[/cyan]")
        else:
            successful = sum(1 for r in all_results if r.get("solution") is not None)
            console.print(f"\n[green]Total solutions generated: {successful}[/green]")
