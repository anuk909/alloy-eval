import re

from alloy_eval.ui_utils import console


class SolutionProcessor:
    """Handles the processing of solutions from OpenAI responses."""

    def __init__(self, num_solutions: int = 1):
        """
        Initialize the solution processor.

        Args:
            num_solutions: Number of different solutions to generate for each problem
        """
        self.num_solutions = num_solutions

    def clean_solution(self, solution: str) -> str:
        """
        Clean up the solution text.

        Args:
            solution: The raw solution text

        Returns:
            Cleaned solution text
        """
        if not solution:
            return ""
        solution = solution.strip().rstrip("}").strip()

        # Extract code from markdown blocks if present
        code_match = re.search(r"```(?:alloy)?\s*(.*?)```", solution, re.DOTALL)
        if code_match:
            solution = code_match.group(1).strip()

        # Remove triple quotes if present
        solution = solution.replace('"""', "").strip()

        return solution

    def process_solutions(self, task_id: str, response: str | None) -> list[str | None]:
        """
        Process the response and extract solutions.

        Args:
            task_id: The task ID
            response: The response from OpenAI

        Returns:
            A list of processed solutions
        """
        if not response:
            return [None] * self.num_solutions

        # Clean up solution
        solution = self.clean_solution(response)

        # Split the solution into multiple solutions if needed
        solutions = [s.strip() for s in solution.split("\n\n") if s.strip()]

        # If we got fewer solutions than requested, pad with None
        while len(solutions) < self.num_solutions:
            solutions.append(None)
        if len(solutions) < self.num_solutions:
            console.print(
                f"[yellow]Warning: Got fewer solutions than requested, requested {self.num_solutions} and got {len(solutions)}[/yellow]"
            )

        # If we got more solutions than requested, truncate
        solutions = solutions[: self.num_solutions]
        if len(solutions) > self.num_solutions:
            console.print(
                f"[yellow]Warning: Got more solutions than requested. requested {self.num_solutions} and got {len(solutions)}[/yellow]"
            )

        return solutions
