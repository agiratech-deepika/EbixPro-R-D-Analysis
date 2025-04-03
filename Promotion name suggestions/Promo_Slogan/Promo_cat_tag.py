# ------------------------------------- Promo without taggline

# import os
# import json
# from groq import Groq
# import random

# # Initialize Groq Client
# api_key = os.getenv("GROQ_API_KEY", "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")  # Replace with actual API key
# client = Groq(api_key=api_key)

# # Define categories and required slogans count
# CATEGORY_TEMPLATE = {
#     "General Taglines": {
#         "description": "Catchy eCommerce slogans focused on shopping, savings, and convenience.",
#         "count": 3
#     },
#     "Urgency-Based Promotions": {
#         "description": "Limited-time offers, act fast messages.",
#         "count": 4
#     },
#     "Emotion-Driven Promotions": {
#         "description": "Excitement, aspiration, empowerment in shopping.",
#         "count": 3
#     },
#     "Seasonal Promotions": {
#         "description": "Holiday, event-based deals.",
#         "count": 3
#     },
#     "Trendy/Meme-Based": {
#         "description": "Uses internet slang, viral trends.",
#         "count": 2
#     }
# }

# # Function to Generate the Prompt
# def generate_prompt(selected_categories):
#     selected_prompts = [
#         f"- **{category}** ({CATEGORY_TEMPLATE[category]['count']} slogans) → {CATEGORY_TEMPLATE[category]['description']}"
#         for category in selected_categories if category in CATEGORY_TEMPLATE
#     ]
    
#     if not selected_prompts:
#         return None  # Return None if no valid categories are selected
    
#     prompt = f"""
#         🎯 **Task:**  
#         Generate promotional sales slogans, each **exactly 8 words long**, based on the selected categories.  

#         🔹 **Categories & Slogan Count:**  
#         {'\n'.join(selected_prompts)}

#         🔥 **Rules:**  
#         ✔ Each slogan must be **exactly 8 words** (No more, no less)  
#         ✔ Must focus on **eCommerce, online shopping, discounts, deals**  
#         ✔ No repetitive words across slogans  
#         ✔ Must be fresh & unique every time  
#         ✔ Avoid brand names, company names, or specific products  

#         📌 **Return JSON format only:**  
#         {{
#             "slogans": {{
#                 {', '.join([f'"{category}": []' for category in selected_categories])}
#             }}
#         }}

#         ⚠ **Important:** Every slogan **must** be exactly **8 words** long!
#     """
#     return prompt.strip()

# # Function to Generate Slogans Based on Selected Categories
# def generate_slogans_by_categories(selected_categories):
#     prompt = generate_prompt(selected_categories)
    
#     if not prompt:
#         return {"error": "No valid categories selected. Please choose from the available options."}

#     try:
#         response = client.chat.completions.create(
#             model="mixtral-8x7b-32768",
#             # model="deepseek-r1-distill-qwen-32b",
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.6,
#             max_tokens=4096,
#             top_p=0.95,
#             response_format={"type": "json_object"},
#             stop=None
#         )

#         json_response = response.choices[0].message.content.strip()
#         return json.loads(json_response)

#     except Exception as e:
#         return {"error": f"❌ Error: {str(e)}"}

# # Example Usage
# # selected_categories = ["General Taglines", "Urgency-Based Promotions"]
# selected_categories = ["General Taglines", "Urgency-Based Promotions", "Emotion-Driven Promotions","Seasonal Promotions","Trendy/Meme-Based"]
# slogans = generate_slogans_by_categories(selected_categories)
# print(json.dumps(slogans, indent=2))

# --------------------------------------------------- promo with tagline

import os
import json
from groq import Groq
import random

# Initialize Groq Client
api_key = os.getenv("GROQ_API_KEY", "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")  # Replace with actual API key
client = Groq(api_key=api_key)

# Define categories and required slogans count
CATEGORY_TEMPLATE = {
    "General Taglines": {
        "description": "Catchy eCommerce slogans focused on shopping, savings, and convenience.",
        "count": 3
    },
    "Urgency-Based Promotions": {
        "description": "Limited-time offers, act fast messages.",
        "count": 4
    },
    "Emotion-Driven Promotions": {
        "description": "Excitement, aspiration, empowerment in shopping.",
        "count": 3
    },
    "Seasonal Promotions": {
        "description": "Holiday, event-based deals.",
        "count": 3
    },
    "Trendy/Meme-Based": {
        "description": "Uses internet slang, viral trends.",
        "count": 2
    }
}

# Function to Generate the Prompt
def generate_prompt(selected_categories):
    selected_prompts = [
        f"- **{category}** ({CATEGORY_TEMPLATE[category]['count']} slogans) → {CATEGORY_TEMPLATE[category]['description']}"
        for category in selected_categories if category in CATEGORY_TEMPLATE
    ]
    
    if not selected_prompts:
        return None  # Return None if no valid categories are selected
    
    prompt = f"""
        🎯 **Task:**  
        Generate promotional sales slogans, each **exactly 8 words long**, followed by a supporting tagline.  

        🔹 **Categories & Slogan Count:**  
        {'\n'.join(selected_prompts)}

        🔥 **Rules:**  
        ✔ Each slogan must be **exactly 8 words**  
        ✔ Must focus on **eCommerce, online shopping, discounts, deals**  
        ✔ Must be catchy, engaging, and marketing-friendly  
        ✔ After each slogan, add a **supporting tagline (10-15 words)**  
        ✔ No repetitive words across slogans  
        ✔ Avoid brand names, company names, or specific products  

        📌 **Return JSON format only:**  
        {{
            "slogans": {{
                {', '.join([f'"{category}": []' for category in selected_categories])}
            }}
        }}

        ⚠ **Important:** Every slogan **must** be exactly **8 words** long, followed by a supporting tagline.
    """
    return prompt.strip()

# Function to Generate Slogans Based on Selected Categories
def generate_slogans_by_categories(selected_categories):
    prompt = generate_prompt(selected_categories)
    
    if not prompt:
        return {"error": "No valid categories selected. Please choose from the available options."}

    try:
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": prompt}],
            temperature=random.uniform(0.7, 1.0),
            max_tokens=1024,
            top_p=1,
            response_format={"type": "json_object"},
            stop=None
        )

        json_response = response.choices[0].message.content.strip()
        return json.loads(json_response)

    except Exception as e:
        return {"error": f"❌ Error: {str(e)}"}

# Example Usage
# selected_categories = ["General Taglines", "Urgency-Based Promotions"]
selected_categories = ["General Taglines", "Urgency-Based Promotions", "Emotion-Driven Promotions","Seasonal Promotions","Trendy/Meme-Based"]
slogans = generate_slogans_by_categories(selected_categories)
print(json.dumps(slogans, indent=2))

