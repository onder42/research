import os
import requests
import wikipediaapi
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load sensitive environment variables from our hidden .env file
load_dotenv()
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

class ResearchEngine:
    """
    Blueprint responsible for orchestrating web data collection
    and managing a FileHandler to cache the results.
    """
    def __init__(self):
        self.serp_api_key = SERPAPI_API_KEY
        self.youtube_api_key = YOUTUBE_API_KEY

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

    def fetch_youtube_search(self, query, max_results=10):
        """
        Queries the YouTube Data API v3 and returns the raw response dictionary.
        """
        if not self.youtube_api_key:
            print("[ResearchEngine Error] YOUTUBE_API_KEY is missing from environment setup.")
            return None

        try:
            # Build the YouTube service client
            youtube = build("youtube", "v3", developerKey=self.youtube_api_key)
            
            # Execute the search request
            request = youtube.search().list(
                q=query, 
                part="id,snippet", 
                type="video", 
                maxResults=max_results
            )
            return request.execute()
        except Exception as e:
            print(f"YouTube API request failed: {e}")
            return None

