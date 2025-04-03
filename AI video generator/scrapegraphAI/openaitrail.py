# # from scrapegraphai.graphs import SmartScraperGraph
# # from dotenv import load_dotenv
# # import pandas as pd
# # import os

# # load_dotenv()

# # openai_key = os.getenv("OPENAI_APIKEY")

# # graph_config = {
# #     "llm": {
# #         "api_key": openai_key,
# #         "model": "gpt-3.5-turbo",
# #     }
# # }

# # smart_scraper_graph = SmartScraperGraph(
# #     prompt="List me all the articles",
# #     # also accepts a string with the already downloaded HTML code
# #     source="https://www.wired.com/",
# #     config=graph_config
# # )

# # result = smart_scraper_graph.run()

# # df = pd.DataFrame(result['articles'])
# # df.to_excel("wired.xlsx",index=False)

# from scrapegraphai.graphs import SmartScraperGraph
# from langchain.prompts import PromptTemplate
# OPENAI_API_KEY = "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"



# graph_config = {
#     "llm": {
#         "api_key": OPENAI_API_KEY,
#         "model": "gpt-3.5-turbo",
#     },
# }
# prompt_template = PromptTemplate(
#     input_variables=["content", "question"],
#     template="{content}\n{question}"
# )

# content = "This is the content to scrape from the website."
# question = "List all articles"

# smart_scraper_graph = SmartScraperGraph(
#     prompt=prompt_template.format(content=content, question=question),
#     source="https://www.wired.com/",  # Also accepts downloaded HTML code strings
#     config=graph_config
# )

# result = smart_scraper_graph.run()
# print(result)


# # from scrapegraphai.graphs import SmartScraperGraph

# # OPENAI_API_KEY = "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"

# # graph_config = {
# #     "llm": {
# #         "api_key": OPENAI_API_KEY,
# #         "model": "gpt-3.5-turbo",
# #     },
# #     "inputs": {
# #         "content": "Please extract relevant articles from the provided URL.",
# #         "question": "List all articles from the source."
# #     }
# # }

# # smart_scraper_graph = SmartScraperGraph(
# #     prompt="Content: {content}\nQuestion: {question}",  # Updated prompt template
# #     source="https://www.wired.com/",  # Also accepts downloaded HTML code strings
# #     config=graph_config
# # )

# # result = smart_scraper_graph.run()
# # print(result)



# -----------------------------------------------------------------------------------------------------------

from scrapegraphai.graphs import SmartScraperGraph
OPENAI_API_KEY = "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"

graph_config = {
    "llm": {
        "api_key": OPENAI_API_KEY,
        "model": "gpt-3.5-turbo",
    },
}

smart_scraper_graph = SmartScraperGraph(
    prompt="List me all the articles",
    # also accepts a string with the already downloaded HTML code
    source="https://perinim.github.io/projects",
    config=graph_config
)

result = smart_scraper_graph.run()
print(result)