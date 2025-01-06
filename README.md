# Firesurf

Firesurf is an interactive CLI based coding assistant that leverages the power of large language models to help users with their coding tasks. It uses a Google Gemini model, along with a ReAct agent framework, to provide intelligent and context-aware assistance.

## Project Structure

- `.env`: Contains environment variables such as API keys. **Note:** This file is not tracked by Git and should be created with your own API keys.
- `.env.example`: An example `.env` file with placeholder API keys.
- `.gitignore`: Specifies intentionally untracked files that Git should ignore.
- `guidelines.py`: Contains the guidelines for the project.
- `main.py`: The main entry point of the application. This script sets up the chat interface and interacts with the agent executor.
- `model_manager.py`: Manages the language model, agent setup, and tool configurations.
- `prompts.py`: Contains the prompt template used by the ReAct agent.
- `requirements.txt`: Lists the Python dependencies required to run the project.
- `scraper.py`: Contains the code for web scraping functionality. It uses `requests` and `BeautifulSoup` to scrape data from a given URL, extracting the title, headers, and paragraphs.
- `search.py`: Contains the code for web search functionality. It uses `requests` and `BeautifulSoup` to search on DuckDuckGo and extract the title, link, and description of the search results.
- `tools.py`: Defines the tools available to the agent, such as listing directory contents, writing code, reading files, running PowerShell commands, searching the internet, scraping websites, and reading notebook files.

## How it Works

1. **Environment Setup:**
   - Create a `.env` file in the project directory and add your API key for Google Gemini. Refer to `.env.example` for the required keys.
   - Install the required Python packages using `pip install -r requirements.txt`.

2. **Main Application (`main.py`):**
   - The main script initializes a chat interface where you can interact with the coding assistant.
   - It takes user input, passes it to the agent executor, and displays the response.
   - It also maintains a chat history to provide context for future interactions.

3. **Model Management (`model_manager.py`):**
   - This file sets up the Google Gemini language model and its API.
   - It configures a ReAct agent using a prompt defined in `prompts.py`. The prompt is loaded from the langchain hub and the template is set from the prompts.py file.
   - It also defines the tools that the agent can use, which are defined in `tools.py`.

4. **Prompt Template (`prompts.py`):**
    - This file contains the prompt template used by the ReAct agent. It instructs the agent on how to behave, use tools, and follow a specific format for its responses.

5. **Tools (`tools.py`):**
   - This file defines the custom tools available to the agent, such as:
     - `List Directory`: Useful for when you need to get files in a directory. Args: directory:str, which is the name of directory where you're using list directory command. use '.' for current directory.
     - `Write code`: Useful for when you need to write code to a file. Args: {'filename': filename, 'code': code} both filename and code should be string.
     - `Read file`: Useful for when you need to read file. Arg: filename:str
     - `Execute comands`: Useful for when you need to run commands of Windows-11-10.0.26100-SP0 operating system, run codes, control the computer through Powershell CLI, etc. Run commands of Windows-11-10.0.26100-SP0 operating system only, nothing else. Arg: command: str
     - `Search Internet`: Useful for searching for documentation, error fixing guides, etc. from internet. Arg: query: str
     - `Scrape website`: Useful for scraping website to get more information about a link. Arg: query: str, which is the link to the website obtained from Search Internet tool
     - `Notebook Reader`: Useful for when you need to read an ipynb notebook. Args: filename: str, directory to the file

## Dependencies

The project dependencies are listed in `requirements.txt`.

## Usage

1. Ensure you have a `.env` file with the required API keys.
2. Run `python main.py` to start the interactive coding assistant.
3. Enter your coding questions or tasks in the chat prompt.

## Contributing

Contributions to Firesurf are welcome! Please feel free to submit pull requests with improvements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.