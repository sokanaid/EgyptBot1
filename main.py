from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram_calendar import simple_cal_callback, SimpleCalendar
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, ReplyKeyboardMarkup, ContentType
import config
import keyboards
import states
import google_sheets
import checking
import datetime

bot = Bot(config.Token)
dp = Dispatcher(bot, storage=MemoryStorage())


# Начало работы приветствие
@dp.message_handler(commands=['start'], state='*')
async def start_message(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Привет!")
    await bot.send_message(message.from_user.id, "Я бот помошник по бронированию морской прогулки в красное море "
                                                 "от команды \"Utopia Team\"",
                           reply_markup=keyboards.Next_step_buttons)
    await states.User.Started_chat.set()


# Предложение заполнить данные
@dp.message_handler(text=keyboards.Next_step_button.text, state=states.User.Started_chat)
async def start_survey(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Для бронирования Для бронирования на морскую прогулку нужно"
                                                 " сделать простые шаги, мы поможем тебе в этом:"
                                                 " \n- укажите свое ФИО,"
                                                 " \n- отель, \n- номер комнаты,"
                                                 " \n- желаемую дату поездки, \n- количество человек."
                           , reply_markup=keyboards.Enter_data_buttons)
    await states.User.next()


# Предложение ввести ФИО
@dp.message_handler(text=keyboards.Enter_data_button.text, state=states.User.Started_survey)
async def send_name(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Введите ФИО", reply_markup=types.ReplyKeyboardRemove())
    await states.User.next()


# Предложение ввести ФИО
@dp.message_handler(text=keyboards.Edit_form_button.text, state=states.User.Sent_form)
async def send_name1(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Введите ФИО", reply_markup=types.ReplyKeyboardRemove())
    await states.User.Entered_name.set()


# Предложение ввести отель
@dp.message_handler(state=states.User.Entered_name)
async def send_hotel_name(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Введите название отеля")
    await states.User.next()
    async with state.proxy() as data:
        data['name'] = message.text


# Предложение ввести номер комнаты
@dp.message_handler(state=states.User.Entered_hotel_name)
async def send_room_number(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Введите номер комнаты")
    await states.User.next()
    async with state.proxy() as data:
        data['hotel'] = message.text


# Предложение ввести номер телефона
@dp.message_handler(state=states.User.Entered_room_number)
async def send_phone_number(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Нажмите на кнопку для ввода номера телефона."
                           , reply_markup=keyboards.Send_phone_number_buttons)
    await states.User.next()
    async with state.proxy() as data:
        data['room_number'] = message.text


# Предложение ввести дату экскурсии
@dp.message_handler(content_types=ContentType.CONTACT, state=states.User.Entered_phone_number)
async def send_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        #print( message.contact.phone_number)
        data['phone_number'] = message.contact.phone_number

    await message.answer("Введите дату экскурсии", reply_markup=types.ReplyKeyboardRemove())
    await message.answer("-", reply_markup=await SimpleCalendar().start_calendar())
    await states.User.next()


# Предложение ввести колличество детей
@dp.callback_query_handler(simple_cal_callback.filter(), state=states.User.Chose_date)
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'Вы выбрали {date.strftime("%d.%m.%Y")}'
        )
        now = datetime.datetime.today()
        if now >= date:
            await callback_query.message.answer('Введенная дата некорректна. Выберите другую.',
                                                reply_markup=await SimpleCalendar().start_calendar())
            return
        async with state.proxy() as data:
            data['date'] = date
        await callback_query.message.answer('Введите число детей не достигших 14 лет')
        await states.User.next()


# Предложение ввести колличество взрослых
@dp.message_handler(state=states.User.Entered_number_of_children)
async def send_adults(message: types.Message, state: FSMContext):
    if not checking.is_number_of_people(message.text):
        await bot.send_message(message.from_user.id, 'Введенное значение не корректно. Введите число еще раз')
        return
    async with state.proxy() as data:
        data['number_of_children'] = message.text
    await bot.send_message(message.from_user.id, 'Введите число взрослых ')
    await states.User.next()


# Подтвердить отправку заявку
@dp.message_handler(state=states.User.Entered_number_of_adults)
async def send_form(message: types.Message, state: FSMContext):
    if not checking.is_number_of_people(message.text):
        await bot.send_message(message.from_user.id, 'Введенное значение не корректно. Введите число еще раз')
        return
    async with state.proxy() as data:
        data['number_of_adults'] = message.text
    async with state.proxy() as data:
        await bot.send_message(message.from_user.id, "Подтвердите заявку: \n ФИО:" + data['name'] +
                               "\n Отель:" + data['hotel'] + "\n Номер комнаты:" + data['room_number'] +
                               "\n Номер телефона:" + data['phone_number'] +
                               "\n Число взрослых:" + data['number_of_adults'] + "\n Число детей младше 14 лет:"
                               + data['number_of_children'] + "\n Дата:" +
                               data['date'].strftime("%d.%m.%Y"),
                               reply_markup=keyboards.Sent_form_buttons)
    await states.User.next()


@dp.message_handler(text=keyboards.Sent_form_button.text, state=states.User.Sent_form)
async def sent_form(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        sheet = google_sheets.find_sheet(data['date'].strftime("%m.%Y"))
        google_sheets.write_data(message.from_user.id, data['name'], data['hotel'], data['room_number'],
                                 data['date'].strftime("%d.%m.%Y"), data['number_of_adults'],
                                 data['number_of_children'],
                                 data['phone_number'], sheet)
    await bot.send_message(message.from_user.id, "Ваша заявка отправлена. За день до экскурсии мы попросим" +
                           " вас подтвердить ее. В случае изменений менеджер свяжется"
                           " с вами по указанному номеру через Telegram", reply_markup=keyboards.New_form_buttons)
    await states.User.next()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
