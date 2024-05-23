from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message, app_commands, utils
import random
import asyncio
from difflib import SequenceMatcher

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)
tree = app_commands.CommandTree(client)

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

async def send_message(message, user_message):
    if not user_message:
        print('message was empty')
        return
    try:
        response = "la la la al la"
        await message.channel.send(response)
    except Exception as e:
        print(e)

# startup
@client.event
async def on_ready():
    print("now running")









@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    args = message.content.split()
    if len(args) == 0:
        return
    if args[0] != "!gm":
        return
    print(args)
    print(len(args))
    send_channel = message.channel
    scan_channel = message.channel
    if len(args) >= 2:
        scan_channel = utils.get(client.get_all_channels(), name=args[1])
        print("bingo")
    else:
         await send_channel.send("Did not specify channel! Will be guessing messages from #" + str(message.channel))


    await send_channel.send("Starting game...")
    messages = [message async for message in scan_channel.history(limit=1000)]


    #print(len(messages))
    index = random.randrange(0, len(messages))
    message_to_guess = messages[index]
    global correctGuesser
    correctGuesser = message.author
    def check(m):
        print("should be " + str(message_to_guess.author))
        print("guess " +  m.content)
        correctGuesser = m.author


        return (similar(m.content.lower(), str(message_to_guess.author).lower())) > 0.7 or similar(m.content.lower(), str(message_to_guess.author.display_name).lower()) > 0.7
    await message.channel.send("Who sent this: \n`" + message_to_guess.content +"`")
    try:
        msg = await client.wait_for("message", check=check, timeout=20.0)
        await send_channel.send(str(msg.author) + " got it right! It was " + str(message_to_guess.author.display_name)  + " ("  + str(message_to_guess.author) + ")\n " + message_to_guess.jump_url)
        await send_channel.send(message_to_guess.jump_url)
    except asyncio.TimeoutError:
        return await send_channel.send("Time's up! Message was sent by " + str(message_to_guess.author.display_name)  + " ("  + str(message_to_guess.author) + ")\n" + message_to_guess.jump_ur)
    

def main():
    client.run(token=TOKEN)

if __name__ == '__main__':
    main() 