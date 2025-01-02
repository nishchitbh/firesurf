import requests
from bs4 import BeautifulSoup

def scrape_link(url):
    print(f"Scraping: {url}")
    
    try:
        # Send a GET request to the URL
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract title (if available)
        title = soup.title.string.strip() if soup.title else "No title found"

        # Extract headers (filter out empty ones)
        headers = [h1.get_text(strip=True) for h1 in soup.find_all('h1') if h1.get_text(strip=True)]

        # Extract meaningful paragraphs
        paragraphs = [
            p.get_text(strip=True) for p in soup.find_all('p')
            if len(p.get_text(strip=True)) > 10  # Ignore very short or irrelevant text
        ]

        # Combine results
        scraped_data = {
            "Title": title,
            "Headers": headers,
            "Paragraphs": paragraphs[:5],  # Limit to first 5 paragraphs for brevity
        }

        return scraped_data

    except Exception as e:
        return {"Error": f"Failed to scrape {url}. Error: {e}"}

