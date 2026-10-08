import os
import json
import requests
import wikipediaapi
from dotenv import load_dotenv

# Load sensitive environment variables from our hidden .env file
load_dotenv()
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

# ==========================================
# 1. Network & Data Fetching Layer
# ==========================================

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

    # Parse out a short 2-sentence summary snippet
    sentences = page.summary.split('.')
    summary_two_sentences = ".".join(sentences[:2]) + "."

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


# ==========================================
# 2. Local Data Persistence Layer
# ==========================================

def save_wikipedia_data(data, directory="data"):
    """
    Persistence Function: Formats and saves Wikipedia payload dictionary 
    to text and JSON formats locally.
    """
    if not data:
        return
        
    os.makedirs(directory, exist_ok=True)
    
    # Save Wikipedia raw text payload
    with open(os.path.join(directory, "response.txt"), "w", encoding="utf-8") as f:
        f.write(data["text"])
        
    # Save Wikipedia structured JSON
    with open(os.path.join(directory, "response.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    print(f"Saved Wikipedia data to local '{directory}/' folder.")


def save_search_results(data, directory="data"):
    """
    Persistence Function: Saves the SerpAPI JSON payload locally.
    """
    if not data:
        return
        
    os.makedirs(directory, exist_ok=True)
    
    # Save Web Search structured JSON
    with open(os.path.join(directory, "search_results.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    print(f"Saved Web Search results to '{directory}/search_results.json'")


# ==========================================
# Execution Entry Point
# ==========================================
if __name__ == "__main__":
    # 1. Fetch data from web sources
    wiki_payload = fetch_wikipedia_data("Python (programming language)")
    search_payload = fetch_web_search("what is python")

    # 2. Call our persistence functions explicitly to handle storage
    save_wikipedia_data(wiki_payload)
    save_search_results(search_payload)

