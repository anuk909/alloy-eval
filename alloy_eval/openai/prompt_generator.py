from alloy_eval.models import AlloyProblem


class PromptGenerator:
    """Handles the generation of prompts for OpenAI models."""

    def __init__(self, num_solutions: int = 1):
        """
        Initialize the prompt generator.

        Args:
            num_solutions: Number of different solutions to generate for each problem
        """
        self.num_solutions = num_solutions

    def create_prompt(self, problem: AlloyProblem) -> str:
        """
        Create a prompt for the language model.

        Args:
            problem: The Alloy problem to generate a prompt for

        Returns:
            A formatted prompt string
        """
        if self.num_solutions == 1:
            prompt = f"""
            I need you to implement an Alloy predicate that satisfies the following requirements:

            Problem: {problem.prompt}

            Here's the signature definition:
            ```alloy
            {problem.signatures}
            ```

            Please complete this predicate implementation:
            ```alloy
            {problem.predicate_definition}
            ```           

            Output only the inner implemenation of the predicate in the required format for AlloyPred.          
            """
        else:
            prompt = f"""
            I need you to implement {self.num_solutions} unique Alloy predicates that satisfies the following requirements:

            Problem: {problem.prompt}

            Here's the signature definition:
            ```alloy
            {problem.signatures}
            ```

            Please complete this predicate implementation:
            ```alloy
            {problem.predicate_definition}
            ```           

            Output only the inner implemenation of the predicate in the required format for AlloyPred.
            
            IMPORTANT: Provide exactly {self.num_solutions} different solutions, separated by blank lines. Each solution should be a complete implementation of the predicate body.
            """

        return prompt
