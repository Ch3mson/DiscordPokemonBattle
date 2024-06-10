import discord
import random
import logging
import logging.handlers
from dotenv import load_dotenv
from discord.ext import commands
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
intents.members = True  # lets bot see all members

# Create the bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Define events
@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)  # from all guilds, take the name of guild we have as GUILD
    print(
        f'{bot.user} is connected to the following guild:\n'  # bot's name
        f'{guild.name}(id: {guild.id})'  # guild's name with ID
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Hi {member.name}, welcome to Jamauls discord server!')  # on invite, send a message from bot

@bot.command(name='hello', help="responds with hello")
async def hello(ctx):
    await ctx.send('Hello!')

@bot.command(name='jamaul', help="responds with a crime")
async def jamaul(ctx):
    quotes = ["i hopped a fence", "i shot a cop with a stick", "i run fast and jump high"]
    response = random.choice(quotes)
    await ctx.send(response)

@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int): # cast to int
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

@bot.command(name='rpc', help='plays rock paper scissors with you')
async def rpc(ctx, message):
    answer = message.lower()
    choice = ['rock', 'paper', 'scissors']
    comp = random.choice(choice)

    if answer not in choice:
        await ctx.reply("answer invalid")
    else:
        if comp == choice:
            await ctx.reply(f'Tie! I chose {comp}')
        elif answer == 'rock' and comp == 'scissors':
            await ctx.reply(f'You win! I chose {comp}')
        elif answer == 'rock' and comp == 'paper':
            await ctx.reply(f'You lose! I chose {comp}')
        elif answer == 'paper' and comp == 'scissors':
            await ctx.reply(f'You Lose! I chose {comp}')
        elif answer == 'paper' and comp == 'rock':
            await ctx.reply(f'You win! I chose {comp}')
        elif answer == 'scissors' and comp == 'paper':
            await ctx.reply(f'You win! I chose {comp}')
        elif answer == 'scissors' and comp == 'rock':
            await ctx.reply(f'You Lose! I chose {comp}')
@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

# Run the bot, suppressing the default logging configuration
bot.run(token, log_handler=None)
