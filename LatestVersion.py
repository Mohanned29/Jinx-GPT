import os
import discord
from discord.ext import commands
from datetime import datetime
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import random
import requests
import google.generativeai as genai
from google.generativeai import GenerationConfig
import asyncio
import logging
logging.basicConfig(level=logging.INFO)


Discordtoken = os.environ.get('DISCORD_TOKEN')
google_api_key = os.environ.get('GOOGLE_API_KYE')

if not Discordtoken:
    raise ValueError("DISCORD_TOKEN is missing from environment variables.")
if not google_api_key:
    raise ValueError("GOOGLE_API_KYE is missing from environment variables.")

genai.configure(api_key=google_api_key)

nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    global model
    logging.info(f'Logged in as {bot.user}')
    try:
        generation_config = GenerationConfig(
            temperature=1,
            top_p=0.95,
            top_k=40,
            max_output_tokens=8192,
            response_mime_type="text/plain",
        )
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config
        )
        logging.info("Google Generative AI model initialized successfully.")
    except Exception as e:
        logging.error(f"Failed to initialize Google Generative AI model: {e}")

    try:
        synced = await bot.tree.sync()
        logging.info(f"Synced {len(synced)} commands globally.")
        logging.info("Registered commands:")
        for command in bot.tree.get_commands():
            logging.info(f"- {command.name}")
    except Exception as e:
        logging.error(f"Failed to sync commands: {e}")

@bot.tree.command(name='sentiment', description='Analyzes the sentiment of the provided text.')
async def sentiment(interaction: discord.Interaction, text: str):
    score = sia.polarity_scores(text)
    compound_score = score['compound']
    if compound_score >= 0.05:
        response = "That's positive! 😊"
    elif compound_score <= -0.05:
        response = "That seems negative. 😢"
    else:
        response = "Looks pretty neutral to me. 🤔"
    await interaction.response.send_message(response)



@bot.tree.command(
    name="speak",
    description="Speak with the bot using AI-generated responses."
)
async def speak(interaction: discord.Interaction, message: str):
    global model
    if model is None:
        await interaction.response.send_message("AI model is not initialized yet. Please try again later.")
        return
    try:
        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [f"{message}\n"],
                },
                {
                    "role": "model",
                    "parts": ["Hello there! How can I help you today?\n"],
                }
            ]
        )
        response = chat_session.send_message(message)
        response_text = response.text
        if len(response_text) <= 2000:
            await interaction.response.send_message(response_text)
        else:
            await interaction.response.send_message("Response is too long, sending in parts.")
            for i in range(0, len(response_text), 2000):
                await interaction.followup.send(response_text[i:i+2000])
                await asyncio.sleep(1)
    except Exception as e:
        await interaction.response.send_message(f"Error: {e}")
        logging.error(f"Error in 'speak' command: {e}")





@bot.tree.command(name="ask", description="Ask a question and get an answer")
async def ask(interaction: discord.Interaction, question: str):
    try:
        params = {
            'action': 'query',
            'format': 'json',
            'list': 'search',
            'utf8': 1,
            'srsearch': question,
            'srlimit': 1,
        }
        response = requests.get("https://en.wikipedia.org/w/api.php", params=params).json()
        pageid = response['query']['search'][0]['pageid']
        params = {
            'action': 'query',
            'prop': 'extracts',
            'format': 'json',
            'exintro': True,
            'explaintext': True,
            'pageids': pageid,
        }
        response = requests.get("https://en.wikipedia.org/w/api.php", params=params).json()
        extract = response['query']['pages'][str(pageid)]['extract']
        if len(extract) <= 2000:
            await interaction.response.send_message(extract)
        else:
            await interaction.response.send_message("Response is too long, sending in parts.")
            for chunk in [extract[i:i + 2000] for i in range(0, len(extract), 2000)]:
                await interaction.followup.send(chunk)
                await asyncio.sleep(1)
    except Exception as e:
        await interaction.response.send_message("Sorry, I can't process your request right now. Please try again later.")
        logging.error(f"Error in 'ask' command: {e}")

@bot.tree.command(name='hello', description="Greet based on the time of day")
async def hello(interaction: discord.Interaction):
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        greeting = "Hellooo, sbah el khir!"
    elif 12 <= current_hour < 18:
        greeting = "Good afternoooooooooon!"
    elif 18 <= current_hour < 23:
        greeting = "Good evening!"
    else:
        greeting = "It's too late! Roh tr9d 💤"
    await interaction.response.send_message(greeting)

@bot.tree.command(name="iq", description="Are you smart enough?")
async def iq(interaction: discord.Interaction):
    user_name = interaction.user.display_name
    current_date = datetime.now().strftime('%Y-%m-%d')
    user_name = user_name.lower()
    seed = current_date + user_name
    random.seed(seed)
    random_number = random.randint(0, 200)
    await interaction.response.send_message(f'The IQ of {user_name} is {random_number}')


bot.run(Discordtoken)
