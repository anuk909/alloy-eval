from pathlib import Path
from typing import Any

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

        # Initialize components
        self.client = OpenAIClient(
            model=model,
            temperature=temperature,
            max_tokens=512,  # Single solution needs fewer tokens
        )
        self.prompt_generator = PromptGenerator(1)  # Always generate 1 solution
        self.solution_processor = SolutionProcessor(1)  # Always process 1 solution
        self.result_handler = ResultHandler(model)

    def test_problem(self, problem: AlloyProblem) -> EvaluationResult:
        """
        Test a single problem.

        Args:
            problem: The Alloy problem to test

        Returns:
            The evaluation result for the generated solution
        """
        task_id = problem.task_id
        console.print(f"\n[blue]Testing: {task_id}[/blue]")

        solution = self._generate_solution(problem)
        return self._evaluate_solution(problem, solution)

    def generate_solution(self, problem: AlloyProblem) -> dict[str, Any]:
        """
        Generate a solution for a problem without evaluation.

        Args:
            problem: The Alloy problem to generate a solution for

        Returns:
            A dictionary containing the generated solution
        """
        task_id = problem.task_id
        console.print(f"\n[blue]Generating solution for: {task_id}[/blue]")

        solution = self._generate_solution(problem)
        return self._create_solution_result(task_id, solution)

    def _generate_solution(self, problem: AlloyProblem) -> str | None:
        """
        Generate a single solution.

        Args:
            problem: The Alloy problem to generate a solution for

        Returns:
            The generated solution or None if generation failed
        """
        prompt = self.prompt_generator.create_prompt(problem)
        response = self.query_openai(prompt)
        solutions = self.solution_processor.process_solutions(problem.task_id, response)
        return solutions[0] if solutions else None

    def _evaluate_solution(
        self,
        problem: AlloyProblem,
        solution: str | None,
    ) -> EvaluationResult:
        """
        Evaluate a single solution.

        Args:
            problem: The Alloy problem being tested
            solution: Solution to evaluate

        Returns:
            The evaluation result
        """
        if solution is None:
            return self.result_handler.create_result(
                problem.task_id,
                error="No solution generated",
                passed=False,
            )

        # Pass the task_id to evaluate_single_problem
        result = evaluate_single_problem(
            problem, solution, self.alloy_path, self.debug_dir, problem.task_id
        )

        # Display test result immediately
        status = "[green]✓ PASSED[/green]" if result.passed else "[red]✗ FAILED[/red]"
        console.print(f"    Solution: {status}")

        return result

    def _create_solution_result(
        self,
        task_id: str,
        solution: str | None,
    ) -> dict[str, Any]:
        """
        Create a result dictionary for a solution.

        Args:
            task_id: The task ID
            solution: Solution to add

        Returns:
            A dictionary containing the solution result
        """
        if solution is None:
            return self.result_handler.create_result(
                task_id,
                error="No solution generated",
            )

        result = self.result_handler.create_result(task_id, solution=solution)
        console.print("    Solution generated")
        return result

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

    def run_tests(self, output_file: str | Path) -> None:
        """
        Run tests for all problems.

        Args:
            output_file: Path to save results to
        """
        all_results = []

        for problem in track(self.problems, description="Testing problems"):
            result = self.test_problem(problem)
            # Convert EvaluationResult to dictionary using model_dump() if needed
            result_dict = (
                result.model_dump() if hasattr(result, "model_dump") else result
            )
            all_results.append(result_dict)

            # Display problem summary
            console.print(f"Problem summary: {'PASSED' if result.passed else 'FAILED'}")

        # Save results
        self.result_handler.save_results(
            output_file,
            all_results,
            "Alloy OpenAI Testing Report",
            include_report=True,
        )

    def generate_solutions(self, output_file: str | Path) -> None:
        """
        Generate solutions for all problems without evaluation.

        Args:
            output_file: Path to save results to
        """
        all_results = []

        for problem in track(self.problems, description="Generating solutions"):
            result = self.generate_solution(problem)
            all_results.append(result)

        # Save results
        self.result_handler.save_results(
            output_file, all_results, "Alloy OpenAI Generation Report"
        )
