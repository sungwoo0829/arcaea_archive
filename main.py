import gspread
from difflib import SequenceMatcher
import time
import numpy


gc=gspread.service_account(filename="arcaea-archive-0e9be9d11882.json")
main_sh=gc.open_by_url("https://docs.google.com/spreadsheets/d/1K5Bjx0NvI3WzIn92Q3I8o-4rcjshCu5TJARUXbMZlDA/edit")

sh=gc.open_by_url("https://docs.google.com/spreadsheets/d/1AzIQwbwCJkjtlc9RWxX_pLWXuaUuv1P5D4mfEaJDhq8/edit")

all_sheet=main_sh.worksheets()
all_sheet=[x.title for x in all_sheet]
data_sheet=['Arcaea 기록 아카이브','Lv.7',"Lv.8","Lv.9","Lv.9+","Lv.10",'Lv.10+','Lv.11 이상','B30']
nb30_sheet=['Lv.7',"Lv.8","Lv.9","Lv.9+","Lv.10",'Lv.10+','Lv.11 이상']

step=0

if step==0:
    for i in data_sheet:
        sh.worksheet(i).update_title(i+"_old")
    step=1

if step==1:
    for i in [x for x in all_sheet if x not in data_sheet]:
        sh.del_worksheet_by_id(sh.worksheet(i).id)
    
    step=2

if step==2:
    for i in all_sheet:
        main_sh.worksheet(i).copy_to(sh.id)

    for i in range(8,19):
        try:
            sh.get_worksheet(i).update_title(all_sheet[i-8])
        except:
            pass
        if i == 18:
            step=3
            
if step==3:
    for i in data_sheet:
        old_ws = sh.worksheet(i+"_old")
        we = sh.worksheet(i)

        w=we.get_all_values(value_render_option='FORMULA')
        ow=old_ws.get_all_values( value_render_option='FORMULA')

        x=1
        ox=1

        if i in nb30_sheet:

            while True:
                if len(ow)<=ox or len(w)<=x:
                    b = list(zip(*w))[4]
                    c=list([x] for x in b)
                    we.update("E1:E",c)
                    b = list(zip(*w))[6]
                    c=list([x] for x in b)
                    we.update("G1:G",c)
                    sh.del_worksheet_by_id(old_ws.id)
                    break
                elif ow[ox][4]=='0':
                    x+=1
                    ox+=1
                elif ow[ox][4]=='' or w[x][4]=='':
                    if w[x][4]=='':
                        x+=1
                    else:
                        ox+=1
                elif w[x][3]==ow[ox][3] or SequenceMatcher(None,w[x][3],ow[ox][3]).ratio()>=0.8:
                    w[x][4]=ow[ox][4]
                    w[x][6]=ow[ox][6]
                    x+=1
                    ox+=1

                else:
                    x+=1
        else:
            time.sleep(60)
            we.update(1,8,[old_ws.cell(1,8).value()])
            we.update(8,8,[old_ws.cell(8,8).value()])
            sh.del_worksheet_by_id(old_ws.id)


