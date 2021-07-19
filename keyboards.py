from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

Next_step_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
Next_step_button.add(KeyboardButton("Далее"))

Enter_data_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
Enter_data_button.add(KeyboardButton("Ввести данные"))
