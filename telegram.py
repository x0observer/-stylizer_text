import logging

from aiogram import Bot, Dispatcher, executor, types
from setup import settings
from src.utils.extensions.openai import OpenAIService
API_TOKEN = settings["telegram"]["api_key"]

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dispather = Dispatcher(bot)


@dispather.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):

    
    """
    This handler will be called when user sends `/start` or `/help` command
    """

    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")




@dispather.message_handler()
async def echo(message: types.Message):
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


executor.start_polling(dispather, skip_updates=False)