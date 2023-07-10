import logging

from aiogram import Bot, Dispatcher, executor, types
from setup import settings
from src.utils.extensions.openai import OpenAIService
API_TOKEN = settings["telegram"]["api_key"]

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")




@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    print(dict(message.from_user), dict(message.chat))
    precompile_prompt = "Imagine that you are a financial advisor. Having received the news, you must extract the main meaning from it and convey it in a few easily accessible sentences. Add as many emoticons as you can."
    finite_prompt = "%s : %s" % (precompile_prompt, message.text) 
    stylized_text = OpenAIService.generate_response_by_prompt(finite_prompt)
    await message.answer(stylized_text.encode('utf-8').decode())


executor.start_polling(dp, skip_updates=True)