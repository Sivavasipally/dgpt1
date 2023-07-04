import streamlit as st
from datetime import datetime
import openai

# Set OpenAI API credentials
openai.api_key = "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"

# Define the conversation history
conversation = []

# Function to send user message to the AI model
def send_message(message):
    conversation.append({
        'role': 'user',
        'message': message,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    response = openai.Completion.create(
        engine="davinci",
        prompt=message,
        max_tokens=50,
        temperature=0.7,
        n=1,
        stop=None,
        top_p=None,
        frequency_penalty=None,
        presence_penalty=None
    )
    conversation.append({
        'role': 'assistant',
        'message': response.choices[0].text.strip(),
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

# Set page title and layout
st.title("Chat with AI Assistant")
st.markdown("---")

if 'user_input' not in st.session_state:
    st.session_state['user_input'] = ''

# Get user input message
user_input = st.text_input("You", value="", max_chars=500)

# Send user message when Enter key is pressed
if st.button("Send") or (user_input and st.session_state.user_input != user_input):
    st.session_state.user_input = user_input
    send_message(user_input)
    st.text_area("AI Assistant", value=conversation[-1]['message'], height=100, max_chars=500, key='output')

# Display conversation history
st.markdown("---")
st.subheader("Conversation History")
for message in conversation:
    role = message['role']
    timestamp = message['timestamp']
    message_text = message['message']
    st.markdown(f"**{role.capitalize()}** ({timestamp}): {message_text}")
