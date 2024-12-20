# YouTube Transcript CLI Tool

This tool fetches transcripts for YouTube videos and playlists. It uses a combination of HTML parsing and transcript APIs to retrieve video transcripts. The results are saved locally with transcripts and metadata for easy analysis.

## Features

- **Single Video Support**: Given a YouTube video URL, fetch its transcript and save it locally.
- **Playlist Support**: Given a YouTube playlist URL, fetch transcripts for every video in the playlist, saving each transcript and generating a metadata file summarizing results.
- **Parallelization**: Fetch multiple transcripts from a playlist concurrently to speed up the process.
- **Retries and Error Handling**: Robust error handling with retries for network failures and structured error messages.
- **Configurable Output**: Easily specify an output directory, verbosity, max retries, and parallelization.


## Requirements

- **Python 3.9+** (Recommended)
- **Poetry** for dependency management. If you don't have it installed:
  
  ```bash
  pip install poetry
  ```
  
## Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/your-repo.git
cd your-repo
```
2. Install dependencies using Poetry:
```bash
poetry install
```

## Usage

### Single Video
To fetch a transcript for a single YouTube video (e.g., https://www.youtube.com/watch?v=HNJmWKndUA4):

```bash
make transcript https://www.youtube.com/watch?v=HNJmWKndUA4
```

By default, results are saved under `output/single_<video_id>` directory. The directory contains:

- `transcript.txt`: The fetched transcript.
- `metadata.json`: Information about the fetch status and any errors.

### Playlist
To fetch transcripts for all videos in a playlist (e.g., https://www.youtube.com/playlist?list=PLkmvmF0zhgT-riVHhIpsyTysp9n-5-C6G):

```bash
make transcript https://www.youtube.com/playlist?list=PLkmvmF0zhgT-riVHhIpsyTysp9n-5-C6G
```

The results are saved under `output/playlist_<playlist_id>` directory. This directory contains:

- multiple transcript_{index}_{video_id}.txt files, one for each video in the playlist.
- a metadata.json file with an overview of all processed videos, their success/failure status, and any error messages.


## Customizing Options
You can customize options by passing them to make:

### Change output directory:

```bash
make transcript https://www.youtube.com/watch?v=HNJmWKndUA4 OUTPUT_DIR="myresults"
```

### Increase verbosity (debug logs):

```bash
make transcript https://www.youtube.com/watch?v=HNJmWKndUA4 VERBOSE=1
```

### Change max retries:

```bash
make transcript https://www.youtube.com/watch?v=HNJmWKndUA4 MAX_RETRIES=5
```

### Increase parallel workers for playlists:

```bash
make transcript https://www.youtube.com/playlist?list=PLkmvmF0zhgT-riVHhIpsyTysp9n-5-C6G PARALLEL=10
```

## Cleaning Up
To remove the output directory and all generated files:

```bash
make clean
```
## Logging

Without `VERBOSE=1`, the script logs at INFO level, showing key steps and outcomes.
With `VERBOSE=1`, logs are at `DEBUG` level, providing detailed step-by-step output including attempts, retries, and intermediate parsing steps.

## Error Handling

- If the tool fails to fetch transcripts (due to unavailable transcripts or network errors), it records the failure in metadata.json but continues processing other videos.
- The script exits with code 0 on successful completion and 1 on severe failures (e.g., invalid URLs, inability to parse required data).

## License
This project is licensed under the MIT License.