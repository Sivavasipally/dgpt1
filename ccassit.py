import openai
import yaml
import speech_recognition as sr
from gtts import gTTS
import os

## OPENAI API CONNECTION
## ---------------------------------------------------------------------------------------------------------------------
# Loading the API key and organization ID from file (NOT pushed to GitHub)
with open('openai-keys.yaml') as f:
    keys_yaml = yaml.safe_load(f)
# Set your OpenAI API key here
api_key = keys_yaml['API_KEY']
openai.api_key = api_key

def get_gpt3_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",  # GPT-3.5 engine
        prompt=prompt,
        max_tokens=150  # Maximum number of tokens in the response
    )
    return response.choices[0].text.strip()

# Test the function
#user_input = "Hello, CCASIST!"
#response = get_gpt3_response(user_input)
#print("CCASIST:", response)
def listen_to_user():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        user_input = recognizer.recognize_google(audio)
        print("You:", user_input)
        return user_input
    except sr.UnknownValueError:
        print("CCASIST could not understand your speech.")
        return ""
    except sr.RequestError:
        print("There was a problem with the speech recognition service.")
        return ""

def speak(response_text):
    tts = gTTS(text=response_text, lang='en')
    tts.save('response.mp3')
    os.system('start response.mp3')

# Main loop for CCASIST
while True:
    user_input = listen_to_user()
    if user_input.lower() == 'exit':
        print("CCASIST: Goodbye!")
        break

    response = get_gpt3_response(user_input)
    print("CCASIST:", response)
    speak(response)
