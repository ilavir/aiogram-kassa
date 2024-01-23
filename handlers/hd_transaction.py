from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards import kb_common
from utils.states import AddTransaction
from utils.google_sheets import gs_save_transaction


transaction_types = ['Поступление', 'Выбытие']
transaction_category = ['Категория 1', 'Категория 2', 'Категория 3']

router = Router()


@router.message(Command('add_transaction'))
@router.message(F.text == 'Новая транзакция')
async def add_transaction(message: Message, state: FSMContext):
    await state.set_state(AddTransaction.GET_DATE)
    await message.answer(f'<b>Новая транзакция</b>\n\n' \
                         f'Введите дату транзакции в виде 21.12.23', reply_markup=kb_common.cancel_keyboard)


@router.message(AddTransaction.GET_DATE)
async def process_transaction_date(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    await state.set_state(AddTransaction.GET_TYPE)
    await message.answer('Выберите тип транзакции', reply_markup=kb_common.transaction_markup_keyboard(transaction_types))


@router.message(AddTransaction.GET_TYPE, F.text.in_(transaction_types))
async def process_transaction_type(message: Message, state: FSMContext):
    await state.update_data(type=message.text)
    await state.set_state(AddTransaction.GET_SUM)
    await message.answer('Введите сумму', reply_markup=kb_common.cancel_keyboard)

@router.message(AddTransaction.GET_TYPE)
async def process_transaction_type(message: Message, state: FSMContext):
    await message.answer('Неправильный тип транзакции. Выберите тип транзакции из предложенных', reply_markup=kb_common.transaction_markup_keyboard(transaction_types))


@router.message(AddTransaction.GET_SUM)
async def process_transaction_sum(message: Message, state: FSMContext):
    await state.update_data(sum=message.text)
    await state.set_state(AddTransaction.GET_CATEGORY)
    await message.answer('Выберите категорию', reply_markup=kb_common.transaction_markup_keyboard(transaction_category))


@router.message(AddTransaction.GET_CATEGORY, F.text.in_(transaction_category))
async def process_transaction_category(message: Message, state: FSMContext):
    await state.update_data(category=message.text)
    await state.set_state(AddTransaction.GET_DESCRIPTION)
    await message.answer('Введите описание транзакции', reply_markup=kb_common.cancel_keyboard)

@router.message(AddTransaction.GET_CATEGORY)
async def process_transaction_category(message: Message, state: FSMContext):
    await message.answer('Неправильная категория. Выберите категорию из предложенных', reply_markup=kb_common.transaction_markup_keyboard(transaction_category))


@router.message(AddTransaction.GET_DESCRIPTION)
async def process_transaction_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(AddTransaction.SAVE)
    context_data = await state.get_data()
    await message.answer(f'<b>Данные транзакции</b>\n\n'
                         f'Дата: {context_data.get("date")}\n' \
                         f'Тип: {context_data.get("type")}\n' \
                         f'Сумма: {context_data.get("sum")}\n' \
                         f'Категория: {context_data.get("category")}\n' \
                         f'Описание: {context_data.get("description")}')
    await message.answer('Сохранить транзакцию?', reply_markup=kb_common.transaction_save_keyboard)


@router.message(AddTransaction.SAVE, F.text == 'Сохранить')
async def save_transaction(message: Message, state: FSMContext):
    context_data = await state.get_data()
    balance = gs_save_transaction(context_data.get("date"), context_data.get("type"), context_data.get("sum"), context_data.get("category"), context_data.get("description"))
    await state.clear()
    await message.answer(f'Транзакция сохранена\n\nРасчетный остаток: {balance}', reply_markup=kb_common.common_keyboard)

@router.message(AddTransaction.SAVE)
async def save_transaction(message: Message, state: FSMContext):
    await message.answer('Выберите действие: "Сохранить" или "Отменить"', reply_markup=kb_common.transaction_save_keyboard)