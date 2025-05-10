import os
import multiprocessing
import uvicorn
from dotenv import load_dotenv

load_dotenv(override=True)

from facade_service import FACade as facade_app
from logging_service import logging_service
from messages_service import messages_service
from config_server import config_server

def run_facade():
    uvicorn.run(facade_app, host="0.0.0.0", port=int(os.getenv("FACADE_PORT")))

def run_logging(port: int):
    uvicorn.run(logging_service, host="0.0.0.0", port=port)

def run_messages():
    uvicorn.run(messages_service, host="0.0.0.0", port=int(os.getenv("MESSAGES_PORT")))

def run_config():
    uvicorn.run(config_server, host="0.0.0.0", port=int(os.getenv("CONFIG_SERVER_PORT")))

if __name__ == "__main__":
    ports = [
        int(os.getenv("LOGGING_PORT1")),
        int(os.getenv("LOGGING_PORT2")),
        int(os.getenv("LOGGING_PORT3")),
    ]

    processes = [
        multiprocessing.Process(target=run_config),
        multiprocessing.Process(target=run_facade),
        multiprocessing.Process(target=run_messages),
    ]
    # spawn all logging instances
    for p in ports:
        processes.append(multiprocessing.Process(target=run_logging, args=(p,)))

    for proc in processes:
        proc.start()
    for proc in processes:
        proc.join()
