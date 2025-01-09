from playwright.sync_api import sync_playwright
from langchain_core.tools import Tool
import ast
from collections import defaultdict
from bs4 import BeautifulSoup


# Initialize Playwright context
def init_playwright():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    return playwright, browser, context


# Global variables to share Playwright context
playwright, browser, context = init_playwright()

# Tool functions


def open_page(url: str):
    try:
        print(f"Opening page: {url}")
        page = context.new_page()
        page.goto(url)
        return f"Page opened successfully: {url}"
    except Exception as e:
        return f"Error opening page: {e}"


def click_element(selector: str):
    try:
        print(f"Clicking element: {selector}")
        page = context.pages[-1]  # Use the last opened page
        page.click(selector)
        return f"Element clicked successfully: {selector}"
    except Exception as e:
        return f"Error clicking element: {e}"


def extract_text(inputs):
    try:
        inputs = ast.literal_eval(inputs)
        selector = inputs["selector"]
        index = int(inputs['index'])
        print(f"Extracting text from element: {selector}")
        page = context.pages[-1]  # Use the last opened page
        text = page.text_content(selector)[2000*index:2000*(index+1)]
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
                tags_with_selectors[tag.name].update(
                    tag.get("class"))  # Add all classes
            if tag.get("id"):
                tags_with_selectors[tag.name].add(
                    f"#{tag.get('id')}")  # Add id prefixed with #

        return f"HTML tags and CSS selectors: {dict(tags_with_selectors)}"

    except Exception as e:
        return f"Error extracting HTML: {e}"


def extract_html_content(index):
    try:
        print(f"Extracting HTML content from the page, segment index: {index}")
        page = context.pages[-1]  # Use the last opened page
        full_html = page.content()
        segment = full_html[2000*index:2000*(index+1)]
        return f"Extracted HTML segment: {segment}"
    except Exception as e:
        return f"Error extracting HTML content: {e}"

# Example usage:
# Call `extract_html_content({'index': 0})` to get the first 2000 characters of the HTML content.


def extract_button_elements(*args, **kwargs):
    try:
        # Get the most recently opened page in the context
        page = context.pages[-1]
        full_html = page.content()
        soup = BeautifulSoup(full_html, "html.parser")
        print("Extracting button elements...")

        # List to collect button details
        buttons_info = []

        # Find all <button> tags
        for button in soup.find_all('button'):
            button_info = {
                "html_code": str(button),
                "text": button.get_text(strip=True),
            }
            buttons_info.append(button_info)

        # Find all <input> tags with type "button" or "submit"
        for input_tag in soup.find_all('input', {'type': ['button', 'submit']}):
            input_info = {
                "html_code": str(input_tag),

                "value": input_tag.get("value", ""),
                "type": input_tag.get("type", ""),
            }
            buttons_info.append(input_info)

        return buttons_info

    except Exception as e:
        return f"Error extracting button elements: {e}"

# Example usage:
# Call `extract_button_elements()` after opening a page with `open_page(url)` to get details of all button elements.


def extract_anchor_tags(*args, **kwargs):
    try:
        # Get the most recently opened page in the context
        page = context.pages[-1]
        full_html = page.content()
        soup = BeautifulSoup(full_html, "html.parser")
        print("Extracting anchor tags...")

        # Dictionary to collect anchor tags with details
        anchors_info = []

        # Find all anchor tags in the HTML
        for anchor in soup.find_all('a', href=True):
            # Collecting necessary details for each anchor tag
            anchor_info = {
                "html_code": str(anchor),
                "link": anchor["href"],
                "text": anchor.get_text(strip=True),
            }
            anchors_info.append(anchor_info)

        return anchors_info

    except Exception as e:
        return f"Error extracting anchor tags: {e}"


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


