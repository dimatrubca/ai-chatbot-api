# AI-Chatbot-API

API for document based question answering build with FastAPI, exposed by [Haystack](https://github.com/deepset-ai/haystack) AI framework, adjusted and configured for [e-learning AIChatbot](https://github.com/Victor0120/ServerPBL) web application.


To serve the API, adjust the values in `api/config.py` and run:

      uvicorn api.app:app -host 0.0.0.0:8000 --port 8000

You will find the Swagger API documentation at
<http://127.0.0.1:8000/docs>

## Usage
-	Create a new document question answering model
-	Load a document for a specific model (supported formats: .pdf / .txt)
-	Query the doc-qa model
-	Create a new faq question answering model
-	Load a predefined question-answer
-	Query the faq-qa model
-	Delete a model by id

To use the API you have to have elasticsearch installed. 

### Another Project components</br>
Backend repository: https://github.com/Victor0120/ServerPBL</br>
Frontend repository:  https://github.com/encodedemotions/pbl

## Screenshots
<img src="https://user-images.githubusercontent.com/32422633/115343876-34af7a80-a1b5-11eb-89d2-a588d1330916.png" width="750"></br>
[Fig. 1 Example questions-answers ]

<img src="https://user-images.githubusercontent.com/32422633/115344208-b6070d00-a1b5-11eb-89dd-036edf3745d2.png" width="650"></br>
[Fig. 2 Document with answer highlighted ]

Project demo video: [link](https://drive.google.com/file/d/1duShq7cm-lRRRz04AV5zD5zmtTtHa9MX/view?usp=sharing)
