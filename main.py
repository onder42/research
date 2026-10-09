# Import our specialized research engine from our system layers
from src.research import ResearchEngine

def main():
    print("==============================================")
    print("Launching Automated Clean Research Pipeline")
    print("==============================================\n")
    
    # 1. Instantiate our core service engine
    # The engine handles its own internal FileHandler setup automatically!
    engine = ResearchEngine()
    
    # 2. Define explicit, clean data persistence paths in our main workspace
    wiki_file_output = "data/wiki_response.json"
    search_file_output = "data/search_response.json"
    
    # 3. Execute our automated pipelines using simple, declarative commands
    print("[Pipeline Stage 1] Querying Wikipedia Index...")
    page_data = engine.fetch_wikipedia_data("Python (programming language)")
    
    print("[Pipeline Stage 2] Querying Web Search Index...")
    search_data = engine.fetch_web_search("what is python")
    
    # 4. Delegate explicit storage caching to the engine's internal tools
    print("\n[Pipeline Stage 3] Routing Payloads to Storage Cache...")
    engine.file_handler.save_json(page_data, wiki_file_output)
    engine.file_handler.save_json(search_data, search_file_output)
    
    print("\n==============================================")
    print("Pipeline Execution Completed Successfully!")
    print("==============================================")

if __name__ == "__main__":
    main()

