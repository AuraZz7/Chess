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
                if self.get_tile_from_pos((x, y)) in self.pieces:
                    self.active_tile = self.get_tile_from_pos((x, y))

                    self.active_piece[self.active_tile] = self.pieces[self.active_tile]
                    self.pieces.pop(self.active_tile)

                    colour, p_type = self.active_piece[self.active_tile].split("_")

                    # all the logic to determine which tiles the piece can move to
                    # pawn
                    if p_type == "p":
                        if colour == "w":
                            if self.active_tile - 8 not in self.pieces:
                                self.available_tiles = [self.active_tile - (8*i) for i in range(1, (3 if 48 <= self.active_tile <= 55 else 2))]
                        elif colour == "b":
                            if self.active_tile + 8 not in self.pieces:
                                self.available_tiles = [self.active_tile + (8*i) for i in range(1, (3 if 8 <= self.active_tile <= 15 else 2))]
                    # rook
                    elif p_type == "r":
                        for d in range(4):
                            for i in range(1, rows):
                                plus_condition = (-8 * i) if d == 0 else (8 * i) if d == 1 else (-i) if d == 2 else (i)
                                tile_x, tile_y = self.get_pos_from_tile(self.active_tile + plus_condition)
                                if d in (0, 1):
                                    if self.get_pos_from_tile(self.active_tile)[0] != tile_x: break
                                elif d in (2, 3):
                                    if self.get_pos_from_tile(self.active_tile)[1] != tile_y: break
                                if self.active_tile + plus_condition in self.pieces or tile_x < 0 or tile_x > 7 or tile_y < 0 or tile_y > 7:
                                    break
                                self.available_tiles.append(self.active_tile + plus_condition)

                    elif p_type == "b":
                        for d in range(4):
                            for i in range(1, rows):
                                plus_condition = (-9 * i) if d == 0 else (-7 * i) if d == 1 else (7 * i) if d == 2 else (9 * i)
                                tile_x, tile_y = self.get_pos_from_tile(self.active_tile + plus_condition)

                                if self.active_tile + plus_condition in self.pieces or tile_x < 0 or tile_x > 7 or tile_y < 0 or tile_y > 7:
                                    break

                                print(tile_x, tile_y)
                                self.available_tiles.append(self.active_tile + plus_condition)
                    elif p_type == "k":
                        allowed_moves = (-15, -17, -6, 10, -10, 6, 17, 15)
                        for move in allowed_moves:
                            tile_x, tile_y = self.get_pos_from_tile(self.active_tile + move)
                            if self.active_tile + move not in self.pieces and 0 <= tile_x <= 7 and 0 <= tile_y <= 7:
                                self.available_tiles.append(self.active_tile + move)
                        print(self.available_tiles)

                else:
                    self.active_tile = None
            # check if the user WAS pressing it, but has released the LMB,
            # everything here happens just once on initial release.
            if not click and self.clicked:
                self.clicked = False
                self.drop_tile = self.get_tile_from_pos((x, y))
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
            x, y = self.get_pos_from_tile(piece[0])
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
