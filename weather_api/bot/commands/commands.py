import os
import aiohttp
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from .states import Form
from dotenv import load_dotenv

from . import dp

load_dotenv()

API_HOST = os.getenv('API_HOST')

API_LINK = f'http://{API_HOST}:8000/api'

@dp.message(F.text.regexp(r'/start'))
async def send_greetings(message: types.Message):
    start_message = "Привет! Этот бот может помочь узнать погоду в разных городах России."
    markup = types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="Узнать погоду")]], resize_keyboard=True)
    await message.reply(start_message, reply_markup=markup)


@dp.message(F.text == "Узнать погоду")
async def main_command(message: types.Message, state: FSMContext):
    await state.set_state(Form.old)
    answer = "Введите название города"
    await message.reply(answer)


@dp.message(Form.old)
async def send_city_name(message: types.Message, state: FSMContext):
    await state.set_state(Form.new)
    async with aiohttp.ClientSession() as session:
        data = {'lang_code': "ru_RU",
                'city_name': message.text}
        async with session.get(API_LINK, params=data) as response:
            result = await response.json()
    error = result.get("error", None)
    if error:
        answer = "Что то пошло не так. Повторите попытку позднее"
    else:
        temp, pressure, wind, city_name = result["temp"], result["pressure"], result["wind"], result["city_name"]
        answer = f'Погода в городе {city_name}: температура - {temp}, давление - {pressure} мм рт ст, скорость ветра - {wind} м/с'
    markup = types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="Узнать погоду")]], resize_keyboard=True)
    await message.reply(answer, reply_markup=markup)


@dp.message(Form.new)
async def fallback(message: types.Message):
    answer = "Простите, я вас не понимаю"
    await message.reply(answer)
