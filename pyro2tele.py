import sqlite3, os, glob

sessions = glob.glob('*.session')
for file_session in sessions:

    if '_telethon' in file_session:
        continue
    
    file_session_telethon = file_session.replace('.session','_telethon.session')

    try:
        os.remove(file_session_telethon)
    except Exception as e:
        print(e)

    tele_server_adress = '149.154.167.92'
    tele_port = 443

    try:

        sqlite_connection_pyro = sqlite3.connect(file_session)
        sqlite_connection_tele = sqlite3.connect(file_session_telethon)
        
        pyro_cursor = sqlite_connection_pyro.cursor()
        tele_cursor = sqlite_connection_tele.cursor()

        keys = []

        for row in pyro_cursor.execute("pragma table_info('sessions')").fetchall():
            keys.append(row[1])

        sqlite_select_query = """SELECT * from sessions"""
        pyro_cursor.execute(sqlite_select_query)
        session = pyro_cursor.fetchone()
        session_dict = {}
        for index, value in enumerate(session):
            session_dict[keys[index]] = value
            print(keys[index],': ', value)
        pyro_cursor.close()


        #create telethon tables
        print('create table sessions')

        sqlite_create_table_query = '''CREATE TABLE sessions (
                                    dc_id INTEGER PRIMARY KEY,
                                    server_adress TEXT,
                                    port INTEGER,
                                    auth_key BLOB,
                                    takeout_id INTEGER);'''

        tele_cursor.execute(sqlite_create_table_query)

        print('create table entities')
        sqlite_create_table_query = '''CREATE TABLE entities (
                                    id INTEGER PRIMARY KEY,
                                    hash INTEGER,
                                    username text,
                                    phone INTEGER,
                                    name text,
                                    date INTEGER);'''

        tele_cursor.execute(sqlite_create_table_query)

        print('create table sent_files')

        sqlite_create_table_query = '''CREATE TABLE sent_files (
                                    md5_digest BLOB,
                                    file_size INTEGER,
                                    type INTEGER,
                                    id INTEGER,
                                    hash INTEGER,
                                    PRIMARY KEY (md5_digest, file_size, type));'''

        tele_cursor.execute(sqlite_create_table_query)

        sqlite_create_table_query = '''CREATE TABLE update_state (
                                    id INTEGER PRIMARY KEY,
                                    pts INTEGER,
                                    qts INTEGER,
                                    date INTEGER,
                                    seq INTEGER);'''

        tele_cursor.execute(sqlite_create_table_query)
        
        print('create table version')

        sqlite_create_table_query = '''CREATE TABLE version (
                                    version INTEGER PRIMARY KEY);'''

        tele_cursor.execute(sqlite_create_table_query)

        sqlite_connection_tele.commit()
                
        print('tables created success')
        
        sqlite_insert_query = f"""INSERT INTO sessions  (dc_id, server_adress, port, auth_key, takeout_id)  VALUES  ({session_dict['dc_id']}, "{tele_server_adress}", {tele_port}, ?, null)"""

        tele_cursor.execute(sqlite_insert_query, (memoryview(session_dict['auth_key']),))

        sqlite_insert_query = f"""INSERT INTO version  (version)  VALUES  (7)"""

        tele_cursor.execute(sqlite_insert_query)
        sqlite_connection_tele.commit()

        tele_cursor.close()
    
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection_pyro):
            sqlite_connection_pyro.close()
            print("sqlite connect sqlite_connection_pyro closed")


        if (sqlite_connection_tele):
            sqlite_connection_tele.close()
            print("sqlite connect sqlite_connection_tele closed")


    from telethon.sync import TelegramClient, events

    try:
        print(file_session_telethon)
        with TelegramClient(file_session_telethon.replace('.session',''), 20886214, "ba51cbd8e8f1dd0fce0d755ce0970600") as client:

            me = client.get_me()
            print(me)

    except Exception as e:
        os.remove(file_session_telethon)
        print('BAD SESSION: ', file_session_telethon)
    
