import wikipediaapi
import os, json
from dotenv import load_dotenv
import requests

load_dotenv()

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

# Initialize the Wikipedia API client with a required, custom User-Agent
wiki = wikipediaapi.Wikipedia(
    user_agent="ChrisResearchAssistant/1.0 (chris@example.com)",
    language="en"
)

page = wiki.page("Python (programming language)")
if page.exists():
    print("\nPage Title:", page.title)
    print("Page URL:", page.fullurl)
    
    # Structure the extracted data into a standard Python dictionary
    page_data = {
        "title": page.title,
        "url": page.fullurl, 
        "summary": page.summary,
        "text": page.text
    }
    
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save the structured dictionary as a clean JSON file
    with open("data/response.json", "w", encoding="utf-8") as file:
        json.dump(page_data, file, ensure_ascii=False, indent=4)
        
    print("\nSuccessfully saved page data to response.json")

    
params = {
    "api_key": SERPAPI_API_KEY,
    "engine": "duckduckgo",
    "q": "what is python"
}

search = requests.get("https://serpapi.com/search", params=params)
response = search.json()
with open("data/web_response.json", "w", encoding="utf-8") as file:
    json.dump(response, file, ensure_ascii=False, indent=4)
    
print("\nSuccessfully saved page data to web_response.json")
print("#######################")
print(json.dumps(response, indent=4)) 

