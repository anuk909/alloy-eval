# AlloyEval

A benchmark for evaluating language models on Alloy formal specification tasks, inspired by OpenAI's HumanEval.

## Overview

AlloyEval is a collection of Alloy formal specification problems designed to test the capabilities of language models in generating correct formal specifications. Each problem consists of:

- A natural language task description
- Alloy signatures and type definitions
- A predicate signature to implement
- Test assertions to verify correctness

## Requirements

- Python 3.11 or higher
- Alloy Analyzer 6.0 or higher
- OpenAI API key (for OpenAI-based testing)

## Installation

```bash
pip install -e .
```

## Usage

### Evaluating GPT on Graph Benchmark

The quickest way to evaluate GPT on the graph benchmark:

```bash
# Set your OpenAI API key
export OPENAI_API_KEY=your_api_key

# Run the evaluation
eval_alloy_openai \
    --problems-file data/alloy_graph_benchmark.jsonl \
    --alloy-path /path/to/alloy \
    --model gpt-4o-mini \
    --temperature 0.2 \
    --debug-dir debug_files \
    --output results.jsonl
```

For more control, you can use the Python API:

```python
from alloy_eval import OpenAITester

# Initialize the tester
tester = OpenAITester(
    problems_file="data/alloy_graph_benchmark.jsonl",
    model="gpt-4o-mini",  # or any other OpenAI model
    alloy_path="/path/to/alloy",
    temperature=0.2,  # Optional: control randomness
    debug_dir="debug_files"  # Optional: save debug files
)

# Run tests
tester.run_tests("results.jsonl")
```

The results will be saved in JSONL format, containing:

- Pass/fail status for each problem
- Generated solutions
- Error messages for failed cases
- Paths to debug files (if enabled)

### Basic Evaluation

For evaluating your own solutions:

```python
from alloy_eval import evaluate_functional_correctness

# Evaluate a single solution
result = evaluate_functional_correctness(
    solution="your solution here",
    problem_id="problem_0",
    alloy_path="/path/to/alloy",
    problems_file="data/alloy_graph_benchmark.jsonl",
    debug_dir="debug_files"  # Optional: save debug files
)
```

## Problem Format

Each problem in AlloyEval follows this structure:

```python
{
    "task_id": "unique_identifier",
    "prompt": "Natural language description of the task",
    "signatures": "Alloy signature and type definitions",
    "predicate_signature": "Predicate signature to implement",
    "check": "Assertions to verify the solution"
}
```

## Results Format

The evaluation results have the following structure:

```python
{
    "task_id": "problem identifier",
    "passed": true/false,
    "error_message": "error message if failed",
    "debug_file": "path to debug .als file (if debugging enabled)"
}
```

For OpenAI testing, results also include:

```python
{
    "solution": "generated solution",
}
```

## Debugging

When debugging is enabled (via `debug_dir`), the evaluator will:

1. Create a separate `.als` file for each test case
2. Name files as `{task_id}.als` for easy identification
3. Include in each file:
   - Problem description as comments
   - Complete Alloy specification
   - Solution being tested
   - Test assertions

This makes it easy to:

- Inspect failed solutions
- Manually run specific test cases
- Modify and experiment with solutions