from pathlib import Path
import shutil
from typing import Any, Sequence
from rich.console import Console

console = Console()


def generate_report(
    title: str,
    model: str,
    results: Sequence[dict[str, Any]],
    success_key: str = "passed",
    success_label: str = "Tests passed",
) -> None:
    """Generate a report for test or generation results.

    Args:
        title: Report title
        model: Model name
        results: List of result dictionaries
        success_key: Key to check for success in results
        success_label: Label for successful results
    """
    total = len(results)
    successful = sum(1 for r in results if r.get(success_key))

    console.print(
        f"""
    ===== {title} =====
    Model: {model}
    Total problems: {total}
    {success_label}: {successful}
    Success rate: {successful/total*100:.2f}%
    """
    )


def setup_debug_dir(debug_dir: str | Path | None) -> Path | None:
    """Set up debug directory if provided."""
    if not debug_dir:
        return None

    debug_path = Path(debug_dir)
    # Clean any existing files
    if debug_path.exists():
        shutil.rmtree(debug_path)
    debug_path.mkdir(parents=True, exist_ok=True)
    return debug_path
