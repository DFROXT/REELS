import os
import re
import shutil
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_temp_files(paths):
    """Delete temporary files/folders with error handling."""
    for p in paths:
        try:
            if os.path.isfile(p):
                os.remove(p)
                logger.info(f"Deleted file: {p}")
            elif os.path.isdir(p):
                shutil.rmtree(p)
                logger.info(f"Deleted folder: {p}")
        except Exception as e:
            logger.error(f"Failed to delete {p}: {e}")

def parse_time(seconds):
    """Convert seconds to HH:MM:SS.mmm format."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}"

def vtt_to_text(vtt_path):
    """Extract plain text from a VTT subtitle file."""
    try:
        with open(vtt_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        text = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('WEBVTT') and not re.match(r'^\d{2}:\d{2}', line) and '-->' not in line:
                text.append(line)
        return ' '.join(text)
    except Exception as e:
        logger.error(f"VTT parsing error: {e}")
        return ""
