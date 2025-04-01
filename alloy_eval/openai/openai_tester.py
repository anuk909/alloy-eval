import json
import re
from pathlib import Path
from typing import Any

from alloy_eval.data_utils import read_problems
from alloy_eval.evaluation import evaluate_single_problem
from alloy_eval.models import AlloyProblem, EvaluationResult
from alloy_eval.openai.openai_client import OpenAIClient
from alloy_eval.ui_utils import console, generate_report, setup_debug_dir
from rich.progress import track


class OpenAITester:
    """
    Tests Alloy specifications using OpenAI models.

    This class handles:
    1. Loading problems from JSONL
    2. Generating prompts for the language model
    3. Querying the OpenAI API
    4. Evaluating solutions using Alloy
    5. Saving results in JSONL format
    """

    def __init__(
        self,
        problems_file: str | Path,
        model: str,
        alloy_path: str,
        temperature: float,
        debug_dir: str | Path | None = None,
    ) -> None:
        """
        Initialize the tester.

        Args:
            problems_file: Path to JSONL file containing problems
            model: OpenAI model to use
            alloy_path: Path to Alloy analyzer
            temperature: OpenAI temperature parameter
            debug_dir: Directory to save debug files (None to disable)
        """
        self.problems = read_problems(problems_file)
        self.alloy_path = alloy_path
        self.debug_dir = setup_debug_dir(debug_dir)
        self.client = OpenAIClient(
            model=model,
            temperature=temperature,
        )

    def create_prompt(self, problem: AlloyProblem) -> str:
        """Create a prompt for the language model."""
        prompt = f"""
        I need you to implement an Alloy predicate that satisfies the following requirements:

        Problem: {problem.prompt}

        Here's the signature definition:
        ```alloy
        {problem.signatures}
        ```

        Please complete this predicate implementation:
        ```alloy
        {problem.predicate_definition}
        ```           

        Output only the inner implemenation of the predicate in the required format for AlloyPred.          
        """

        return prompt

    def query_openai(self, prompt: str) -> str | None:
        """Query the OpenAI API."""
        try:
            response = self.client.query(prompt)
            return response
        except Exception as e:
            console.print(f"[red]Error querying OpenAI API: {e}[/red]")
            return None

    def clean_solution(self, solution: str) -> str:
        """Clean up the solution text."""
        if not solution:
            return ""
        solution = solution.strip().rstrip("}").strip()

        # Extract code from markdown blocks if present
        code_match = re.search(r"```(?:alloy)?\s*(.*?)```", solution, re.DOTALL)
        if code_match:
            solution = code_match.group(1).strip()

        return solution

    def test_problem(self, problem: AlloyProblem) -> EvaluationResult:
        """Test a single problem."""
        task_id = problem.task_id
        console.print(f"\n[blue]Testing: {task_id}[/blue]")

        # Generate solution
        prompt = self.create_prompt(problem)
        response = self.query_openai(prompt)

        if not response:
            return EvaluationResult(
                task_id=task_id,
                passed=False,
                solution=None,
                error_message="No response from OpenAI",
            )

        # Clean up solution
        solution = self.clean_solution(response)

        # Evaluate solution using core module
        return evaluate_single_problem(
            problem, solution, self.alloy_path, self.debug_dir
        )

    def generate_solution(self, problem: AlloyProblem) -> dict[str, Any]:
        """Generate a solution for a problem without evaluation."""
        task_id = problem.task_id
        console.print(f"\n[blue]Generating solution for: {task_id}[/blue]")

        # Generate solution
        prompt = self.create_prompt(problem)
        response = self.query_openai(prompt)

        if not response:
            return {
                "task_id": task_id,
                "solution": None,
                "error": "No response from OpenAI",
            }

        # Clean up solution
        solution = self.clean_solution(response)

        return {
            "task_id": task_id,
            "solution": solution,
        }

    def generate_solutions(self, output_file: str | Path) -> None:
        """Generate solutions for all problems without evaluation."""
        results = []

        for problem in track(self.problems, description="Generating solutions"):
            result = self.generate_solution(problem)
            results.append(result)

        # Save results
        with open(output_file, "w") as f:
            json.dump(
                {
                    "model": self.client.model,
                    "results": results,
                },
                f,
                indent=2,
            )

        # Generate report for console output
        generate_report(
            title="Alloy OpenAI Generation Report",
            model=self.client.model,
            results=results,
            success_key="solution",
            success_label="Solutions generated",
        )

    def run_tests(self, output_file: str | Path) -> None:
        """Run tests for all problems."""
        results = []

        for problem in track(self.problems, description="Testing problems"):
            result = self.test_problem(problem)
            # Convert EvaluationResult to dictionary
            results.append(result.model_dump())

        # Calculate metrics for the report
        total = len(results)
        successful = sum(1 for r in results if r.get("passed"))
        success_rate = f"{successful/total*100:.2f}%"

        # Save results with standardized format
        with open(output_file, "w") as f:
            json.dump(
                {
                    "model": self.client.model,
                    "results": results,
                    "report": {
                        "total_problems": total,
                        "total_success": successful,
                        "success_rate": success_rate,
                    },
                },
                f,
                indent=2,
            )

        # Generate report for console output
        generate_report(
            title="Alloy OpenAI Testing Report",
            model=self.client.model,
            results=results,
        )
