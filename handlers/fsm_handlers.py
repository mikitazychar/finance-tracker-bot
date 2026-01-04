from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from states.finance_states import FinanceStates
from database.db_sqlite import set_user_income, add_expense
from keyboards.keyboards import get_main_kb, get_cancel_kb

router = Router()


@router.message(F.text == "❌ Отмена")
async def process_cancel(message: types.Message, state: FSMContext):
    """
    Универсальный обработчик отмены.
    Сбрасывает любое состояние и возвращает в главное меню.
    """
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()

    await message.answer(
        "Действие отменено. Вы вернулись в главное меню.",
        reply_markup=get_main_kb()
    )


@router.message(F.text == "💰 Установить доход")
async def process_set_income(message: types.Message, state: FSMContext):
    await state.set_state(FinanceStates.waiting_for_income)
    await message.answer("Введите ваш общий доход (число):", reply_markup=get_cancel_kb())


@router.message(FinanceStates.waiting_for_income)
async def income_received(message: types.Message, state: FSMContext):
    # Если пользователь нажал другую кнопку меню вместо ввода числа
    if message.text in ["📉 Добавить расход", "📊 Статистика", "💰 Установить доход"]:
        await message.answer("Сначала завершите ввод дохода или нажмите '❌ Отмена'")
        return

    try:
        income = float(message.text.replace(" ", "").replace(",", "."))
        set_user_income(message.from_user.id, income)
        await message.answer(f"✅ Доход {income} успешно установлен!", reply_markup=get_main_kb())
        await state.clear()
    except ValueError:
        await message.answer("Ошибка! Введите число. Для выхода нажмите '❌ Отмена'")


@router.message(F.text == "📉 Добавить расход")
async def process_add_expense(message: types.Message, state: FSMContext):
    await state.set_state(FinanceStates.waiting_for_category)
    await message.answer("Введите категорию (например: Еда):", reply_markup=get_cancel_kb())


@router.message(FinanceStates.waiting_for_category)
async def category_received(message: types.Message, state: FSMContext):
    if message.text in ["💰 Установить доход", "📊 Статистика", "📉 Добавить расход"]:
        await message.answer("Сначала введите категорию или нажмите '❌ Отмена'")
        return

    await state.update_data(category=message.text)
    await state.set_state(FinanceStates.waiting_for_amount)
    await message.answer(f"Сколько потратили на '{message.text}'?", reply_markup=get_cancel_kb())


@router.message(FinanceStates.waiting_for_amount)
async def amount_received(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text.replace(" ", "").replace(",", "."))
        data = await state.get_data()
        add_expense(message.from_user.id, data['category'], amount)
        await message.answer(f"✅ Расход записан!", reply_markup=get_main_kb())
        await state.clear()
    except ValueError:
        await message.answer("Ошибка! Введите сумму числом.")
