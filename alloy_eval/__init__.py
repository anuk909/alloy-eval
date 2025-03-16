"""
AlloyEval: A benchmark for evaluating language models on Alloy formal specification tasks.
"""

from alloy_eval.evaluation import evaluate_functional_correctness
from alloy_eval.openai_tester import OpenAITester
from alloy_eval.models import AlloyProblem, EvaluationResult

__version__ = "0.1.0"
__all__ = [
    # Core evaluation
    "evaluate_functional_correctness",
    "AlloyProblem",
    "EvaluationResult",
    # OpenAI testing
    "OpenAITester",
]
