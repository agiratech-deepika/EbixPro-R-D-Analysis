import openai
import json
import os
import re
import asyncio
import edge_tts
import datetime
import streamlit as st
import tempfile

# Replace with your OpenAI API Key
openai.api_key = "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"

SCRIPT_FILE = "generated_script.json"

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
        messages=[
            {"role": "system", "content": "You are a professional scriptwriter."},
            {"role": "user", "content": prompt}
        ]
    )

    return response["choices"][0]["message"]["content"]

# Function to extract only the voiceover lines
# def extract_voiceover(script_text):
#     voiceover_lines = []
    
#     # Find all voiceover lines using regex
#     matches = re.findall(r'(?:VO:|Voiceover:)\s*(?:\((.*?)\))?\s*(.*)', script_text, re.IGNORECASE)
    
#     for match in matches:
#         _, line = match  # Extract only the spoken text
#         voiceover_lines.append(line.strip())

    # return " ".join(voiceover_lines)  # Return as a single string

def extract_voiceover(script_text, duration):
    voiceover_lines = []
    
    # Identify the correct script based on duration
    if "15 sec" in duration:
        match = re.search(r"15-Second Script:\n\n(.*?)(?:\n---|$)", script_text, re.DOTALL)
    else:  # For 30-50 sec
        match = re.search(r"30-50 Second Script:\n\n(.*)", script_text, re.DOTALL)

    if match:
        selected_script = match.group(1)
        matches = re.findall(r'(?:VO:|Voiceover:)\s*(?:\((.*?)\))?\s*(.*)', selected_script, re.IGNORECASE)
        
        for _, line in matches:
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

# Function to generate a unique voiceover file using Edge TTS
async def generate_voice_edge(script_text, voice_name):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    voice_file = f"{timestamp}.mp3"  # Unique filename

    communicate = edge_tts.Communicate(script_text, voice_name)
    await communicate.save(voice_file)
    
    return voice_file

# Function to generate and play sample voice
async def play_sample_voice(voice_name):
    sample_text = "Here is a sample voice"
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        temp_filename = tmp_file.name

    communicate = edge_tts.Communicate(sample_text, voice_name)
    await communicate.save(temp_filename)
    
    st.audio(temp_filename, format="audio/mp3")

# Function to clean extracted text
def clean_text(text):
    return text.replace('"', '').strip()

# Streamlit UI
st.title("🎬 AI Video Script & Voice Generator")
st.write("Generate a promotional video script and voiceover using AI.")

# Input Fields
product_name = st.text_input("Enter Product Name")
product_description = st.text_area("Enter Product Description")
duration = st.selectbox("Select Video Duration", ["15 sec", "30 sec", "40 sec", "50 sec"])
category = st.selectbox("Select Script Category", ["Brand Story", "Trending Topics", "Call To Action", "Product Lifestyle", "Special Offers", "Product Highlights", "Problem Solution", "Benefits"])
tone = st.selectbox("Select Tone", ["Engaging", "Motivational", "Just Summary", "Storytelling"])
discount = st.text_input("Enter Discount Details (if any)")

# Voice Selection
voice_name = st.selectbox("Select Voice", [
    "en-US-JennyNeural", "en-US-GuyNeural", "en-GB-SoniaNeural", "en-GB-RyanNeural", 
    "en-IN-NeerjaNeural", "en-IN-PrabhatNeural"
])

# Play sample voice on selection
if voice_name:
    st.subheader("🔊 Sample Voice")
    if st.button("Play Sample Voice"):
        asyncio.run(play_sample_voice(voice_name))

# Load existing script
saved_script = load_script()
if saved_script:
    st.subheader("📜 Previously Generated Script Found")
    st.text_area("Loaded Script", saved_script["script"], height=200)

    if st.button("Use Saved Script for Voiceover"):
        script = saved_script["script"]
        # voiceover_text = extract_voiceover(script)
        voiceover_text = extract_voiceover(script, duration)
        voiceover_text = clean_text(voiceover_text)

        if voice_name:
            voice_file = asyncio.run(generate_voice_edge(voiceover_text, voice_name))
            st.success(f"✅ Voiceover generated successfully!")
            st.audio(voice_file, format="audio/mp3")
        else:
            st.warning("⚠️ Please select a voice!")

# Generate Script
if st.button("Generate Script"):
    if product_name and product_description:
        script = generate_video_script(product_name, product_description, duration, category, tone, discount)
        save_script(script, product_name)

        st.subheader("📜 Generated Script")
        st.text_area("Generated Script", script, height=200)

        # Extract only voiceover content
        # voiceover_text = extract_voiceover(script)
        voiceover_text = extract_voiceover(script, duration)
        voiceover_text = clean_text(voiceover_text)

        st.subheader("🗣 Extracted Voiceover Text")
        st.text_area("Voiceover Text", voiceover_text, height=150)

    else:
        st.warning("⚠️ Product Name and Description are required!")

# # Generate Voiceover
# if st.button("Generate Voiceover"):
#     saved_script = load_script()
#     if saved_script:
#         script = saved_script["script"]
#         voiceover_text = extract_voiceover(script)
#         voiceover_text = clean_text(voiceover_text)

#         if voice_name:
#             voice_file = asyncio.run(generate_voice_edge(voiceover_text, voice_name))
#             st.success(f"✅ Voiceover generated successfully!")
#             st.audio(voice_file, format="audio/mp3")
#         else:
#             st.warning("⚠️ Please select a voice!")
#     else:
#         st.warning("⚠️ Generate a script first before creating a voiceover!")

if st.button("Generate Voiceover"):
    saved_script = load_script()
    if saved_script:
        script = saved_script["script"]
        voiceover_text = extract_voiceover(script, duration)  # Pass duration
        voiceover_text = clean_text(voiceover_text)

        if voice_name:
            voice_file = asyncio.run(generate_voice_edge(voiceover_text, voice_name))
            st.success(f"✅ Voiceover generated successfully!")
            st.audio(voice_file, format="audio/mp3")
        else:
            st.warning("⚠️ Please select a voice!")
    else:
        st.warning("⚠️ Generate a script first before creating a voiceover!")

