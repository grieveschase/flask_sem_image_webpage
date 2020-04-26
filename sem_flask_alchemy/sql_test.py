import sqlite3
import datetime
import io
from io import BytesIO
from PIL import Image

def get_measdisplay(db_file, db_table):
    try:

        conn = sqlite3.connect(db_file, detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        cur = conn.cursor()
        sql_in = '''select distinct
                    slot,
                    fov,
                    iprobe,
                    lot,
                    vacc,
                    vhar,
                    recipe,
                    site_type,
                    site_order,
                    fieldx,
                    fieldy,
                    locx,
                    locy,
                    date,
                    port,
                    cycle,
                    target,
                    measdate,
                    image from %s LIMIT 100'''%db_table
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
def insert_data_dev(table, new_data):
    try:
        db_file= "data-dev.sqlite"
        conn = sqlite3.connect(db_file, detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        cur = conn.cursor()
        sql_insert = '''INSERT INTO '%s'
                        ('tool',
                        'slot',
                        'fov',
                        'iprobe',
                        'lot',
                        'vacc',
                        'vhar',
                        'recipe',
                        'site_type',
                        'site_order',
                        'fieldx',
                        'fieldy',
                        'locx',
                        'locy',
                        'date',
                        'port',
                        'cycle',
                        'target',
                        'measdate',
                        'image')
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);'''%table
        cur.execute(sql_insert, new_data)
        conn.commit()
        cur.close()
        conn.close()

    except sqlite3.Error as error:
        print("Error while working with SQLite: ", error)
    finally:
        if conn:
            conn.close()

def pop_sem_data_dev_db():
    db_file= "vera402.db"
    table = "vera402_obs"
    data = get_measdisplay(db_file)
    new_data = []
    for i in data:
        slot = int(i[0])
        fov = i[1]
        ip = i[2]
        lot = i[3]
        vacc = 500
        vhar = int(i[4].split()[0])
        recipe = i[5]
        site_type = i[6].split()[0]
        site_order = int(i[6].split()[1])
        fieldx = i[8]
        fieldy = i[9]
        locx = i[10]
        locy = i[11]
        date = i[12]
        port = int(i[13][1])
        cycle = i[14]
        target = i[15]
        measdate = i[16]
        image = i[-1]
        new_data.append([slot, fov, ip, lot, vacc, vhar, recipe, site_type, site_order, fieldx, fieldy, locx, locy, date, port, cycle, target, measdate, image ])
    for tic in new_data:
        insert_data_dev(table, tic)
    print("DONE VERA402")

    db_file= "vera401.sqlite"
    table = "vera401_obs"
    data = get_measdisplay(db_file)
    new_data = []
    for i in data:
        slot = int(i[0])
        fov = i[1]
        ip = i[2]
        lot = i[3]
        vacc = 500
        vhar = int(i[4].split()[0])
        recipe = i[5]
        site_type = i[6].split()[0]
        site_order = int(i[6].split()[1])
        fieldx = i[8]
        fieldy = i[9]
        locx = i[10]
        locy = i[11]
        date = i[12]
        port = int(i[13][1])
        cycle = i[14]
        target = i[15]
        measdate = i[16]
        image = i[-1]
        new_data.append([slot, fov, ip, lot, vacc, vhar, recipe, site_type, site_order, fieldx, fieldy, locx, locy, date, port, cycle, target, measdate, image ])
    for tic in new_data:
        insert_data_dev(table, tic)
    print("DONE VERA401")

    db_file= "verity401.db"
    table = "verity401_obs"
    data = get_measdisplay(db_file)
    new_data = []
    for i in data:
        slot = int(i[0])
        fov = i[1]
        ip = i[2]
        lot = i[3]
        vacc = 500
        vhar = int(i[4].split()[0])
        recipe = i[5]
        site_type = i[6].split()[0]
        site_order = int(i[6].split()[1])
        fieldx = i[8]
        fieldy = i[9]
        locx = i[10]
        locy = i[11]
        date = i[12]
        port = int(i[13][1])
        cycle = i[14]
        target = i[15]
        measdate = i[16]
        image = i[-1]
        new_data.append([slot, fov, ip, lot, vacc, vhar, recipe, site_type, site_order, fieldx, fieldy, locx, locy, date, port, cycle, target, measdate, image ])
    for tic in new_data:
        insert_data_dev(table, tic)
    print("DONE VERITY401")


#Slot,FOV,Iprobe,Lot,Vhar,Recipe,Site,Field,FieldX,FieldY,ToolId,LocationX,LocationY,Date,Port,Cycle,Target,DirDate
if __name__ == "__main__":
    # backup_db = "backup_db.sqlite"
    # backup_table = "vera401_obs"
    # data_backup = get_measdisplay(backup_db, backup_table)
    # new_table = "measdisplay_obs"
    # for tic in data_backup:
    #     tic.insert(0,'vera401')
    #     insert_data_dev(new_table, tic)
    #
    # backup_db = "backup_db.sqlite"
    # backup_table = "verity401_obs"
    # data_backup = get_measdisplay(backup_db, backup_table)
    # new_table = "measdisplay_obs"
    # for tic in data_backup:
    #     tic.insert(0,'verity401')
    #     insert_data_dev(new_table, tic)

    backup_db = "backup_db_fov.sqlite"
    backup_table = "vera401_fov"
    data_backup = get_measdisplay(backup_db, backup_table)
    new_table = "patternfov"
    for tic in data_backup:
        tic.insert(0,'vera401')
        insert_data_dev(new_table, tic)

    backup_db = "backup_db_fov.sqlite"
    backup_table = "verity401_fov"
    data_backup = get_measdisplay(backup_db, backup_table)
    new_table = "patternfov"
    for tic in data_backup:
        tic.insert(0,'verity401')
        insert_data_dev(new_table, tic)
