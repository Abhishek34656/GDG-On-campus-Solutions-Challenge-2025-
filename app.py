from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import subprocess
from transformers import pipeline
from diffusers import StableDiffusionPipeline
from gtts import gTTS

app = Flask(__name__, static_folder="static", template_folder="templates")

# Directory to store generated videos and images
OUTPUT_DIR = "static/videos"
IMAGE_DIR = "static/images"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)

@app.route('/')
def index():
    # Serve the index.html file
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_video():
    try:
        data = request.json
        topic = data.get('topic')

        if not topic:
            return jsonify({"error": "Topic is required"}), 400

        # Step 1: Generate Script
        script = generate_script(topic)

        # Step 2: Generate Images
        images = generate_images(script)

        # Step 3: Generate Audio
        audio_path = generate_audio(script)

        # Step 4: Combine into Video
        video_path = assemble_video(images, audio_path)

        # Return the video URL
        video_url = f"/{video_path}"
        return jsonify({"video_url": video_url})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

def generate_script(topic):
    try:
        # Use Hugging Face's GPT-2 model for text generation
        generator = pipeline("text-generation", model="gpt2", device=-1)  # Use CPU (device=-1)
        prompt = f"Write a short video script about {topic}."
        response = generator(prompt, max_length=300, num_return_sequences=1, truncation=True)  # Add truncation=True
        return response[0]['generated_text'].strip()
    except Exception as e:
        raise RuntimeError(f"Error generating script: {e}")

def generate_images(script):
    try:
        # Force re-download of the Stable Diffusion model
        pipe = StableDiffusionPipeline.from_pretrained(
            "CompVis/stable-diffusion-v1-4",
            force_download=True  # Force re-download to ensure the file is complete
        )
        pipe.to("cpu")  # Use CPU

        # Generate images based on the script
        prompt = f"An artistic representation of: {script}"
        images = []
        for i in range(3):  # Generate 3 images
            image = pipe(prompt).images[0]
            image_path = os.path.join(IMAGE_DIR, f"image{i + 1}.png")
            image.save(image_path)
            images.append(image_path)

        return images
    except Exception as e:
        raise RuntimeError(f"Error generating images: {e}")

def generate_audio(script):
    try:
        audio_path = os.path.join(OUTPUT_DIR, "output_audio.mp3")
        tts = gTTS(script)
        tts.save(audio_path)
        return audio_path
    except Exception as e:
        raise RuntimeError(f"Error generating audio: {e}")

def assemble_video(images, audio_path):
    try:
        video_path = os.path.join(OUTPUT_DIR, "output_video.mp4")
        # Use FFmpeg to combine the first image and audio into a video
        command = [
            "ffmpeg", "-y",
            "-i", audio_path,
            "-loop", "1",
            "-i", images[0],  # Use the first image as a placeholder
            "-c:v", "libx264",
            "-t", "10",  # Duration of the video in seconds
            "-pix_fmt", "yuv420p",
            video_path
        ]
        subprocess.run(command, check=True)
        return video_path
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error assembling video: {e}")

# Serve static files (e.g., generated videos)
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory("static", filename)

if __name__ == '__main__':
    app.run(debug=True)