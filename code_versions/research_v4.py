import os
import json
import requests
import wikipediaapi
from dotenv import load_dotenv

# Load sensitive environment variables from our hidden .env file
load_dotenv()
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")


# 1. Network & Data Fetching Layer
def fetch_wikipedia_data(topic):
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


def fetch_web_search(query):
    """
    Queries SerpAPI using the DuckDuckGo engine and prints the JSON response.
    """
    
    params = {
        "api_key": SERPAPI_API_KEY,
        "engine": "duckduckgo",
        "q": query
    }

    try:
        search = requests.get("https://serpapi.com/search", params=params)
        return search.json()
    except requests.exceptions.RequestException as e:
        print(f"Network request failed: {e}")
        return None


# 2. Local Data Persistence Layer
def save_json(data, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# Execution Entry Point

if __name__ == "__main__":
    directory="data"
    os.makedirs(directory, exist_ok=True)
    wiki_file_path = os.path.join(directory, "wiki_response.json")
    search_file_path = os.path.join(directory, "search_response.json")
    
    # 1. Fetch data from web sources
    page = fetch_wikipedia_data("Python (programming language)")
    search = fetch_web_search("what is python")
    save_json(page, wiki_file_path)
    save_json(search, search_file_path)

