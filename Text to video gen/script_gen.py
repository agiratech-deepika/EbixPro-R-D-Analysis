import openai
import streamlit as st

#openai

# OpenAI API Key (Replace with your own)
openai.api_key = "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"

# def generate_video_script(product_name, product_description, duration, category, tone, discount):
#     prompt = f"""
#     You are going to create a promotional video script for the following product:
    
#     Product Name: {product_name}
#     Product Description: {product_description}
    
#     The script should be generated under the category: {category}
#     Tone of the script: {tone}
    
#     If there is a discount available, incorporate it naturally into the script.
    
#     Generate the script according to the selected video duration:
#     - 15 sec: Concise, engaging, and attention-grabbing
#     - 30-50 sec: More detailed, storytelling format with product benefits
    
#     Discount: {discount if discount else 'No discount available'}
#     """
    
#     response = openai.ChatCompletion.create(
#         model="gpt-4",
#         messages=[{"role": "system", "content": "You are a professional scriptwriter."},
#                   {"role": "user", "content": prompt}]
#     )
    
#     return response["choices"][0]["message"]["content"]

# # Streamlit UI
# st.title("Video Script Generator")

# product_name = st.text_input("Enter Product Name")
# product_description = st.text_area("Enter Product Description")
# duration = st.selectbox("Select Video Duration", ["15 sec", "30 sec", "40 sec", "50 sec"])
# category = st.selectbox("Select Script Category", ["Brand Story", "Trending Topics", "Call To Action", "Product Lifestyle", "Special Offers", "Product Highlights", "Problem Solution", "Benefits"])
# tone = st.selectbox("Select Tone", ["Engaging", "Motivational", "Just Summary", "Storytelling"])
# discount = st.text_input("Enter Discount Details (if any)")

# if st.button("Generate Script"):
#     if product_name and product_description:
#         script = generate_video_script(product_name, product_description, duration, category, tone, discount)
#         st.subheader("Generated Script")
#         st.write(script)
#     else:
#         st.warning("Please enter product details to generate a script.")

import openai
import streamlit as st

# Function to generate video script
def generate_video_script(product_name, product_description, duration, category, tone, discount):
    # Enhanced prompt for better script quality
    prompt = f"""
    You are an expert scriptwriter creating a high-converting promotional video script.

    Product Name: {product_name}
    Product Description: {product_description}
    
    **Video Details:**
    - Duration: {duration}
    - Category: {category}
    - Tone: {tone}
    
    **Requirements:**
    - For a 15-sec script: Make it concise, engaging, and attention-grabbing.
    - For a 30-50 sec script: Use a storytelling format highlighting product benefits.
    - Naturally incorporate the discount if available.

    Discount: {discount if discount else 'No discount available'}
    
    **Structure:** 
    - Start with a compelling hook
    - Introduce the product in a captivating way
    - Highlight its key benefits
    - End with a strong call-to-action (CTA)
    
    Generate a professional, engaging script accordingly.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a professional advertising scriptwriter."},
            {"role": "user", "content": prompt}
        ]
    )

    return response["choices"][0]["message"]["content"]

# Streamlit UI
st.set_page_config(page_title="Video Script Generator", layout="centered")
st.title("🎬 AI Video Script Generator")

# Input fields
product_name = st.text_input("📌 Enter Product Name", placeholder="e.g., Painting Mantra's White Flower Set")
product_description = st.text_area("📝 Enter Product Description", placeholder="Describe the product briefly...")
duration = st.selectbox("⏳ Select Video Duration", ["15 sec", "30 sec", "40 sec", "50 sec"])
category = st.selectbox("🎭 Select Script Category", [
    "Brand Story", "Trending Topics", "Call To Action", 
    "Product Lifestyle", "Special Offers", "Product Highlights", 
    "Problem Solution", "Benefits"
])
tone = st.selectbox("🎤 Select Tone", ["Engaging", "Motivational", "Just Summary", "Storytelling"])
discount = st.text_input("💰 Enter Discount Details (if any)", placeholder="e.g., 15% OFF for a limited time!")

# Generate script
if st.button("🚀 Generate Script"):
    if product_name and product_description:
        script = generate_video_script(product_name, product_description, duration, category, tone, discount)
        st.subheader("📜 Generated Script")
        st.markdown(f"```{script}```")
    else:
        st.warning("⚠️ Please enter product details to generate a script.")
