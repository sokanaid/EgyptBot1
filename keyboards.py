from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

Next_step_buttons = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
Next_step_button = KeyboardButton("Далее")
Next_step_buttons.add(Next_step_button)

Enter_data_buttons = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
Enter_data_button = KeyboardButton("Ввести данные")
Enter_data_buttons.add(Enter_data_button)

Sent_form_buttons = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
Sent_form_button = KeyboardButton("Отправить заявку")
Edit_form_button = KeyboardButton("Изменить заявку")
Sent_form_buttons.add(Sent_form_button)
Sent_form_buttons.add(Edit_form_button)

New_form_buttons = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
New_form_button = KeyboardButton("Создать новую заявку")
New_form_buttons.add(New_form_button)

Confirm_buttons = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
Confirm_button1 = KeyboardButton("Подтверждаю заявку на экскурсию")
Confirm_button2 = KeyboardButton("Отменить заявку на экскурсию")
Confirm_buttons.add(Confirm_button1).add(Confirm_button2)

Send_phone_number_buttons = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Отправить свой контакт ☎️', request_contact=True))