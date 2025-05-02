import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.deep_linking import create_start_link

from db import load, write

TOKEN = "7895750104:AAGyV_sKf7yWFJWVJbfxxqiODzJEDSG1DnA"
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message, command: CommandObject) -> None:
    data = load()
    user_id = str(message.from_user.id)

    if user_id not in data:
        data[user_id] = 0

    # Referal tugmasini yaratish
    link = await create_start_link(bot=bot, payload=user_id)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👥 Referalni ulashish", url=link)]
        ]
    )

    # Xush kelibsiz va tugmali xabar
    await message.answer(
        f"Hello, {html.bold(message.from_user.full_name)}!",
        reply_markup=keyboard
    )

    # Agar referal link orqali kirgan bo‘lsa
    chat_id = command.args
    if chat_id:
        if chat_id != user_id:
            old_cnt = data.get(chat_id, 0)
            data[chat_id] = old_cnt + 1
            await message.answer(f"Siz quyidagi foydalanuvchiga refer bo‘ldingiz: {chat_id}")
        else:
            await message.answer("Siz o‘zingizga refer bo‘la olmaysiz.")

    write(data)


@dp.message(Command("refer"))
async def refer_handler(message: Message) -> None:
    link = await create_start_link(bot=bot, payload=str(message.from_user.id))
    await message.answer(link)


@dp.message(Command("count"))
async def count_handler(message: Message) -> None:
    data = load()
    chat_id = str(message.from_user.id)
    await message.answer(f"Sizda {data.get(chat_id, 0)} ta referal bor.")


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
