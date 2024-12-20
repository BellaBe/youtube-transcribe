import json
import logging
import os
from urllib.parse import urlparse, parse_qs
from typing import Optional, Dict, Any

def extract_video_id(url: str) -> Optional[str]:
    logging.debug("Extracting video ID from URL: %s", url)
    parsed_url = urlparse(url)
    if parsed_url.hostname in ['www.youtube.com', 'youtube.com', 'm.youtube.com']:
        video_id = parse_qs(parsed_url.query).get('v')
        if video_id:
            vid = video_id[0]
            logging.debug("Extracted video ID: %s", vid)
            return vid
    if parsed_url.hostname == 'youtu.be':
        vid = parsed_url.path.lstrip('/')
        logging.debug("Extracted video ID from shortened URL: %s", vid)
        return vid
    logging.debug("No video ID found in URL.")
    return None

def extract_playlist_id(url: str) -> Optional[str]:
    logging.debug("Extracting playlist ID from URL: %s", url)
    parsed_url = urlparse(url)
    if parsed_url.hostname in ['www.youtube.com', 'youtube.com', 'm.youtube.com']:
        playlist_id = parse_qs(parsed_url.query).get('list')
        if playlist_id:
            pid = playlist_id[0]
            logging.debug("Extracted playlist ID: %s", pid)
            return pid
    logging.debug("No playlist ID found in URL.")
    return None

def save_transcript(transcript: str, file_path: str):
    logging.debug("Saving transcript to %s", file_path)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(transcript)

def write_metadata(metadata: Dict[str, Any], file_path: str):
    logging.debug("Writing metadata to %s", file_path)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)
