import os
import streamlit as st
import re
from streamlit_chat import message
import anthropic
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
from groq import Groq
from langchain_groq import ChatGroq


# Streamlit setup
st.subheader("HELPDESK CHAT")

# Initialize session state variables
if 'responses' not in st.session_state:
    st.session_state['responses'] = ["Hi there! What can I assist you with today?"]
if 'requests' not in st.session_state:
    st.session_state['requests'] = []

# Initialize the language model
client = Groq(api_key="")
client1 = anthropic.Anthropic(api_key="")

# Functions for analysis and response generation
def generate_analysis(message):
    analysis = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {
                "role": "system",
                "content": """You are a Kannada query analyzer. For each query, detect and return only these parameters:
                                {
                                 "language_level": "formal/informal/technical",
                                 "context_type": "educational/business/general/technical",
                                 "cultural_elements": ["detected cultural references"],
                                 "technical_depth": "basic/intermediate/advanced",
                                 "regional_context": "identified Karnataka-specific elements"
                                 }
                                 Do not generate responses, only analyze query parameters."""
            },
            {
                "role": "user",
                "content": message
            }
        ],
        temperature=0.3,
        max_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )
    return analysis

def generate_response(query, analysis):
    message = client1.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=2000,
        temperature=0.3,
        messages=[
            {"role": "user", "content": f"""Original Query: {query}
                                            Query Analysis:
                                            {analysis}
                                         Please provide a response that:
                                         1. Matches the detected language level
                                         2. Incorporates relevant cultural elements
                                         3. Uses appropriate technical depth
                                         4. Includes regional context where relevant
                                        5. Maintains natural Kannada language flow"""}]
    )
    text_part = message.content[0].text if hasattr(message.content[0], 'text') else None
    return text_part

# Initialize conversation memory with last 3 messages
if 'buffer_memory' not in st.session_state:
    st.session_state.buffer_memory = ConversationBufferWindowMemory(k=3, return_messages=True)

link = 'meera11.jpg'

# Container for chat history
response_container = st.container()
# Container for text box
text_container = st.container()

# Input and response handling
with text_container:
    user_query = st.chat_input("Enter your query")

    if user_query:
        with st.spinner("typing..."):
            analysis = generate_analysis(user_query)
            response = generate_response(user_query, analysis)

        # Append the new query and response to the session state  
        st.session_state.requests.append(user_query)
        st.session_state.responses.append(response)

# Styling for chat
st.markdown(
    """
    <style>
    [data-testid="stChatMessageContent"] p{
        font-size: 1rem;
    }
    </style>
    """, unsafe_allow_html=True
)

# Display chat history
with response_container:
    if st.session_state['responses']:
        for i in range(len(st.session_state['responses'])):
            with st.chat_message('Momos', avatar=link):
                st.write(st.session_state['responses'][i])
            if i < len(st.session_state['requests']):
                message(st.session_state["requests"][i], is_user=True, key=str(i) + '_user')
