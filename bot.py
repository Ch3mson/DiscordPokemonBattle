# This example requires the 'message_content' intent.

import discord
import logging
import logging.handlers
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# Setup logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logging.getLogger('discord.http').setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename='discord.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Create intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True # lets bot see all members

# Create the client
client = discord.Client(intents=intents)

# Define events
@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD) # from all guilds, take the name of guild we have as GUILD
    print(
        f'{client.user} is connected to the following guild:\n' # clients name
        f'{guild.name}(id: {guild.id})' # guilds name with ID
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')



# Run the client, suppressing the default logging configuration
client.run(token, log_handler=None)
