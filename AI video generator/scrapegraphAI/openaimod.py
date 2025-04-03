import os
from dotenv import load_dotenv
from scrapegraphai.graphs import SmartScraperGraph
from scrapegraphai.utils import prettify_exec_info

load_dotenv()

openai_key = os.getenv("OPENAI_APIKEY")
print(openai_key)

# graph_config = {
#    "llm": {
#       "model": "openai/gpt-4o",
#       "api_key": openai_key,
#    },
# }

# # ************************************************
# # Create the SmartScraperGraph instance and run it
# # ************************************************
# amazon_url="https://www.amazon.in/SAF-flower-wall-painting-Decoration/dp/B0CYCHLB2L/?th=1"

# prompt = '''
# {
#     "content": "{{contents}}",
#     "question": "Extract product name, description, and images from the page"
# }
# '''

# smart_scraper_graph = SmartScraperGraph(
#    prompt=prompt,
#    # also accepts a string with the already downloaded HTML code
#    source=amazon_url,
#    config=graph_config
# )

# result = smart_scraper_graph.run()
# print(result)


# Configuration for the scraping pipeline
graph_config = {
    "llm": {
        "api_key": openai_key,
        "model": "openai/gpt-4o",
    },
}

# Amazon product page URL
# amazon_url = "https://www.amazon.in/SAF-flower-wall-painting-Decoration/dp/B0CYCHLB2L/?th=1"  # Replace with the actual product URL

# Create the SmartScraperGraph instance
smart_scraper_graph = SmartScraperGraph(
    # prompt='{"content": "{content}", "question": "Extract the product name, description, and image URLs from the Amazon product page."}',
    prompt="List me all the projects with their description.",
    # source="https://www.amazon.in/SAF-flower-wall-painting-Decoration/dp/B0CYCHLB2L/?th=1",
    source="https://perinim.github.io/projects/",
    config=graph_config
)

# Run the scraper and get the result
result = smart_scraper_graph.run()

# Print the extracted data
print(result)