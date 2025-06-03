
import pyttsx3

#Text to speech
def speak_response(chatbot_response):
    chatbot = pyttsx3.init()
    voices = chatbot.getProperty('voices')
    chatbot.setProperty('voice', voices[1].id)
    chatbot.say(chatbot_response)
    chatbot.runAndWait()
