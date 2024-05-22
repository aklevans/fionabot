from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message, app_commands
import random

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)
tree = app_commands.CommandTree(client)

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

# Add the guild ids in which the slash command will appear.
# If it should be in all, remove the argument, but note that
# it will take some time (up to an hour) to register the
# command if it's for all guilds.
@tree.command(
    name="scan",
    description="My first application Command",
)
async def first_command(interaction):

    messages = [message async for message in interaction.channel.history(limit=100)]
    index = random.randrange(0, len(messages))
    message = messages[index]
    def check(m):
        return True
        if message.author == m.content:
            return True
        return False
    await interaction.response.send_message("Who sent this: \n" + message.content)
    msg = await client.wait_for("message", check=check)
    await interaction.response.send_message("YES")




@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content[0:2] != "!g":
        return
    username = str(message.author)
    user_message = message.content
    channel = message.channel

    messages = [message async for message in channel.history(limit=None)]
    print(len(messages))
    index = random.randrange(0, len(messages))
    message2 = messages[index]
    def check(m):
        print("should be " + str(message2.author))
        print("guess " +  m.content)
        if  m.content in str(message2.author):
            return True
        return False
    await channel.send("Who sent this: \n" + message.content)
    msg = await client.wait_for("message", check=check)
    await channel.send("YES")

def main():
    client.run(token=TOKEN)

if __name__ == '__main__':
    main() 