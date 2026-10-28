from src.infrastructure import FileHandler
from src.services import ResearchService

if __name__ == "__main__":
    print("=== PRESENTATION LAYER: Runtime Initialized ===")
    
    # 1. Instantiate persistence dependency
    file_handler = FileHandler()
    
    # 2. Inject FileHandler directly into the service orchestrator
    search_service = ResearchService(file_handler=file_handler)
    
    # 3. Target profile entity contract
    target_topic = "SQL"
    
    print(f"\n[Caller] Executing independent data routines for: '{target_topic}'...")
    
    # 4. Run commands completely separate from one another
    search_service.search_wikipedia(topic=target_topic)
    search_service.search_web(topic=target_topic)
    search_service.search_youtube(topic=target_topic, max_results=5)
    
    print("\nPipeline completed. Check your 'data/' workspace folder directory for output structures.")
