import json
from pathlib import Path
from typing import Any, Dict, List

from alloy_eval.data_utils import read_problems
from alloy_eval.evaluation import evaluate_single_problem
from alloy_eval.models import AlloyProblem, EvaluationResult
from alloy_eval.openai.openai_client import OpenAIClient
from alloy_eval.openai.prompt_generator import PromptGenerator
from alloy_eval.openai.result_handler import ResultHandler
from alloy_eval.openai.solution_processor import SolutionProcessor
from alloy_eval.ui_utils import console, setup_debug_dir
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
        num_solutions: int = 1,
    ) -> None:
        """
        Initialize the tester.

        Args:
            problems_file: Path to JSONL file containing problems
            model: OpenAI model to use
            alloy_path: Path to Alloy analyzer
            temperature: OpenAI temperature parameter
            debug_dir: Directory to save debug files (None to disable)
            num_solutions: Number of different solutions to generate for each problem
        """
        self.problems = read_problems(problems_file)
        self.alloy_path = alloy_path
        self.debug_dir = setup_debug_dir(debug_dir)
        self.num_solutions = num_solutions

        # Calculate max_tokens based on number of solutions
        # Each solution is roughly 100 tokens, plus some overhead
        max_tokens = max(512, num_solutions * 150)

        # Initialize components
        self.client = OpenAIClient(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        self.prompt_generator = PromptGenerator(num_solutions)
        self.solution_processor = SolutionProcessor(num_solutions)
        self.result_handler = ResultHandler(model)

    def query_openai(self, prompt: str) -> str | None:
        """
        Query the OpenAI API.

        Args:
            prompt: The prompt to send to OpenAI

        Returns:
            The response from OpenAI or None if there was an error
        """
        try:
            response = self.client.query(prompt)
            return response
        except Exception as e:
            console.print(f"[red]Error querying OpenAI API: {e}[/red]")
            return None

    def test_problem(self, problem: AlloyProblem) -> List[EvaluationResult]:
        """
        Test a single problem with multiple solutions.

        Args:
            problem: The Alloy problem to test

        Returns:
            A list of EvaluationResult objects
        """
        task_id = problem.task_id
        console.print(f"\n[blue]Testing: {task_id}[/blue]")

        # Generate solutions
        prompt = self.prompt_generator.create_prompt(problem)
        response = self.query_openai(prompt)

        # Process solutions
        solutions = self.solution_processor.process_solutions(task_id, response)

        # Evaluate each solution
        results = []
        for i, solution in enumerate(solutions):
            if solution is None:
                results.append(
                    self.result_handler.create_result_with_index(
                        task_id, i, error="No solution generated", passed=False
                    )
                )
                continue

            # Create a modified task_id with solution index
            modified_task_id = f"{task_id}_sol{i}"

            # Pass the modified task_id to evaluate_single_problem
            result = evaluate_single_problem(
                problem, solution, self.alloy_path, self.debug_dir, modified_task_id
            )

            # Add solution index to the task_id
            result.task_id = modified_task_id

            results.append(result)

            # Display test result immediately
            status = (
                "[green]✓ PASSED[/green]" if result.passed else "[red]✗ FAILED[/red]"
            )
            console.print(f"  Solution {i+1}/{self.num_solutions}: {status}")

        return results

    def generate_solution(self, problem: AlloyProblem) -> List[Dict[str, Any]]:
        """
        Generate multiple solutions for a problem without evaluation.

        Args:
            problem: The Alloy problem to generate solutions for

        Returns:
            A list of dictionaries containing the generated solutions
        """
        task_id = problem.task_id
        console.print(f"\n[blue]Generating solutions for: {task_id}[/blue]")

        # Generate solutions
        prompt = self.prompt_generator.create_prompt(problem)
        response = self.query_openai(prompt)

        # Process solutions
        solutions = self.solution_processor.process_solutions(task_id, response)

        # Create results
        results = []
        for i, solution in enumerate(solutions):
            if solution is None:
                results.append(
                    self.result_handler.create_result_with_index(
                        task_id, i, error="No solution generated"
                    )
                )
                continue

            results.append(
                self.result_handler.create_result_with_index(
                    task_id, i, solution=solution
                )
            )

            # Display solution count
            console.print(f"  Solution {i+1}/{self.num_solutions} generated")

        return results

    def generate_solutions(self, output_file: str | Path) -> None:
        """
        Generate solutions for all problems without evaluation.

        Args:
            output_file: Path to save results to
        """
        all_results = []

        for problem in track(self.problems, description="Generating solutions"):
            results = self.generate_solution(problem)
            all_results.extend(results)

        # Save results
        self.result_handler.save_results(
            output_file, all_results, "Alloy OpenAI Generation Report"
        )

    def run_tests(self, output_file: str | Path) -> None:
        """
        Run tests for all problems.

        Args:
            output_file: Path to save results to
        """
        all_results = []

        for problem in track(self.problems, description="Testing problems"):
            results = self.test_problem(problem)
            # Convert EvaluationResult to dictionary using dict() instead of model_dump()
            result_dicts = [dict(r) for r in results]
            all_results.extend(result_dicts)

            # Count successful solutions
            problem_successful = sum(1 for r in result_dicts if r.get("passed", False))
            console.print(
                f"  Problem summary: {problem_successful}/{len(results)} solutions passed"
            )

        # Save results
        self.result_handler.save_results(
            output_file, all_results, "Alloy OpenAI Testing Report", include_report=True
        )
