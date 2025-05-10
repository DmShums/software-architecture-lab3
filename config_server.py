import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

config_server = FastAPI()

SERVICE_REGISTRY = {
    "logging-service": [
        f"http://127.0.0.1:{os.getenv('LOGGING_PORT1')}/logging-service",
        f"http://127.0.0.1:{os.getenv('LOGGING_PORT2')}/logging-service",
        f"http://127.0.0.1:{os.getenv('LOGGING_PORT3')}/logging-service",
    ],
    "message-service": [
        f"http://127.0.0.1:{os.getenv('MESSAGES_PORT')}/message"
    ],
}

class InstancesResponse(BaseModel):
    instances: List[str]

@config_server.get("/services/{service_name}", response_model=InstancesResponse)
def get_instances(service_name: str):
    """
    Return a list of base-URLs for all running instances
    of the requested service.
    """
    if service_name not in SERVICE_REGISTRY:
        raise HTTPException(status_code=404, detail="Service not found")
    return InstancesResponse(instances=SERVICE_REGISTRY[service_name])
