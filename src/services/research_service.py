from pathlib import Path
from src.core import ResearchEngine 


class ResearchService:
    """
    Service layer coordinating different search actions, orchestrating
    the ResearchEngine, and mapping execution data to clean file exports.
    """
    def __init__(self, file_handler):
        self.engine = ResearchEngine()
        self.file_handler = file_handler

    def create_save_path(self, topic: str, search_type: str) -> Path:
        """
        Dynamically generates a Path object based on the topic and search engine.
        Formats as: data/formatted_topic/formatted_topic_search_type.json
        """
        # Format names safely (replace spaces with underscores for file systems)
        formatted_topic = topic.replace(" ", "_")
        formatted_search_type = search_type.replace(" ", "_")
        
        # Generates structure matching data/topic/topic_search_type.json
        return Path("data") / formatted_topic / f"{formatted_topic}_{formatted_search_type}.json"

    def search_wikipedia(self, topic: str):
        """Orchestrates a Wikipedia extraction and caches the payload."""
        output_path = self.create_save_path(topic, "wikipedia")
        page_data = self.engine.fetch_wikipedia_data(topic)
        
        self.file_handler.save_json(page_data, output_path)
        return page_data

    def search_web(self, topic: str = None):
        """Orchestrates a SerpAPI DuckDuckGo extraction and caches the payload."""
        output_path = self.create_save_path(topic, "web_search")
        search_data = self.engine.fetch_web_search(topic)
        self.file_handler.save_json(search_data, output_path)
        return search_data

    def search_youtube(self, topic: str = None, max_results: int = 10):
        """Orchestrates a YouTube Data API extraction and caches the payload."""
        output_path = self.create_save_path(topic, "youtube")
        youtube_data = self.engine.fetch_youtube_search(topic, max_results=max_results)
        self.file_handler.save_json(youtube_data, output_path)
        return youtube_data
    