# Hackathon Project: Video Generation App

This project is a Flask-based web application that generates short videos based on user-provided topics. It uses state-of-the-art AI models for text generation, image generation, and text-to-speech synthesis.

## Features

- **Script Generation**: Automatically generates a video script using GPT-2.
- **Image Generation**: Creates artistic images using Stable Diffusion.
- **Audio Generation**: Converts the script into audio using Google Text-to-Speech (gTTS).
- **Video Assembly**: Combines the generated images and audio into a video using FFmpeg.

## Project Structure

```
hackathon-project/
├── app.py               # Main Flask application
├── static/
│   ├── videos/          # Directory for generated videos
│   ├── images/          # Directory for generated images
├── templates/
│   ├── index.html       # Frontend HTML file
└── README.md            # Project documentation
```

## Prerequisites

- Python 3.8 or higher
- Pip (Python package manager)
- FFmpeg (for video processing)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd hackathon-project
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure FFmpeg is installed and available in your system's PATH. You can download it from [FFmpeg.org](https://ffmpeg.org/).

## Usage

1. Run the Flask application:
   ```bash
   python app.py
   ```

2. Open your browser and navigate to `http://127.0.0.1:5000/`.

3. Enter a topic in the input field and click "Generate". The app will create a video based on the topic and provide a link to download or view it.

## API Endpoints

- `GET /`: Serves the homepage.
- `POST /generate`: Accepts a JSON payload with a `topic` field and returns the URL of the generated video.
- `GET /static/<filename>`: Serves static files like generated videos and images.

## Troubleshooting

- **Model Download Issues**: Ensure you have a stable internet connection. The models are downloaded from Hugging Face and other sources.
- **FFmpeg Errors**: Verify that FFmpeg is correctly installed and accessible from the command line.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

- [Hugging Face Transformers](https://huggingface.co/transformers/)
- [Diffusers by Hugging Face](https://huggingface.co/docs/diffusers/)
- [Google Text-to-Speech (gTTS)](https://pypi.org/project/gTTS/)
- [FFmpeg](https://ffmpeg.org/)
