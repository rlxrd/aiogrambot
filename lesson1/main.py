from aiogram import Bot, Dispatcher, executor, types

bot = Bot('6088099037:AAH-Ts7oJdlvCGxxvl3GbJLJwD6pC3QJkEw')
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(f'{message.from_user.first_name}, добро пожаловать в магазин кроссовок!')


@dp.message_handler()
async def answer(message: types.Message):
    await message.reply('Я тебя не понимаю.')


if __name__ == '__main__':
    executor.start_polling(dp)
