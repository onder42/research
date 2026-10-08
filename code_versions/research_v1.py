import json
import os
import wikipediaapi

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
    
    # Check if the directory exists; if not, make it automatically
    # exist_ok=True prevents Python from throwing an error if 'data' already exists
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save the structured dictionary as a clean JSON file
    with open("data/response.json", "w", encoding="utf-8") as file:
        json.dump(page_data, file, ensure_ascii=False, indent=4)
        
    print("\nSuccessfully saved page data to response.json")

