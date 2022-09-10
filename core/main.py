from core.prepare import *
from core import game


def main():
    running = True
    while running:
        clock.tick(fps)

        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False

        game.board.draw()
        game.board.update()

        pg.display.update()
