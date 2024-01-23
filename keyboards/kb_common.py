from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

common_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Новая транзакция',
            description='Добавить новую транзакцию'
        )
    ],
    [
        KeyboardButton(
            text='Расчетный остаток',
            description='Запросить расчетный остаток'
        )
    ],
    [
        KeyboardButton(
            text='Фактический остаток',
            description='Задать фактический остаток'
        )
    ]
], resize_keyboard=True)


cancel_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Отменить',
            description='Отменить действие'
        )
    ]
], resize_keyboard=True)


def transaction_markup_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    markup = [
        row,
        [
            KeyboardButton(
            text='Отменить',
            description='Отменить действие'
        )
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=markup, resize_keyboard=True)


transaction_save_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Сохранить',
            description='Сохранить транзакцию'
        )
    ],
    [
        KeyboardButton(
            text='Отменить',
            description='Отменить транзакцию'
        )
    ]
], resize_keyboard=True)


actual_balance_save_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Сохранить',
            description='Сохранить ввод баланса'
        )
    ],
    [
        KeyboardButton(
            text='Отменить',
            description='Отменить ввод баланса'
        )
    ]
], resize_keyboard=True)