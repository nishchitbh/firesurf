import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, unquote


def search(query):
    print(f"Searching on internet: {query}")
    # DuckDuckGo search URL
    search_url = "https://duckduckgo.com/html/"

    # Set up search parameters (query)
    params = {'q': query}

    # Send a GET request to DuckDuckGo with the query
    response = requests.get(search_url, params=params)

    if response.status_code == 200:
        # Parse the HTML content of the search results page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all the search result links and their snippets
        results = soup.find_all('div', class_='result')

        try:
            result_list = []
            for result in results:
                # Title and link
                title_tag = result.find('a', class_='result__a')
                if title_tag:
                    title = title_tag.get_text()
                    raw_link = title_tag.get('href')

                    # Decode the redirected link
                    parsed_url = urlparse(raw_link)
                    query_params = parse_qs(parsed_url.query)
                    actual_link = unquote(query_params.get('uddg', [''])[0])
                else:
                    title, actual_link = "No title", "No link"

                # Snippet
                snippet_tag = result.find('a', class_='result__snippet')
                snippet = snippet_tag.get_text().strip(
                ) if snippet_tag else "No description available"

                # Combine result
                result_item = {"Title": title,
                               "Link": actual_link,
                               "Description": snippet}
                result_list.append(result_item)

            return result_list
        except Exception as e:
            return f"Error: {e}"
    else:
        return "Error occurred while searching."


# Example usage
if __name__ == "__main__":
    results = search("latest version of python")
    for res in results:
        print(res)
        print("-" * 60)
