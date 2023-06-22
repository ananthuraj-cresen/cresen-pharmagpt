import os
import openai
from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from flask import session

# Load environment variables (set OPENAI_API_KEY and OPENAI_API_BASE in .env)
load_dotenv()

# Configure OpenAI API
openai.api_type = "azure"
openai.api_version = "2023-03-15-preview"
#openai.api_base = "https://cresen-open-ai.openai.azure.com/"    #os.getenv('OPENAI_API_BASE')
#openai.api_key = "70cfad14bc804b44a3b2b294e98ddbe6"     #os.getenv("AZ_OPENAI_API_KEY")

# Initialize gpt-35-turbo and our embedding model
llm = AzureChatOpenAI(deployment_name="cresen-gpt-35-turbo", openai_api_version="2023-03-15-preview", openai_api_key = "70cfad14bc804b44a3b2b294e98ddbe6", openai_api_base = "https://cresen-open-ai.openai.azure.com/") # For Chat
embeddings = OpenAIEmbeddings(model='text-embedding-ada-002', deployment='text-embedding-ada-002', chunk_size=1, openai_api_key = "70cfad14bc804b44a3b2b294e98ddbe6", openai_api_base = "https://cresen-open-ai.openai.azure.com/") # For Embeddings

# Load vectorstore
persist_directory = 'db'
vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
#vectorstore.persist()

# Set up retrieval chain
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
qa = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever)

app = Flask(__name__)
# Set the secret key for the Flask app
app.config['SECRET_KEY'] = 'POnNOsbdnqxyimIft/oCUMwEowQr9kAW'
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['POST'])
def get_data():
    data = request.get_json()
    question = data.get('data')
    
    # Get this session's chat history, or an empty list if this is a new session
    chat_history = session.get('chat_history', [])
    
    response = qa({"question": question, "chat_history": chat_history})
    answer = response['answer']
    chat_history.append((question, answer))
    
    # Store the updated chat history in this session
    session['chat_history'] = chat_history
    
    return jsonify({"response": True, "message": answer})

@app.route('/clear', methods=['POST'])
def clear_chat():
    # Clear the chat history for this session
    session['chat_history'] = []
    return jsonify({"response": True})


if __name__ == '__main__':
    app.run()
