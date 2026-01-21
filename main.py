from fastapi import FastAPI, File, UploadFile, HTTPException
from utils.ocr import extract_text
from utils.sentiment import analyze_mood
from utils.music import search_tracks
from fastapi.staticfiles import StaticFiles          # <--- NEW IMPORT
from fastapi.responses import FileResponse

app = FastAPI(title="Mood2Music API")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")                                        # <--- NEW ROUTE
async def read_index():
    return FileResponse('static/index.html')

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    # ... (Keep existing code exactly the same) ...
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a JPEG or PNG.")

    image_bytes = await file.read()

    text = extract_text(image_bytes)
    mood = analyze_mood(text)
    tracks = search_tracks(mood)

    return {
        "status": "success",
        "ocr_text_preview": text[:100] + "..." if len(text) > 100 else text,
        "detected_mood": mood.value,
        "recommendations": tracks
    }

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    # 1. Validation
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a JPEG or PNG.")

    # 2. Read file
    image_bytes = await file.read()

    # 3. Pipeline Execution
    text = extract_text(image_bytes)
    mood = analyze_mood(text)
    tracks = search_tracks(mood)

    return {
        "status": "success",
        "ocr_text_preview": text[:100] + "..." if len(text) > 100 else text,
        "detected_mood": mood.value,
        "recommendations": tracks
    }

@app.post("/feedback")
async def feedback(track_id: str, liked: bool):
    # Placeholder for future reinforcement learning
    print(f"Feedback received: Track {track_id} is {'Liked' if liked else 'Disliked'}")
    return {"status": "recorded"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)