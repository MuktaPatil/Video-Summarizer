# 🎧 YouTube Video Summarizer with Whisper & Transformers
This project allows you to stream audio from any YouTube video, transcribe it using OpenAI's Whisper, and summarize the transcript using Hugging Face's facebook/bart-large-cnn model.

### 📌 Features
No need to download the entire video

Transcription with Whisper (base model)

Summarization using Hugging Face Transformers

Fully automated from URL to summary

### 🚀 How It Works
Stream Audio: Uses yt-dlp to extract and stream best-quality audio from a YouTube video.

Transcribe: Uses OpenAI's Whisper model to transcribe the audio to text.

Summarize: Splits the text into chunks and summarizes them using the facebook/bart-large-cnn model from Hugging Face.

### 🧪 Example Usage
Replace the video_url with the YouTube link you want to summarize:

```
video_url = "https://youtu.be/wo_e0EvEZn8?si=baQuTnFySjjK4KPb"
summary = summarize_youtube_video(video_url)
print(f"Summary: {summary}")
```
⏱️ Note: The script takes ~7 minutes depending on video length, system performance, and internet speed.

### 💡 Future Improvements
* Add support for multilingual videos

* Add a web interface with Gradio or Streamlit

* Allow summarization in different styles (bullet points, TL;DR, etc.)

### 📈 Flowchart Overview

- `YouTube Video URL`
     ↓
    - `Step 1: Stream Audio with yt-dlp`
        - Downloads best-quality audio as MP3
        - Streams it to memory using BytesIO
    - ↓
    - `Step 2: Transcribe with Whisper`
        - Saves audio to a temporary .mp3 file
        - Loads Whisper base model
        - Transcribes speech to text
    - ↓
    - `Step 3: Summarize with BART`
        - Splits text into 1000-character chunks
        - Uses facebook/bart-large-cnn to summarize
        - Joins all summaries into final output
    - ↓
    - `Step 4: Output Final Summary`
        - Final summary is printed or returned



