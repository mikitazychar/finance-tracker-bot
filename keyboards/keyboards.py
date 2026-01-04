from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_main_kb() -> ReplyKeyboardMarkup:
    """Создает основное меню бота"""
    kb_builder = ReplyKeyboardBuilder()

    kb_builder.row(
        KeyboardButton(text="💰 Установить доход"),
        KeyboardButton(text="📉 Добавить расход")
    )
    kb_builder.row(
        KeyboardButton(text="📊 Статистика")
    )

    return kb_builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Выберите действие из меню..."
    )


def get_cancel_kb() -> ReplyKeyboardMarkup:
    """Клавиатура для отмены текущего действия (FSM)"""
    kb_builder = ReplyKeyboardBuilder()
    kb_builder.button(text="❌ Отмена")
    return kb_builder.as_markup(resize_keyboard=True)
