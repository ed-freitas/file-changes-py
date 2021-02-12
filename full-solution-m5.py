import os
import sys
import sqlite3
import hashlib

# From milestones 1 and 2
def getbasefile():
    """Name of the SQLite DB file"""
    return os.path.splitext(os.path.basename(__file__))[0]

def connectdb():
    """Connect to the SQLite DB"""
    try:
        dbfile = getbasefile() + '.db'
        conn = sqlite3.connect(dbfile, timeout=2)
    except BaseException as err:
        print(str(err))
        conn = None
    return conn

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
    conn = connectdb()
    try:
        if not conn is None:
            if tableexists('files'):
                cursor = conn.cursor()
                try:
                    cursor.execute(qry, args)
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

def updatehashtable(fname, md5):
    """Update the SQLite File Table"""
    qry = "UPDATE files SET md5=? WHERE file=?"
    args = (md5, fname)
    runcmd(qry, args)

def inserthashtable(fname, md5):
    """Insert into the SQLite File Table"""
    qry = "INSERT INTO files (file, md5) VALUES (?, ?)"
    args = (fname, md5)
    runcmd(qry, args)

def setuphashtable(fname, md5):
    """Setup's the Hash Table"""
    createhashtable()
    createhashtableidx()
    inserthashtable(fname, md5)

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

# From milestone 3
def haschanged(fname, md5):
    """Checks if a file has changed"""
    result = False
    oldmd5 = md5indb(fname)
    numits = len(oldmd5)
    if numits > 0:
        if oldmd5[0] != md5:
            result = True
            updatehashtable(fname, md5)
    else:
        setuphashtable(fname, md5)
    return result

def getfileext(fname):
    """Get the file name extension"""
    return os.path.splitext(fname)[1]

def getmoddate(fname):
    """Get file modified date"""
    try:
        mtime = os.path.getmtime(fname)
    except OSError as emsg:
        print(str(emsg))
        mtime = 0
    return mtime

def md5short(fname):
    """Get md5 file hash tag"""
    return hashlib.md5(str(fname + '|' + str(getmoddate(fname))).encode('utf-8')).hexdigest()

# From milestone 4
def checkfilechanges(folder, exclude, ws):
    changed = False
    """Checks for files changes"""
    for subdir, dirs, files in os.walk(folder):
        for fname in files:
            origin = os.path.join(subdir, fname)
            if os.path.isfile(origin):
                fext = getfileext(origin)
                if not fext in exclude:
                    md5 = md5short(origin)
                    headerxlsreport(ws) # To be done in the last milestone
                    if haschanged(origin, md5):
                        # To be done in the last milestone
                        now = getdt("%d-%b-%Y %H:%M:%S")
                        dt = now.split(' ')
                        # To be done in the last milestone
                        rowxlsreport(ws, fname, origin, subdir, dt[0], dt[1])
                        print(origin + ' has changed on ' + now)
                        changed = True
    return changed

def loadflds():
    flds = []
    ext = []
    config = getbasefile() + '.ini'
    if os.path.isfile(config):
        cfile = open(config, 'r')
        for line in cfile.readlines():
            if '|' in line:
                flds.append(line.split('|')[0])
                exts = line.split('|')[1]
                if len(exts) > 0:
                    extl = exts.split(',')
                    ext.append(extl)
            else:
                flds.append(line)
                ext.append([])
        cfile.close()
    return flds, ext

def runfilechanges(ws):
    changed = False
    fldexts = loadflds()
    for i, fld in enumerate(fldexts[0]):
        exts = fldexts[1]
        changed = checkfilechanges(fld, exts[i], ws)
    return changed

# Milestone 5
def execute(args):
    chn = 0
    if len(args) > 1:
        if args[1].lower() == '--loop':
            # To be done in the last milestone
            wb, ws, st = startxlsreport()
            try:
                while True:
                    changed = runfilechanges(ws)
                    if changed:
                        chn += 1
            except KeyboardInterrupt:
                print('Stopped...')
                if chn > 0:
                    # To be done in the last milestone
                    endxlsreport(wb, st)
    else:
        # To be done in the last milestone
        wb, ws, st = startxlsreport()
        changed = runfilechanges(ws)
        if changed:
            # To be done in the last milestone
            endxlsreport(wb, st)

if __name__ == '__main__':
    execute(sys.argv)
