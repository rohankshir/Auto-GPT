import docker
import os
import subprocess
<<<<<<< Updated upstream
=======
from config import Config

cfg = Config()
>>>>>>> Stashed changes


WORKSPACE_FOLDER = "auto_gpt_workspace"


def execute_python_file(file):
    """Execute a Python file in a Docker container and return the output"""

<<<<<<< Updated upstream
    print (f"Executing file '{file}' in workspace '{WORKSPACE_FOLDER}'")
=======
    print(f"Executing file '{file}' in workspace '{WORKSPACE_FOLDER}'")
>>>>>>> Stashed changes

    if not file.endswith(".py"):
        return "Error: Invalid file type. Only .py files are allowed."

    file_path = os.path.join(WORKSPACE_FOLDER, file)

    if not os.path.isfile(file_path):
        return f"Error: File '{file}' does not exist."

    try:
        client = docker.from_env()

        image_name = 'python:3.10'
        try:
            client.images.get(image_name)
            print(f"Image '{image_name}' found locally")
        except docker.errors.ImageNotFound:
<<<<<<< Updated upstream
            print(f"Image '{image_name}' not found locally, pulling from Docker Hub")
=======
            print(
                f"Image '{image_name}' not found locally, pulling from Docker Hub")
>>>>>>> Stashed changes
            # Use the low-level API to stream the pull response
            low_level_client = docker.APIClient()
            for line in low_level_client.pull(image_name, stream=True, decode=True):
                # Print the status and progress, if available
                status = line.get('status')
                progress = line.get('progress')
                if status and progress:
                    print(f"{status}: {progress}")
                elif status:
                    print(status)

        # You can replace 'python:3.8' with the desired Python image/version
        # You can find available Python images on Docker Hub:
        # https://hub.docker.com/_/python
        container = client.containers.run(
            image_name,
            f'python {file}',
            volumes={
                os.path.abspath(WORKSPACE_FOLDER): {
                    'bind': '/workspace',
                    'mode': 'ro'}},
            working_dir='/workspace',
            stderr=True,
            stdout=True,
            detach=True,
        )

        output = container.wait()
        logs = container.logs().decode('utf-8')
        container.remove()

        # print(f"Execution complete. Output: {output}")
        # print(f"Logs: {logs}")

        return logs

    except Exception as e:
        return f"Error: {str(e)}"


<<<<<<< Updated upstream
=======


def run_python_tests(file):
    executable = cfg.pytest_executable
    file_path = os.path.join(WORKSPACE_FOLDER, file)
    output = subprocess.run(
        f"{executable} {file_path}", shell=True, capture_output=True)
    return output
>>>>>>> Stashed changes
def execute_shell(command_line):

    current_dir = os.getcwd()

<<<<<<< Updated upstream
    if not WORKSPACE_FOLDER in current_dir: # Change dir into workspace if necessary
        work_dir = os.path.join(os.getcwd(), WORKSPACE_FOLDER)
        os.chdir(work_dir)

    print (f"Executing command '{command_line}' in working directory '{os.getcwd()}'")
=======
    if not WORKSPACE_FOLDER in current_dir:  # Change dir into workspace if necessary
        work_dir = os.path.join(os.getcwd(), WORKSPACE_FOLDER)
        os.chdir(work_dir)

    print(
        f"Executing command '{command_line}' in working directory '{os.getcwd()}'")
>>>>>>> Stashed changes

    result = subprocess.run(command_line, capture_output=True, shell=True)
    output = f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

<<<<<<< Updated upstream
    # Change back to whatever the prior working dir was
=======
    # Change back to whatever the prior working dir wasππ
>>>>>>> Stashed changes

    os.chdir(current_dir)

    return output
