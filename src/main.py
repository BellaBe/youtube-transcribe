import argparse
import logging
import sys

from utils import extract_video_id, extract_playlist_id
from processors import process_single_video, process_playlist

def setup_logging(verbose: bool):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format='%(asctime)s [%(levelname)s] %(message)s')
    logging.debug("Logging configured. Verbose mode: %s", verbose)

def main():
    parser = argparse.ArgumentParser(
        description="Fetch and save transcripts from a YouTube video or playlist."
    )
    parser.add_argument("url", type=str, help="The URL of the YouTube video or playlist.")
    parser.add_argument("--output-dir", type=str, default=".", help="Root directory for output files.")
    parser.add_argument("--verbose", action="store_true", help="Increase logging verbosity.")
    parser.add_argument("--max-retries", type=int, default=3, help="Number of retries for network requests.")
    parser.add_argument("--parallel", type=int, default=5, help="Number of parallel fetches for playlist videos.")

    args = parser.parse_args()
    setup_logging(args.verbose)

    playlist_id = extract_playlist_id(args.url)
    video_id = extract_video_id(args.url)

    if playlist_id and not video_id:
        logging.info("Detected playlist ID: %s", playlist_id)
        exit_code = process_playlist(playlist_id, args.output_dir, args.max_retries, args.parallel)
        sys.exit(exit_code)
    else:
        if not video_id:
            logging.error("Could not extract video ID or playlist ID from the provided URL.")
            sys.exit(1)
        logging.info("Detected video ID: %s", video_id)
        exit_code = process_single_video(video_id, args.output_dir, args.max_retries)
        sys.exit(exit_code)

if __name__ == "__main__":
    main()
