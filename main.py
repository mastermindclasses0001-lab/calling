from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import edge_tts
import asyncio

app = FastAPI()

# Cross-Origin (CORS) allow karna taaki Chrome isko access kar sake
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/tts")
async def get_tts(text: str):
    # 'hi-IN-SwaraNeural' ekdam natural ladki ki aawaz hai
    communicate = edge_tts.Communicate(text, "hi-IN-SwaraNeural")
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    
    return Response(content=audio_data, media_type="audio/mp3")

@app.get("/")
def home():
    return {"message": "TTS Server is Running!"}