import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple

from fetchers import fetch_html, get_transcript
from parsers import extract_yt_initial_data, parse_playlist_videos
from exceptions import FetchError, TranscriptError
from utils import write_metadata, save_transcript

def process_single_video(video_id: str, output_dir: str, max_retries: int) -> int:
    logging.debug("Processing single video: %s", video_id)
    dir_name = os.path.join(output_dir, f"single_{video_id}")
    os.makedirs(dir_name, exist_ok=True)
    logging.info("Created directory %s for single video", dir_name)

    metadata = {
        "type": "single_video",
        "video_id": video_id,
        "status": "success",
        "error": None
    }

    transcript_path = os.path.join(dir_name, "transcript.txt")
    metadata_path = os.path.join(dir_name, "metadata.json")

    try:
        transcript = get_transcript(video_id, max_retries)
        save_transcript(transcript, transcript_path)
        logging.info("Transcript saved for video %s at %s", video_id, transcript_path)
    except TranscriptError as e:
        logging.warning("Video %s: %s", video_id, e)
        metadata["status"] = "failed"
        metadata["error"] = str(e)

    write_metadata(metadata, metadata_path)
    logging.info("Metadata written for single video %s at %s", video_id, metadata_path)

    return 0

def process_playlist(playlist_id: str, output_dir: str, max_retries: int, parallel: int) -> int:
    logging.debug("Processing playlist: %s", playlist_id)
    dir_name = os.path.join(output_dir, f"playlist_{playlist_id}")
    os.makedirs(dir_name, exist_ok=True)
    logging.info("Created directory %s for playlist", dir_name)

    playlist_url = f"https://www.youtube.com/playlist?list={playlist_id}"
    try:
        html = fetch_html(playlist_url, max_retries)
        yt_data = extract_yt_initial_data(html)
        videos = parse_playlist_videos(yt_data)
    except FetchError as e:
        logging.error("Failed to process playlist %s: %s", playlist_id, e)
        return 1

    logging.info("Found %d videos in the playlist %s.", len(videos), playlist_id)

    metadata = {
        "type": "playlist",
        "playlist_id": playlist_id,
        "video_count": len(videos),
        "videos": []
    }

    def fetch_video_transcript(data):
        idx, vid = data
        logging.debug("Fetching transcript for playlist video %s at index %d", vid, idx)
        result = {
            "index": idx,
            "video_id": vid,
            "status": "success",
            "error": None
        }

        file_path = os.path.join(dir_name, f"transcript_{idx}_{vid}.txt")
        try:
            transcript = get_transcript(vid, max_retries)
            save_transcript(transcript, file_path)
            logging.info("Transcript saved for video %s (index %d) at %s", vid, idx, file_path)
        except TranscriptError as e:
            logging.warning("Video %s (index %d): %s", vid, idx, e)
            result["status"] = "failed"
            result["error"] = str(e)

        return result

    with ThreadPoolExecutor(max_workers=parallel) as executor:
        logging.debug("Fetching transcripts in parallel with %d workers.", parallel)
        futures = {executor.submit(fetch_video_transcript, v): v for v in videos}

        results = []
        for future in as_completed(futures):
            res = future.result()
            results.append(res)

    results.sort(key=lambda x: x["index"])
    metadata["videos"] = results

    metadata_path = os.path.join(dir_name, "metadata.json")
    write_metadata(metadata, metadata_path)
    logging.info("Metadata written for playlist %s at %s", playlist_id, metadata_path)

    return 0
