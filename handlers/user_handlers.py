from aiogram import Router, types, F
from aiogram.filters import CommandStart
from keyboards.keyboards import get_main_kb

router = Router()


@router.message(CommandStart())
async def process_start_command(message: types.Message):
    """Обработка команды /start"""
    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        "Я помогу тебе следить за бюджетом.\n"
        "Сначала установи свой доход, а затем записывай расходы по категориям.",
        reply_markup=get_main_kb()
    )


@router.message(F.text == "❌ Отмена")
async def process_cancel(message: types.Message):
    await message.answer(
        "Действие отменено.",
        reply_markup=get_main_kb()
    )
