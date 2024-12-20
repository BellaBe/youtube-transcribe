import logging
import requests
import xml.etree.ElementTree as ET
from exceptions import FetchError, TranscriptError

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
URL_TRANSCRIPT_FORMAT = 'https://youtubetranscript.com/?server_vid2={}'

def fetch_html(url: str, max_retries: int) -> str:
    logging.debug("Fetching HTML from URL: %s with max_retries=%d", url, max_retries)
    for attempt in range(1, max_retries+1):
        try:
            response = requests.get(url, headers={"User-Agent": USER_AGENT})
            if response.status_code == 200:
                logging.debug("Successfully fetched HTML on attempt %d", attempt)
                return response.text
            else:
                logging.warning("Attempt %d: Failed to fetch %s, status %d", attempt, url, response.status_code)
        except requests.RequestException as e:
            logging.warning("Attempt %d: Request error %s", attempt, e)
    raise FetchError(f"Failed to fetch HTML from {url} after {max_retries} attempts.")

def get_transcript(video_id: str, max_retries: int) -> str:
    logging.debug("Fetching transcript for video ID: %s with max_retries=%d", video_id, max_retries)
    transcript_url = URL_TRANSCRIPT_FORMAT.format(video_id)
    for attempt in range(1, max_retries+1):
        try:
            response = requests.get(transcript_url, headers={"User-Agent": USER_AGENT})
            if response.status_code == 200:
                root = ET.fromstring(response.text)
                transcript = ' '.join([elem.text for elem in root.findall('.//text') if elem.text])
                transcript = transcript.strip()
                if not transcript:
                    logging.warning("No transcript text found for video %s on attempt %d", video_id, attempt)
                    continue
                logging.debug("Transcript fetched successfully for video %s on attempt %d", video_id, attempt)
                return transcript
            else:
                logging.warning("Attempt %d: Failed to fetch transcript for %s, status %d", attempt, video_id, response.status_code)
        except requests.RequestException as e:
            logging.warning("Attempt %d: Error fetching transcript for %s: %s", attempt, video_id, e)
        except ET.ParseError:
            logging.warning("Attempt %d: Failed to parse transcript XML for %s.", attempt, video_id)
    raise TranscriptError(f"Failed to get a valid transcript for {video_id} after {max_retries} attempts.")
