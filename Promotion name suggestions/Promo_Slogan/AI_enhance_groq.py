import streamlit as st
import pandas as pd
import os
import json
from groq import Groq

# Initialize Groq Client
api_key = os.getenv("GROQ_API_KEY", "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")  # Replace with actual API key
client = Groq(api_key=api_key)

# Load CSV Data
@st.cache_data
def load_data():
    return pd.read_csv("C:\\Projects\\Promotion name suggestions\\promotion.csv")

df = load_data()

# Streamlit UI
st.title("🚀 AI-Powered Promotion Name Generator")
st.write("Select your product, target audience, and offer type to generate compelling promotional messages!")

# Dropdown Selections
product_name = st.selectbox("🛍️ Choose a Product", df["Product Name"].unique())
target_audience = st.selectbox("🎯 Choose a Target Audience", df["Target Audience"].unique())
offer_type = st.selectbox("🎁 Choose an Offer Type", df["Offer Type"].unique())

# Fetch Discount Percentage
discount_percentage = df[
    (df["Product Name"] == product_name) & (df["Target Audience"] == target_audience)
]["Discount Percentage"].values

discount_percentage = discount_percentage[0] if len(discount_percentage) > 0 and pd.notna(discount_percentage[0]) else "N/A"

# Function to Generate Promotional Messages
def generate_promotion_messages(product_name, target_audience, offer_type, discount_percentage):
    prompt = f"""
        🎯 **Task:**  
        Generate **10 promotional slogans** in **strictly defined categories** using the **given structure**.  

        🔹 **Message Categories:**  
        - **(3) Common Taglines** : Must be general marketing phrases with NO mention of any product, offer, or discount. 
        - **(2) Urgency-Based Promotions**: Focus on time-limited deals.  
        - **(2) Emotion-Driven Promotions**: Appeal to emotions like joy, excitement, or self-worth.  
        - **(2) Seasonal Promotions**: Tie promotions to events like New Year, Black Friday, etc.  
        - **(1) Trendy/Meme-Based**: Use a modern phrase or internet slang (e.g., "FOMO").  

        🔹 **Product Context (Use only in relevant message categories):**  
        - **Product Name:** {product_name}  
        - **Target Audience:** {target_audience}  
        - **Offer Type:** {offer_type}  
        - **Discount Percentage:** {discount_percentage}  

        🔹 **Rules:**  
        ✔ **Common Taglines:** Must be broad, engaging, and universal (**NO product, offer, or discount mention**).  
        ✔ **Urgency & Emotion-Based:** Can mention product/discount but with strong call-to-action.  
        ✔ **Seasonal:** Must connect the offer to an event/holiday.  
        ✔ **Trendy/Meme-Based:** Use social media language like "YOLO," "FOMO," or other viral phrases.  
        ✔ **Return JSON format only** – NO extra text, explanations, or greetings.  

        📌 **Expected JSON Output Format:**  
        {{
            "messages": {{
                "common_taglines": [
                    "Common tagline 1",
                    "Common tagline 2",
                    "Common tagline 3"
                ],
                "urgency_promotions": [
                    "Urgency-based promo 1",
                    "Urgency-based promo 2"
                ],
                "emotion_promotions": [
                    "Emotion-based promo 1",
                    "Emotion-based promo 2"
                ],
                "seasonal_promotions": [
                    "Seasonal promo 1",
                    "Seasonal promo 2"
                ],
                "trendy_promotions": [
                    "Trendy/meme-based promo"
                ]
            }}
        }}
    """
    try:
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            response_format={"type": "json_object"}, 
            stop=None
        )

        json_response = response.choices[0].message.content.strip()

        # Debugging: Print the raw response
        # print("AI Response:", json_response)

        return json.loads(json_response)

    except Exception as e:
        return {"error": f"❌ Error: {str(e)}"}

# Generate & Display Promotions
if st.button("✨ Generate Promotional Slogans"):
    st.subheader("🔥 AI-Generated Promotional Slogans")
    promo_slogans = generate_promotion_messages(product_name, target_audience, offer_type, discount_percentage)
    
    if "error" in promo_slogans:
        st.error(promo_slogans["error"])
    else:
        categories = {
            "⭐ Common Taglines": "common_taglines",
            "⏳ Urgency-Based Promotions": "urgency_promotions",
            "❤️ Emotion-Driven Promotions": "emotion_promotions",
            "🎄 Seasonal Promotions": "seasonal_promotions",
            "🔥 Trendy/Meme-Based Promotion": "trendy_promotions",
        }

        for category_name, key in categories.items():
            if key in promo_slogans["messages"]:
                st.write(f"### {category_name}")
                for i, slogan in enumerate(promo_slogans["messages"][key], start=1):
                    st.write(f"**{i}.** {slogan}")
