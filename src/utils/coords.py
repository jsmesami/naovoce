def dd2dms(dd, prec=2):
    dd = abs(dd)
    d = int(dd)
    m = int(dd % 1 * 60)
    s = round(dd * 60 % 1 * 60, prec)
    return d, m, s
