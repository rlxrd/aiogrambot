from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from app import keyboards as kb
from app import database as db
from dotenv import load_dotenv
import os

load_dotenv()
storage = MemoryStorage()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot, storage=storage)


async def on_startup(_):
    await db.db_start()
    print('Бот успешно запущен!')


class SendToAll(StatesGroup):
    text = State()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await db.cmd_start_db(message.from_user.id)
    await message.answer_sticker('CAACAgIAAxkBAAMpZBAAAfUO9xqQuhom1S8wBMW98ausAAI4CwACTuSZSzKxR9LZT4zQLwQ')
    await message.answer(f'{message.from_user.first_name}, добро пожаловать в магазин кроссовок!',
                         reply_markup=kb.main)
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(f'Вы авторизовались как администратор!', reply_markup=kb.main_admin)


@dp.message_handler(text='Добавить товар')
async def cmd_id(message: types.Message):
    await message.answer(f'Добавить товар пока нельзя!')


@dp.message_handler(text='Каталог')
async def catalog(message: types.Message):
    await message.answer(f'Каталог пуст!', reply_markup=kb.catalog_list)


@dp.message_handler(text='Корзина')
async def cart(message: types.Message):
    await message.answer(f'Корзина пуста!')


@dp.message_handler(text='Контакты')
async def contacts(message: types.Message):
    await message.answer(f'Покупать товар у него: @mesudoteach')


@dp.message_handler(text='Админ-панель')
async def contacts(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(f'Вы вошли в админ-панель', reply_markup=kb.admin_panel)
    else:
        await message.reply('Я тебя не понимаю.')


@dp.message_handler(text='Сделать рассылку')
async def send_to_all_func(message: types.Message):
    await SendToAll.text.set()
    await message.answer('Отправьте сообщение для рассылки.')


@dp.message_handler(state=SendToAll.text)
async def send_to_all_send(message: types.Message, state: FSMContext):
    users = await db.send_to_all_db()
    for user in users:
        try:
            await bot.send_message(user[0], text=message.text)
        except Exception as error:
            print(error)
            continue
    await message.answer(f'Рассылка завершена!')
    await state.finish()


@dp.message_handler()
async def answer(message: types.Message):
    await message.reply('Я тебя не понимаю.')


@dp.callback_query_handler()
async def callback_query_keyboard(callback_query: types.CallbackQuery):
    if callback_query.data == 't-shirt':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Вы выбрали футболки')
    elif callback_query.data == 'shorts':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Вы выбрали шорты')
    elif callback_query.data == 'sneakers':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Вы выбрали кроссовки')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
