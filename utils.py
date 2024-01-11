from shapely import wkt
from geoalchemy2 import functions, WKBElement
from shapely.wkb import loads
import threading
import time

def convert_to_point(location: tuple):
    return f"POINT({location[0]} {location[1]})"


def get_coordinates_from_geom(geom: WKBElement) -> tuple:
    shapely_geometry = loads(bytes(geom.data))
    x_coordinates, y_coordinates = shapely_geometry.coords.xy
    return (x_coordinates[0], y_coordinates[0])


def set_interval(func, interval_in_seconds: int):
    def wrapper():
        while True:
            func()
            time.sleep(interval_in_seconds)

    thread = threading.Thread(target=wrapper)
    thread.daemon = True
    thread.start()