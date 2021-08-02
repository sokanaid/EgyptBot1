import time

import google_sheets
import checking
import datetime
import main
import keyboards
from threading import Thread


# Оповещение о подтверждении экскурсии
async def user_agreed():
    tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
    month_str = tomorrow.strftime("%m.%Y")
    sheet = google_sheets.find_sheet(month_str)
    values = sheet.get_all_values()
    cell_list = sheet.findall(tomorrow.strftime("%d.%m.%Y"))
    id_and_rows = dict()
    for cell in cell_list:
        id_and_rows[sheet.cell(cell.row, 1).value] = cell.row

    for id in id_and_rows.keys():
        await main.bot.send_message(int(id), 'У вас забронирована экскурсия на корабле. Подтвердите ее',
                                    reply_markup=keyboards.Confirm_buttons)
