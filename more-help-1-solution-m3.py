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
