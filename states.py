from aiogram.dispatcher.filters.state import State, StatesGroup


class User(StatesGroup):
    Started_chat = State()
    Started_survey = State()
    Entered_name = State()
    Entered_hotel_name = State()
    Entered_room_number = State()
    Chose_date = State()
    Entered_number_of_children = State()
    Entered_number_of_adults = State()
    Sent_form = State()
