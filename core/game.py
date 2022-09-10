from core.prepare import *


class Board:
    def __init__(self):
        self.grid = [(x, y) for x in range(rows) for y in range(cols)]
        self.grid = [i for i in range(rows*cols)]
        self.pieces = {
            0: "w_r", 1: "w_k", 2: "w_b", 3: "w_queen", 4: "w_king", 5: "w_b", 6: "w_k", 7: "w_r",
            8: "w_p", 9: "w_p", 10: "w_p", 11: "w_p", 12: "w_p", 13: "w_p", 14: "w_p", 15: "w_p",
            48: "b_p", 49: "b_p", 50: "b_p", 51: "b_p", 52: "b_p", 53: "b_p", 54: "b_p", 55: "b_p",
            56: "b_r", 57: "b_k", 58: "b_b", 59: "b_queen", 60: "b_king", 61: "b_b", 62: "b_k", 63: "b_r"
        }

    def draw(self):
        self.draw_grid()
        # self.draw_pieces()

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
        for piece in self.pieces.items():
            x, y = self.get_pos_from_tile(piece[0])
            rect = (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            colour = piece[1][:2]
            p_type = piece[1][2:]
            # If the piece is white
            if colour == "w_":
                screen.blit(p_white[p[p_type]], rect)
            elif colour == "b_":
                screen.blit(p_black[p[p_type]], rect)

    @staticmethod
    def get_pos_from_tile(tile):
        """
        :param: tile
        :return: x, y breakdown of tile
        """

        return tile % rows, tile // rows


board = Board()
board.draw()
board.draw_pieces()
