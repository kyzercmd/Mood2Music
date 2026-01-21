import requests
import random
from typing import List
from .sentiment import Genre

ITUNES_SEARCH_URL = "https://itunes.apple.com/search"

# Genre -> Cinematic/Atmospheric Search Terms
GENRE_TO_QUERIES = {
    Genre.FANTASY: [
        "lord of the rings soundtrack",
        "fantasy orchestral music",
        "magical instrumental",
        "video game adventure soundtrack"
    ],
    Genre.SCIFI: [
        "blade runner atmospheric",
        "cyberpunk ambient",
        "sci-fi movie score",
        "space synthesizer instrumental"
    ],
    Genre.ROMANCE: [
        "romantic piano instrumental",
        "love theme movie score",
        "soft acoustic guitar",
        "emotional violin"
    ],
    Genre.HORROR: [
        "dark ambient horror",
        "creepy movie soundtrack",
        "suspense tension instrumental",
        "scary atmosphere"
    ],
    Genre.THRILLER: [
        "hans zimmer tension",
        "action movie soundtrack",
        "spy film score",
        "intense cinematic drums"
    ],
    Genre.HISTORY: [
        "classical period piece soundtrack",
        "historical drama score",
        "baroque instrumental",
        "orchestral history"
    ],
    Genre.PHILOSOPHY: [
        "minimalist piano",
        "deep focus ambient",
        "contemplative instrumental",
        "brian eno ambient"
    ],
    Genre.MYSTERY: [
        "noir jazz instrumental",
        "detective movie soundtrack",
        "mysterious ambient",
        "sherlock holmes soundtrack"
    ]
}

def search_tracks(genre: Genre, limit: int = 6) -> List[dict]:
    """
    Searches iTunes for tracks fitting the literary genre.
    """
    try:
        # Pick a random query variation
        possible_queries = GENRE_TO_QUERIES.get(genre, ["cinematic score"])
        term = random.choice(possible_queries)
        
        params = {
            "term": term,
            "media": "music",
            "entity": "song",
            "limit": limit * 2
        }
        
        resp = requests.get(ITUNES_SEARCH_URL, params=params, timeout=10)
        resp.raise_for_status()
        
        results = resp.json().get("results", [])
        
        # Filter for longer tracks (background music)
        filtered_results = [
            t for t in results 
            if t.get("trackTimeMillis", 0) > 90000 # > 1.5 mins
        ]

        return [
            {
                "name": t.get("trackName"),
                "artist": t.get("artistName"),
                "url": t.get("trackViewUrl"),
                "preview_url": t.get("previewUrl")
            }
            for t in filtered_results[:limit]
        ]
    except Exception as e:
        print(f"iTunes API Error: {e}")
        return []