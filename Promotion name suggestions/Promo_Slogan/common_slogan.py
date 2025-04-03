# common tagline 

import streamlit as st
import os
import json
from groq import Groq
import random

# Initialize Groq Client
api_key = os.getenv("GROQ_API_KEY", "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")  # Replace with actual API key
client = Groq(api_key=api_key)

# Function to Generate Fresh Promotional Slogans (8 Words Each)
def generate_promotional_slogans():
    prompt = f"""
        🎯 **Task:**  
        Generate **10 unique promotional sales slogans**, each exactly **8 words long**.  

        🔹 **Rules:**  
        ✔ Must focus on **sales, discounts, or limited-time offers**  
        ✔ Must sound **exciting, urgent, and engaging**  
        ✔ No repetitive words across slogans  
        ✔ Avoid brand names, company names, or specific products  
        ✔ Must be fresh & unique every time  
        ✔ Each slogan must be exactly 8 words  

        ✨ **Examples:**  
        - "Hurry! Limited-time discounts, grab your savings today!"  
        - "Flash sale now, shop before the deals expire!"  
        - "Exclusive deals waiting, save more while stocks last!"  
        
        🔄 **Generate different slogans every time.**  

        📌 **Return JSON format only:**  
        {{
            "slogans": [
                "Slogan 1",
                "Slogan 2",
                "Slogan 3",
                "Slogan 4",
                "Slogan 5",
                "Slogan 6",
                "Slogan 7",
                "Slogan 8",
                "Slogan 9",
                "Slogan 10"
            ]
        }}
    """

    try:
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": prompt}],
            temperature=random.uniform(0.7, 1.0),  # Randomized temperature for variety
            max_tokens=512,
            top_p=1,
            response_format={"type": "json_object"},
            stop=None
        )

        json_response = response.choices[0].message.content.strip()
        return json.loads(json_response)

    except Exception as e:
        return {"error": f"❌ Error: {str(e)}"}

# Streamlit UI
st.title("🚀 AI-Powered Sales Slogan Generator")
st.write("Click the button below to generate **new** promotional sale slogans every time!")

if st.button("✨ Generate Fresh Slogans"):
    st.subheader("🔥 AI-Generated Sales Slogans")
    slogans_data = generate_promotional_slogans()

    if "error" in slogans_data:
        st.error(slogans_data["error"])
    else:
        for i, slogan in enumerate(slogans_data["slogans"], start=1):
            st.write(f"**{i}.** {slogan}")
