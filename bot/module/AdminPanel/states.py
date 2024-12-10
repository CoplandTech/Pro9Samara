from aiogram.dispatcher.filters.state import State, StatesGroup

class AdminPanelState(StatesGroup):
    activ = State()
    users = State()
    reqs = State()
    reqs_tools = State()
    reqs_photoshoots = State()
    reqs_busscons = State()
    publications = State()
    tools = State()
    posts = State()