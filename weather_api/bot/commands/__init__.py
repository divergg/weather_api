
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Configure logging
dp = Dispatcher()

# Initialize bot and dispatcher
async def main():
    bot = Bot(token=TELEGRAM_TOKEN)
    await dp.start_polling(bot)


from . import commands