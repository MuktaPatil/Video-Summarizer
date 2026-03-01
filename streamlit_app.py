import os
import subprocess
import tempfile
import textwrap
from io import BytesIO

import streamlit as st
import whisper
from transformers import pipeline


# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="VidInsight", page_icon="🎬", layout="centered")

st.title("🎬 VidInsight")
st.markdown("Paste a YouTube URL to get an AI-generated transcript and summary.")

# ── Core functions ────────────────────────────────────────────────────────────

def stream_youtube_audio(video_url: str) -> BytesIO:
    cmd = [
        "yt-dlp",
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", "mp3",
        "-o", "-",
        video_url,
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f"yt-dlp error: {stderr.decode()}")
    return BytesIO(stdout)


@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")


@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")


def transcribe_audio(audio_stream: BytesIO) -> str:
    model = load_whisper_model()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(audio_stream.read())
        tmp_path = tmp.name
    try:
        result = model.transcribe(tmp_path)
    finally:
        os.remove(tmp_path)
    return result["text"]


def summarize_text(text: str) -> str:
    summarizer = load_summarizer()
    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
    summary_parts = []
    for chunk in chunks:
        out = summarizer(chunk, max_length=130, min_length=30, do_sample=False)
        summary_parts.append(out[0]["summary_text"])
    return " ".join(summary_parts).strip()


# ── UI ────────────────────────────────────────────────────────────────────────

video_url = st.text_input(
    "YouTube URL",
    placeholder="https://youtu.be/...",
)

run_btn = st.button("🚀 Analyze Video", disabled=not video_url)

if run_btn and video_url:
    try:
        # Step 1 — Download audio
        with st.status("⏳ Processing video...", expanded=True) as status:
            st.write("🔊 Streaming audio from YouTube...")
            audio_stream = stream_youtube_audio(video_url)

            # Step 2 — Transcribe
            st.write("🗣️ Transcribing with Whisper (this takes a minute)...")
            transcript = transcribe_audio(audio_stream)
            audio_stream.close()

            # Step 3 — Summarize
            st.write("🧠 Summarizing transcript...")
            summary = summarize_text(transcript)

            status.update(label="✅ Done!", state="complete")

        # ── Results ──────────────────────────────────────────────────────────
        st.divider()

        tab1, tab2 = st.tabs(["📋 Summary", "📝 Full Transcript"])

        with tab1:
            st.subheader("Summary")
            wrapped = textwrap.fill(summary, width=100)
            st.write(wrapped)
            st.download_button(
                "⬇️ Download Summary",
                data=summary,
                file_name="summary.txt",
                mime="text/plain",
            )

        with tab2:
            st.subheader("Full Transcript")
            st.write(transcript)
            st.download_button(
                "⬇️ Download Transcript",
                data=transcript,
                file_name="transcript.txt",
                mime="text/plain",
            )

    except RuntimeError as e:
        st.error(f"Something went wrong: {e}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")
