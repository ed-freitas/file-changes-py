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