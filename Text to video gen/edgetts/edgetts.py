# import edge_tts
# import asyncio

# async def generate_voice_edge(text, voice="en-US-JennyNeural", output_file="voiceover.mp3"):
#     communicate = edge_tts.Communicate(text, voice)
#     await communicate.save(output_file)
#     return output_file

# # Example usage
# text = "Hello! This is a test using Microsoft's Edge TTS."
# asyncio.run(generate_voice_edge(text))
import edge_tts
import asyncio
import json

# Function to get available voices
async def list_voices():
    voices = await edge_tts.list_voices()
    return voices

# Function to generate voice and save as an audio file
async def generate_voice_edge(text, voice_name, output_file):
    communicate = edge_tts.Communicate(text, voice_name)
    await communicate.save(output_file)
    return output_file

# Main function to run the script
async def main():
    # Get available voices
    voices = await list_voices()
    
    # Save voice list to a JSON file
    with open("voices.json", "w") as f:
        json.dump(voices, f, indent=4)
    
    print("Available voices saved in voices.json")

    # Short sample text
    sample_text = "Hello! This is a test using Microsoft's Edge TTS."

    # Save multiple voices in a loop (saving first 5 voices for demonstration)
    for idx, voice in enumerate(voices[:5]):  # Limit to first 5 voices
        voice_name = voice["Name"]
        output_file = f"voice_{idx+1}.mp3"
        print(f"Generating voice: {voice_name} -> {output_file}")
        await generate_voice_edge(sample_text, voice_name, output_file)

# Run the script
asyncio.run(main())
