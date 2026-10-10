import json, os
from googleapiclient.discovery import build
from dotenv import load_dotenv
load_dotenv()

YOUTUBE_API = os.getenv("YOUTUBE_API_KEY")


def search_youtube(
    query, max_results=10
):
    output_file="youtube_results.json"
    """Searches YouTube Data API v3 and saves the results to a JSON file."""
    # Build the YouTube service client
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API)

    # Execute the search request
    request = youtube.search().list(
      q=query, part="id,snippet", type="video", maxResults=max_results
    )
    response = request.execute()

    # Save the raw response dictionary as a JSON file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(response, f, ensure_ascii=False, indent=4)

    print(f"Results saved successfully to {output_file}")
    return response


# Example Usage:
search_youtube(query="Python programming", max_results=5)
 
