
def pos_to_str_dms(pos, axe):

        dir  = axe[0] if pos >= 0  else axe[1]
        pos  = abs(pos)
        deg  = int(pos)
        min  = (pos  - deg)  * 60
        sec  = (min  - int(min))  * 60
        min  = int(min)

        return f"{deg}&deg; {min}' {sec:.2f}'' {dir}"