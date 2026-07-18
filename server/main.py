import os
from fastapi import FastAPI, Request, HTTPException
from dotenv import load_dotenv
import httpx
import redis
import uuid
import time
import json
import threading
import asyncio

load_dotenv()

app = FastAPI()

rds = redis.Redis(decode_responses=True)

QUEUE_KEY="pqueue:prompts"

PRIORITY_HIGH = 10
PRIORITY_NORMAL = 5
PRIORITY_LOW = 1

VLLM_BASE_URL = os.getenv("VLLM_BASE_URL")
VLLM_API_KEY = os.getenv("VLLM_API_KEY")

vllm_url = f"{VLLM_BASE_URL}/v1/chat/completions"
http_headers = { "Authorization": f"Bearer {VLLM_API_KEY}"}

def enqueue(payload: dict, priority:int = PRIORITY_NORMAL) -> str:
    job_id = str(uuid.uuid4())
    job = {**payload, "id": job_id, "enqueue_at": time.time(), "priority": priority}
    score = (20 - priority) * 1e12 + time.time()

    rds.zadd(QUEUE_KEY, {json.dumps(job, sort_keys=True): score})
    return job_id

def dequeue() -> dict | None:
    results = rds.zpopmin(QUEUE_KEY, count=1)
    if not results:
        return None
    raw, score = results[0]
    return json.loads(raw)

def blocking_worker():
    print("Priority worker started...")
    while True:
        result = rds.bzpopmin(QUEUE_KEY, timeout=5)
        if result is None:
            continue
        _, raw, score = result
        job = json.loads(raw)
        print(f"Processing job {job['id']} with priority {job['priority']}")
    
        try:
            response = asyncio.run(process_job(job))
            rds.set(f"result:{job['id']}", json.dumps(response))
        
        except httpx.HTTPError as error:
            raise HTTPException(status_code=500, detail=str(error))

async def process_job(job_body: dict):
    try:
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(vllm_url, json=job_body, headers=http_headers)

            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as error:
        raise HTTPException(status_code=500, detail=str(error))

t = threading.Thread(target=blocking_worker, daemon=True)
t.start()

@app.get("/")
def read_root():
    return {"status": "success", "message": "FastAPI is running!"}

@app.post("/v1/chat")
async def chat_handler(request: Request):
    if not VLLM_BASE_URL:
        raise HTTPException(status_code=500, detail="VLLM_BASE_URL environment variable not set")
    elif not VLLM_API_KEY:
        raise HTTPException(status_code=500, detail="VLLM_API_KEY environment variable not set")
    try:
        body = await request.json()
        enqueued_job = enqueue(body)
        return { "job_id": enqueued_job, "status": "queued" }
    
    except httpx.HTTPError as error:
        raise HTTPException(status_code=500, detail=str(error))
    
@app.get("/v1/jobs/{job_id}")
def get_jobs(job_id: str):
    try:
        found_jobs = rds.get(f"result:{job_id}")

        if found_jobs is None:
            return { "status": "pending" }
        else:
            return json.loads(found_jobs)
    except:
        raise HTTPException(status_code=500, detail=f"Failed to fetch job: {job_id}")