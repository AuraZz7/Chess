import pygame as pg


def strip_coordinates_from_sheet(sheet, coordinates, size, desired_size=None):
    frames = []
    sheet = pg.image.load(sheet).convert_alpha()
    for i, coord in enumerate(coordinates):
        top_left = pg.Rect(coord, size)
        img = pg.transform.smoothscale(sheet.subsurface(pg.Rect(top_left)), desired_size)
        frames.append(img)
    return frames
