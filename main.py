from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message, app_commands, utils, Embed
import asyncio
from difflib import SequenceMatcher
import random
from datetime import timedelta
from random import randrange

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)
tree = app_commands.CommandTree(client)

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")

def random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    args = message.content.split()
    if len(args) == 0:
        return
    if args[0] != "!gm":
        return

    send_channel = message.channel
    scan_channel = message.channel
    if len(args) >= 2:
        scan_channel = utils.get(client.get_all_channels(), name=args[1])
    else:
        await send_channel.send("Did not specify channel! Will be guessing messages from #" + str(message.channel))
        
    recent = False
    if "recent" in args:
        recent = True
        await send_channel.send("Selecting from recent messages!")
    else:
        await send_channel.send("Selecting from all time messages!")

        
    await send_channel.send("Starting game...")
    
    
    # pick message
    
    try:
        first_message_date = [message async for message in scan_channel.history(limit=1, oldest_first=True)][0].created_at
        last_message_date = [message async for message in scan_channel.history(limit=1, oldest_first=False)][0].created_at
    except:
        await send_channel.send("Did not have access to channel #" + str(args[1]))
        return


    
    if not recent:
        messages = [message async for message in scan_channel.history(limit=100, around=random_date(first_message_date, last_message_date))]
    else:
        messages = [message async for message in scan_channel.history(limit=1000)]
    def pick():
        index = random.randrange(0, len(messages))
        message_to_guess = messages[index]

        if message_to_guess.embeds:
            return pick()
        return message_to_guess

    def check(m):
        print("should be " + str(message_to_guess.author))
        print("guess " +  m.content)
        correctGuesser = m.author


        return (similar(m.content.lower(), str(message_to_guess.author).lower())) > 0.7 or similar(m.content.lower(), str(message_to_guess.author.display_name).lower()) > 0.7
    
    message_to_guess = pick()

    embed = Embed(title="Who sent this?")
    if message_to_guess.attachments:
        embed.set_image(url=message_to_guess.attachments[0].url)
    elif message_to_guess.embeds:
        embed.description = message_to_guess.embeds[0].description
        if message_to_guess.embeds[0].image:
            embed.set_image(url=message_to_guess.embeds[0].image.url)
    else:
        embed.description = message_to_guess.content
    
    await send_channel.send(embed=embed)
    try:
        msg = await client.wait_for("message", check=check, timeout=15.0)
        response_embed = Embed(title=str(msg.author) + " got it right!")
        response_embed.description = "It was " + str(message_to_guess.author.display_name)  + " ("  + str(message_to_guess.author) + ")\n\n" + message_to_guess.jump_url
        await send_channel.send(embed=response_embed)
    except asyncio.TimeoutError:
        response_embed = Embed(title="Time's Up!") 
        response_embed.description =  "Message was sent by " + str(message_to_guess.author.display_name)  + " ("  + str(message_to_guess.author) + ")\n\n" + message_to_guess.jump_url
        return await send_channel.send(embed=response_embed)
    

def main():
    client.run(token=TOKEN)

if __name__ == '__main__':
    main() 