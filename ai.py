import os
import logging
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

client = OpenAI(
    api_key=os.getenv("A4F_API_KEY"),
    base_url="https://api.a4f.co/v1"
)

def generate_hook(transcript, max_words=10):
    """Generate a viral hook from the transcript."""
    try:
        prompt = f"Generate a short, attention‑grabbing hook (max {max_words} words) for a viral reel based on this transcript:\n{transcript}"
        resp = client.chat.completions.create(
            model="provider-3/deepseek-v3",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        hook = resp.choices[0].message.content.strip()
        logger.info(f"Generated hook: {hook}")
        return hook
    except Exception as e:
        logger.error(f"Hook generation failed: {e}")
        return "🔥 This is viral!"  # fallback

def suggest_highlight_segments(transcript, total_duration):
    """Suggest start and end times for the best 20‑second highlight."""
    try:
        prompt = f"""
        This is a transcript of a video (total duration {total_duration:.1f} seconds).
        Find the most engaging 20‑second segment that would make a viral reel.
        Return only two numbers: start second and end second (e.g., 12.5 32.5).
        Transcript: {transcript}
        """
        resp = client.chat.completions.create(
            model="provider-3/deepseek-v3",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        parts = resp.choices[0].message.content.strip().split()
        if len(parts) >= 2:
            start, end = float(parts[0]), float(parts[1])
            logger.info(f"AI suggested segment: {start}-{end}")
            return start, end
    except Exception as e:
        logger.error(f"Highlight suggestion failed: {e}")
    # fallback: middle 20 seconds
    mid = total_duration / 2
    return max(0, mid-10), min(total_duration, mid+10)
