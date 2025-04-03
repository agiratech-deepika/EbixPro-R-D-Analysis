import openai
import streamlit as st
from gtts import gTTS
import os
import json
import re
openai.api_key = "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"

SCRIPT_FILE = "generated_script.json"
VOICE_FILE = "voiceover.mp3"

# Function to generate a video script
def generate_video_script(product_name, product_description, duration, category, tone, discount):
    prompt = f"""
    You are going to create a promotional video script for the following product:
    
    Product Name: {product_name}
    Product Description: {product_description}
    
    The script should be generated under the category: {category}
    Tone of the script: {tone}
    
    If there is a discount available, incorporate it naturally into the script.
    
    Generate the script according to the selected video duration:
    - 15 sec: Concise, engaging, and attention-grabbing
    - 30-50 sec: More detailed, storytelling format with product benefits
    
    Discount: {discount if discount else 'No discount available'}
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a professional scriptwriter."},
                  {"role": "user", "content": prompt}]
    )
    
    return response["choices"][0]["message"]["content"]

# Function to extract only the voiceover lines
def extract_voiceover(script_text):
    voiceover_lines = []
    
    # Find all voiceover lines using regex
    matches = re.findall(r'Voiceover:\s*\((.*?)\)\s*(.*)', script_text)
    
    for match in matches:
        _, line = match  # Extract only the spoken text
        voiceover_lines.append(line.strip())

    return " ".join(voiceover_lines)  # Return as a single string

# Function to save script to a file
def save_script(script_text, product_name):
    data = {"product_name": product_name, "script": script_text}
    with open(SCRIPT_FILE, "w") as file:
        json.dump(data, file)

# Function to load the stored script
def load_script():
    if os.path.exists(SCRIPT_FILE):
        with open(SCRIPT_FILE, "r") as file:
            return json.load(file)
    return None

# Function to generate voice-over using gTTS
def generate_voice(script_text, output_file=VOICE_FILE):
    tts = gTTS(script_text, lang="en-US", slow=False)
    tts.save(output_file)
    return output_file

def clean_text(text):
    # Remove unnecessary quotes and extra spaces
    text = text.replace('"', '').strip()
    return text

# Streamlit UI
st.title("AI Video Script & Voice Generator")

# Check if script already exists
saved_script = load_script()
if saved_script:
    st.subheader("Previously Generated Script")
    st.write(saved_script["script"])

product_name = st.text_input("Enter Product Name")
product_description = st.text_area("Enter Product Description")
duration = st.selectbox("Select Video Duration", ["15 sec", "30 sec", "40 sec", "50 sec"])
category = st.selectbox("Select Script Category", ["Brand Story", "Trending Topics", "Call To Action", "Product Lifestyle", "Special Offers", "Product Highlights", "Problem Solution", "Benefits"])
tone = st.selectbox("Select Tone", ["Engaging", "Motivational", "Just Summary", "Storytelling"])
discount = st.text_input("Enter Discount Details (if any)")

if st.button("Generate Script & Voice"):
    if product_name and product_description:
        # Check if script is already stored
        script_data = load_script()
        if script_data and script_data["product_name"] == product_name:
            script = script_data["script"]
        else:
            script = generate_video_script(product_name, product_description, duration, category, tone, discount)
            save_script(script, product_name)  # Store script

        # Extract only voiceover content
        voiceover_text = extract_voiceover(script)
        voiceover_text = clean_text(voiceover_text)

        # Display script
        st.subheader("Generated Script")
        st.write(script)
        
        # Display extracted voiceover lines
        st.subheader("Extracted Voiceover Text")
        st.write(voiceover_text)

        # Generate voice-over
        voice_file = generate_voice(voiceover_text)
        
        # Display audio player
        st.subheader("Generated Voice-over")
        st.audio(voice_file, format="audio/mp3")
        
    else:
        st.warning("Please enter product details to generate a script and voice-over.")


        
# Button to generate voice only from existing script
if saved_script and st.button("Generate Voice Only"):
    script = saved_script["script"]
    
    # Extract only voiceover content
    voiceover_text = extract_voiceover(script)
    voiceover_text = clean_text(voiceover_text)
    
    # Generate voice-over
    voice_file = generate_voice(voiceover_text)

    # Display extracted voiceover lines
    st.subheader("Extracted Voiceover Text")
    st.write(voiceover_text)

    # Display audio player
    st.subheader("Generated Voice-over")
    st.audio(voice_file, format="audio/mp3")