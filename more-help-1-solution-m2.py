def createhashtable():
    """Creates a SQLite DB Table"""
    result = False
    query = "CREATE TABLE files (file TEXT, md5 TEXT)"
    conn = connectdb()
    try:
        if not conn is None:
            if not tableexists('files'):
                cursor = conn.cursor()
                try:
                    cursor.execute(query)
                except sqlite3.OperationalError:
                    if cursor != None:
                        cursor.close()
                finally:
                    conn.commit()
                    if cursor != None:
                        cursor.close()
                    result = True
    except sqlite3.OperationalError as err:
        print(str(err))
        if conn != None:
            conn.close()
    finally:
        if conn != None:
            conn.close()
    return result