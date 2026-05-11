import urllib.parse
from exa_py import Exa
from src.core.configs import settings
from src.core.logger import logger

def search_courses(topic_name: str) -> list:
    """Uses Exa API to search for courses and tutorials."""
    logger.info("Searching Exa for Courses", topic=topic_name)
    try:
        exa_key = settings.EXA_API_KEY
        if not exa_key:
            raise ValueError("EXA_API_KEY environment variable is missing.")
            
        exa = Exa(api_key=exa_key)
        
        search_query = f"best online courses, certifications, and tutorials to learn {topic_name}"
        search_results = exa.search(
            search_query,
            num_results=3,
        )
        
        links = []
        for res in search_results.results:
            links.append(f"[{res.title}]({res.url})")
        return links
            
    except Exception as e:
        logger.error("Exa Search Failed", error=str(e))
        encoded_topic = urllib.parse.quote(topic_name) # ensure safe characters for URL (avoid #, &, ?,...)
        return [
            f"[YouTube: Video Tutorials for '{topic_name}'](https://www.youtube.com/results?search_query={encoded_topic}+tutorial)",
            f"[Coursera: Search '{topic_name}'](https://www.coursera.org/search?query={encoded_topic})",
            "*(Note: Exa API failed to fetch dynamic courses)*"
        ]
