import sys, os
sys.path.append(os.path.abspath(''))
print(sys.path)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.controller.router import router as api_router
from api.controller import utils

from api.config import PROJECT_NAME, LOG_LEVEL
import uvicorn
import logging
from multiprocessing import freeze_support


def get_app() -> FastAPI:
    app = FastAPI(title=PROJECT_NAME, debug=True)

    app.add_middleware(
        CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
    )

    app.include_router(api_router)
    utils.initialize_existing_models()

    return app

print("INSIDE APP PY \n\n\n...\\n\n\n\n")
app = get_app()

# logging
logging.basicConfig(format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.info("Open http://127.0.0.1:8000/docs to see Swagger API Documentation.")

if __name__ == "__main__":
    freeze_support()
    uvicorn.run(app, host="0.0.0.0", port=8000)
    




