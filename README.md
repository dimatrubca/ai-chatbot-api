# AI-Chatbot-API

Rest API for document based question answering build with FastAPI, exposed by [Haystack](https://github.com/deepset-ai/haystack), adjusted and configured for [e-learning AIChatbot](https://github.com/Victor0120/ServerPBL) web application.


To serve the API, adjust the values in `rest_api/config.py` and run:

    gunicorn rest_api.application:app -b 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker -t 300

You will find the Swagger API documentation at
<http://127.0.0.1:8000/docs>
