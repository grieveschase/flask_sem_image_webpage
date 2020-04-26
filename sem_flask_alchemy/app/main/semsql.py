import os
import sqlite3
import datetime
import io
from io import BytesIO
from PIL import Image
db_file_path = "C://Python3//sem_flask//"
save_image_file_path = "C://Python3//sem_flask//app//static//FOV//"

def lot_selection(tool, lot_form, recipe_form, img_table):
    try:
        conn = sqlite3.connect(db_file_path + tool+'.db', detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        cur = conn.cursor()
        sql_in = '''select distinct
                    Lot,
                    Recipe,
                    Slot,
                    Port,
                    DirDate
                    from {} where Lot like '%{}%' and
                    Recipe like '%{}%' order by DirDate desc'''.format(img_table,lot_form, recipe_form)

        cur.execute(sql_in)
        data = [list(row) for row in cur]
        cur.close()
        conn.close()
    except sqlite3.Error as error:
        print("Error while working with SQLite: ", error)
    finally:
        if conn:
            conn.close()
    return data

def lot_query(l,s,r,p,dd,t, img_table):
    try:
        conn = sqlite3.connect(db_file_path +t+'.db', detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        cur = conn.cursor()
        sql_in = '''select
                    Slot,
                    FOV,
                    Iprobe,
                    Lot,
                    Vhar,
                    Recipe,
                    Site,
                    Field,
                    ToolId,
                    LocationX,
                    LocationY,
                    Date,
                    Port,
                    Cycle,
                    Target,
                    Image
                    from {} where
                    Lot='{}' and
                    Recipe='{}' and
                    Slot={} and
                    Port='{}' and
                    DirDate like '{}%' order by Date asc'''.format(img_table,l,r,s,p, datetime.datetime.strptime(dd, "%Y-%m-%d %H:%M:%S"))

        cur.execute(sql_in)
        data = []
        for row in cur:
            r = list(row)
            print(r[-5])
            html_file_name ="/static/FOV/%s_%s_%s_%s_%s_.jpg"%(r[3],r[5],r[6].replace(" ",""),r[-5].strftime("%Y_%m_%d_%H_%M_%S").strip(),str(r[-3]))
            #save_file_name ="C://Python3//sem_flask//app/static//FOV//%s_%s_%s_%s_%s_.JPG"%(r[3],r[5],r[6],r[-5].strftime("%Y_%m_%d_%H_%M_%S"),str(r[-3]))
            save_file_name =save_image_file_path+"%s_%s_%s_%s_%s_.jpg"%(r[3],r[5],r[6].replace(" ",""),r[-5].strftime("%Y_%m_%d_%H_%M_%S").strip(),str(r[-3]))
            img_blob = r[-1]
            image = Image.open(io.BytesIO(img_blob))
            image.save(save_file_name, quality=80)
            image.close()
            r[-1] = html_file_name
            r[-5] = r[-5].strftime("%Y-%m-%d %H:%M:%S")
            data.append(r)

        cur.close()
        conn.close()
    except sqlite3.Error as error:
        print("Error while working with SQLite: ", error)
    finally:
        if conn:
            conn.close()
    return data

if __name__ =="__main__":
    conn = sqlite3.connect('/home/ccag/' + 'verity401'+'.db', detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = conn.cursor()
    lot = '4938192RS8'
    sql_in = '''select distinct
                Lot,
                Recipe,
                Slot,
                Port,
                DirDate
                from PatternFov where Lot like '%{}%' order by DirDate desc'''.format('49')
    cur.execute(sql_in)
    data = [list(row) for row in cur]
    conn.close()
    print(len(data))
    print(data[0])
    # for i in data:
    #     print(i)
