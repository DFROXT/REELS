import os
import logging
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip, CompositeAudioClip
from moviepy.video.fx.all import resize, crop
import cv2
import numpy as np

logger = logging.getLogger(__name__)

def zoom_effect(get_frame, t):
    """Zoom punch every 2 seconds."""
    frame = get_frame(t)
    cycle = (t // 2) % 2
    progress = (t % 2) / 2.0
    if cycle == 0:
        scale = 1.0 + 0.1 * progress
    else:
        scale = 1.1 - 0.1 * progress
    h, w = frame.shape[:2]
    new_h, new_w = int(h * scale), int(w * scale)
    resized = cv2.resize(frame, (new_w, new_h))
    y1 = (new_h - h) // 2
    x1 = (new_w - w) // 2
    return resized[y1:y1+h, x1:x1+w]

def create_reel(input_video, output_path, start_time, end_time, hook_text, bgm_path='bgm.mp3'):
    """Main editing function with error handling."""
    try:
        # Load clip
        clip = VideoFileClip(input_video).subclip(start_time, end_time)
        
        # Crop to 9:16
        target_ratio = 9/16
        w, h = clip.w, clip.h
        current_ratio = w / h
        if current_ratio > target_ratio:
            new_w = int(h * target_ratio)
            x_center = w / 2
            clip = crop(clip, x1=x_center - new_w/2, y1=0, width=new_w, height=h)
        else:
            new_h = int(w / target_ratio)
            y_center = h / 2
            clip = crop(clip, x1=0, y1=y_center - new_h/2, width=w, height=new_h)
        clip = resize(clip, (720, 1280))
        
        # Apply zoom effect
        clip = clip.fl(zoom_effect)
        
        # Add hook text
        txt_clip = TextClip(hook_text, fontsize=70, color='white', font='Arial-Bold',
                            stroke_color='black', stroke_width=3)
        txt_clip = txt_clip.set_position(('center', 1000)).set_duration(clip.duration)
        
        # Add background music
        if os.path.exists(bgm_path):
            bgm = AudioFileClip(bgm_path).volumex(0.15)
            bgm = bgm.subclip(0, clip.duration)
            final_audio = CompositeAudioClip([clip.audio, bgm])
            clip = clip.set_audio(final_audio)
        
        # Loop ending: freeze last frame and crossfade
        last_frame = clip.to_ImageClip(clip.duration - 0.04)
        last_frame = last_frame.set_duration(0.5)
        loop = CompositeVideoClip([clip, last_frame.set_start(clip.duration - 0.5).crossfadein(0.5)])
        loop = loop.set_duration(clip.duration + 0.5)
        
        final = CompositeVideoClip([loop, txt_clip])
        
        # Write video
        final.write_videofile(output_path, codec='libx264', audio_codec='aac', threads=2, preset='ultrafast')
        logger.info(f"Reel created: {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Video editing failed: {e}")
        raise
