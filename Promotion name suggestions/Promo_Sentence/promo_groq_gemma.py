import streamlit as st
import pandas as pd
import os
from groq import Groq
import json

# Initialize Groq Client (Ensure API Key is stored securely)
api_key = os.getenv("GROQ_API_KEY", "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")  # Replace with your actual API key or set it in environment variables
client = Groq(api_key=api_key)

# Load CSV Data
@st.cache_data
def load_data():
    return pd.read_csv("C:\\Projects\\Promotion name suggestions\\promotion.csv")

df = load_data()

# Streamlit UI
st.title("🎯 AI-Powered Promotion Name Generator")
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

def generate_promotion_messages(product_name, target_audience, offer_type, discount_percentage):
    prompt = f"""
    Generate 5 short, catchy, and engaging promotional messages in a single sentence as **json format**.

    🔹 **Message Distribution:**  
    - **First 3 messages**: Must be general marketing phrases with NO mention of any product, offer, or discount. Example: "Hurry! Limited-time exclusive deals!"  
    - **Last 2 messages**: Must be specific to the given product and discount.  

    🔹 **Details:**  
    - **Product:** {product_name}  
    - **Target Audience:** {target_audience}  
    - **Offer Type:** {offer_type}  
    - **Discount Percentage:** {discount_percentage}  

    🔹 **Rules:**  
    ✔ First 3 messages **MUST NOT** mention product, discount, or offer.  
    ✔ Last 2 messages **MUST** mention product and discount.  
    ✔ Use power words like "Exclusive," "Limited Time," "Hurry," "Don't Miss Out!"  
    ✔ Avoid repetition; make each message unique.  
    ✔ Structure output as JSON.

    📌 **Expected JSON Output Format:**  
    ```json
    {{
        "messages": [
            "Common catchy phrase 1",
            "Common catchy phrase 2",
            "Common catchy phrase 3",
            "Discount-specific phrase 1",
            "Discount-specific phrase 2"
        ]
    }}
    ```
    **Return only a JSON object, nothing else.**
    """

    try:
        response = client.chat.completions.create(
            model="gemma2-9b-it",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=1024,
            top_p=0.5,
            response_format={"type": "json_object"},
            stop=None
        )
        json_response = response.choices[0].message.content.strip()
        return json.loads(json_response)

    except Exception as e:
        return {"error": str(e)}

# Generate & Display Promotions
if st.button("✨ Generate Promotional Messages"):
    st.subheader("🔥 AI-Generated Promotional Messages")
    promo_messages = generate_promotion_messages(product_name, target_audience, offer_type, discount_percentage)
    if "error" in promo_messages:
        st.error(promo_messages["error"])
    else:
        for i, message in enumerate(promo_messages["messages"], start=1):
            st.write(f"**{i}.** {message}")
    # st.write(promo_messages)
