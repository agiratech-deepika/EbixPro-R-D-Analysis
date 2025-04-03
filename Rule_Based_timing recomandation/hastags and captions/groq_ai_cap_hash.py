# Groq deepseek without product name
from groq import Groq
import json  # Import json module for parsing
from config import groq_api_key

client = Groq(api_key=groq_api_key)

class AICaptionHashtagsGenerator:
    def __init__(self, model="deepseek-r1-distill-llama-70b"):
        self.model = model

    def generate_caption_and_hashtags(self, product_category, product_description):
        """
        Generate an AI caption and relevant hashtags for a given product description and category.
        """
        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an AI assistant. Respond strictly in JSON format."},
                    {"role": "user", "content": f"Create a catchy and engaging caption for a product in the {product_category} category. Also, suggest 10 hashtags for the product. The product description is: {product_description}. Respond in valid JSON format with 'caption' and 'hashtags' keys."}
                ],
                temperature=0.6,
                max_tokens=4096,  
                top_p=0.95,
                stream=False,
                response_format={"type": "json_object"},
                stop=None,
            )

            # Print the entire response for debugging purposes
            print("Response from groq API:", response)
            
            # Extract and parse JSON response
            content = response.choices[0].message.content.strip()
            response_data = json.loads(content)  # Convert JSON string to Python dictionary
            
            # Extract caption and hashtags
            caption = response_data.get("caption", "No caption generated.")
            hashtags = response_data.get("hashtags", [])
            
            return caption, hashtags
        
        except json.JSONDecodeError:
            print("Error: Failed to parse JSON response.")
            return None, None
        except Exception as e:
            print(f"Error generating caption and hashtags: {e}")
            return None, None

# Running the class separately
if __name__ == "__main__":
    generator = AICaptionHashtagsGenerator()  # Create an instance of the class
    product_category = "Fashion"  # Example product category
    product_description = "This is a stylish and elegant dress for women, perfect for any occasion."
    
    caption, hashtags = generator.generate_caption_and_hashtags(product_category, product_description)
    
    if caption and hashtags:
        print("Generated Caption:", caption)
        print("Suggested Hashtags:", ", ".join(hashtags))
    else:
        print("No caption or hashtags were generated.")
