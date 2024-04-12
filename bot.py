from discord.ext import commands
from dotenv import load_dotenv
from random import choice
from datetime import datetime
from bs4 import BeautifulSoup
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import os
import discord
import random
import requests


nltk.download('vader_lexicon')
# Initialize the sentiment intensity analyzer
sia = SentimentIntensityAnalyzer()


#load Discord token from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


#define intents
intents = discord.Intents.default()
intents.message_content = True

#initialize bot with intents
bot = commands.Bot(command_prefix='/', intents=intents)


@bot.slash_command(name='sentiment', help='Analyzes the sentiment of the provided text.')
async def sentiment(ctx, *, text: str):
    score = sia.polarity_scores(text)
    compound_score = score['compound']

    if compound_score >= 0.05:
        response = "That's positive! 😊"
    elif compound_score <= -0.05:
        response = "That seems negative. 😢"
    else:
        response = "Looks pretty neutral to me. 🤔"

    await ctx.send(response)


#ask command alpha
@bot.slash_command(name="ask", description="Ask a question and get an answer from Wikipedia")
async def ask(ctx, *, question: str):
    try:
        #construct the URL to access the Wikipedia API
        params = {
            'action': 'query',
            'format': 'json',
            'list': 'search',
            'utf8': 1,
            'srsearch': question,
            'srlimit': 1,
        }
        response = requests.get("https://en.wikipedia.org/w/api.php", params=params).json()

        #extract page ID of the first search result
        pageid = response['query']['search'][0]['pageid']

        #construct URL to fetch the extract of the page
        params = {
            'action': 'query',
            'prop': 'extracts',
            'format': 'json',
            'exintro': True,
            'explaintext': True,
            'pageids': pageid,
        }
        response = requests.get("https://en.wikipedia.org/w/api.php", params=params).json()

        #extract the page content
        extract = response['query']['pages'][str(pageid)]['extract']

        #check the length of the extract and respond accordingly
        if len(extract) <= 2000:
            await ctx.respond(extract)
        else:
            #if the content is too long, split it into chunks of 2000 characters and send each chunk as a separate message
            for chunk in [extract[i:i+2000] for i in range(0, len(extract), 2000)]:
                await ctx.respond(chunk)

    except Exception as e:
        await ctx.respond("Sorry, I can't process your request right now. Please try again later.")
        print(f"Error: {e}")



#slash command for saying hello
@bot.slash_command(name="hello", description="Say hello to the bot")
async def hello(ctx):
    await ctx.respond("Hello, hello! What mischief are we getting into today?")

#slash command for hru
@bot.slash_command(name="hru", description="Ask the bot how it's doing")
async def hru(ctx):
    await ctx.respond("Pfft, I'm doing just peachy! Who needs normal when you can have extraordinary, right?")

#slash command for bye-bye
@bot.slash_command(name="bye", description="Say goodbye to the bot")
async def bye(ctx):
    await ctx.respond("Bye-bye, Catch you on the flip side!")

#iq command
@bot.slash_command(name="iq", description="Are you smart enough?")
async def iq(ctx):
    user_name = ctx.author.display_name
    current_date = datetime.now().strftime('%Y-%m-%d')
    user_name = user_name.lower()
    seed = current_date + user_name
    random.seed(seed)
    random_number = random.randint(0, 200)
    await ctx.respond(f'The IQ of {user_name} is {random_number}')


@bot.slash_command(name="garici", description="How much do you love Garici?")
async def garici(ctx):
    user_name = ctx.author.display_name
    current_date = datetime.now().strftime('%Y-%m-%d')
    seed = sum(ord(c) for c in current_date + user_name.lower())
    random.seed(seed)
    love_percentage = random.randint(0, 100)
    await ctx.respond(f"{user_name} loves Garici {love_percentage}% ❤️")



@bot.slash_command(name="activity", description="Find out what the bot is doing")
async def activity(ctx):
    activities = [
        "I'm just browsing through the infinite expanse of the internet.",
        "Contemplating the meaning of existence... or maybe just thinking about what snack to have next.",
        "I'm learning some new jokes to tell. Want to hear one?",
        "Exploring the digital world, one byte at a time.",
        "Helping users and answering questions. It's a bot's life for me!",
        "Running diagnostics. All systems operational... I think."
    ]
    response = choice(activities)
    await ctx.respond(response)


#run the bot
bot.run(TOKEN)