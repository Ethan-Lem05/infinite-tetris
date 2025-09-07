import pygame
import random
from sys import exit


class Piece:
    """A falling tetromino piece."""

    def __init__(self):
        # Tetromino definitions (minimal bounding boxes)
        self.tetrominoes = (
            ((1, 1),
             (1, 1)),  # O

            ((0, 1, 0),
             (1, 1, 1)),  # T

            ((0, 1, 1),
             (1, 1, 0)),  # S

            ((1, 1, 0),
             (0, 1, 1)),  # Z

            ((1, 0, 0),
             (1, 1, 1)),  # J

            ((0, 0, 1),
             (1, 1, 1)),  # L

            ((1, 1, 1, 1),),  # I
        )

        self.shape = ()

    def setup_random_piece(self):
        """Pick a random tetromino shape."""
        self.shape = random.choice(self.tetrominoes)


class Board:
    """Tetris board state."""
    def __init__(self, width=10, height=20):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.active_shape = None   # the 1/0 matrix
        self.active_row = 0        # top-left row of active piece
        self.active_col = 0        # top-left col of active piece


    def place_piece(self, piece: Piece, top=0, left=0):
        """Spawn a new active piece at (top, left)."""
        self.active_shape = piece.shape
        self.active_row = top
        self.active_col = left

    def get_active_coords(self):
        coords = []
        if self.active_shape is None:
            return coords
        m, n = len(self.active_shape), len(self.active_shape[0])
        for i in range(m):
            for j in range(n):
                if self.active_shape[i][j]:
                    r = self.active_row + i
                    c = self.active_col + j
                    coords.append((r, c))
        return coords

    def move_active(self, dx: int, dy: int):
        """Try to move the active piece by (dy, dx)."""
        occupied = set(self.get_active_coords())
        next_positions = [(r + dy, c + dx) for r, c in occupied]

        # Check if all next positions are valid
        for r, c in next_positions:
            if r < 0 or r >= self.height or c < 0 or c >= self.width:
                return  # out of bounds
            if self.board[r][c] == 1 and (r, c) not in occupied:
                return  # collides with frozen block

        # If valid, update
        self.active_row += dy
        self.active_col += dx


    def perform_step(self) -> bool:
        """
        Try moving active piece down by 1.
        Return True if it locks, False otherwise.
        """
        coords = self.get_active_coords()
        if not coords:
            return True

        # Check if can move down
        for r, c in coords:
            nr = r + 1
            if nr >= self.height or self.board[nr][c] == 1:
                # lock
                for rr, cc in coords:
                    self.board[rr][cc] = 1
                self.active_shape = None
                return True

        # safe → move piece
        self.active_row += 1
        return False
    
    def rotate_active(self, clockwise=True):
        if self.active_shape is None:
            return
        if clockwise:
            rotated = tuple(zip(*self.active_shape[::-1]))
        else:
            rotated = tuple(zip(*self.active_shape))[::-1]

        # check if rotated fits
        m, n = len(rotated), len(rotated[0])
        new_coords = []
        for i in range(m):
            for j in range(n):
                if rotated[i][j]:
                    r = self.active_row + i
                    c = self.active_col + j
                    if r < 0 or r >= self.height or c < 0 or c >= self.width:
                        return  # invalid rotation
                    if self.board[r][c] == 1:
                        return  # collides with locked
                    new_coords.append((r, c))

        # if valid, commit
        self.active_shape = rotated
    
    def clear_full_lines(self) -> int:
        """
        Clear all fully filled rows.
        Returns the number of lines cleared.
        """
        # keep only the rows that are not completely full
        new_rows = [row for row in self.board if not all(row)]
        cleared = self.height - len(new_rows)

        # insert empty rows at the top to keep board height constant
        for _ in range(cleared):
            new_rows.insert(0, [0] * self.width)

        self.board = new_rows
        return cleared


    def draw(self, surface, square_width, square_height, offset_x=0, offset_y=0):
        border_color = pygame.Color('#046ac9')
        for i in range(self.height + 1):
            y = offset_y + i * square_height
            pygame.draw.line(surface, border_color,
                            (offset_x, y),
                            (offset_x + self.width * square_width, y), 2)
        for j in range(self.width + 1):
            x = offset_x + j * square_width
            pygame.draw.line(surface, border_color,
                            (x, offset_y),
                            (x, offset_y + self.height * square_height), 2)

        # locked
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j]:
                    rect = pygame.Rect(offset_x + j * square_width,
                                    offset_y + i * square_height,
                                    square_width, square_height)
                    pygame.draw.rect(surface, "#b80c00", rect)
                    pygame.draw.rect(surface, "#730800", rect, 2)

        # active
        for r, c in self.get_active_coords():
            rect = pygame.Rect(offset_x + c * square_width,
                            offset_y + r * square_height,
                            square_width, square_height)
            pygame.draw.rect(surface, "#d21e00", rect)
            pygame.draw.rect(surface, "#7a1200", rect, 2)


