import os
import uuid
import random
import asyncio

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
from dotenv import load_dotenv

load_dotenv(override=True)

FACade = FastAPI()

CONFIG_SERVER_URL = os.getenv("CONFIG_SERVER_URL", "http://127.0.0.1:8005")

class RequestModel(BaseModel):
    text: str

async def fetch_instances(service_name: str) -> list[str]:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{CONFIG_SERVER_URL}/services/{service_name}")
        resp.raise_for_status()
        return resp.json()["instances"]

@FACade.post("/facade-service")
async def post_request(data: RequestModel):
    new_uuid = str(uuid.uuid4())
    payload = {"id": new_uuid, "text": data.text}

    # Discover all logging-service instances
    try:
        instances = await fetch_instances("logging-service")
    except httpx.HTTPError:
        raise HTTPException(503, "Config-server unavailable")

    # Shuffle for basic load-balancing
    for url in random.sample(instances, len(instances)):
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(url, json=payload, timeout=2.0)
                resp.raise_for_status()
                return {"status": "Message logged", "message_id": new_uuid}
        except httpx.RequestError:
            # could log here: f"Failed to reach {url}"
            await asyncio.sleep(1)

    raise HTTPException(503, "All logging instances unreachable")

@FACade.get("/facade-service")
async def get_request():
    # Discover logging instances
    try:
        instances = await fetch_instances("logging-service")
    except httpx.HTTPError:
        raise HTTPException(503, "Config-server unavailable")

    for url in random.sample(instances, len(instances)):
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(url, timeout=2.0)
                resp.raise_for_status()
                logs = resp.json()
                # Now get the static message
                msg_instances = await fetch_instances("message-service")
                msg_url = random.choice(msg_instances)
                msg_resp = await client.get(msg_url, timeout=2.0)
                msg_resp.raise_for_status()
                return {
                    "logged_messages": logs.get("messages") or logs,
                    "message": msg_resp.json()["message"],
                }
        except httpx.RequestError:
            await asyncio.sleep(1)

    raise HTTPException(503, "All logging instances unreachable")
