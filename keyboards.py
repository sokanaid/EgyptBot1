from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

Next_step_buttons = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
Next_step_button = KeyboardButton("Далее")
Next_step_buttons.add(Next_step_button)

Enter_data_buttons = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
Enter_data_button = KeyboardButton("Ввести данные")
Enter_data_buttons.add(Enter_data_button)

Sent_form_buttons = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
Sent_form_button = KeyboardButton("Отправить заявку")
Sent_form_buttons.add(Sent_form_button)
