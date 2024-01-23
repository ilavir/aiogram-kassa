import gspread
import re

from config_reader import config

gc = gspread.service_account(filename=config.sheets_token_file.get_secret_value())

wks = gc.open_by_key('1R-ru-anppfJyt9FiGvm-Ny2ZcPz8TACidv26neURZLk').sheet1

def gs_save_transaction(date, type, value, category, description):
    count = 0
    all_rows = wks.get()

    for row in all_rows:
        count += 1

    wks.append_row([date, type, value, category, description,
                    f'=SWITCH(B{count+1},"Поступление",F{count}+C{count+1},"Выбытие",F{count}-C{count+1})'],
                    value_input_option='USER_ENTERED')
    
    return wks.acell(f'F{count+1}').value

def gs_get_balance():
    count = 0
    all_rows = wks.get()

    for row in all_rows:
        count += 1

    return wks.acell(f'F{count}').value

def gs_add_actual_balance(date, value):
    rows = wks.findall(date)
    row_num = re.search(r'R(\d+)', str(rows[-1]).split()[1]).group(1)
    wks.update(values=[[float(value)]], range_name=f'G{row_num}')