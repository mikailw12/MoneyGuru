from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, 
                           ReplyKeyboardMarkup, KeyboardButton)

user_start_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Добавить расход/доход')], # ex_or_in_kb
    [KeyboardButton(text='Узнать расходы'),
     KeyboardButton(text='Узнать доходы')], #wk_or_mon_ex_kb
    [KeyboardButton(text='Информация')] 
], resize_keyboard=True)

admin_start_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Добавить расход/доход')], # ex_or_in_kb
    [KeyboardButton(text='Узнать расходы'),
     KeyboardButton(text='Узнать доходы')], #wk_or_mon_ex_kb
    [KeyboardButton(text='Информация'),
     KeyboardButton(text='Рассылка')] 
], resize_keyboard=True)

ex_or_in_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Расход', callback_data='new_expense'), 
     InlineKeyboardButton(text='Доход', callback_data='new_income')]
])

date_ex_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Неделя', callback_data='ex_week'),
     InlineKeyboardButton(text='Месяц', callback_data='ex_month')],
     [InlineKeyboardButton(text='Год', callback_data='ex_year')]
])

date_in_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Неделя', callback_data='in_week'),
     InlineKeyboardButton(text='Месяц', callback_data='in_month')],
    [InlineKeyboardButton(text='Год', callback_data='in_year')]
])

ex_categories_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Кафе и рестораны', callback_data='cat_food'),
     InlineKeyboardButton(text='Развлечения',  callback_data='cat_enter')],
     [InlineKeyboardButton(text='Транспорт', callback_data='cat_trans'),
     InlineKeyboardButton(text='Другое',  callback_data='cat_other')]
])
