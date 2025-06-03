import sys
import threading
import time
import asyncio
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
from chatbot_module.speech_to_text import recognize_speech
from chatbot_module.text_to_speech import speak_response
from chatbot import get_bot_response
from chatbot_module.basic_module import get_local_time, get_weather
import server
import uvicorn

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chatbot UI")
        self.showFullScreen()
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)
        self.browser.load(QUrl("http://127.0.0.1:8000/static/chatbot_ui.html"))

def run_server():
    uvicorn.run(server.app, host="127.0.0.1", port=8000)

def pulse_event():
    asyncio.run(server.send_pulse_event())

def main(app, window):
    print("Chatbot is ready! Say goodbye or say 'exit' to quit.\n")

    while True:
        user_input = recognize_speech()
        pulse_event()

        if user_input.strip() == "":
            print(" Could not recognize speech. Please try again.")
            continue

        print(f"\n👤 You: {user_input}")


        if "what time is it" in user_input or 'what date is it today' in user_input:
            if 'in' in user_input:
                city = user_input.split('in')[-1].strip()
                try:
                    time, date_today = get_local_time(city)
                    if 'time' in user_input:
                        print(f"🤖 Bot: The current time in {city} is {time}")
                        pulse_event()
                        speak_response(f"The current time in {city} is {time}")
                    elif 'date' in user_input:
                        print(f"🤖 Bot: Today in {city} is {date_today}")
                        pulse_event()
                        speak_response (f"Today in {city} is {date_today}")
                except:
                    print("🤖 Bot: Sorry, I couldn't find that city. Please try again.")
                    pulse_event()
                    speak_response("Sorry, I couldn't find that city. Please try again.")
            else:
                print("🤖 Bot: Please specify a city for the time or date.")
                pulse_event()
                speak_response("Please specify a city for the time or date.")
        elif 'how is the weather today' in user_input or 'what is the weather today' in user_input:
            # Extract city name from recognized text
            if 'in' in user_input:
                city = user_input.split('in')[-1].strip()
                if city:
                    print(f"🤖 Bot: {asyncio.run(get_weather(city))}")
                    pulse_event()
                    speak_response(asyncio.run(get_weather(city)))
                else:
                    print("🤖 Bot: Please tell me the name of the city.")
                    pulse_event
                    speak_response("Please tell me the name of the city.")
            else:
                print("🤖 Bot: Please specify a city for the weather.")
                pulse_event
                speak_response("Please specify a city for the weather.")

        elif user_input.lower() in ["exit", "quit", 'goodbye']:
            print("🤖 Bot: Goodbye, have a nice day!")
            pulse_event()
            speak_response("Goodbye, have a nice day!")
            # Close the PyQt window and quit the app
            window.close()
            app.quit()
            break

        else:
            bot_reply = get_bot_response(user_input)
            pulse_event()
            speak_response(bot_reply)

if __name__ == "__main__":
    # Start FastAPI server in a background thread
    threading.Thread(target=run_server, daemon=True).start()
    time.sleep(1)  # wait for server to start

    app = QApplication(sys.argv)
    window = BrowserWindow()
    window.show()

    # Run your chatbot voice loop in a separate thread to keep UI responsive
    threading.Thread(target=main, args=(app, window), daemon=True).start()

    sys.exit(app.exec())


