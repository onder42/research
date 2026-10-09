import os
import requests
import wikipediaapi
from dotenv import load_dotenv

# Load sensitive environment variables from our hidden .env file
load_dotenv()
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")


class ResearchEngine:
    """
    Blueprint responsible for orchestrating web data collection
    and managing a FileHandler to cache the results.
    """
    def __init__(self):
        # Dynamically import and instantiate the FileHandler from our infrastructure package
        from src.infrastructure.file_handler import FileHandler
        self.file_handler = FileHandler()
        self.serp_api_key = SERPAPI_API_KEY

    def fetch_wikipedia_data(self, topic):
        """
        Pure Network Function: Fetches an introduction summary and full text
        payload from Wikipedia. Does NOT save files.
        """
        wiki = wikipediaapi.Wikipedia(
            user_agent="ChrisResearchAssistant/1.0 (chris@example.com)",
            language="en"
        )
        
        page = wiki.page(topic)
        if not page.exists():
            print(f"Error: Wikipedia page '{topic}' does not exist.")
            return None

        # Structure and return the extracted data dictionary
        return {
            "title": page.title,
            "url": page.fullurl,
            "summary": page.summary,
            "text": page.text
        }

    def fetch_web_search(self, query):
        """
        Queries SerpAPI using the DuckDuckGo engine and returns the response dictionary.
        """
        if not self.serp_api_key:
            print("[ResearchEngine Error] SERPAPI_API_KEY is missing from environment setup.")
            return None

        params = {
            "api_key": self.serp_api_key,
            "engine": "duckduckgo",
            "q": query
        }

        try:
            search = requests.get("https://serpapi.com/search", params=params)
            return search.json()
        except requests.exceptions.RequestException as e:
            print(f"Network request failed: {e}")
            return None

