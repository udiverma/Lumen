import nextcord
import os
from dotenv import load_dotenv
from nextcord.ext import commands

load_dotenv()

DISCORD_TOKEN = os.getenv('BOT_TOKEN')
YOUR_CHANNEL_ID = os.getenv('CHANNEL_ID')

intents = nextcord.Intents.default()
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    channel = bot.get_channel(YOUR_CHANNEL_ID)
    if channel:
        await channel.send('Hello, World!')

@bot.slash_command(name='hello', description='Say Hello, World!')
async def hello(interaction: nextcord.Interaction):
    await interaction.response.send_message('Hello, World!')

bot.run(DISCORD_TOKEN)