from pydantic import BaseModel
from typing import Optional


class AlloyProblem(BaseModel):
    """Represents a single Alloy benchmark problem."""

    task_id: str
    prompt: str
    signatures: str
    predicate_signature: str
    check: str
    canonical_solution: Optional[str] = None


class AlloyPred(BaseModel):
    """Pydantic model for parsing OpenAI API responses."""

    content: str


class EvaluationResult(BaseModel):
    """Represents the result of evaluating a single problem."""

    task_id: str
    passed: bool
    solution: Optional[str] = None
    details: str = ""
    error_message: Optional[str] = None
    debug_file: Optional[str] = None
