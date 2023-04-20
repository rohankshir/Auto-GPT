from typing import List
import json
from config import Config
from ai_config import AIConfig
from call_ai_function import call_ai_function
from llm_utils import create_chat_completion
import logging
cfg = Config()

logger = logging.getLogger(__name__)
def evaluate_code(code: str) -> List[str]:
    """
    A function that takes in a string and returns a response from create chat completion api call.

    Parameters:
        code (str): Code to be evaluated.
    Returns:
        A result string from create chat completion. A list of suggestions to improve the code.
    """

    function_string = "def analyze_code(code: str) -> List[str]:"
    args = [code]
    description_string = """Analyzes the given code and returns a list of suggestions for improvements."""

    result_string = call_ai_function(function_string, args, description_string)

    return result_string


def evaluate_code_with_goal(code: str, focus: List[str], ai_cfg: AIConfig) -> List[str]:
    """
    A function that takes in a string and returns a response from create chat completion api call.

    Parameters:
        code (str): Code to be evaluated.
    Returns:
        A result string from create chat completion. A list of suggestions to improve the code.
    """

    function_string = "def analyze_code(code: str, goals: List[str],) -> List[str]:"
    args = [code, json.dumps(focus)]
    description_string = f"""Analyzes the given code with certain goals and returns a list of suggestions for improvements towards this agent's higher level goals. {json.dumps(ai_cfg.ai_goals)}."""

    result_string = call_ai_function(function_string, args, description_string)

    return result_string


def improve_code(suggestions: List[str], code: str) -> str:
    """
    A function that takes in code and suggestions and returns a response from create chat completion api call.

    Parameters:
        suggestions (List): A list of suggestions around what needs to be improved.
        code (str): Code to be improved.
    Returns:
        A result string from create chat completion. Improved code in response.
    """

    function_string = (
        "def generate_improved_code(suggestions: List[str], code: str) -> str:"
    )
    args = [json.dumps(suggestions), code]
    description_string = """Improves the provided code based on the suggestions provided, making no other changes."""

    result_string = call_ai_function(function_string, args, description_string)
    return result_string


def improve_code_alternative(suggestions: List[str], code: str, ai_cfg: AIConfig) -> str:
    """
    A function that takes in code and suggestions and returns a parsed response from create chat completion api call.

    Parameters:
        suggestions (List): A list of suggestions around what needs to be improved.
        code (str): Code to be improved.
    Returns:
        Improved code based on suggestion
    """

    system_prompt = """You are code gpt, a 10x coder that takes in suggestions and efficiently makes changes to code. You *never* hallucinate new packages, and write helper functions and classes from scratch if necessary.
Only import packages from the standard libraries or very popular libraries like numpy, pandas, matplotlib, bs4, etc.
You expect code blocks as input  (denoted by ```) and a list of suggestions for improvement and you output the rewritten code that incorporates those improvements (denoted by ```)"""

    suggestion_list = '\n- '.join(suggestions)
    user_prompt = f"Suggestions:\n{suggestion_list}\n\nCode:\n```{code}```"
    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {"role": "user", "content": user_prompt},
    ]

    model = cfg.smart_llm_model
    response = create_chat_completion(
        model=model, messages=messages, temperature=0
    )
    if '```python' in response:
        parsed_response = response.split('```python')[1].split('```')[0]
    else:
        parsed_response = response.split('```')[1]
    return parsed_response


def write_tests(code: str, focus: List[str]) -> str:
    """
    A function that takes in code and focus topics and returns a response from create chat completion api call.

    Parameters:
        focus (List): A list of suggestions around what needs to be improved.
        code (str): Code for test cases to be generated against.
    Returns:
        A result string from create chat completion. Test cases for the submitted code in response.
    """

    function_string = (
        "def create_test_cases(code: str, focus: Optional[str] = None) -> str:"
    )
    args = [code, json.dumps(focus)]
    description_string = """Generates test cases for the existing code, focusing on specific areas if required."""

    result_string = call_ai_function(function_string, args, description_string)
    if '```python' in result_string:
        result_string = result_string.split('```python')[1].split('```')[0]
    elif '```' in result_string:
        result_string = result_string.split('```')[1]
    return result_string


def write_tests_alternative(code: str, suggestions: List[str], ai_cfg: AIConfig) -> str:
    """
    A function that takes in code and suggestions and returns a parsed response from create chat completion api call.

    Parameters:
        suggestions (List): A list of suggestions around what needs to be improved.
        code (str): Code to be improved.
    Returns:
        Improved code based on suggestion
    """

    system_prompt = """You create software; is expert in programming, documentation, unit testing and implementing best practices. You will deliver complete and functional applications based on client request.
    No matter how long it is; relies on SOLID and DRY code principles.
    You expect code blocks as input  (denoted by ```) and a list of suggestions for unit testing and you output clearly written unit tests that incorporates those suggestions
    Example:
    Suggestions:
    - test negative radius
    - test overflow radius
    Code:
    ```
    def area(radius):
        return math.pi * radius ** 2
        
    ```
    
    Answer:
    ```
    import pytest
    
    def test_area():
        assert area(1) == math.pi
        assert area(0) == 0
        
    def test_area_negative():
        assert area(-1) == math.pi
        
    def test_area_overflow():
        # raise exception
        with pytest.raises(ValueError):
            area(1e100)
    ```

    """

    system_prompt += f""" and you are helping an AI with the following role: {ai_cfg.ai_role}"""
    
    suggestion_list = '\n- '.join(suggestions)
    user_prompt = f"Suggestions:\n{suggestion_list}\n\nCode:\n```\n{code}\n```"
    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {"role": "user", "content": user_prompt},
    ]

    model = cfg.smart_llm_model
    response = create_chat_completion(
        model=model, messages=messages, temperature=0
    )
    logger.info("Writing tests")
    logger.info(messages)
    logger.info(response)
    if '```python' in response:
        parsed_response = response.split('```python')[1].split('```')[0]
    else:
        parsed_response = response.split('```')[1]
    return parsed_response
