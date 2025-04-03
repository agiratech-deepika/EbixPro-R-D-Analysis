# import torch
# from diffusers import StableVideoDiffusionPipeline
# import cv2
# import numpy as np
# import moviepy.editor as mp

# # Load Stable Video Diffusion Model
# pipe = StableVideoDiffusionPipeline.from_pretrained("stabilityai/stable-video-diffusion-img2vid")
# pipe.to("cpu")  # Use GPU for faster processing

# # Define your script's scenes with descriptions
# scenes = [
#     "A close-up shot of a beautifully crafted brass Kalpavriksha tree, glowing under warm lighting.",
#     "A slow zoom-in on the intricate details of the brass leaves and trunk.",
#     "The brass tree placed elegantly on a living room table, with a cozy background.",
#     "A bright festive setup where the brass tree is presented as a gift.",
#     "A text overlay showing '5% Off' offer with the product in focus."
# ]

# # Generate Video Frames
# video_clips = []
# for scene in scenes:
#     frames = pipe(scene, num_inference_steps=50).frames
#     height, width, _ = frames[0].shape
#     out = cv2.VideoWriter("temp.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 10, (width, height))

#     for frame in frames:
#         frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
#         out.write(frame)
#     out.release()

#     video_clips.append(mp.VideoFileClip("temp.mp4"))

# # Merge Clips into a Final Video
# final_video = mp.concatenate_videoclips(video_clips, method="compose")
# final_video.write_videofile("generated_video.mp4", fps=24)

# print("AI-generated video saved as generated_video.mp4")

import torch
from diffusers import StableDiffusionPipeline, StableVideoDiffusionPipeline
import cv2
import numpy as np
import moviepy.editor as mp
from PIL import Image

# Load Stable Diffusion (Text-to-Image) Model
text_to_image_pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")
text_to_image_pipe.to("cpu")  # Use CPU (change to "cuda" if using GPU)

# Load Stable Video Diffusion (Img2Vid) Model
video_pipe = StableVideoDiffusionPipeline.from_pretrained("stabilityai/stable-video-diffusion-img2vid")
video_pipe.to("cpu")  # Use CPU (change to "cuda" if using GPU)

# Define script's scenes (text prompts)
scenes = [
    "A close-up shot of a beautifully crafted brass Kalpavriksha tree, glowing under warm lighting.",
    "A slow zoom-in on the intricate details of the brass leaves and trunk.",
    "The brass tree placed elegantly on a living room table, with a cozy background.",
    "A bright festive setup where the brass tree is presented as a gift.",
    "A text overlay showing '5% Off' offer with the product in focus."
]

# Generate Video Frames
video_clips = []
for i, scene in enumerate(scenes):
    print(f"Generating scene {i+1}...")

    # **Step 1: Generate Image from Text**
    image = text_to_image_pipe(scene).images[0]  # Get the generated image

    # **Step 2: Generate Video from Image**
    output = video_pipe(image, num_inference_steps=50)
    frames = output.frames  # List of images

    if not frames:
        print(f"Warning: No frames generated for scene {i+1}. Skipping.")
        continue

    height, width, _ = frames[0].shape
    temp_video_path = f"temp_scene_{i}.mp4"

    # Save frames as a video
    out = cv2.VideoWriter(temp_video_path, cv2.VideoWriter_fourcc(*"mp4v"), 10, (width, height))

    for frame in frames:
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        out.write(frame)
    out.release()

    # Load saved clip
    video_clips.append(mp.VideoFileClip(temp_video_path))

# Merge Clips into a Final Video
if video_clips:
    final_video = mp.concatenate_videoclips(video_clips, method="compose")
    final_video.write_videofile("generated_video.mp4", fps=24)

    print("AI-generated video saved as generated_video.mp4")
else:
    print("No valid scenes were generated.")
