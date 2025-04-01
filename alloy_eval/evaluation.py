import subprocess
import tempfile
from pathlib import Path
from alloy_eval.models import AlloyProblem, EvaluationResult
from alloy_eval.data_utils import read_problems


def create_alloy_file(
    problem: AlloyProblem, solution: str, debug_dir: Path | None = None
) -> tuple[str, str | None]:
    """
    Create an Alloy file with the problem and solution.

    Args:
        problem: The Alloy problem
        solution: The solution to test
        debug_dir: Optional directory to save debug files

    Returns:
        Tuple of (temp file path, debug file path or None)
    """
    content = f"""
/* Problem: {problem.task_id} */

{problem.signatures}

/* 
{problem.prompt}
*/
{problem.predicate_definition}\t{solution}
}}

{problem.check}
""".strip()

    # Create temporary file for evaluation
    with tempfile.NamedTemporaryFile(suffix=".als", mode="w", delete=False) as f:
        f.write(content)
        temp_file = f.name

    # If debug directory provided, create a permanent copy
    debug_file = None
    if debug_dir:
        clean_name = problem.task_id.replace("/", "_")
        debug_file = debug_dir / f"{clean_name}.als"
        with open(debug_file, "w") as f:
            f.write(content)

    return temp_file, str(debug_file) if debug_file else None


def check_alloy_solution(
    als_file: str, alloy_path: str, timeout: int = 30
) -> tuple[bool, str | None]:
    """Run Alloy analyzer to check the solution."""
    try:
        cmd = [alloy_path, "exec", "-o", "/tmp", "-f", als_file]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)

        if "UNSAT" in result.stderr:
            return True, None
        return False, "Counterexample found"

    except subprocess.TimeoutExpired:
        return False, "Timeout: Alloy check took too long"
    except Exception as e:
        return False, f"Error: {str(e)}"


def evaluate_single_problem(
    problem: AlloyProblem,
    solution: str,
    alloy_path: str,
    debug_dir: str | Path | None = None,
) -> EvaluationResult:
    """Evaluate a single Alloy problem with the provided solution."""
    # Create Alloy file
    als_file, debug_file = create_alloy_file(problem, solution, debug_dir)

    # Run Alloy check
    passed, error = check_alloy_solution(als_file, alloy_path)

    return EvaluationResult(
        task_id=problem.task_id,
        passed=passed,
        solution=solution,
        error_message=error,
        debug_file=debug_file,
    )


def evaluate_functional_correctness(
    solution: str,
    alloy_path: str,
    problems_file: str | Path,
    debug_dir: str | Path | None = None,
) -> list[EvaluationResult]:
    """
    Evaluate a single solution against multiple problems.

    Args:
        solution: The Alloy predicate implementation
        alloy_path: Path to Alloy analyzer executable
        problems_file: Optional path to problems file. If not provided,
                      will look for default problems.json in package data
        debug_dir: Optional directory to save debug files

    Returns:
        A list of EvaluationResult containing pass/fail and error messages for each problem.
    """
    problems = read_problems(problems_file)
    return [
        evaluate_single_problem(problem, solution, alloy_path, debug_dir)
        for problem in problems
    ]
