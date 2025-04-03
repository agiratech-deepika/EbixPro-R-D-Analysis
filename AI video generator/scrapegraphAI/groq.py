# from scrapegraphai.graphs import SmartScraperGraph
# # from langchain.prompts import PromptTemplate
# # OPENAI_API_KEY = "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"

# GROQ_API_KEY="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"


# graph_config = {
#     "llm": {
#         "api_key": GROQ_API_KEY,
#         "model": "groq/llama3-70b-8192",
#         "temperature": 0,
#     },
# }

# smart_scraper_graph = SmartScraperGraph(
#     prompt="List all articles",
#     source="https://www.wired.com/",  # Also accepts downloaded HTML code strings
#     config=graph_config
# )

# result = smart_scraper_graph.run()
# print(result)

# Documentation
from scrapegraphai.graphs import SmartScraperGraph
from scrapegraphai.utils import prettify_exec_info

groq_key = "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"

graph_config = {
    "llm": {
        "model": "groq/gemma-7b-it",
        "api_key": groq_key,
        "temperature": 0
    },
    "embeddings": {
        "model": "ollama/nomic-embed-text",
        "temperature": 0,
        "base_url": "http://localhost:11434", 
    },
    "headless": False
}

smart_scraper_graph = SmartScraperGraph(
    prompt="List me all the projects with their description and the author.",
    source="https://perinim.github.io/projects",
    config=graph_config
)

result = smart_scraper_graph.run()
print(result)
