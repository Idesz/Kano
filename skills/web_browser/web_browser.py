import requests
from bs4 import BeautifulSoup
import json

class WebBrowser:
    def execute(self, action: str, url: str = None, query: str = None):
        if action == "scrape" and url:
            return self._scrape(url)
        elif action == "search" and query:
            return self._search(query)
        return "Invalid action or parameters"

    def _scrape(self, url):
        try:
            headers = {"User-Agent": "Kano/1.0 (Autonomous Agent)"}
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract text content, focus on main content if possible
            for script in soup(["script", "style"]):
                script.decompose()
            return soup.get_text(separator=' ', strip=True)[:5000] # Limit size
        except Exception as e:
            return f"Error scraping {url}: {e}"

    def _search(self, query):
        # Using a simple search redirect or a placeholder for actual search API
        return f"Search capability for '{query}' would typically use DuckDuckGo or Google API. Placeholder active."
