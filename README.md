
## Langchain Conversational Retrieval System
Langchain is a language model-powered conversational retrieval system. It leverages the GPT-35-Turbo model by OpenAI, the Chroma vector store, and Flask for API serving.

The system uses a Flask server for front-end communication, which interfaces with an OpenAI powered backend that conducts a conversational retrieval process using Azure.

## Prerequisites
To run the Langchain system, you will need to have Python 3.7 or later installed on your computer. You will also need the following Python libraries: os, dotenv, Flask, CORS, openai, and several Langchain proprietary modules. Install the necessary dependencies via pip using:


pip install -r requirements.txt
Also, make sure you have an Azure account, as well as access to OpenAI's GPT-35-Turbo and Ada's Text Embedding services.

## Configuration
Before running the application, you need to configure some environment variables. Create a .env file in your project's root directory and add the following variables:

OPENAI_API_BASE = "Your OpenAI API base"
AZ_OPENAI_API_KEY = "Your Azure OpenAI Key"
Remember to replace "Your OpenAI API base" and "Your Azure OpenAI Key" with your actual values.

## Project Structure
The project is organized as follows:

Import the necessary modules and libraries.
Load environment variables (OPENAI_API_BASE and AZ_OPENAI_API_KEY) from the .env file.
Configure OpenAI API settings.
Initialize OpenAI models and embedding service.
Load Chroma Vectorstore from the 'db' directory.
Set up the conversational retrieval chain.
Create a Flask application and configure CORS.
Define the Flask application routes, including index, data (for POST request handling), and clear (for clearing chat history).
Usage
To start the application, run:
python main.py

Once the server is running, you can navigate to  http://127.0.0.1:5000 in your web browser to view the application.

The following endpoints are available:

GET /: Returns the index.html home page.
POST /data: Accepts a JSON payload containing a 'data' field, which is the question to ask the language model. Returns a JSON response containing the answer.
POST /clear: Clears the chat history for the current session.

## Notes
Do not forget to provide your own secret key in the Flask app configuration.
Adjust the search_kwargs argument to the as_retriever method as necessary to modify the behavior of the search (e.g., the number of results to consider).
Make sure to properly handle the session data and clear chat history as needed.

