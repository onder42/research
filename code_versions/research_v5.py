import os
import json
import requests
import wikipediaapi
from dotenv import load_dotenv

# Load sensitive environment variables from our hidden .env file
load_dotenv()
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")


# 1. Infrastructure Layer (File Storage)
class FileHandler:
    """
    Blueprint responsible strictly for low-level file system 
    interactions like writing and serializing data.
    """
    def save_json(self, data, file_path):
        """Serializes and writes a Python dictionary to a JSON file."""
        if not data:
            print(f"[FileHandler Warning] No data provided to save for {file_path}")
            return

        # Automatically extract and create the base folder structure if missing
        dir_name = os.path.dirname(file_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


# 2. Service Layer (Data Orchestration)
class ResearchEngine:
    """
    Blueprint responsible for orchestrating web data collection
    and using a FileHandler to cache the results.
    """
    def __init__(self):
        # Composition: We inject and instantiate the FileHandler inside our engine
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
        Queries SerpAPI using the DuckDuckGo engine and prints the JSON response.
        """
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


# Execution Entry Point
if __name__ == "__main__":
    # 1. Initialize our service engine
    engine = ResearchEngine()
    
    # 2. Define explicit, clean data persistence paths
    wiki_file_path = "data/wiki_response.json"
    search_file_path = "data/search_response.json"
    
    
    # 3. Fetch data across network protocols using the engine
    page_data = engine.fetch_wikipedia_data("Python (programming language)")
    search_data = engine.fetch_web_search("what is python")
    
    # 4. Route the payloads explicitly to the internal file handler tool
    engine.file_handler.save_json(page_data, wiki_file_path)
    engine.file_handler.save_json(search_data, search_file_path)
    
    print("\n=== Pipeline Execution Completed Successfully ===")
