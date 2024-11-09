from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.filters import CommandStart
from config import ADMINS
from database import add_user, get_users, add_ex, add_in, get_expenses_by_term, get_incomes_by_term
from my_keyboards import user_start_kb, admin_start_kb, ex_or_in_kb, ex_categories_kb , date_in_kb, date_ex_kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import arrow


router = Router()

class Spam(StatesGroup):
    text = State()

class Expense(StatesGroup):
    category = State()
    name = State()
    amount = State()

class Income(StatesGroup):
    name = State()
    amount = State()

@router.message(CommandStart())
async def start(message:Message, state:FSMContext):
    await state.clear()
    await add_user(message.from_user.id)
    if message.from_user.id in ADMINS:
        users = await get_users()
        await message.answer(f'Привет, админ, помимо базовых функций бота тебе доступна рассылка сообщений всем пользователям.\nТекущее количество пользователей: {len(users)}', reply_markup=admin_start_kb)
    else:
        await message.answer('Добро пожаловать в MoneyGuruBot, с помощью него вы можете добавлять и отслеживать свои доходы и расходы за определённый срок',  reply_markup=user_start_kb)

@router.message(F.text=='Информация')
async def information(message:Message):
    await message.answer('Данный бот был разработан @sunimassen для портфолио')


#добавление

@router.message(F.text=='Добавить расход/доход')
async def new_ex_or_in(message:Message):
    await message.answer('Выберите тип транзакции', reply_markup=ex_or_in_kb)

@router.callback_query(F.data=='new_income')
async def new_in(callback:CallbackQuery, state:FSMContext):
    await callback.answer()
    await state.set_state(Income.name)
    await callback.message.answer('Напишите имя транзакции')

@router.message(Income.name)
async def set_in_name(message:Message, state:FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Income.amount)
    await message.answer('Напишите сумму транзакции (только числа)')

@router.message(Income.amount)
async def set_in_amount(message: Message, state: FSMContext):
    if message.text.isdigit():
        data = await state.get_data()
        name = data['name']
        amount = float(message.text)  # Преобразуем сумму в число
        await add_in(name, amount, message.from_user.id)
        await state.clear()
        await message.answer('Транзакция добавлена!\nГлавное меню - /start')
    else:
        await state.set_state(Income.amount)
        await message.answer('Напишите сумму транзакции (только числа)')
@router.callback_query(F.data=='new_expense')
async def new_ex(callback:CallbackQuery, state:FSMContext):
    await callback.answer()
    await state.set_state(Expense.name)
    await callback.message.answer('Напишите имя транзакции')

@router.message(Expense.name)
async def set_ex_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Expense.amount)
    await message.answer('Напишите сумму транзакции (только числа)')

@router.message(Expense.amount)
async def set_ex_amount(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(amount=float(message.text))  # Преобразуем сумму в число
        await message.answer('Выберите категорию транзакции', reply_markup=ex_categories_kb)
    else:
        await state.set_state(Expense.amount)
        await message.answer('Напишите сумму транзакции (только числа)')

@router.callback_query(F.data.startswith('cat_'))
async def set_category(callback: CallbackQuery, state: FSMContext):
    category = callback.data[4:]  # Извлекаем категорию из data, убирая "cat_"
    data = await state.get_data()
    name = data['name']
    amount = data['amount']
    await add_ex(name, amount, category, callback.from_user.id)
    await state.clear()
    await callback.message.answer('Транзакция добавлена!\nГлавное меню - /start')


@router.message(F.text=='Узнать доходы')
async def get_incomes_date(message:Message):
    await message.answer('Выберите желаемый срок', reply_markup=date_in_kb)

@router.callback_query(F.data.startswith('in'))
async def get_incomes(callback: CallbackQuery):
    term = callback.data[3:]
    incomes = await get_incomes_by_term(term, callback.from_user.id)
    if incomes:
        for income in incomes:
            name = income.name
            amount = income.amount
            date = income.created_at  # Use created_at, which should be datetime
            await callback.message.answer(
                f'Наименование дохода: {name}\nСумма: {amount}\nДата: {date.strftime("%d %B %Y, %H:%M:%S")}'
            )
    else:
        await callback.message.answer('В данный момент у вас нет доходов')

@router.message(F.text=='Узнать расходы')
async def get_expenses_date(message:Message):
    await message.answer('Выберите желаемый срок', reply_markup=date_ex_kb)

@router.callback_query(F.data.startswith('ex'))
async def get_incomes(callback: CallbackQuery):
    term = callback.data[3:]
    expenses = await get_expenses_by_term(term, callback.from_user.id)
    if expenses:
        for expense in expenses:
            name = expense.name
            amount = expense.amount
            date = expense.created_at  # Use created_at, which should be datetime
            category = 'Транспорт' if expense.category == 'trans' else 'Еда' if expense.category == 'food' else 'Развлечения' if expense.category == 'enter' else 'Другое'
            await callback.message.answer(
                f'Наименование расхода: {name}\nКатегория: {category}\nСумма: {amount}\nДата: {date.strftime("%d %B %Y, %H:%M:%S")}'
            )
    else:
        await callback.message.answer('В данный момент у вас нет расходов')

    


@router.message(F.text=='Рассылка')
async def spam(message:Message, state:FSMContext):
    await state.set_state(Spam.text)
    await message.answer('Введите текст для рассылки')

@router.message(Spam.text)
async def spam_text(message:Message, state:FSMContext):
    await state.clear()
    users_id  = await get_users()
    for user_id in users_id:
        await message.bot.send_message(user_id, f'{message.text}')
    await message.answer('Рассылка завершена')

        