import server
import asyncio
from chatbot_module.text_to_speech import speak_response

def full_response(chatbot_response):
    print(f"🤖 Bot: {chatbot_response}")
    asyncio.run(server.send_pulse_event())
    speak_response(chatbot_response)
