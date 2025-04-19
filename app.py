# YouTube Video Transcript Summarizer using Streamlit + HuggingFace

# import streamlit as st
# from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
# from transformers import pipeline
# import re
#
# # --- Setup summarizer ---
#
# summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
#
# def extract_video_id(url):
#     match = re.search(r"(?:v=|youtu.be/)([\w-]+)", url)
#     return match.group(1) if match else None
#
# def fetch_transcript(video_id):
#     try:
#         transcript = YouTubeTranscriptApi.get_transcript(video_id)
#         full_text = " ".join([entry['text'] for entry in transcript])
#         return full_text
#     except (TranscriptsDisabled, NoTranscriptFound):
#         return None
#
# def summarize_text(text):
#     if len(text) > 1000:
#         text = text[:1024]  # Truncate if too long for model
#     summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
#     return summary[0]['summary_text']
#
# # --- Streamlit App ---
# st.title("📺 YouTube Video Summarizer")
# st.write("Paste a YouTube link and get a short summary of the video transcript.")
#
# url = st.text_input("Enter YouTube URL")
#
# if url:
#     with st.spinner("Fetching transcript and summarizing..."):
#         video_id = extract_video_id(url)
#         transcript = fetch_transcript(video_id)
#
#         if transcript:
#             summary = summarize_text(transcript)
#             st.subheader("Summary")
#             st.write(summary)
#             with st.expander("See full transcript"):
#                 st.write(transcript)
#         else:
#             st.error("❌ Transcript not available for this video.")
#
# import streamlit as st
# from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
# from transformers import pipeline
# import re
#
# def extract_video_id(url):
#     match = re.search(r"(?:v=|youtu.be/)([\w-]+)", url)
#     return match.group(1) if match else None
#
# def fetch_transcript(video_id):
#     try:
#         transcript = YouTubeTranscriptApi.get_transcript(video_id)
#         full_text = " ".join([entry['text'] for entry in transcript])
#         return full_text
#     except (TranscriptsDisabled, NoTranscriptFound):
#         return None
#
# def summarize_text(text, summarizer):
#     if len(text) > 1000:
#         text = text[:1024]
#     summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
#     return summary[0]['summary_text']
#
# # --- Streamlit UI ---
# st.title("📺 YouTube Video Summarizer")
# st.write("Paste a YouTube link and get a short summary of the video transcript.")
#
# url = st.text_input("Enter YouTube URL")
#
# if url:
#     with st.spinner("Loading summarization model..."):
#         summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
#
#     with st.spinner("Fetching transcript and summarizing..."):
#         video_id = extract_video_id(url)
#         transcript = fetch_transcript(video_id)
#
#         if transcript:
#             summary = summarize_text(transcript, summarizer)
#             st.subheader("Summary")
#             st.write(summary)
#             with st.expander("See full transcript"):
#                 st.write(transcript)
#         else:
#             st.error("❌ Transcript not available for this video.")
# else:
#     st.info("👆 Paste a YouTube video link above to generate a summary.")


import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from transformers import pipeline
import re

# --- Helper Functions ---
def extract_video_id(url):
    match = re.search(r"(?:v=|youtu.be/)([\w-]+)", url)
    return match.group(1) if match else None

def fetch_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join([entry['text'] for entry in transcript])
        return full_text
    except (TranscriptsDisabled, NoTranscriptFound):
        return None

# def summarize_text(text, summarizer):
#     if len(text) > 1000:
#         text = text[:1024]
#     summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
#     return summary[0]['summary_text']

def split_text(text, max_tokens=1000):
    sentences = text.split('. ')
    chunks = []
    chunk = ''
    for sentence in sentences:
        if len(chunk) + len(sentence) <= max_tokens:
            chunk += sentence + '. '
        else:
            chunks.append(chunk.strip())
            chunk = sentence + '. '
    if chunk:
        chunks.append(chunk.strip())
    return chunks

def summarize_text(text, summarizer):
    chunks = split_text(text)
    summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=150, min_length=30, do_sample=False)
        summaries.append(summary[0]['summary_text'])
    final_summary = ' '.join(summaries)
    return final_summary

# --- Load Summarization Model Once ---
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

summarizer = load_summarizer()

# --- Streamlit UI ---
st.title("📺 YouTube Video Summarizer")
st.write("Paste a YouTube link and get a short summary of the video transcript.")

url = st.text_input("Enter YouTube URL")

if url:
    video_id = extract_video_id(url)
    if not video_id:
        st.error("❌ Invalid YouTube URL.")
    else:
        with st.spinner("Fetching transcript and summarizing..."):
            transcript = fetch_transcript(video_id)

            if transcript:
                summary = summarize_text(transcript, summarizer)
                st.subheader("Summary")
                st.write(summary)
                with st.expander("See full transcript"):
                    st.write(transcript)
            else:
                st.error("❌ Transcript not available for this video.")
else:
    st.info("👆 Paste a YouTube video link above to generate a summary.")



