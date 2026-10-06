import json
import os
import wikipediaapi

# Initialize the Wikipedia API client with a required, custom User-Agent
wiki = wikipediaapi.Wikipedia(
    user_agent="ChrisResearchAssistant/1.0 (chris@example.com)",
    language="en"
)

# To limit sentences, we pull the full introduction text and slice it locally
page_summary = wiki.page("Python (programming language)")
if page_summary.exists():
    # .summary returns the introduction section of the page
    sentences = page_summary.summary.split('.')
    summary_two_sentences = ".".join(sentences[:2]) + "."
    print("\nSummary:\n", summary_two_sentences)

# 3. Fetch the full page object
page_full = wiki.page("Python (programming language)")
if page_full.exists():
    print("\nPage Title:", page_full.title)
    print("Page URL:", page_full.fullurl)
    
    # Structure the extracted data into a standard Python dictionary
    page_data = {
        "title": page_full.title,
        "url": page_full.fullurl,
        "summary": page_full.summary,
        "text": page_full.text
    }
    
    # Check if the directory exists; if not, make it automatically
    # exist_ok=True prevents Python from throwing an error if 'data' already exists
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)
    
    # Task 1: Save the parsed clean text payload to the data directory
    print(f"\nSaving clean text payload to {output_dir}/response.txt...")
    with open(os.path.join(output_dir, "response.txt"), "w", encoding="utf-8") as text_file:
        text_file.write(page_full.text)
    
    # Save the structured dictionary as a clean JSON file
    with open("data/response.json", "w", encoding="utf-8") as file:
        json.dump(page_data, file, ensure_ascii=False, indent=4)
        
    print("\nSuccessfully saved page data to response.json")
