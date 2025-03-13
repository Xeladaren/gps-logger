
import math

eart_circ = 40_075_016 # meters
meter_by_lat_deg = eart_circ / 360

def lat_to_meter(dlat):
    return meter_by_lat_deg * dlat

def lon_to_meter(dlon, lat):
    return (( eart_circ * math.cos(lat) ) / 360) * dlon

def meter_to_lat(meter):
    return meter / meter_by_lat_deg

def meter_to_lon(meter, lat):
    return meter * ( 360 / ( eart_circ * math.cos(lat) ) )

# better between 1 000 m and 2 000 000 m
def square_box(center: (float, float), size: float):
    delta_lat = meter_to_lat(size/2)
    delta_lon = meter_to_lon(size/2, center[0])

    min_pos = (center[0] - delta_lat, center[1] - delta_lon)
    max_pos = (center[0] + delta_lat, center[1] + delta_lon)

    return (min_pos, max_pos)

def get_link(lat, lon, zoom=10_000):

    center = (lat, lon)
    bbox = square_box(center, zoom)

    return f"https://www.openstreetmap.org/export/embed.html?bbox={bbox[1][1]}%2C{bbox[1][0]}%2C{bbox[0][1]}%2C{bbox[0][0]}&amp;layer=mapnik&amp;marker={center[0]}%2C{center[1]}"