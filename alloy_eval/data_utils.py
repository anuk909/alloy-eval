import json
from pathlib import Path
from typing import Any, List
from .models import AlloyProblem


def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    """Read a JSONL file."""
    data = []
    with open(path) as f:
        for line in f:
            data.append(json.loads(line))
    return data


def write_jsonl(path: str | Path, data: list[dict[str, Any]]) -> None:
    """Write data to a JSONL file."""
    with open(path, "w") as f:
        for item in data:
            f.write(json.dumps(item) + "\n")


def read_problems(file_path: str | Path) -> List[AlloyProblem]:
    """Read problems from a JSONL file."""
    problems = []
    with open(file_path) as f:
        for line in f:
            data = json.loads(line)
            problems.append(AlloyProblem.model_validate(data))
    return problems


def write_results(results: list[dict[str, Any]], output_file: str | Path) -> None:
    """Write evaluation results to a JSONL file."""
    write_jsonl(output_file, results)
