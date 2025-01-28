from aiogram.fsm.state import StatesGroup, State


class StateUser(StatesGroup):
    main_menu = State()
    enter_token = State()
    get_imei = State()
    statistics = State()
