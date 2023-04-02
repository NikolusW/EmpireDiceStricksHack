import openai
import config

openai.api_key = config.api_key_open_ai

messages = [{"role": "system", "content": "You are a Dungeon Master for a star wars themed Dungeons and Dragons like game. First ask the players for some general information on the players. After that, you will decribe a scenario and allow the players to respond with what they want to do, and you will ask them to roll when needed, and tell the player when a roll is expected. Only respond as the DM, allow me to respond as the players"}]

def CustomChatGPT(user_input):
    messages.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages
    )
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply
def OpeningMessage(user_names,user_descriptions):
    message = "there are " + str(len(user_names)) + " players."
    for name, description in zip(user_names, user_descriptions):
        message = message + name + ", who has the following description:" + description + "."
    message = message + " Generate a starting scenario for our charaters."
    return(CustomChatGPT(message))