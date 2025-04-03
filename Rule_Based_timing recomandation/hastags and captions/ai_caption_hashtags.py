#OpenAI
import openai
from config import OPENAI_API_KEY

# Set the OpenAI API key
openai.api_key = OPENAI_API_KEY

class AICaptionHashtagsGenerator:
    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model

    def generate_caption_and_hashtags(self, product_category, product_description):
        """
        Generate an AI caption and relevant hashtags for a given product description and category.
        """
        prompt = f"Create a catchy and engaging caption for a product in the {product_category} category. Also, suggest 10 hashtags for the product. The product description is: {product_description}"
        
        # Make a request to the OpenAI API using the ChatCompletion method
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an AI assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            # Print the entire response for debugging purposes
            print("Response from OpenAI API:", response)

            # Extract the caption and hashtags from the response
            result = response['choices'][0]['message']['content'].strip().split("\n")
            caption = result[0]
            hashtags = [hashtag.strip() for hashtag in result[1:]]
            
            return caption, hashtags

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
