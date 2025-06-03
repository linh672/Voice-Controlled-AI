from chatbot_module.speech_to_text import recognize_speech
from chatbot_module.text_to_speech import speak_response
from chatbot import get_bot_response

def main():
    print("Sarah chatbot (Ollama + Voice) is ready! Say something or say 'exit' to quit.\n")
    while True:
        user_input = recognize_speech()
        if user_input.strip() == "":
            print(" Could not recognize speech. Please try again.")
            continue
        print(f"\n👤 You: {user_input}")
        if user_input.lower() in ["exit", "quit"]:
            print(" Goodbye!")
            break

        print("🤖 Bot: ", end="", flush=True)
        bot_reply = get_bot_response(user_input)
        print("\n")
        speak_response(bot_reply)

if __name__ == "__main__":
    main()
