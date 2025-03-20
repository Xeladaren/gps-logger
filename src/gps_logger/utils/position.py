
def dist_to_zoom(dist):

    for i in range(0, 12):
        if dist < 1024 * 2**i:
            return 17 - i

    return 5

def pos_to_str_dms(pos, axe):

    dir  = axe[0] if pos >= 0  else axe[1]
    pos  = abs(pos)
    deg  = int(pos)
    min  = (pos  - deg)  * 60
    sec  = (min  - int(min))  * 60
    min  = int(min)

    return f"{deg}&deg; {min}' {sec:.2f}'' {dir}"

def dist_human(dist):

    if dist >= 1e6:
        return f"{dist/1e6:.1f} Mm"
    elif dist >= 1e3:
        return f"{dist/1e3:.1f} km"
    else:
        return f"{int(dist)} m"