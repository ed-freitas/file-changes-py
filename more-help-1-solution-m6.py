def startxlsreport():
    wb = Workbook()
    ws = wb.active
    ws.title = socket.gethostname()
    st = getdt("%d-%b-%Y %H_%M_%S")
    return wb, ws, st
