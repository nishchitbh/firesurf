from langchain_core.tools import Tool
import ast
import subprocess
from search import search
import os
import platform
import distro
import nbformat
import difflib

os_type = platform.platform()

if 'linux' in os_type.lower():
    os_type = f"{distro.name()} {distro.version()}"

print(f"OS Type: {os_type}")


def extract_code_cells(file_path):
    # Read the notebook
    print(f"Reading notebook: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        notebook = nbformat.read(f, as_version=4)

    # Extract code from code cells
    code_cells = [
        cell["source"] for cell in notebook["cells"] if cell["cell_type"] == "code"
    ]
    cell_string = "\n".join(code_cells)

    return cell_string


def get_dir(directory):
    print(f"Searching directory: {directory}")
    try:
        return os.listdir(directory)
    except Exception as e:
        return f"Error: {e}"
# Useful for when you need to write code to a file. Args: {'filename': filename, 'code': code} both filename and code should be string.


def write_code(inputs: dict):
    try:
        inputs = ast.literal_eval(inputs)
        filename = inputs["filename"]
        new_code = inputs["code"]

        # Check if file exists
        file_exists = os.path.exists(filename)
        original_content = ""

        if file_exists:
            # Read the original content
            with open(filename, "r") as f:
                original_content = f.read()

            # Generate and display the diff in the terminal
            diff = list(difflib.unified_diff(
                original_content.splitlines(),
                new_code.splitlines(),
                fromfile=f"Original: {filename}",
                tofile=f"New: {filename}"
            ))

            # Print the diff to the console with colors
            for line in diff:
                if line.startswith('+'):
                    print(f"\033[92m{line}\033[0m")  # Green for additions
                elif line.startswith('-'):
                    print(f"\033[91m{line}\033[0m")  # Red for deletions
                elif line.startswith('^'):
                    print(f"\033[94m{line}\033[0m")  # Blue for indicators
                else:
                    print(line)
        else:
            # If file doesn't exist, show the code that will be created
            print(f"File {filename} doesn't exist. New file will contain:")
            print("=" * 50)
            print(new_code)
            print("=" * 50)

        # Ask for confirmation
        response = input(f"Accept changes to {filename}? (yes/no): ").lower()

        if response in ["yes", "y"]:
            # Write to the actual file
            with open(filename, "w") as f:
                f.write(new_code)
            return f"Changes accepted and written to {filename}"
        else:
            return f"Changes to {filename} were rejected"

    except Exception as e:
        return str(e)
# Useful for when you ened to read file. Arg: filename:str


def read_file(filename):
    print(f"Reading file: {filename}")
    try:
        with open(filename, "r") as f:
            return f.read()
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"


def get_cwd(a):
    print("Running getcwd")
    try:
        directory = os.getcwd()
        print(f"Current directory: {directory}")
        return directory
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"
# Useful for when you need to run powershell commands. Arg: command: str


def run_powershell(command):
    print(f"Running Command: {command}")
    try:
        command = command.strip("'")
        command = command.strip('"')
        result = subprocess.run(['powershell', '-Command', command],
                                capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        error = None
    except subprocess.CalledProcessError as e:
        output = e.stdout.strip()
        error = e.stderr.strip()
    print(f"Output: {output}\nError: {error if error else 'None'}")
    return f"Output: {output}\nError: {error if error else 'None'}"


def get_directory_structure(directory):
    print("Getting project structure...")

    def build_structure(path, prefix=""):
        ignored_dirs = {'node_modules', 'venv', 'env'}
        entries = sorted([e for e in os.listdir(path)
                          # Filter out ignored entries
                          if not e.startswith(('-', '_', '.')) and e not in ignored_dirs])
        structure = []

        for i, entry in enumerate(entries):
            entry_path = os.path.join(path, entry)
            is_last = (i == len(entries) - 1)
            connector = "└── " if is_last else "├── "
            sub_prefix = "    " if is_last else "│   "

            if os.path.isdir(entry_path):
                structure.append(f"{prefix}{connector}{entry}/")
                structure.extend(build_structure(
                    entry_path, prefix + sub_prefix))
            else:
                structure.append(f"{prefix}{connector}{entry}")

        return structure

    if not os.path.isdir(directory):
        raise ValueError(f"'{directory}' is not a valid directory.")
    return "\n".join(build_structure(directory))


# Collect all tools
tools = [
    Tool.from_function(
        name="List Directory",
        func=get_dir,
        description="Useful for when you need to get files in a directory. Args: directory:str, which is the name of directory where you're using list directory command. use '.' for current directory."
    ),
    Tool.from_function(
        name="Get Project Structure",
        func=get_directory_structure,
        description="Useful for when you need to get entire structure of directory including subdirectories, files inside subdirectories, etc. Args: directory:str, which is the name of directory where you're using list directory command. use '.' for current directory. ignore files inside .gitignore if the user asks about project structure."
    ),
    Tool.from_function(
        name="Write code",
        func=write_code,
        description="Useful for when you need to write code to a file. Args: {'filename': filename, 'code': code} both filename and code should be string."
    ),
    Tool.from_function(
        name="Read file",
        func=read_file,
        description="Useful for when you need to read file. Arg: filename:str"
    ),
    Tool.from_function(
        name="Execute comands",
        func=run_powershell,
        description=f"Useful for when you need to run commands of {os_type} operating system, run codes, control the computer through Powershell CLI, etc. Run commands of {os_type} operating system only, nothing else. Arg: command: str"
    ),
    Tool.from_function(
        name="Search Internet",
        func=search,
        description="Useful for searching for documentation, error fixing guides, etc. from internet. Arg: query: str"
    ),
    Tool.from_function(
        name="Get Current Working Directory",
        func=get_cwd,
        description="Useful for when you need to know which directory you are working on. Args: None"
    ),
    Tool.from_function(
        name="Notebook Reader",
        func=extract_code_cells,
        description="Useful for when you need to read an ipynb notebook. Args: filename: str, directory to the file"
    ),
]
