from django.template import Library

from utils.coords import dd2dms


register = Library()


DMS_FMT = '{}\u00B0{}\u2032{}\u2033{dir}'


@register.simple_tag
def dms_coords(lt, lg, fmt='{lt},&nbsp;{lg}', prec=2):
    return fmt.format(
        lt=DMS_FMT.format(*dd2dms(lt, prec), dir='S' if lt < 0 else 'N'),
        lg=DMS_FMT.format(*dd2dms(lg, prec), dir='W' if lg < 0 else 'E'),
    )
