import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import Router
from aiogram.types import ChatMemberUpdated
import asyncio
from get_course import get_usd_to_rub_rate

API_TOKEN = '7649386783:AAHq28Jnm182Zzz2emAZQ_toVsticXH2T-g'
API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Создаем экземпляр бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher()  # В версии 3.x не нужно передавать storage напрямую, если не используется FSM

# Создаем роутер для обработки команд и сообщений
router = Router()


# Обработчик команды /start
@router.message(Command(commands=["start"]))
async def send_welcome(message: types.Message):
    await message.answer("Добрый день, как вас зовут?")


# Обработчик текстовых сообщений (ответ на запрос имени)
@router.message()
async def get_name(message: types.Message):
    user_name = message.text
    usd_rate = get_usd_to_rub_rate()
    if user_name and usd_rate:
        await message.answer(f"Рад знакомству, {user_name}! Курс доллара сегодня {usd_rate}")
    elif usd_rate:
        await message.answer(f"Курс доллара сегодня {usd_rate}")
    elif user_name:
        await message.answer(f"Рад знакомству, {user_name}! Не могу получить курс доллара. Попробуй позже!")
    else:
        await message.answer(f"Я не вижу имени и не могу получить курс доллара :(")


# Обработчик события добавления бота в группу
@router.chat_member()
async def bot_added_to_group(event: ChatMemberUpdated):
    # Проверяем, что событие связано с добавлением бота в группу
    if event.new_chat_member.user.id == (await bot.get_me()).id and event.new_chat_member.status == 'member':
        chat_id = event.chat.id
        await bot.send_message(chat_id, "Привет, я бот который пишет курсы валют!")

# Регистрация роутеров в диспетчере
dp.include_router(router)


# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
