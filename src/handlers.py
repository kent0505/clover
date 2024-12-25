from aiogram         import Router
from aiogram.filters import CommandStart
from aiogram.types   import Message, InlineKeyboardButton, InlineKeyboardMarkup

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        text="Hello", 
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Play", 
                        url="https://t.me/otvw_bot/test"
                    ),
                ],
            ],
        ),
    )

@router.message()
async def cmd_delete(message: Message):
    await message.delete()
