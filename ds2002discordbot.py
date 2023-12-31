# Talked to Professor prior and he said that we could have a group of three.
# Ashley Luk, Emily Brown, and Angela Hong are in this group (group 8).

import discord
import time
import os
from discord.ext import commands
# you will pip install ---> pip install openai==0.28
import openai
from dotenv import load_dotenv



load_dotenv()


# # You  pip install python-dotenv (this is fulfilled)
# Initialize variables for chat history
explicit_input = ""
chatgpt_output = 'Chat log: /n'
cwd = os.getcwd()
i = 1

# Find an available chat history file
while os.path.exists(os.path.join(cwd, f'chat_history{i}.txt')):
    i += 1

history_file = os.path.join(cwd, f'chat_history{i}.txt')

# Create a new chat history file
with open(history_file, 'w') as f:
    f.write('\n')

# Initializing chat history
chat_history = ''

# OPEN AI STUFF
# We put our key in a .env File and grabbing it here
openai.api_key = os.getenv("OPENAI_API_KEY")

name = 'Weather Man'

# Defining the role of the bot
role = 'customer service'
with open('WLSeattle.csv', 'r') as data_file:
    # Reading the contents of the file into a string variable
    file_contents = data_file.read()

#Here is a description of the role
impersonated_role = f"""
    You will act as {name}. Your role is {role}.
    You will reply to all requests using news reporting slang.
    You will be informed by the CSV data here: {file_contents}"""


# Function to complete chat input using OpenAI's GPT-3.5 Turbo
def chatcompletion(user_input, impersonated_role, explicit_input, chat_history):
    output = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        temperature=1,
        presence_penalty=0,
        frequency_penalty=0,
        max_tokens=2000,
        messages=[
            {"role": "system", "content": f"{impersonated_role}. Conversation history: {chat_history}"},
            {"role": "user", "content": f"{user_input}. {explicit_input}"},
        ]
    )

    for item in output['choices']:
        chatgpt_output = item['message']['content']

    return chatgpt_output


# Function to handle user chat input
def chat(user_input):
    global chat_history, name, chatgpt_output
    current_day = time.strftime("%d/%m", time.localtime())
    current_time = time.strftime("%H:%M:%S", time.localtime())
    chat_history += f'\nUser: {user_input}\n'
    chatgpt_raw_output = chatcompletion(user_input, impersonated_role, explicit_input, chat_history).replace(f'{name}:',
                                                                                                             '')
    chatgpt_output = f'{name}: {chatgpt_raw_output}'
    chat_history += chatgpt_output + '\n'
    with open(history_file, 'a') as f:
        f.write(
            '\n' + current_day + ' ' + current_time + ' User: ' + user_input + ' \n' + current_day + ' ' + current_time + ' ' + chatgpt_output + '\n')
        f.close()
    return chatgpt_raw_output


# DISCORD STUFF

intents = discord.Intents().all()
client = commands.Bot(command_prefix="!", intents=intents)


@client.event
async def on_ready():
    print("Bot is ready")


@client.command()
async def hi(ctx):
    await ctx.send("Hello, nothing to see here")


responses = 0
list_user = []




@client.event
async def on_message(message):
    global chat_history
    #we were trying to make sure chat_history was empty here
    print(message.content)
    if message.author == client.user:
        return
    print(message.author)
    print(client.user)
    print(message.content)
    chat_history =''
    answer = chat(message.content)
    print("Weather Man Says:" + answer)

    await message.channel.send(answer)


@client.command()
@commands.is_owner()
async def shutdown(context):
    exit()

TOKEN = os.getenv('DISCORD_TOKEN')
client.run(TOKEN)