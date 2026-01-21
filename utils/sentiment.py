from enum import Enum
from transformers import pipeline

# Load a Zero-Shot Classification pipeline
# This allows us to define our own custom labels (Genres)
classifier_pipe = pipeline(
    "zero-shot-classification",
    model="valhalla/distilbart-mnli-12-1"  # ~350MB, fast and accurate
)

class Genre(Enum):
    FANTASY = "fantasy"
    SCIFI = "science fiction"
    ROMANCE = "romance"
    HORROR = "horror"
    THRILLER = "thriller"
    HISTORY = "history"
    PHILOSOPHY = "philosophy"
    MYSTERY = "mystery"

def analyze_genre(text: str) -> Genre:
    """
    Classifies text into a literary genre using Zero-Shot Learning.
    """
    if not text or len(text.strip()) < 5:
        return Genre.PHILOSOPHY # Default fallback

    # Define the candidate labels (the genres we want to detect)
    candidate_labels = [e.value for e in Genre]

    # Run the classification
    # We truncate to 512 chars because that's usually enough to guess the genre
    result = classifier_pipe(text[:512], candidate_labels)
    
    # The result contains labels sorted by score. Take the top one.
    top_label = result['labels'][0]
    
    return Genre(top_label)