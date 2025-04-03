#openAI
import streamlit as st
import pandas as pd
import random
import openai
import os

# Set OpenAI API Key 
openai.api_key = "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"

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

discount_percentage = discount_percentage[0] if len(discount_percentage) > 0 and pd.notna(discount_percentage[0]) else None

# Function to Generate Promotional Messages
def generate_promotion_messages(product_name, target_audience, offer_type, discount_percentage):
    prompt = f"""
    Generate 5 unique single line, catchy, and engaging promotional messages for a marketing campaign.

    - **Target Audience:** {target_audience}
    - **Offer Type:** {offer_type}
    - **Discount Percentage:** {discount_percentage if discount_percentage else 'N/A'}
    
    **Rules:** 
    1️⃣ **Mention Discount (1 message, only if applicable eg. ⏳ Still deciding? Here’s an exclusive offer just for you—Get your Smartwatch today at a special price! 🎉)**  
    2️⃣ **Without Mentioning Discount (2 messages eg 1. Your Smartwatch is waiting! Secure it before it’s too late. ⏳"
eg. 2. Hey, we saved your cart! Don’t miss out on your perfect tech companion. 🚀)**  
    3️⃣ **Common Catchy Sentences (2 messages) (eg.Common Catchy Sentences:
"Something amazing is waiting inside—Come take a look! 👀✨"
"Surprise! There's something special waiting for you. Click now to discover! 🎁"
 )** 
    **Requirements:**  
    - Keep it **one sentence** only.  
    - Make it **short, engaging, and persuasive**.  
    - Use action-driven words (e.g., "Shop now!", "Grab yours today!").  
    - Create urgency if relevant (e.g., "Limited Time!", "Hurry!").  
   
    - Keep it fresh and engaging  

    Generate 5 messages as a bullet point list.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["choices"][0]["message"]["content"].strip()

# Generate & Display Promotions
if st.button("✨ Generate Promotional Messages"):
    st.subheader("🔥 AI-Generated Promotional Messages")
    promo_messages = generate_promotion_messages(product_name, target_audience, offer_type, discount_percentage)
    st.write(promo_messages)
