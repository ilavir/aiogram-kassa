import logging

from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards import kb_common

from utils.google_sheets import gs_get_balance


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Hello, <b>{message.from_user.full_name}</b>!', reply_markup=kb_common.common_keyboard)


@router.message(Command('cancel'), ~StateFilter(None))
@router.message(F.text == 'Отменить', ~StateFilter(None))
async def cmd_cancel_transaction(message: Message, state: FSMContext):
    cancel_message = await cancel_trigger(state)
    await message.answer(cancel_message, reply_markup=kb_common.common_keyboard)

async def cancel_trigger(state: FSMContext):
    current_state = await state.get_state()

    if current_state is None:
        return
    elif current_state.startswith('ActualBalance'):
        cancel_message = 'Ввод фактического остатка отменен'
    elif current_state.startswith('AddTransaction'):
        cancel_message = 'Транзакция отменена'
    else:
        cancel_message = 'Нечего отменять'
    
    logging.info('Cancelling state %r', current_state)
    await state.clear()

    return cancel_message


@router.message(Command('get_balance'))
@router.message(F.text == 'Расчетный остаток')
async def cmd_get_balance(message: Message):
    balance = gs_get_balance()
    await message.answer(f'Расчетный остаток: {balance}', reply_markup=kb_common.common_keyboard)