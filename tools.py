from langchain_core.tools import Tool
import ast
import subprocess
from pathlib import Path
from search import search
from scraper import scrape_link
import os
# Useful for when you need to run a code. Args: filename:str
def execute_code(filename) -> str:
    print(f"Executing code: {filename}")
    try:
        filename = filename.strip("'")
        filename = filename.strip('"')
        result = subprocess.run(
            ['python', filename],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return result.stdout.decode()
    except subprocess.CalledProcessError as e:
        return  f"Code execution failed: {e.stderr.decode()}"

def get_dir(directory):
    print(f"Searching directory: {directory}")
    try:
        return os.listdir(directory)
    except Exception as e:
        return f"Error: {e}"
# Useful for when you need to fetch contents inside directory and its sub-directories. Args: directory:str
def get_project_structure(root_dir: str) -> str:
    print(f"Looking at project structure in directory: {root_dir}")
    try:
        root_dir = root_dir.strip("'")
        root_dir = root_dir.strip('"')
        default_ignore = ['venv', '__pycache__', 'env', '.git']
        ignore_dirs =  default_ignore
        
        root_path = Path(root_dir)
        output = []
        
        for path in root_path.rglob('*'):
            relative_path = path.relative_to(root_path)
            
            if any(ignored_dir in relative_path.parts for ignored_dir in ignore_dirs):
                continue
                
            path_str = '/'.join(relative_path.parts)
            type_ = 'directory' if path.is_dir() else 'file'
            output.append(f"{path_str} ({type_})")
        
        return "\n".join(output)
    except Exception as e:
        return str(e)

# Useful for when you need to write code to a file. Args: {'filename': filename, 'code': code} both filename and code should be string.
def write_code(inputs:dict):
    print("Writing code...")
    try:
        inputs = ast.literal_eval(inputs)
        filename = inputs["filename"]
        code = inputs["code"]
        with open(filename, "w") as f:
            f.write(code)
        return f"{code} written to {filename} successfully!"
    except Exception as e:
        return str(e)

# Useful for when you ened to read file. Arg: filename:str
def read_file(filename):
    print(f"Reading file: {filename}")
    try:
        with open(filename, "r") as f:
            return f.read()
    except Exception as e:
        return str(e)

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
    
    return f"Output: {output}\nError: {error if error else 'None'}"


# Collect all tools
tools = [
    Tool.from_function(
        name="Execute code",
        func=execute_code,
        description="Useful for when you need to run a code. Args: filename:str"
        ),
    Tool.from_function(
        name="List Directory",
        func=execute_code,
        description="Useful for when you need to get files in a directory. Args: directory:str"
        ),
    Tool.from_function(
        name="Get Project Structure",
        func=get_project_structure,
        description="Useful for when you need to get the project structure of the current directory. Get Project Structure like the List Directory tool except it nests through all sub-directories as well. Args: directory:str"
        ),
    Tool.from_function(
        name="Write code",
        func=write_code,
        description="Useful for when you need to write code to a file. Args: {'filename': filename, 'code': code} both filename and code should be string."
    ),
    Tool.from_function(
        name="Read file",
        func=read_file,
        description="Useful for when you ened to read file. Arg: filename:str"
    ),
    Tool.from_function(
        name="Execute powershell comands",
        func=run_powershell,
        description="Useful for when you need to run powershell commands (powershell only, nothing else). Arg: command: str"
    ),
    Tool.from_function(
        name="Search Internet",
        func=search,
        description="Useful for searching for documentation, error fixing guides, etc. from internet. Arg: query: str"
    ),
    Tool.from_function(
        name="Scrape website",
        func=scrape_link,
        description="Useful for scraping website to get more information about a link. Arg: query: str, which is the link to the website obtained from Search Internet tool"
    ),
]
