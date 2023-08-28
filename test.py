import gspread
from difflib import SequenceMatcher
import time
import numpy

gc=gspread.service_account(filename="arcaea-archive-0e9be9d11882.json")
main_sh=gc.open_by_url("https://docs.google.com/spreadsheets/d/1K5Bjx0NvI3WzIn92Q3I8o-4rcjshCu5TJARUXbMZlDA/edit")

a=main_sh.worksheets()
a=[x.title for x in a]
print(a)
