from discord.ext import commands
import discord
from dotenv import load_dotenv
import os
from random import choice

#load Discord token from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#define intents
intents = discord.Intents.default()
intents.message_content = True

#initialize bot with intents
bot = commands.Bot(command_prefix='/', intents=intents)

#function to get bot response based on user input
def get_response(user_input: str) -> str:
    lowered = user_input.lower()
    if lowered == '':
        return 'Aww, did you lose your voice or are you just feeling shy UwU ?'
    elif 'hello' in lowered:
        return 'Hello, hello! What mischief are we getting into today?'
    elif 'how are you doing' in lowered:
        return "Pfft, I'm doing just peachy! Who needs normal when you can have extraordinary, right?"
    elif 'bye' in lowered:
        return "Bye-bye, pookie! Catch you on the flip side!"
    else:
        return choice([
            "Ha! I love it when things get unpredictable! What's on your mind, wild one?",
            "Hmmmm, I don't really understand that :(",
            "My creator didn't finish me yet, sorry I can't understand you."
        ])
#inform users that /ask functionality will be available soon (chatgpt)
@bot.slash_command(name="ask", description="This functionality will be available soon")
async def ask(ctx):
    await ctx.respond("This functionality will be available soon. Stay tuned!")

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
    await ctx.respond("Bye-bye, pookie! Catch you on the flip side!")

#run the bot
bot.run(TOKEN)