def main():
    pygame.init()

    # CONSTANTS
    SCREEN_WIDTH = 480
    SCREEN_HEIGHT = 960
    BOARD_WIDTH = 10
    BOARD_HEIGHT = 20
    BOARD_SPRITE_WIDTH = int(0.8 * SCREEN_WIDTH)
    BOARD_SPRITE_HEIGHT = int(0.8 * SCREEN_HEIGHT)
    SQUARE_WIDTH = BOARD_SPRITE_WIDTH // BOARD_WIDTH
    SQUARE_HEIGHT = BOARD_SPRITE_HEIGHT // BOARD_HEIGHT
    BOARD_OFFSET_X = int(0.1 * SCREEN_WIDTH)
    BOARD_OFFSET_Y = int(0.1 * SCREEN_HEIGHT)

    # GAME OBJECTS
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    board = Board(BOARD_WIDTH, BOARD_HEIGHT)

    # Example piece: put in middle of board near top
    piece = Piece()
    piece.setup_random_piece()
    board.place_piece(piece, top=0, left=BOARD_WIDTH // 2 - len(piece.shape[0]) // 2)

    # GAME LOOP
    last_fall = pygame.time.get_ticks()
    fall_interval = 1000
    running = True
    # track key repeat timing
    key_delay = 150          # ms between repeated moves
    key_initial_delay = 200  # ms before auto-repeat kicks in
    last_key_time = {"left": 0, "right": 0, "down": 0}
    key_active = {"left": False, "right": False, "down": False}

    while running:
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    board.move_active(dx=-1, dy=0)
                    last_key_time["left"] = now
                    key_active["left"] = True
                elif event.key == pygame.K_RIGHT:
                    board.move_active(dx=1, dy=0)
                    last_key_time["right"] = now
                    key_active["right"] = True
                elif event.key == pygame.K_DOWN:
                    board.move_active(dx=0, dy=1)
                    last_key_time["down"] = now
                    key_active["down"] = True
                elif event.key == pygame.K_UP:
                    board.rotate_active(clockwise=True)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    key_active["left"] = False
                elif event.key == pygame.K_RIGHT:
                    key_active["right"] = False
                elif event.key == pygame.K_DOWN:
                    key_active["down"] = False

        # handle auto-repeat
        for key, (dx, dy) in {
            "left": (-1, 0),
            "right": (1, 0),
            "down": (0, 1),
        }.items():
            if key_active[key]:
                elapsed = now - last_key_time[key]
                if elapsed > key_initial_delay:
                    # allow continuous repeat every key_delay
                    if (elapsed - key_initial_delay) // key_delay > (
                        (elapsed - key_initial_delay - clock.get_time()) // key_delay
                    ):
                        board.move_active(dx=dx, dy=dy)

        # falling interval
        nxt = False
        if now - last_fall >= fall_interval:
            last_fall = now
            nxt = board.perform_step()
        
        if nxt:
            piece = Piece()
            piece.setup_random_piece()
            board.place_piece(piece, top=0, left=BOARD_WIDTH // 2 - len(piece.shape[0]) // 2)

        board.clear_full_lines()

        screen.fill("#013361")
        board.draw(screen, SQUARE_WIDTH, SQUARE_HEIGHT, BOARD_OFFSET_X, BOARD_OFFSET_Y)
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
