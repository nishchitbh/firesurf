from playwright.sync_api import sync_playwright
from langchain_core.tools import Tool
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_experimental.text_splitter import SemanticChunker
import ast
from collections import defaultdict
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()


embedding = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004", google_api_key=os.getenv("GOOGLE_GEMINI_API2"))

text_splitter = SemanticChunker(embeddings=embedding)

folder_path = "db"
vector_store = Chroma(persist_directory=folder_path,
                      embedding_function=embedding)


# Initialize Playwright context
def init_playwright():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    return playwright, browser, context


# Global variables to share Playwright context
playwright, browser, context = init_playwright()

# Tool functions


def open_page(url: str):
    """Opens a webpage and returns the page object."""
    try:
        print(f"Opening page: {url}")
        page = context.new_page()
        page.goto(url)
        return f"Page opened successfully: {url}"
    except Exception as e:
        return f"Error opening page: {e}"


def click_element(selector: str):
    """Clicks on an element identified by a selector."""
    try:
        print(f"Clicking element: {selector}")
        page = context.pages[-1]  # Use the last opened page
        page.click(selector)
        return f"Element clicked successfully: {selector}"
    except Exception as e:
        return f"Error clicking element: {e}"


def extract_text(selector: str):
    """Extracts text from an element identified by a selector."""
    try:
        print(f"Extracting text from element: {selector}")
        page = context.pages[-1]  # Use the last opened page
        text = page.text_content(selector)
        return f"Extracted text: {text}"
    except Exception as e:
        return f"Error extracting text: {e}"

def extract_html_tags(*args, **kwargs):
    try:
        # Get the most recently opened page in the context
        page = context.pages[-1]
        full_html = page.content()
        soup = BeautifulSoup(full_html, "html.parser")
        print("Extracting HTML Tags and CSS Selectors...")
    
        # Dictionary to collect tags and their CSS selectors
        tags_with_selectors = defaultdict(set)

        # Iterate over all elements in the HTML
        for tag in soup.find_all(True):  # True finds all tags
            # Add class and id attributes if present
            if tag.get("class"):
                tags_with_selectors[tag.name].update(tag.get("class"))  # Add all classes
            if tag.get("id"):
                tags_with_selectors[tag.name].add(f"#{tag.get('id')}")  # Add id prefixed with #

        return f"HTML tags and CSS selectors: {dict(tags_with_selectors)}"

    except Exception as e:
        return f"Error extracting HTML: {e}"

def type_into_field(inputs: str):
    """Types text into a field identified by a selector."""
    try:

        inputs = ast.literal_eval(inputs)
        selector = inputs["selector"]
        text = inputs["text"]
        print(f"Typing {text} into {selector}")
        print(f"Typing into field: {selector}, text: {text}")
        page = context.pages[-1]  # Use the last opened page
        page.fill(selector, text)
        to_print = f"Text typed successfully: {text} into {selector}"
        print(to_print
              )
        return to_print
    except Exception as e:
        return f"Error typing into field: {e}"


def close_browser(*args, **kwargs):
    """Closes the browser and Playwright context."""
    try:
        print("Closing browser...")
        browser.close()
        playwright.stop()
        return "Browser closed successfully."
    except Exception as e:
        return f"Error closing browser: {e}"


# Define tools
playwright_tools = [
    Tool.from_function(
        name="Open Page",
        func=open_page,
        description="Useful for opening a webpage. Args: url:str -> URL of webpage to open"
    ),
    Tool.from_function(
        name="Click Element",
        func=click_element,
        description="Useful for clicking an element on a webpage. Args: selector:str -> CSS selector of the element to click"
    ),
    Tool.from_function(
        name="Extract Text",
        func=extract_text,
        description="Useful for extracting text from an element (HTML tag or CSS Selector). Args: selector:str -> CSS selector of the element to extract text from"
    ),
    Tool.from_function(
        name="Extract HTML Tags and CSS Selectors",
        func=extract_html_tags,
        description="Useful for extracting all the HTML tags and CSS selectors present in a website"
    ),
    Tool.from_function(
        name="Type Into Field",
        func=type_into_field,
        description="Useful for typing text into a field. Args: {'selector': 'CSS selector of the field', 'text': 'Text to type'}"
    ),
    Tool.from_function(
        name="Close Browser",
        func=close_browser,
        description="Closes the browser and cleans up resources. Args: None"
    )
]

def main():
    open_page("http://fedan.com.np/")
    print(extract_html_tags())
    close_browser()

if __name__ == "__main__":
    main()