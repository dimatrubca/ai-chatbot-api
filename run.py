import uvicorn
from api.app import app

uvicorn.run(app, port=8080, host='0.0.0.0')