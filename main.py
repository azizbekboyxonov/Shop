
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode, ChatMemberStatus
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import TOKEN


CHANNEL = "@boyxonovv"


dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def is_subscribed(bot, channel, user_id):
    user = await bot.get_chat_member(channel, user_id)
    return user.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR]


def get_subscription_buttons():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Kanalga obuna bo‘lish", url=f"https://t.me/{CHANNEL[1:]}")],
        [InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_subs")]
    ])
    return keyboard


@dp.message(CommandStart())
async def start_handler(message: Message):
    is_sub = await is_subscribed(bot, CHANNEL, message.from_user.id)
    if is_sub:
        await message.answer("✅ Xush kelibsiz!")
    else:
        await message.answer("❗️ Iltimos, kanalga obuna bo‘ling:", reply_markup=get_subscription_buttons())


@dp.callback_query(lambda c: c.data == "check_subs")
async def check_subscription(callback: CallbackQuery):
    is_sub = await is_subscribed(bot, CHANNEL, callback.from_user.id)
    if is_sub:
        await callback.message.edit_text("✅ Obuna bo‘lganingiz tasdiqlandi. Endi botdan foydalanishingiz mumkin.")
    else:
        await callback.answer("❗️ Hali obuna bo‘lmagansiz!", show_alert=True)


@dp.message()
async def echo_handler(message: Message):
    is_sub = await is_subscribed(bot, CHANNEL, message.from_user.id)

    if not is_sub:
        await message.answer("❗️ Botdan foydalanish uchun avval kanalga obuna bo‘ling:", reply_markup=get_subscription_buttons())
        return

    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Bu turdagi xabarni yuborib bo‘lmaydi!")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
