from typing import Final
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response
import os

#load our token:
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

#bot setup:
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents = intents)

#message functionality:
async def send_message(message:Message , user_message:str) -> None:
  if not user_message:
    print("(Message was empty because intents were not enabled)")
    return
  
  #if the user wanna talk to the bot in a private way (to the inbox):
  if is_private:= user_message[0] == "?" :
    #since the private message yebda with '?' alors the real message starts from index 1
    user_message = user_message[1:]
  
  try:
    response: str = get_response(user_message)
    #if user wants private message alors author , else its gonna be printed f channel
    await message.author.send(response) if is_private else await message.channel.send(response)

  except Exception as e:
    print(e)


#handling the startup:
@client.event
async def on_ready() -> None:
  print(f' {client.user} is now running')

#incoming messages:
@client.event
async def on_message(message : Message) -> None:
  if message.author == client.user:
    return
  
  username :str = str(message.author)
  user_message:str = message.content
  channel : str = str(message.channel)
  print(f'[{channel}] {username}: "{user_message}"')
  await send_message(message , user_message)


#main entry point
def main() -> None:
  client.run(token = TOKEN)

if __name__ == '__main__':
  main()