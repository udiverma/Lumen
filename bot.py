import os
import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv
from transformers import pipeline
import requests
from bs4 import BeautifulSoup

# Load environment variables from .env file
load_dotenv()

# Get environment variables
DISCORD_TOKEN = os.getenv('BOT_TOKEN')
YOUR_CHANNEL_ID = int(os.getenv('CHANNEL_ID'))  # Ensure this is an integer

# Define the intents your bot will use
intents = nextcord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True  # Enable message content intent

# Initialize the bot with a command prefix and intents
bot = commands.Bot(command_prefix='/', intents=intents)

# Initialize the NLP model explicitly specifying the model and revision
nlp = pipeline('question-answering', model='distilbert-base-cased-distilled-squad', revision='626af31')

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    # Send "Hello, World!" message to a specific channel when the bot starts
    channel = bot.get_channel(YOUR_CHANNEL_ID)
    if channel:
        await channel.send('Hello, World!')

@bot.slash_command(name='ask', description='Ask the bot a question')
async def ask(interaction: nextcord.Interaction, question: str):
    # Fetch chat history
    messages = await interaction.channel.history(limit=100).flatten()
    context = " ".join([message.content for message in messages if message.author != bot.user])

    # Use NLP model to answer question
    result = nlp(question=question, context=context)
    answer = result['answer']

    await interaction.response.send_message(f'Answer: {answer}')

def web_search(query):
    search_url = f'https://www.google.com/search?q={query}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = []
    for g in soup.find_all('div', class_='tF2Cxc'):
        title = g.find('h3').text if g.find('h3') else None
        link = g.find('a')['href'] if g.find('a') else None
        snippet = g.find('span', class_='aCOpRe').text if g.find('span', class_='aCOpRe') else None
        if title and link and snippet:
            results.append({'title': title, 'link': link, 'snippet': snippet})
    return results

@bot.slash_command(name='websearch', description='Search the web for an answer')
async def websearch(interaction: nextcord.Interaction, query: str):
    results = web_search(query)
    if results:
        response = '\n'.join([f"{result['title']}\n{result['link']}\n{result['snippet']}\n" for result in results[:3]])
    else:
        response = 'No results found.'
    await interaction.response.send_message(response)

# Run the bot
bot.run(DISCORD_TOKEN)