from discord.ext import commands
from responses import get_response
from dotenv import load_dotenv
import discord
import os


#load Discord token from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#define intents
intents = discord.Intents.default()
intents.message_content = True

#create bot instance with command prefix and intents
bot = commands.Bot(command_prefix='?', intents=intents)

#command to handle empty message
@bot.command()
async def empty(ctx):
    await ctx.send('Aww, did you lose your voice or are you just feeling shy UwU ?')

#command to greet the user
@bot.command()
async def hello(ctx):
    await ctx.send('Hello, hello! What mischief are we getting into today?')

#command to check how the bot is doing
@bot.command()
async def how_are_you(ctx):
    await ctx.send("Pfft, I'm doing just peachy! Who needs normal when you can have extraordinary, right?")

#command for bye-bye
@bot.command()
async def bye(ctx):
    await ctx.send("Bye-bye, pookie! Catch you on the flip side!")

#command to handle unknown wela random commands
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        user_input = ctx.message.content[len(bot.command_prefix):]
        response = get_response(user_input)
        await ctx.send(response)

#run the bot
bot.run(TOKEN)
