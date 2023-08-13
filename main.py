import streamlit as st
import os
import openai
from llama_index import VectorStoreIndex, SimpleDirectoryReader, LLMPredictor, ServiceContext, PromptHelper, download_loader
from llama_index.query_engine import CitationQueryEngine
from llama_index.response.schema import Response, StreamingResponse
from langchain.chat_models import ChatOpenAI

# Get user input
user_input = st.chat_input("Ask Something...")

# Initialize chat history in session state if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# If the user has entered a message
if user_input is not None:
    # Add user's message to chat history
    st.session_state['chat_history'].append(('User', user_input))
    
    os.environ["OPENAI_API_KEY"] = st.secrets["API_KEY"]
    documents = SimpleDirectoryReader('data').load_data()
    llm_predictor = LLMPredictor(
    llm=ChatOpenAI(temperature=0, model_name="gpt-3.5"))
      
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor,
                                                   chunk_size=500)
    
    index = VectorStoreIndex.from_documents(documents,
                                            service_context=service_context)
    
    query_engine = index.as_query_engine()
    history = st.session_state['chat_history']
    responselmp = query_engine.query(f"You are an Assistant. You need to sell and answer questions about certain products provided in your enchanced data. Keep your responses short and with only the most important information. Stay only on the topic of your task! Politely decline other requests. This is your history: \n {history} \n Use it to answer questions better based on your previous conversation with the user. If the history is blanc then the conversation only started. \n This is your question: {user_input}")


    # Generate a response
    response = f"{responselmp}"

    # Add chatbot's response to chat history
    st.session_state['chat_history'].append(('Assistant', response))

# Display the chat history
for name, message in st.session_state['chat_history']:
    with st.chat_message(name):
        st.write(message)

