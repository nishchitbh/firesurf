from langchain_core.tools import Tool
import ast
import subprocess
from search import search
from scraper import scrape_link
import os


def get_dir(directory):
    print(f"Searching directory: {directory}")
    try:
        return os.listdir(directory)
    except Exception as e:
        return f"Error: {e}"
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
        name="List Directory",
        func=get_dir,
        description="Useful for when you need to get files in a directory. Args: directory:str, which is the name of directory where you're using list directory command. use '.' for current directory."
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
        name="Execute powershell comands",
        func=run_powershell,
        description="Useful for when you need to run powershell commands (powershell only, nothing else), run codes, control the computer through Powershell CLI, etc. Arg: command: str"
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
