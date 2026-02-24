import yt_dlp
import os
import logging
from utils import logger

def download_youtube_video(url, output_path='video.mp4'):
    """Download best quality video up to 720p."""
    try:
        ydl_opts = {
            'format': 'best[height<=720]',
            'outtmpl': output_path,
            'quiet': True,
            'noplaylist': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        logger.info(f"Downloaded video: {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Download failed: {e}")
        raise

def download_audio(url, output_path='audio.m4a'):
    """Download audio for subtitle generation."""
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path,
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        mp3_path = output_path.replace('.m4a', '.mp3')
        logger.info(f"Downloaded audio: {mp3_path}")
        return mp3_path
    except Exception as e:
        logger.error(f"Audio download failed: {e}")
        raise
