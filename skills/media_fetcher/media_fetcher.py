import yt_dlp
import os

class MediaFetcher:
    def execute(self, action: str, url: str):
        if action == "get_info":
            return self._get_info(url)
        elif action == "get_transcript":
            return self._get_transcript(url)
        return "Invalid action"

    def _get_info(self, url):
        ydl_opts = {}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    "title": info.get("title"),
                    "uploader": info.get("uploader"),
                    "duration": info.get("duration"),
                    "view_count": info.get("view_count")
                }
        except Exception as e:
            return f"Error getting info: {e}"

    def _get_transcript(self, url):
        # yt-dlp can get subtitles if available
        ydl_opts = {
            'writesubtitles': True,
            'writeautomaticsub': True,
            'skip_download': True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return f"Subtitles/Transcript logic for {info.get('title')} initialized."
        except Exception as e:
            return f"Error getting transcript: {e}"
