import openai
import json
import os
import re
import asyncio
import edge_tts
import datetime

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

# Function to generate a unique voiceover file using Edge TTS
async def generate_voice_edge(script_text, voice_name, product_name):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    voice_file = f"{timestamp}.mp3"  # Unique filename

    communicate = edge_tts.Communicate(script_text, voice_name)
    await communicate.save(voice_file)
    
    print(f"✅ Voiceover saved as {voice_file}")

# Function to clean extracted text
def clean_text(text):
    return text.replace('"', '').strip()

async def main():
    print("\n🎬 AI Video Script & Voice Generator 🎬")
    
    # Load existing script if available
    saved_script = load_script()
    if saved_script:
        print("\n📜 Previously Generated Script Found:")
        print(saved_script["script"])

        use_existing = input("\nDo you want to generate voice-over from the saved script? (yes/no): ").strip().lower()
        if use_existing == "yes":
            script = saved_script["script"]
            product_name = saved_script["product_name"]
            voiceover_text = extract_voiceover(script)
            voiceover_text = clean_text(voiceover_text)

            # Get voice input
            voice_name = input("\nEnter the Edge TTS voice name (e.g., en-US-JennyNeural): ").strip()
            if voice_name:
                await generate_voice_edge(voiceover_text, voice_name, product_name)
            else:
                print("⚠️ Voice name cannot be empty!")
            return

    # Collect user inputs
    product_name = input("\nEnter Product Name: ").strip()
    product_description = input("Enter Product Description: ").strip()
    duration = input("Select Video Duration (15 sec / 30 sec / 40 sec / 50 sec): ").strip()
    category = input("Select Script Category (Brand Story, Trending Topics, Call To Action, etc.): ").strip()
    tone = input("Select Tone (Engaging, Motivational, Storytelling, Just Summary): ").strip()
    discount = input("Enter Discount Details (or press enter if none): ").strip()

    # Ensure required fields are filled
    if not product_name or not product_description:
        print("⚠️ Product Name and Description are required!")
        return

    # Generate script
    script = generate_video_script(product_name, product_description, duration, category, tone, discount)
    save_script(script, product_name)

    print("\n📜 Generated Script:")
    print(script)

    # Extract only voiceover content
    voiceover_text = extract_voiceover(script)
    voiceover_text = clean_text(voiceover_text)

    print("\n🗣 Extracted Voiceover Text:")
    print(voiceover_text)

    # Get voice input
    voice_name = input("\nEnter the Edge TTS voice name (e.g., en-US-JennyNeural): ").strip()
    if voice_name:
        await generate_voice_edge(voiceover_text, voice_name, product_name)
    else:
        print("⚠️ Voice name cannot be empty!")

# Run the script asynchronously
asyncio.run(main())
