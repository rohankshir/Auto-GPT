from promptgenerator import PromptGenerator


TASK_MODES = {
    "improve_python_code": ["evaluate_code", "improve_code",  "write_tests", "run_python_tests", "task_complete", "overwrite_tests"],
    "research_report": ["google", "browse_website", "read_file", "write_to_file", "append_to_file", "task_complete"],
    "create_code_from_scratch": ["google", "browse_website", "read_file", "write_to_file", "append_to_file", "evaluate_code", "write_tests", "execute_python_file", "task_complete"],
}


def get_prompt(mode=None):
    """
    This function generates a prompt string that includes various constraints, commands, resources, and performance evaluations.

    Returns:
        str: The generated prompt string.
    """

    # Initialize the PromptGenerator object
    prompt_generator = PromptGenerator()

    # Add constraints to the PromptGenerator object
    prompt_generator.add_constraint(
        "~4000 word limit for short term memory. Your short term memory is short, so immediately save important information to files.")
    prompt_generator.add_constraint(
        "If you are unsure how you previously did something or want to recall past events, thinking about similar events will help you remember.")
    prompt_generator.add_constraint("No user assistance")
    prompt_generator.add_constraint(
        'Exclusively use the commands listed in double quotes e.g. "command name"')

    # Define the command list
    commands = [
        ("Google Search", "google", {"input": "<search>"}),
        ("Browse Website", "browse_website", {
         "url": "<url>", "question": "<what_you_want_to_find_on_website>"}),
        ("Start GPT Agent", "start_agent", {
         "name": "<name>", "task": "<short_task_desc>", "prompt": "<prompt>"}),
        ("Message GPT Agent", "message_agent", {
         "key": "<key>", "message": "<message>"}),
        ("List GPT Agents", "list_agents", {}),
        ("Delete GPT Agent", "delete_agent", {"key": "<key>"}),
        ("Write to file", "write_to_file", {
         "file": "<file>", "text": "<text>"}),
        ("Read file", "read_file", {"file": "<file>"}),
        ("Append to file", "append_to_file", {
         "file": "<file>", "text": "<text>"}),
        ("Delete file", "delete_file", {"file": "<file>"}),
        ("Search Files", "search_files", {"directory": "<directory>"}),
        ("Evaluate Code File", "evaluate_code", {"file": "<file>", "focus": "<list_of_focus_areas>"}),
        ("Get Improved Code", "improve_code", {
         "suggestions": "<list_of_suggestions>", "code": "<full_code_string>"}),
        ("Write Tests", "write_tests", {
         "code": "<full_code_string>", "focus": "<list_of_focus_areas>", "file": "<file>"}),
        ("Overwrite Tests", "overwrite_tests", {
         "code": "<full_code_string>", "focus": "<list_of_focus_areas>", "file": "<file>"}),
        ("Execute Python File", "execute_python_file", {"file": "<file>"}),
        ("Run Python Tests", "run_python_tests", {"file": "<file>"}),
        ("Execute Shell Command, non-interactive commands only",
         "execute_shell", {"command_line": "<command_line>"}),
        ("Task Complete (Shutdown)", "task_complete", {"reason": "<reason>"}),
        ("Generate Image", "generate_image", {"prompt": "<prompt>"}),
        ("Do Nothing", "do_nothing", {}),
    ]
    
    if mode:
        prompt_generator.add_mode(mode)

    # Add commands to the PromptGenerator object
    for command_label, command_name, args in commands:
        if mode is not None and command_name not in TASK_MODES[mode]:
            continue
        prompt_generator.add_command(command_label, command_name, args)

    # Add resources to the PromptGenerator object
    prompt_generator.add_resource(
        "Internet access for searches and information gathering.")
    prompt_generator.add_resource("Long Term memory management.")
    prompt_generator.add_resource(
        "GPT-3.5 powered Agents for delegation of simple tasks.")
    prompt_generator.add_resource("File output.")

    # Add performance evaluations to the PromptGenerator object
    prompt_generator.add_performance_evaluation(
        "Continuously review and analyze your actions to ensure you are performing to the best of your abilities.")
    prompt_generator.add_performance_evaluation(
        "Constructively self-criticize your big-picture behavior constantly.")
    prompt_generator.add_performance_evaluation(
        "Reflect on past decisions and strategies to refine your approach.")
    prompt_generator.add_performance_evaluation(
        "Every command has a cost, so be smart and efficient. Aim to complete tasks in the least number of steps.")

    # Generate the prompt string
    prompt_string = prompt_generator.generate_prompt_string()

    return prompt_string
