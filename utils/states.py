from aiogram.fsm.state import StatesGroup, State

class AddTransaction(StatesGroup):
    GET_DATE = State()
    GET_TYPE = State()
    GET_SUM = State()
    GET_CATEGORY = State()
    GET_DESCRIPTION = State()
    SAVE = State()

class ActualBalance(StatesGroup):
    GET_DATE = State()
    GET_SUM = State()
    SAVE = State()