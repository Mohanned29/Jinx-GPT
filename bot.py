from discord.ext import commands
from dotenv import load_dotenv
from random import choice
from datetime import datetime
import os
import discord
import random
import openai

#load Discord token from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


#define intents
intents = discord.Intents.default()
intents.message_content = True

#initialize bot with intents
bot = commands.Bot(command_prefix='/', intents=intents)

#inform users that /ask functionality will be available soon (chatgpt)
@bot.slash_command(name="ask", description="Ask a question and get an answer from Jinx")
async def ask(ctx, *, question: str):
    try:
        openai.api_key = OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ]
        )
        await ctx.respond(response.choices[0].message['content'])
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