from random import randint, choice

def get_response(user_input : str) -> str:
  #python is sensitive so we put everything miniscule
  lowered: str = user_input.lower()

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
      "Hmmmm , i dont really understand that :(",
      "my creator didnt finish me yet ,sorry i cant understand you "
    ])