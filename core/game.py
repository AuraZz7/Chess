from core.prepare import *
import math


class Board:
    def __init__(self):
        self.grid = [(x, y) for x in range(rows) for y in range(cols)]
        self.grid = [i for i in range(rows*cols)]
        self.pieces = {
            0: "b_r", 1: "b_k", 2: "b_b", 3: "b_queen", 4: "b_king", 5: "b_b", 6: "b_k", 7: "b_r",
            8: "b_p", 9: "b_p", 10: "b_p", 11: "b_p", 12: "b_p", 13: "b_p", 14: "b_p", 15: "b_p",
            48: "w_p", 49: "w_p", 50: "w_p", 51: "w_p", 52: "w_p", 53: "w_p", 54: "w_p", 55: "w_p",
            56: "w_r", 57: "w_k", 58: "w_b", 59: "w_queen", 60: "w_king", 61: "w_b", 62: "w_k", 63: "w_r"
        }
        self.active_piece = {}
        self.active_offset = 0

        self.clicked = False

    def update(self):
        pos = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()[0]
        if 0 <= pos[0] <= SCREEN_WIDTH and 0 <= pos[1] <= SCREEN_HEIGHT:
            x, y = math.floor(pos[0] / TILE_SIZE), math.floor(pos[1] / TILE_SIZE)
            tile = self.get_tile_from_pos((x, y))
            if click:
                if not self.clicked:
                    self.clicked = True

                    self.active_piece[tile] = self.pieces[tile]
                    self.pieces.pop(tile)

                    self.active_offset = (pos[0] - 0.5*TILE_SIZE, pos[1] - 0.5*TILE_SIZE)

            if not click and self.clicked:
                self.clicked = False

                self.pieces[tile] = self.active_piece[tile]
                self.active_piece.pop(tile)

    def draw(self):
        self.draw_grid()
        self.draw_pieces()
        self.draw_active_piece()

    def draw_grid(self):
        """
        Draw the background with a checkered pattern
        """
        for tile in self.grid:
            x, y = self.get_pos_from_tile(tile)
            rect = (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if (x+y) % 2 == 0:
                pg.draw.rect(screen, board_col1, rect)
            else:
                pg.draw.rect(screen, board_col2, rect)

    def draw_pieces(self):
        """
        Draws all the pieces in dict 'self.pieces' to the board
        """
        for piece in self.pieces.items():
            x, y = self.get_pos_from_tile(piece[0])
            rect = (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            colour, p_type = piece[1][:2], piece[1][2:]
            screen.blit(p_white[p[p_type]] if colour == "w_" else p_black[p[p_type]], rect)

    def draw_active_piece(self):
        for piece in self.active_piece.items():
            pos = pg.mouse.get_pos()
            self.active_offset = (pos[0] - 0.5*TILE_SIZE, pos[1] - 0.5*TILE_SIZE)
            colour, p_type = piece[1][:2], piece[1][2:]
            screen.blit(p_white[p[p_type]] if colour == "w_" else p_black[p[p_type]], self.active_offset)

    @staticmethod
    def get_pos_from_tile(tile):
        """
        :param: tile
        :return: x, y breakdown of tile
        """

        return tile % rows, tile // rows

    @staticmethod
    def get_tile_from_pos(pos):
        """
        :param: position
        :return: 0-63 number representing the tile, from tuple of (0-7, 0-7)
        """

        return pos[0] + pos[1]*rows


board = Board()
