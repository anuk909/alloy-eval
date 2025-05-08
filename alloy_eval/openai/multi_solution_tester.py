from enum import Enum
from pathlib import Path
from typing import Any
from collections import defaultdict
import numpy as np
import itertools

from alloy_eval.models import AlloyProblem
from alloy_eval.evaluation import evaluate_single_problem
from alloy_eval.openai.openai_tester import OpenAITester
from alloy_eval.openai.prompt_generator import PromptGenerator
from alloy_eval.openai.solution_processor import SolutionProcessor
from alloy_eval.ui_utils import console
from rich.progress import track


class GenerationStrategy(Enum):
    """Strategy for generating multiple solutions."""

    SINGLE_QUERY = "single"  # Generate all solutions in a single query
    MULTIPLE_QUERIES = "multiple"  # Generate solutions using multiple queries

    def __str__(self) -> str:
        return self.value


class MultiSolutionTester(OpenAITester):
    """
    Base class for generating multiple solutions.
    Extends OpenAITester with support for multiple solutions.
    """

    def __init__(
        self,
        *args: Any,
        total_solutions: int = 1,
        k_values: list[int] | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the multi-solution tester.

        Args:
            *args: Arguments to pass to OpenAITester
            total_solutions: Total number of solutions to generate per problem
            k_values: List of k values to compute pass@k for. If None, computes for k=1.
            **kwargs: Keyword arguments to pass to OpenAITester
        """
        super().__init__(*args, **kwargs)
        self.total_solutions = total_solutions
        self.k_values = k_values

        # Calculate max_tokens based on number of solutions
        # Each solution is roughly 100 tokens, plus some overhead
        max_tokens = max(512, total_solutions * 150)
        self.client.max_tokens = max_tokens

        # Initialize components for multiple solutions
        self.solution_processor = SolutionProcessor(total_solutions)

    def _generate_solutions(self, problem: AlloyProblem) -> list[str | None]:
        """
        Generate multiple solutions for a problem.
        To be implemented by subclasses.

        Args:
            problem: The Alloy problem to generate solutions for

        Returns:
            List of generated solutions
        """
        raise NotImplementedError("Subclasses must implement _generate_solutions")

    def estimate_pass_at_k(
        self, num_samples: int | list[int], num_correct: list[int], k: int
    ) -> np.ndarray:
        """
        Estimates pass@k for each problem.

        Args:
            num_samples: Number of samples per problem (int or list of ints)
            num_correct: Number of correct solutions per problem (list of ints)
            k: The k in pass@k

        Returns:
            NumPy array of pass@k estimates for each problem
        """

        def estimator(n: int, c: int, k: int) -> float:
            """Calculates 1 - comb(n - c, k) / comb(n, k)."""
            if n - c < k:
                return 1.0
            return 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))

        if isinstance(num_samples, int):
            num_samples_it = itertools.repeat(num_samples, len(num_correct))
        else:
            assert len(num_samples) == len(num_correct)
            num_samples_it = iter(num_samples)

        return np.array(
            [estimator(int(n), int(c), k) for n, c in zip(num_samples_it, num_correct)]
        )

    def _compute_pass_at_k(
        self, all_results: list[dict[str, Any]], k_values: list[int] | None = None
    ) -> dict[str, float]:
        """
        Compute Pass@K using the custom estimate_pass_at_k function.

        Args:
            all_results: List of result dictionaries
            k_values: List of k values to compute pass@k for. If None, computes for k=1.

        Returns:
            Dictionary with Pass@K values for each k
        """
        # Group results by base problem ID (removing _solN suffix)
        problem_results = defaultdict(list)
        for r in all_results:
            base_id = r["task_id"].rsplit("_sol", 1)[0]
            problem_results[base_id].append(r.get("passed", False))

        # Calculate num_correct for each problem
        num_samples = self.total_solutions
        num_correct = [sum(passes) for passes in problem_results.values()]

        # If no k values specified, default to k=1
        if k_values is None:
            k_values = [1]

        # Calculate Pass@k for each k value
        pass_at_k_dict = {}
        for k in k_values:
            if k > num_samples:
                console.print(
                    f"[yellow]Warning: k={k} is larger than number of samples ({num_samples}), skipping[/yellow]"
                )
                continue
            pass_at_k = self.estimate_pass_at_k(
                num_samples=num_samples, num_correct=num_correct, k=k
            )
            pass_at_k_dict[f"pass@{k}"] = float(pass_at_k.mean())

        return pass_at_k_dict

    def _evaluate_solutions(
        self,
        problem: AlloyProblem,
    ) -> tuple[list[dict[str, Any]], int, dict[str, float]]:
        """
        Evaluate multiple solutions for a problem.

        Args:
            problem: The Alloy problem being tested

        Returns:
            Tuple of (list of result dictionaries, number of successful solutions, pass@k values)
        """
        solutions = self._generate_solutions(problem)
        results = []
        successful = 0

        for i, solution in enumerate(solutions):
            if solution is None:
                result = self.result_handler.create_result(
                    f"{problem.task_id}_sol{i}",
                    error="No solution generated",
                    passed=False,
                )
            else:
                # Pass the task_id to evaluate_single_problem
                result = evaluate_single_problem(
                    problem,
                    solution,
                    self.alloy_path,
                    self.debug_dir,
                    f"{problem.task_id}_sol{i}",
                )
                if result.passed:
                    successful += 1

            # Display test result immediately
            status = (
                "[green]✓ PASSED[/green]" if result.passed else "[red]✗ FAILED[/red]"
            )
            console.print(f"    Solution {i+1}: {status}")

            # Convert EvaluationResult to dictionary
            result_dict = (
                result.model_dump() if hasattr(result, "model_dump") else result
            )
            results.append(result_dict)

        # Calculate pass@k values if k_values are specified
        pass_at_k = {}
        if self.k_values:
            pass_at_k = self._compute_pass_at_k(results, self.k_values)

        return results, successful, pass_at_k

    def run_tests(self, output_file: str | Path) -> None:
        """
        Run tests for all problems.

        Args:
            output_file: Path to save results to
        """
        all_results = []
        total_problems = len(self.problems)
        total_successful = 0
        all_pass_at_k = defaultdict(list)

        for problem in track(self.problems, description="Testing problems"):
            task_id = problem.task_id
            console.print(f"\n[blue]Testing: {task_id}[/blue]")
            results, problem_successful, pass_at_k = self._evaluate_solutions(problem)
            all_results.extend(results)
            total_successful += problem_successful

            # Display problem summary
            console.print(
                f"Problem summary: {problem_successful}/{self.total_solutions} solutions passed"
            )

            # Display pass@k values for this problem
            if pass_at_k:
                for k, value in pass_at_k.items():
                    console.print(f"Pass@{k}: {value:.2%}")
                    all_pass_at_k[k].append(value)

        # Calculate overall statistics
        overall_pass_rate = total_successful / (total_problems * self.total_solutions)
        console.print(f"\nOverall pass rate: {overall_pass_rate:.2%}")

        # Calculate and display overall pass@k values
        overall_pass_at_k = {}
        if all_pass_at_k:
            console.print("\nOverall Pass@K values:")
            for k, values in all_pass_at_k.items():
                avg_pass_at_k = sum(values) / len(values)
                overall_pass_at_k[k] = avg_pass_at_k
                console.print(f"Pass@{k}: {avg_pass_at_k:.2%}")

        # Save results
        self.result_handler.save_results(
            output_file,
            all_results,
            "Alloy OpenAI Testing Report",
            include_report=True,
            pass_at_k=overall_pass_at_k,
        )


class SingleQueryMultiSolutionsTester(MultiSolutionTester):
    """
    Generates multiple solutions in a single query to the language model.
    This is more efficient but may be limited by token constraints.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the single-query multi-solution tester."""
        super().__init__(*args, **kwargs)
        self.prompt_generator = PromptGenerator(self.total_solutions)

    def _generate_solutions(self, problem: AlloyProblem) -> list[str | None]:
        """
        Generate all solutions in a single query.

        Args:
            problem: The Alloy problem to generate solutions for

        Returns:
            List of generated solutions
        """
        prompt = self.prompt_generator.create_prompt(problem)
        response = self.query_openai(prompt)
        return self.solution_processor.process_solutions(problem.task_id, response)


class MultiQueriesMultiSolutionsTester(MultiSolutionTester):
    """
    Generates multiple solutions using multiple queries to the language model.
    This is less efficient but avoids token constraints by generating one solution per query.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the multiple-queries multi-solution tester."""
        super().__init__(*args, **kwargs)
        self.prompt_generator = PromptGenerator(num_solutions=1)

    def _generate_solutions(self, problem: AlloyProblem) -> list[str | None]:
        """
        Generate solutions using multiple queries, one per solution.

        Args:
            problem: The Alloy problem to generate solutions for

        Returns:
            List of generated solutions
        """
        return [self._generate_solution(problem) for _ in range(self.total_solutions)]
