import requests
import urllib.parse
from src.core.configs import settings
from src.core.logger import logger

def search_youtube(topic_name: str) -> list:
    """Uses the official YouTube Data API v3 to search for video tutorials."""
    logger.info("Searching YouTube API for Videos", topic=topic_name)
    
    youtube_key = settings.YOUTUBE_API_KEY
    encoded_topic = urllib.parse.quote(topic_name)
    
    if not youtube_key:
        logger.warning("YOUTUBE_API_KEY is missing. Falling back to dynamic static URL.")
        return [f"[YouTube: Best '{topic_name}' Tutorials](https://www.youtube.com/results?search_query={encoded_topic}+tutorial)"]

    try:
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": f"{topic_name} programming tutorial",
            "maxResults": 3,
            "type": "video",
            "key": youtube_key
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status() # rasie if the request was unsuccessful
        data = response.json()
        
        links = []
        for item in data.get("items", []):
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            links.append(f"[{title}](https://www.youtube.com/watch?v={video_id})")
            
        if not links:
            return [f"[YouTube: Best '{topic_name}' Tutorials](https://www.youtube.com/results?search_query={encoded_topic}+tutorial)"]
            
        return links
            
    except Exception as e:
        logger.error("YouTube API Search Failed", error=str(e))
        return [f"[YouTube: Best '{topic_name}' Tutorials](https://www.youtube.com/results?search_query={encoded_topic}+tutorial)"]
