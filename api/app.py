from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from api.controller import utils
from api.config import PROJECT_NAME, LOG_LEVEL
import uvicorn
import logging
from multiprocessing import freeze_support

logging.basicConfig(level=logging.INFO,  format='%(asctime)s:%(name)s:%(message)s', datefmt="%m/%d/%Y %I:%M:%S %p")
logger = logging.getLogger(__name__)

def get_app() -> FastAPI:
    app = FastAPI(title=PROJECT_NAME, debug=True)

    app.add_middleware(
        CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
    )

    utils.initialize_existing_models()

    return app

app = get_app()
from api.controller import routes


logger.info("Open http://127.0.0.1:8000/docs to see Swagger API Documentation.")

if __name__ == "__main__":
    freeze_support()
    uvicorn.run(app, host="0.0.0.0", port=8000)