def extract_input_fields(*args, **kwargs):
    try:
        # Get the most recently opened page in the context
        page = context.pages[-1]
        full_html = page.content()
        soup = BeautifulSoup(full_html, "html.parser")
        print("Extracting input fields...")

        # List to collect input field details
        inputs_info = []

        # Find all <input> tags
        for input_tag in soup.find_all('input'):
            input_info = {
                "html_code": str(input_tag),
                "type": input_tag.get("type", ""),
                "name": input_tag.get("name", ""),
                "placeholder": input_tag.get("placeholder", ""),
                "value": input_tag.get("value", ""),
            }
            inputs_info.append(input_info)

        # Find all <textarea> tags
        for textarea in soup.find_all('textarea'):
            textarea_info = {
                "html_code": str(textarea),
                "name": textarea.get("name", ""),
                "placeholder": textarea.get("placeholder", ""),
                "value": textarea.get_text(strip=True),
            }
            inputs_info.append(textarea_info)

        # Find all <select> tags
        for select in soup.find_all('select'):
            select_info = {
                "html_code": str(select),
                "name": select.get("name", ""),
                "options": [option.get_text(strip=True) for option in select.find_all('option')],
                "selected_value": next((option.get_text(strip=True) for option in select.find_all('option') if option.has_attr('selected')), None),
            }
            inputs_info.append(select_info)

        return inputs_info

    except Exception as e:
        return f"Error extracting input fields: {e}"

# Example usage:
# Call `extract_input_fields()` after opening a page with `open_page(url)` to get details of all input fields.


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
        name="Extract HTML Tags and CSS Selectors",
        func=extract_html_tags,
        description="Useful for extracting all the HTML tags and their corresponding CSS selectors present in a website"
    ),
    Tool.from_function(
        name="Extract Anchor Tags",
        func=extract_anchor_tags,
        description="Extracts all anchor tags from the current page, including their HTML code, CSS selectors, links, and text content. Useful for when you need to get more information about anchor tags."
    ),
    Tool.from_function(
        name="Extract Button Elements",
        func=extract_anchor_tags,
        description="Extracts all Button Elements (including submit button) from the current page, including their HTML code, CSS selectors, links, and text content. Useful for when you need to get more information about Button Elements."
    ),
    Tool.from_function(
        name="Extract Input Fields",
        func=extract_input_fields,
        description="Extracts all input fields from the current page, including their HTML code, CSS selectors, types, names, placeholders, values, and options. Useful for when you need to get more information about Inpuit Fields."
    ),
    Tool.from_function(
        name="Extract HTML Content",
        func=extract_html_content,
        description="Extracts the full HTML content of the webpage and returns it in 2000-character segments based on the provided index. Useful for handling large HTML content in manageable parts. Args: index:int -> The index of the 2000-character segment to retrieve. increase index to get the next 2000-character segment"
    ),
    Tool.from_function(
        name="Click Element",
        func=click_element,
        description="Useful for clicking an element (HREF or buttons) on a webpage. Args: selector:str -> HTML tag or CSS selector of the element (href/button) to click"
    ),
    Tool.from_function(
        name="Type Into Field",
        func=type_into_field,
        description="Useful for typing text into a field. Args: {'selector': 'CSS selector of the field obtained from Extract HTML Tags and CSS Selectors tool', 'text': 'Text to type'}"
    ),
    Tool.from_function(
        name="Extract Text",
        func=extract_text,
        description="Extracts up to 2000 characters of text from a specified element on the page using its CSS selector. Useful for handling large amounts of text by specifying an index to paginate through segments of the text. Args: {'selector': 'CSS selector of the element to extract text from', 'index': 'Index of the 2000-character segment to retrieve'} Example: passing 0 as index extracts first 2000 characters, passing 1 extracts 2001th to 4000th text and so on. Increase index to get more context."
    ),
    Tool.from_function(
        name="Close Browser",
        func=close_browser,
        description="Closes the browser and cleans up resources. Args: None"
    )
]

if __name__ == "__main__":
    open_page('https://github.com/nishchitbh')
    print(extract_anchor_tags())