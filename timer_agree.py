import asyncio
import time

import google_sheets
import checking
import datetime
import main
import keyboards

from threading import Thread

id_and_rows = dict()


# Оповещение о подтверждении экскурсии
async def user_agreed():
    tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
    month_str = tomorrow.strftime("%m.%Y")
    sheet = google_sheets.find_sheet(month_str)
    values = sheet.get_all_values()
    cell_list = sheet.findall(tomorrow.strftime("%d.%m.%Y"))
    id_and_rows.clear()
    id_and_rows[0] = sheet
    for cell in cell_list:
        id_and_rows[sheet.cell(cell.row, 1).value] = cell.row

    for id in id_and_rows.keys():
        try:
            await main.bot.send_message(int(id), 'У вас забронирована экскурсия на корабле. Подтвердите ее',
                                        reply_markup=keyboards.Confirm_buttons)
        except:
            print("Неправильный id", id)
        # main.dp.storage.get_data(id)
    when_to_call = main.loop.time() + main.delay  # delay -- промежуток времени в секундах.
    main.loop.call_at(when_to_call, my_callback)


def my_callback():
    asyncio.ensure_future(user_agreed())


def confirm_in_googlesheets(id, text):
    row = id_and_rows[str(id)]
    sheet = id_and_rows[0]
    sheet.update_cell(row, 9, text)
