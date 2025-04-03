import openai
import json
import os
import re
from gtts import gTTS

# Replace with your OpenAI API Key
openai.api_key = "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"

SCRIPT_FILE = "generated_script.json"
VOICE_FILE = "voiceover_1.mp3"

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
    print(f"✅ Voiceover saved as {output_file}")

def clean_text(text):
    # Remove unnecessary quotes and extra spaces
    return text.replace('"', '').strip()

if __name__ == "__main__":
    print("\n🎬 AI Video Script & Voice Generator 🎬")
    
    # Load existing script if available
    saved_script = load_script()
    if saved_script:
        print("\n📜 Previously Generated Script Found:")
        print(saved_script["script"])

        use_existing = input("\nDo you want to generate voice-over from the saved script? (yes/no): ").strip().lower()
        if use_existing == "yes":
            script = saved_script["script"]
            voiceover_text = extract_voiceover(script)
            voiceover_text = clean_text(voiceover_text)
            generate_voice(voiceover_text)
            exit()

    # Collect user inputs
    product_name = input("\nEnter Product Name: ").strip()
    product_description = input("Enter Product Description: ").strip()
    duration = input("Select Video Duration (15 sec / 30 sec / 40 sec / 50 sec): ").strip()
    category = input("Select Script Category (Brand Story, Trending Topics, Call To Action, etc.): ").strip()
    tone = input("Select Tone (Engaging, Motivational, Storytelling, Just Summary): ").strip()
    discount = input("Enter Discount Details (or press enter if none): ").strip()

    if product_name and product_description:
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

        # Generate voice-over
        generate_voice(voiceover_text)
    else:
        print("⚠️ Please enter valid product details to generate a script and voice-over.")
