from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.controller.router import router as api_router

import uvicorn
import logging


def get_application() -> FastAPI:
    app = FastAPI(title='AI-Chatbot-API', debug=True)

    app.add_middleware(
        CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
    )

    app.include_router(api_router)

    return app

app = get_application()

# logging
logging.basicConfig(format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.info("Open http://127.0.0.1:8000/docs to see Swagger API Documentation.")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    




