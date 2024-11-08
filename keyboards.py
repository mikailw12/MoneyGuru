from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, 
                           ReplyKeyboardMarkup, KeyboardButton)

user_start_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Добавить расход/доход')], # ex_or_in_kb
    [KeyboardButton(text='Расходы за последнюю неделю/месяц')], #wk_or_mon_ex_kb
    [KeyboardButton(text='Информация')] 
], resize_keyboard=True)

admin_start_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Добавить расход/доход')], # ex_or_in_kb
    [KeyboardButton(text='Расходы за последнюю неделю/месяц')], #wk_or_mon_ex_kb
    [KeyboardButton(text='Информация'),
     KeyboardButton(text='Рассылка')] 
], resize_keyboard=True)

ex_or_in_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Расход', callback_data='new_expense'), 
     InlineKeyboardButton(text='Доход',  callback_data='new_income')]
])

date_ex_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Месяц', callback_data='mon_ex'),
     InlineKeyboardButton(text='Неделя',  callback_data='wk_ex')],
    [InlineKeyboardMarkup(text='Год', callback_data='all_time_ex')]
])

date_in_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Месяц', callback_data='mon_in'),
     InlineKeyboardButton(text='Неделя', callback_data='year_in')],
    [InlineKeyboardMarkup(text='Год', callback_data='year_in')]
])

ex_categories_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Кафе и рестораны', callback_data='ex_food'),
     InlineKeyboardButton(text='Развлечения',  callback_data='ex_entertainment')],
     [InlineKeyboardButton(text='Транспорт', callback_data='ex_transport'),
     InlineKeyboardButton(text='Другое',  callback_data='ex_other')]
])