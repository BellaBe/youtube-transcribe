import json
import logging
import re
from exceptions import FetchError

def extract_yt_initial_data(html: str) -> dict:
    logging.debug("Extracting ytInitialData from HTML.")
    match = re.search(r'var ytInitialData = (\{.*?\});', html)
    if not match:
        logging.error("ytInitialData not found in HTML.")
        raise FetchError("Could not find ytInitialData in the page HTML.")
    yt_initial_data = json.loads(match.group(1))
    logging.debug("ytInitialData extracted successfully.")
    return yt_initial_data

def parse_playlist_videos(yt_data: dict):
    logging.debug("Parsing playlist videos from ytInitialData.")
    try:
        tabs = yt_data["contents"]["twoColumnBrowseResultsRenderer"]["tabs"]
        for tab in tabs:
            tab_content = tab.get("tabRenderer", {}).get("content", {})
            section_list = tab_content.get("sectionListRenderer", {}).get("contents", [])
            for section in section_list:
                item_section = section.get("itemSectionRenderer", {}).get("contents", [])
                for item in item_section:
                    playlist_data = item.get("playlistVideoListRenderer", {})
                    if "contents" in playlist_data:
                        playlist_items = playlist_data["contents"]
                        videos = []
                        for idx, video_item in enumerate(playlist_items, start=1):
                            renderer = video_item.get("playlistVideoRenderer")
                            if renderer and "videoId" in renderer:
                                vid = renderer["videoId"]
                                videos.append((idx, vid))
                        logging.debug("Parsed %d videos from playlist.", len(videos))
                        return videos
        logging.error("No playlistVideoRenderer found in ytInitialData.")
        raise FetchError("No playlistVideoRenderer found in ytInitialData.")
    except KeyError as e:
        logging.error("JSON structure unexpected, missing key: %s", e)
        raise FetchError(f"JSON structure unexpected. Key not found: {e}")
