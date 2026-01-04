from aiogram import Router, types, F
from database.db_sqlite import get_user_stats

router = Router()


@router.message(F.text == "📊 Статистика")
async def process_statistics(message: types.Message):
    income, expenses, total_spent = get_user_stats(message.from_user.id)

    if income == 0 and not expenses:
        await message.answer("Данных пока нет. Начните с установки дохода!")
        return

    balance = income - total_spent
    percent = (total_spent / income * 100) if income > 0 else 0

    report = [
        "📊 **Ваш финансовый отчет**",
        f"💰 Доход: `{income:.2f}`",
        f"📉 Всего потрачено: `{total_spent:.2f}`",
        f"⚖️ Остаток: `{balance:.2f}`",
        f"📈 Процент трат: `{percent:.1f}%`",
        "\n**Последние траты:**"
    ]

    for cat, amt in expenses[-10:]:
        report.append(f"• {cat}: {amt:.2f}")

    await message.answer("\n".join(report), parse_mode="Markdown")
