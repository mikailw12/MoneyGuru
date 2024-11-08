from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from config import ADMINS
from database import add_user, get_users, add_ex, add_in, get_ex_or_in_for_mon, get_ex_or_in_for_week
from keyboards import user_start_kb, admin_start_kb, ex_or_in_kb, ex_categories_kb , date_in_kb, date_ex_kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage


router = Router()

class Expense(StatesGroup):
    category = State()
    name = State()
    amount = State()

class Income(StatesGroup):
    name = State()
    amount = State()


@router.message(CommandStart())
async def start(message:Message):
    await add_user(message.from_user.id)
    if message.from_user.id in ADMINS:
        message.answer(f'Привет, админ, помимо базовых функций бота тебе доступна рассылка сообщений всем пользователям.\nТекущее количество пользователей: {len(get_users)}', reply_markup=admin_start_kb)
    else:
        message.answer('Добро пожаловать в MoneyGuruBot, с помощью него вы можете добавлять и отслеживать свои доходы и расходы за определённый срок',  reply_markup=user_start_kb)

@router.message(F.text=='Информация')
async def information(message:Message):
    await message.answer('Данный бот был разработан @sunimassen для портфолио')

@router.message(F.text=='Добавить расход/доход')
async def new_ex_or_in(message:Message):
    await message.answer('Выберите тип операции', reply_markup=ex_or_in_kb)

@router.message(F.data=='new_income')
async def new_in(message:Message, state:FSMContext):
    await state.set_state(Income.name)
    await message.answer('Напишите имя транзакции')

@router.message(Income.name)
async def set_in_name(message:Message, state:FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Income.amount)
    await message.answer('Введите сумму транзакции')

@router.message(Income.amount)
async def set_in_amount(message:Message, state:FSMContext):
    await state.update_data(amount=message.text)
    name = await state.get_data('name')
    amount = await state.get_data('amount')
    await add_in(name, amount, message.from_user.id)
    await state.clear()
    await message.answer('Транзакция добавлена!\nГлавное меню - /start')

@router.message(F.data=='new_expense')
async def new_ex(message:Message, state:FSMContext):
    await state.set_state(Expense.name)
    await message.answer('Напишите имя транзакции')

@router.message(Expense.name)
async def set_ex_name(message:Message, state:FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Income.amount)
    await message.answer('Введите сумму транзакции')

@router.message(Expense.amount)
async def set_ex_amount(message:Message, state:FSMContext):
    await state.update_data(amount=message.text)
    await message.answer('Выберите категорию транзакции', reply_markup=ex_categories_kb)

@router.message(F.data.startswith('ex'))
async def set_category(message:Message, state:FSMContext, callback:CallbackQuery):
    category = callback.data[:3]
    name = await state.get_data('name')
    amount = await state.get_data('amount')
    await add_ex(name, amount, category, message.from_user.id)
    await state.clear()
    await message.answer('Транзакция добавлена!\nГлавное меню - /start')



