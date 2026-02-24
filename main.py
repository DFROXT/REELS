import os
import logging
from dotenv import load_dotenv
from download import download_youtube_video
from ai import generate_hook, suggest_highlight_segments
from edit import create_reel
from utils import clean_temp_files

load_dotenv()
logger = logging.getLogger(__name__)

def process_reel(youtube_url):
    """Main function to process a YouTube URL into a viral reel."""
    temp_files = []
    output_file = None
    try:
        # Download video
        video_path = download_youtube_video(youtube_url, 'temp_video.mp4')
        temp_files.append(video_path)
        
        # For transcript, in real scenario use Whisper; here we mock
        transcript = "This is a sample transcript. Replace with actual speech-to-text output."
        
        # Get video duration
        from moviepy.editor import VideoFileClip
        with VideoFileClip(video_path) as clip:
            total_duration = clip.duration
        
        # AI suggestions
        start, end = suggest_highlight_segments(transcript, total_duration)
        hook = generate_hook(transcript)
        
        # Create output directory
        os.makedirs('output', exist_ok=True)
        output_file = f"output/reel_{os.path.basename(youtube_url)}.mp4"
        
        # Edit video
        create_reel(video_path, output_file, start, end, hook, bgm_path='bgm.mp3')
        
        logger.info(f"Processing complete: {output_file}")
        return output_file
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        raise
    finally:
        # Cleanup temp files
        clean_temp_files(temp_files)

# For standalone testing
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python main.py <youtube_url>")
        sys.exit(1)
    process_reel(sys.argv[1])
