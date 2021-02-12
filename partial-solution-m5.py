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
