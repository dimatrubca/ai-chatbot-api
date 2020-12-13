# AI-Chatbot-API

Rest API for document based question answering build with FastAPI, exposed by [Haystack](https://github.com/deepset-ai/haystack) AI framework, adjusted and configured for [e-learning AIChatbot](https://github.com/Victor0120/ServerPBL) web application.


To serve the API, adjust the values in `api/config.py` and run:

      uvicorn api.app:app -host 0.0.0.0:8000 --port 8000

You will find the Swagger API documentation at
<http://127.0.0.1:8000/docs>
