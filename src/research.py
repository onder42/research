import wikipediaapi
import os, json
from dotenv import load_dotenv
import requests


def fetch_wikipedia_data(topic):
    """
    Fetches an introduction summary and full text payload from Wikipedia,
    and immediately prints and saves the response.
    """

    wiki = wikipediaapi.Wikipedia(
        user_agent="ChrisResearchAssistant/1.0 (chris@example.com)",
        language="en"
    )

    # To limit sentences, we pull the full introduction text and slice it locally
    page = wiki.page(topic)
    if page.exists():
        # .summary returns the introduction section of the page
        sentences = page.summary.split('.')
        summary_two_sentences = ".".join(sentences[:2]) + "."
        print("\nSummary:\n", summary_two_sentences)
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
        
        # Task 1: Save the parsed clean text payload to the data directory
        print(f"\nSaving clean text payload to {output_dir}/response.txt...")
        with open(os.path.join(output_dir, "response.txt"), "w", encoding="utf-8") as text_file:
            text_file.write(page.text)
        
        # Save the structured dictionary as a clean JSON file
        with open("data/response.json", "w", encoding="utf-8") as file:
            json.dump(page_data, file, ensure_ascii=False, indent=4)
            
        print("\nSuccessfully saved page data to response.json")
        
def fetch_web_search(query):
    """
    Queries SerpAPI using the DuckDuckGo engine and prints the JSON response.
    """
       
    load_dotenv()
    SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

    params = {
        "api_key": SERPAPI_API_KEY,
        "engine": "duckduckgo",
        "q": query
    }

    search = requests.get("https://serpapi.com/search", params=params)
    response = search.json()
    #print(json.dumps(response, indent=4)) 
    # Save the structured dictionary as a clean JSON file
    with open("data/web_response.json", "w", encoding="utf-8") as file:
        json.dump(response, file, ensure_ascii=False, indent=4)
    
    
if __name__ == "__main__":
      fetch_wikipedia_data("Python (programming language)")
      fetch_web_search("what is python")
      
