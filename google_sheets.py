# import httplib2
# import apiclient.discovery
# from oauth2client.service_account import ServiceAccountCredentials
# import pprint
import gspread

CREDENTIALS_FILE = 'tableforegyptbot.json'  # имя файла с закрытым ключом
"""credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                               ['https://www.googleapis.com/auth/spreadsheets',
                                                                'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())

service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)"""
gc = gspread.service_account(filename=CREDENTIALS_FILE)

sht = gc.open_by_url('https://docs.google.com/spreadsheets/d/1Yx3HqvBdnMn4Uc70rjH3HKFgqZXDFkoFIqLRfRwciZ0')


# sht.add_worksheet("Test2", rows='0', cols='5')
# sht.worksheet('Test2').append_row([2, 2, 2, 2, 2])

def find_sheet(name):
    try:
        return sht.worksheet(name)
    except Exception:
        sht.add_worksheet(name, rows='0', cols='6')

        sht.worksheet(name).append_row(
            ['id', 'Дата', 'ФИО', 'Название отеля', 'Номер комнаты', 'Колличество людей'])
        sht.worksheet(name).format('A1:F1', {'textFormat': {'bold': True}})
        #sht.add_worksheet(name).set_basic_filter('A1:F1')
        return sht.worksheet(name)


def write_data(dialog_id, name, hotel, room_number, date, number_of_people, sheet):
    sheet.append_row([dialog_id, date, name, hotel, room_number, number_of_people])
