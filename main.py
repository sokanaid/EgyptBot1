from aiogram import Bot, Dispatcher, executor, types
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import config
import keyboards
import states

bot = Bot(config.Token)
dp = Dispatcher(bot)  # , storage=MemoryStorage())


# Начало работы приветствие
@dp.message_handler(commands=['start'], state='*')
async def start_message(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Привет!")
    await bot.send_message(message.from_user.id, "Я бот помошник по бронированию морской прогулки в красное море "
                                                 "от команды \"Utopia Team\"",
                           reply_markup=keyboards.Next_step_button)
    await states.user.Start_chat.set()


# Предложение заполнить данные
@dp.message_handler(text=keyboards.Next_step_button.text, state=states.user.Start_chat)
async def start_survey(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Для бронирования Для бронирования на морскую прогулку нужно"
                                                 " сделать простые шаги, мы поможем тебе в этом:"
                                                 " \n- укажите свое ФИО,"
                                                 " \n- отель, \n- номер комнаты,"
                                                 " \n- желаемую дату поездки, \n- количество человек."
                           , keyboards.Enter_data_button)
    await states.User.next()


# Предложение ввести ФИО
@dp.message_handler(text=keyboards.Next_step_button.text, state=states.user.Start_survey)
async def send_name(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Введите ФИО")
    await states.User.next()


# Предложение ввести отель
@dp.message_handler(text=keyboards.Next_step_button.text, state=states.user.Entered_name)
async def send_hotel_name(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Введите название отеля")
    await states.User.next()


# Предложение ввести номер комнаты
@dp.message_handler(text=keyboards.Next_step_button.text, state=states.user.Entered_hotel_name)
async def send_room_number(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Введите номер комнаты")
    await states.User.next()


# Предложение ввести дату экскурсии
@dp.message_handler(text=keyboards.Next_step_button.text, state=states.user.Entered_room_number)
async def send_date(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Введите дату экскурсии")
    await states.User.next()


# Предложение колличество людей
@dp.message_handler(text=keyboards.Next_step_button.text, state=states.user.Entered_room_number)
async def send_people_number(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Введите колличество людей")
    await states.User.next()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
