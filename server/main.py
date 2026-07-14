import os
from fastapi import FastAPI, Request, HTTPException
from dotenv import load_dotenv
import httpx

load_dotenv()

app = FastAPI()

VLLM_BASE_URL = os.getenv("VLLM_BASE_URL")
VLLM_API_KEY = os.getenv("VLLM_API_KEY")

@app.get("/")
def read_root():
    return {"status": "success", "message": "FastAPI is running!"}

@app.post("/v1/chat/completions")
async def chat_completion(request: Request):
    if not VLLM_BASE_URL:
        raise HTTPException(status_code=500, detail="VLLM_BASE_URL environment variable not set")
    elif not VLLM_API_KEY:
        raise HTTPException(status_code=500, detail="VLLM_API_KEY environment variable not set")
    
    body = await request.json()

    vllm_url = f"{VLLM_BASE_URL}/v1/chat/completions"
    http_headers = { "Authorization": f"Bearer {VLLM_API_KEY}"}
    
    try:
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(vllm_url, json=body, headers=http_headers)
            
            response.raise_for_status()
            return response.json()
        
    except httpx.HTTPError as error:
        raise HTTPException(status_code=500, detail=str(error))