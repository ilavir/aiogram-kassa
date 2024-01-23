from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards import kb_common
from utils.states import ActualBalance
from utils.google_sheets import gs_add_actual_balance

router = Router()

@router.message(Command('actual_balance'))
@router.message(F.text == 'Фактический остаток')
async def add_actual_balance(message: Message, state: FSMContext):
    await state.set_state(ActualBalance.GET_DATE)
    await message.answer(f'<b>Фактический остаток</b>\n\n' \
                         f'Введите дату', reply_markup=kb_common.cancel_keyboard)


@router.message(ActualBalance.GET_DATE)
async def process_actual_balance_date(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    await state.set_state(ActualBalance.GET_SUM)
    await message.answer('Введите сумму', reply_markup=kb_common.cancel_keyboard)


@router.message(ActualBalance.GET_SUM)
async def process_actual_balance_sum(message: Message, state: FSMContext):
    await state.update_data(sum=message.text)
    await state.set_state(ActualBalance.SAVE)
    context_data = await state.get_data()
    await message.answer(f'Данные фактического остатка:\n\n'
                         f'Дата: {context_data.get("date")}\n' \
                         f'Сумма: {context_data.get("sum")}\n')
    await message.answer('Сохранить фактический остаток?', reply_markup=kb_common.actual_balance_save_keyboard)


@router.message(ActualBalance.SAVE, F.text == 'Сохранить')
async def save_transaction(message: Message, state: FSMContext):
    context_data = await state.get_data()
    gs_add_actual_balance(context_data.get("date"), context_data.get("sum"))
    await state.clear()
    await message.answer('Фактический остаток сохранен', reply_markup=kb_common.common_keyboard)

@router.message(ActualBalance.SAVE)
async def save_transaction(message: Message, state: FSMContext):
    await message.answer('Выберите действие: "Сохранить" или "Отменить"', reply_markup=kb_common.actual_balance_save_keyboard)