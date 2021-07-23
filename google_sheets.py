# import httplib2
# import apiclient.discovery
# from oauth2client.service_account import ServiceAccountCredentials
# import pprint
import gspread

CREDENTIALS_FILE = 'tableforegyptbot.json'  # имя файла с закрытым ключом
gc = gspread.service_account(filename=CREDENTIALS_FILE)

sht = gc.open_by_url('https://docs.google.com/spreadsheets/d/1Yx3HqvBdnMn4Uc70rjH3HKFgqZXDFkoFIqLRfRwciZ0')


# sht.add_worksheet("Test2", rows='0', cols='5')
# sht.worksheet('Test2').append_row([2, 2, 2, 2, 2])

def find_sheet(name):
    try:
        return sht.worksheet(name)
    except Exception:
        sht.add_worksheet(name, rows='0', cols='7')

        sht.worksheet(name).append_row(
            ['id', 'Дата', 'ФИО', 'Название отеля', 'Номер комнаты', 'Число взрослых', 'Число детей', 'Номер телефона',
             'Подтверждено'])
        sht.worksheet(name).format('A1:I1', {'textFormat': {'bold': True}})
        # sht.add_worksheet(name).set_basic_filter('A1:F1')
        return sht.worksheet(name)


def write_data(dialog_id, name, hotel, room_number, date, number_of_adults, number_of_children, phone_number, sheet):
    sheet.append_row([dialog_id, date, name, hotel, room_number, number_of_adults, number_of_children, phone_number])
