from core.prepare import *
import math


class Board:
    def __init__(self):
        self.grid = [(x, y) for x in range(rows) for y in range(cols)]
        # self.grid = [i for i in range(rows*cols)]
        # self.pieces = {
        #     0: "b_r", 1: "b_k", 2: "b_b", 3: "b_queen", 4: "b_king", 5: "b_b", 6: "b_k", 7: "b_r",
        #     8: "b_p", 9: "b_p", 10: "b_p", 11: "b_p", 12: "b_p", 13: "b_p", 14: "b_p", 15: "b_p",
        #     48: "w_p", 49: "w_p", 50: "w_p", 51: "w_p", 52: "w_p", 53: "w_p", 54: "w_p", 55: "w_p",
        #     56: "w_r", 57: "w_k", 58: "w_b", 59: "w_queen", 60: "w_king", 61: "w_b", 62: "w_k", 63: "w_r"
        # }
        self.pieces = {
            (0, 0): "b_r", (1, 0): "b_k", (2, 0): "b_b", (3, 0): "b_queen", (4, 0): "b_king", (5, 0): "b_b", (6, 0): "b_k", (7, 0): "b_r",
            (0, 1): "b_p", (1, 1): "b_p", (2, 1): "b_p", (3, 1): "b_p", (4, 1): "b_p", (5, 1): "b_p", (6, 1): "b_p", (7, 1): "b_p",
            (0, 6): "w_p", (1, 6): "w_p", (2, 6): "w_p", (3, 6): "w_p", (4, 6): "w_p", (5, 6): "w_p", (6, 6): "w_p", (7, 6): "w_p",
            (0, 7): "w_r", (1, 7): "w_k", (2, 7): "w_b", (3, 7): "w_queen", (4, 7): "w_king", (5, 7): "w_b", (6, 7): "w_k", (7, 7): "w_r"
        }
        # dict containing the current piece being moved
        self.active_piece = {}
        # calculating the offset for drawing the active tile being moved when dragged
        self.active_offset = 0
        # index of the starting position of the tile which is being moved
        self.active_tile = None
        self.drop_tile = None
        # array of available tiles for the current move
        self.available_tiles = []

        self.last_move = []
        self.clicked = False

        self.turn = "w"

    def update(self):

        pos = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()[0]
        if 0 <= pos[0] <= SCREEN_WIDTH and 0 <= pos[1] <= SCREEN_HEIGHT:
            x, y = math.floor(pos[0] / TILE_SIZE), math.floor(pos[1] / TILE_SIZE)
            # check if user clicks left mouse button
            # everything inside this expression only occurs once, on initial click
            if click and not self.clicked:
                self.clicked = True
                # checking if the tile clicked by the user contains a chess piece
                if (x, y) in self.pieces:
                    self.active_tile = (x, y)

                    self.active_piece[self.active_tile] = self.pieces[self.active_tile]
                    self.pieces.pop(self.active_tile)

                    colour, p_type = self.active_piece[self.active_tile].split("_")

                    # all the logic to determine which tiles the piece can move to
                    if p_type == "p":
                        self.available_tiles = self.pawn_move(x, y, colour)
                    elif p_type == "r":
                        self.available_tiles = self.rook_move(x, y)
                    elif p_type == "b":
                        self.available_tiles = self.bishop_move(x, y)
                    elif p_type == "k":
                        self.available_tiles = self.knight_move(x, y)
                    elif p_type == "queen":
                        self.available_tiles = self.rook_move(x, y) + self.bishop_move(x, y)

            # check if the user WAS pressing it, but has released the LMB,
            # everything here happens just once on initial release.
            if not click and self.clicked:
                self.clicked = False
                self.drop_tile = (x, y)
                # check if the tile which the user released the mouse on doesn't have a piece on it
                if self.drop_tile not in self.pieces:
                    # check if the tile can be moved to
                    if self.drop_tile in self.available_tiles:
                        self.last_move = [self.active_tile, self.drop_tile]
                        self.pieces[self.drop_tile] = self.active_piece[self.active_tile]
                        self.active_piece.pop(self.active_tile)
                        self.turn = "w" if self.turn == "b" else "b"
                    else:
                        if self.active_piece:
                            self.pieces[self.active_tile] = self.active_piece[self.active_tile]
                            self.active_piece.pop(self.active_tile)
                else:
                    self.pieces[self.active_tile] = self.active_piece[self.active_tile]
                    self.active_piece.pop(self.active_tile)
                self.available_tiles.clear()

    def pawn_move(self, x, y, colour):
        available_moves = []
        if colour == "w":
            if (x, y - 1) not in self.pieces:
                available_moves = [(x, y - i) for i in range(1, (3 if y == 6 else 2))]
        elif colour == "b":
            if (x, y + 1) not in self.pieces:
                available_moves = [(x, y + i) for i in range(1, (3 if y == 1 else 2))]
        return available_moves

    def rook_move(self, x, y):
        available_moves = []
        for d in range(4):
            for i in range(1, rows):
                tile_x, tile_y = (x, y - i) if d == 0 else (x, y + i) if d == 1 else (x - i, y) if d == 2 else (
                x + i, y)
                if (tile_x, tile_y) in self.pieces or not (0 <= tile_x <= 7 or 0 <= tile_y <= 7):
                    break
                available_moves.append((tile_x, tile_y))
        return available_moves

    def bishop_move(self, x, y):
        available_moves = []
        for d in range(4):
            for i in range(1, rows):
                tile_x, tile_y = (x - i, y - i) if d == 0 else (x + i, y - i) if d == 1 else (x - i, y + i) if d == 2 else (x + i, y + i)

                if (tile_x, tile_y) in self.pieces or not (0 <= tile_x <= 7 or 0 <= tile_y <= 7):
                    break
                available_moves.append((tile_x, tile_y))
        return available_moves

    def knight_move(self, x, y):
        available_moves = []
        for x_operator in range(2):
            for y_operator in range(2):
                for direction in range(2):
                    if direction == 0:
                        tile_x, tile_y = (x - 1 if x_operator == 0 else x + 1, y - 2 if y_operator == 0 else y + 2)
                    else:
                        tile_x, tile_y = (x - 2 if x_operator == 0 else x + 2, y - 1 if y_operator == 0 else y + 1)
                    if (tile_x, tile_y) not in self.pieces and 0 <= tile_x <= 7 and 0 <= tile_y <= 7:
                        available_moves.append((tile_x, tile_y))
        return available_moves


    def draw(self):
        self.draw_grid()
        self.draw_pieces()
        self.draw_active_piece()

    def draw_grid(self):
        """
        Draw the background with a checkered pattern
        """
        for tile in self.grid:
            x, y = tile
            rect = (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if (x+y) % 2 == 0:
                pg.draw.rect(screen, yellow_1 if tile in self.last_move or tile in (self.drop_tile, self.active_tile) else board_col1, rect)
            else:
                pg.draw.rect(screen, yellow_2 if tile in self.last_move or tile in (self.drop_tile, self.active_tile) else board_col2, rect)
            # draw circles on tiles which are a valid move
            if tile in self.available_tiles:
                pg.draw.circle(screen, circle_col1 if (x+y) % 2 == 0 else circle_col2,
                               (x*TILE_SIZE+TILE_SIZE // 2, y*TILE_SIZE+TILE_SIZE // 2), TILE_SIZE // 6)

    def draw_pieces(self):
        """
        Draws all the pieces in dict 'self.pieces' to the board
        """
        for piece in self.pieces.items():
            x, y = piece[0]
            rect = (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            colour, p_type = piece[1].split("_")
            screen.blit(p_white[p[p_type]] if colour == "w" else p_black[p[p_type]], rect)

    def draw_active_piece(self):
        for piece in self.active_piece.items():
            pos = pg.mouse.get_pos()
            self.active_offset = (pos[0] - 0.5*TILE_SIZE, pos[1] - 0.5*TILE_SIZE)
            colour, p_type = piece[1].split("_")
            screen.blit(p_white[p[p_type]] if colour == "w" else p_black[p[p_type]], self.active_offset)

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
