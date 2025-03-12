from fastapi import FastAPI
from pydantic import BaseModel
import uuid
import httpx
import random
import asyncio

facade_service = FastAPI()

class RequestModel(BaseModel):
    text: str

class FacadeController:
    """Facade controller class"""
    logging_service_urls = [
        "http://127.0.0.1:8002/logging-service",
        "http://127.0.0.1:8003/logging-service",
        "http://127.0.0.1:8004/logging-service"
    ]

    @facade_service.post("/facade-service")
    async def post_request(data: RequestModel):
        new_uuid = str(uuid.uuid4())
        message = {"id": new_uuid, "text": data.text}

        fall_back_ctr = 0
        async with httpx.AsyncClient() as client:
            while fall_back_ctr < len(FacadeController.logging_service_urls):
                try:
                    selected_service = random.choice(FacadeController.logging_service_urls)
                    response = await client.post(selected_service, json=message)
                    response.raise_for_status()
                    return {"status": "Message logged", "message_id": new_uuid}
                except httpx.RequestError as e:
                    print(f"Request to {selected_service} failed: {e}")
                    fall_back_ctr += 1
                    await asyncio.sleep(1)

        return {"error": "All logging services are unavailable."}

    @facade_service.get("/facade-service")
    async def get_request():
        fall_back_ctr = 0
        async with httpx.AsyncClient() as client:
            while fall_back_ctr < len(FacadeController.logging_service_urls):
                try:
                    selected_service = random.choice(FacadeController.logging_service_urls)
                    logging_response = await client.get(selected_service)
                    logging_response.raise_for_status()
                    return logging_response.json()
                except httpx.RequestError as e:
                    print(f"Request to {selected_service} failed: {e}")
                    fall_back_ctr += 1
                    await asyncio.sleep(1)

        return {"error": "All logging services are unavailable."}