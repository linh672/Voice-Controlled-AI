from openai import OpenAI

client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama'  
)

chat_history = [
    {"role": "system", "content": "You are a helpful assistant."}
]

def get_bot_response(user_message: str) -> str:
    chat_history.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="gemma3:4b",
        stream=True,
        messages=chat_history,
    )

    bot_reply = ""
    for chunk in response:
        content = chunk.choices[0].delta.content or ""
        bot_reply += content
        print(content, end="", flush=True)

    chat_history.append({"role": "assistant", "content": bot_reply})
    return bot_reply


    