import json  # Import json module for parsing

from groq import Groq
from config import groq_api_key

# print("API",groq_api_key)
client = Groq(api_key=groq_api_key)

# class AICaptionHashtagsGenerator:
#     def __init__(self, model="deepseek-r1-distill-llama-70b"):
#         self.model = model

# def generate_caption_and_hashtags(product_category, product_description):
#     """
#     Generate an AI caption and relevant hashtags for a given product description and category.
#     """
#     try:
#         response = client.chat.completions.create(
#             # model=self.model,
#             model="deepseek-r1-distill-llama-70b",
#             messages=[
#                 {"role": "system", "content": "You are an AI assistant. Respond strictly in JSON format."},
#                 {"role": "user", "content": f"Create a catchy and engaging caption for a product in the {product_category} category. Also, suggest 10 hashtags for the product. The product description is: {product_description}. Respond in valid JSON format with 'caption' and 'hashtags' keys."}
#             ],
#             temperature=0.6,
#             max_tokens=4096,  
#             top_p=0.95,
#             stream=False,
#             response_format={"type": "json_object"},
#             stop=None,
#         )

#         # Print the entire response for debugging purposes
#         # print("Response from groq API:", response)
        
#         # Extract and parse JSON response
#         content = response.choices[0].message.content.strip()
#         response_data = json.loads(content)  # Convert JSON string to Python dictionary
        
#         # Extract caption and hashtags
#         caption = response_data.get("caption", "No caption generated.")
#         hashtags = response_data.get("hashtags", [])
        
#         return caption, hashtags
    
#     except json.JSONDecodeError:
#         print("Error: Failed to parse JSON response.")
#         return None, None
#     except Exception as e:
#         print(f"Error generating caption and hashtags: {e}")
#         return None, None

def generate_caption_and_hashtags(product_category, product_name, product_description):
        """
        Generate an AI caption and relevant hashtags for a given product category, name, and description.
        """
        try:
            response = client.chat.completions.create(
                model="deepseek-r1-distill-llama-70b",
                messages=[
                    {"role": "system", "content": "You are an AI assistant. Respond strictly in JSON format."},
                    {"role": "user", "content": f"Create a catchy and engaging caption for a product in the {product_category} category. The product name is '{product_name}'. The product description is: {product_description}. Also, suggest 10 hashtags for the product. Additionally, rate the accuracy of the generated caption and hashtags as a percentage from 0 to 100, where 100% is highly accurate. Respond in valid JSON format with 'caption' and 'hashtags' keys."}
                ],
                temperature=0.6,
                max_tokens=4096,
                top_p=0.95,
                stream=False,
                response_format={"type": "json_object"},
                stop=None,
            )

            content = response.choices[0].message.content.strip()
            response_data = json.loads(content)

            caption = response_data.get("caption", "No caption generated.")
            hashtags = response_data.get("hashtags", [])
            accuracy = response_data.get("accuracy", "No accuracy rating provided.")

            return caption, hashtags, accuracy
        
        except json.JSONDecodeError:
            print("Error: Failed to parse JSON response.")
            return None, None
        except Exception as e:
            print(f"Error generating caption and hashtags: {e}")
            return None, None