# groq gemma

from groq import Groq
import json  # Import json module for parsing
from config import groq_api_key

client = Groq(api_key=groq_api_key)

class AICaptionHashtagsGenerator:
    def __init__(self, model="gemma2-9b-it"):
        self.model = model

    def generate_caption_and_hashtags(self,product_category, product_name, product_description):
        """
        Generate an AI caption and relevant hashtags for a given product category, name, and description.
        """
        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an AI assistant. Respond strictly in JSON format."},
                    {"role": "user", "content": f"Create a catchy and engaging caption for a product in the {product_category} category. The product name is '{product_name}'. The product description is: {product_description}. Also, suggest 10 hashtags for the product. Respond in valid JSON format with 'caption' and 'hashtags' keys."}
                ],
                temperature=0.5,
                max_tokens=1024,
                top_p=1,
                stream=False,
                response_format={"type": "json_object"},
                stop=None,
            )

            content = response.choices[0].message.content.strip()
            response_data = json.loads(content)

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
    product_category = "Electronics"
    product_name = "Smartphone"
    product_description = "A high-performance smartphone with an advanced camera and long battery life."
    
    caption, hashtags = generator.generate_caption_and_hashtags(product_category,product_name, product_description)
    
    if caption and hashtags:
        print("Generated Caption:", caption)
        print("Suggested Hashtags:", ", ".join(hashtags))
    else:
        print("No caption or hashtags were generated.")


#output 1
# product_category = "Fashion"  # Example product category
# product_name="Leather Jacket"
# product_description = "A stylish leather jacket for a bold and edgy look."
# Generated Caption: Unleash your inner rebel with our iconic Leather Jacket. Crafted for a bold and edgy look, it's the perfect statement piece to elevate any outfit.
# Suggested Hashtags: #LeatherJacket, #EdgyFashion, #StatementPiece, #StyleIcon, #FashionForward, #LeatherLove, #Menswear, #Womenswear, #OutfitGoals, #ShopNow