import os
import sys
import sqlite3

# From milestone 1
def getbasefile():
    """Name of the SQLite DB file"""
    return os.path.splitext(os.path.basename(__file__))[0]

# From milestone 1
def connectdb():
    """Connect to the SQLite DB"""
    try:
        dbfile = getbasefile() + '.db'
        conn = sqlite3.connect(dbfile, timeout=2)
    except BaseException as err:
        print(str(err))
        conn = None
    return conn

# From milestone 1
def corecursor(conn, query, args):
    """Opens a SQLite DB cursor"""
    result = False
    cursor = conn.cursor()
    try:
        cursor.execute(query, args)
        rows = cursor.fetchall()
        numrows = len(list(rows))
        if numrows > 0:
            result = True
    except sqlite3.OperationalError as err:
        print(str(err))
        if cursor != None:
            cursor.close()
    finally:
        if cursor != None:
            cursor.close()
    return result

# From milestone 1
def tableexists(table):
    """Checks if a SQLite DB Table exists"""
    result = False
    conn = connectdb()
    try:
        if not conn is None:
            qry = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
            args = (table,)
            result = corecursor(conn, qry, args)
            if conn != None:
                conn.close()
    except sqlite3.OperationalError as err:
        print(str(err))
        if conn != None:
            conn.close()
    return result

def createhashtableidx():
    """Creates a SQLite DB Table Index"""
    table = 'files'
    query = 'CREATE INDEX idxfile ON files (file, md5)'
    conn = connectdb()
    try:
        if not conn is None:
            if tableexists(table):
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
    except sqlite3.OperationalError as err:
        print(str(err))
        if conn != None:
            conn.close()
    finally:
        if conn != None:
            conn.close()

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

def runcmd(qry, args):
    """Run a specific command on the SQLite DB"""

def updatehashtable(fname, md5):
    """Update the SQLite File Table"""

def inserthashtable(fname, md5):
    """Insert into the SQLite File Table"""

def setuphashtable(fname, md5):
    """Setup's the Hash Table"""

def md5indb(fname):
    """Checks if md5 hash tag exists in the SQLite DB"""
    items = []
    qry = "SELECT md5 FROM files WHERE file= ?"
    args = (fname,)
    conn = connectdb()
    try:
        if not conn is None:
            if tableexists('files'):
                cursor = conn.cursor()
                try:
                    cursor.execute(qry, args)
                    for row in cursor:
                        items.append(row[0])
                except sqlite3.OperationalError as err:
                    print(str(err))
                    if cursor != None:
                        cursor.close()
                finally:
                    if cursor != None:
                        cursor.close()
    except sqlite3.OperationalError as err:
        print(str(err))
        if conn != None:
            conn.close()
    finally:
        if conn != None:
            conn.close()
    return items
