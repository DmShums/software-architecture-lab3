"""runner script"""

import uvicorn
import multiprocessing
import os
import hazelcast

from facade_service import facade_service
from logging_service import logging_service
from messages_service import messages_service

FACADE_PORT = 8000
MESSAGES_PORT = 8001
LOGGING_PORT1 = 8002
LOGGING_PORT2 = 8003
LOGGING_PORT3 = 8004

def run_facade_service():
    uvicorn.run(facade_service, host="0.0.0.0", port=FACADE_PORT)

def run_logging_service(port):
    uvicorn.run(logging_service, host="0.0.0.0", port=port)

def run_messages_service():
    uvicorn.run(messages_service, host="0.0.0.0", port=MESSAGES_PORT)

if __name__ == "__main__":
    process1 = multiprocessing.Process(target=run_facade_service)
    process2 = multiprocessing.Process(target=run_messages_service)
    process3 = multiprocessing.Process(target=run_logging_service, args=(LOGGING_PORT1,))
    process4 = multiprocessing.Process(target=run_logging_service, args=(LOGGING_PORT2,))
    process5 = multiprocessing.Process(target=run_logging_service, args=(LOGGING_PORT3,))

    process1.start()
    process2.start()
    process3.start()
    process4.start()
    process5.start()

    process1.join()
    process2.join()
    process3.join()
    process4.join()
    process5.join()