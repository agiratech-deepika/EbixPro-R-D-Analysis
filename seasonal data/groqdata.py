from groq import Groq

client = Groq(api_key="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")  

completion = client.chat.completions.create(
    model="deepseek-r1-distill-llama-70b",
    messages=[
        {"role": "system", "content": "You are an expert in Chinese seasonal trends and Weibo data analysis."},
        {"role": "user", "content": """
        Extract the top 5 trending seasonal topics from Weibo related to Chinese seasonal events, festivals, or weather patterns.
        Provide the response in structured JSON format with the following keys:

        - `trend_title_zh`: Trending topic in Chinese.
        - `trend_title_en`: English translation of the topic.
        - `description_zh`: Short summary in Chinese.
        - `description_en`: English translation of the summary.
        - `timestamp`: Approximate time when the trend started.
        - `popularity_score`: A numerical indicator of virality (from 1 to 100).
        - `source`: Category of the trend ("weather", "festival", "tradition", or "social trends").
        - `related_hashtags`: List of relevant hashtags in both Chinese and English.

        Example response:
        ```json
        [
            {
                "trend_title_zh": "春分节气来临",
                "trend_title_en": "Spring Equinox Arrives",
                "description_zh": "春分是二十四节气之一，标志着春天的正式到来。",
                "description_en": "The Spring Equinox is one of the 24 solar terms, marking the official arrival of spring.",
                "timestamp": "2025-02-03T08:00:00Z",
                "popularity_score": 92,
                "source": "festival",
                "related_hashtags": ["#春分", "#二十四节气", "#春天", "#SpringEquinox", "#SolarTerms"]
            }
        ]
        ```

        Provide the **top 5 trending** topics in this format.
        """}
    ],
    temperature=0.6,
    max_completion_tokens=4096,
    top_p=0.95,
    stream=False,
    response_format={"type": "json_object"},
    stop=None,
)

print(completion.choices[0].message)
