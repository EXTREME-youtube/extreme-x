import pygame
import random
import time
import pygame.font
import sqlite3  # Import the sqlite3 module

# Initialize Pygame
pygame.init()

# --- Constants ---
DEFAULT_GRID_SIZE = 4
TILE_SIZE = 100
MARGIN = 15
BACKGROUND_COLOR = (250, 248, 239)
EMPTY_CELL_COLOR = (204, 192, 179)
TILE_COLORS = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
    4096: (230, 180, 0),
    'super': (255, 0, 0),
}
FONT_COLOR = (119, 110, 101)
FONT = pygame.font.Font("freesansbold.ttf", 40)
MENU_FONT = pygame.font.Font("freesansbold.ttf", 60)
BUTTON_COLOR = (220, 220, 220)
BUTTON_HOVER_COLOR = (200, 200, 200)
BUTTON_TEXT_COLOR = (0, 0, 0)
MENU_BACKGROUND_COLOR = (255, 240, 245)
GAME_BACKGROUND_COLOR = (240, 255, 240)
BUTTON_GRADIENT_COLOR_1 = (224, 255, 255)
BUTTON_GRADIENT_COLOR_2 = (176, 224, 230)
GAME_TITLE_COLOR = (0, 128, 128)
BUTTON_BORDER_COLOR = (0, 128, 128)
INPUT_BOX_COLOR = (255, 255, 255)
INPUT_TEXT_COLOR = (0, 0, 0)
INPUT_BOX_BORDER_COLOR = (100, 100, 100)
INPUT_FONT = pygame.font.Font("freesansbold.ttf", 30)
MESSAGE_COLOR = (0, 0, 255)  # Color for messages
MESSAGE_FONT = pygame.font.Font("freesansbold.ttf", 24)
SCORE_FONT = pygame.font.Font("freesansbold.ttf", 24)  # Font for displaying score
BEST_SCORE_FONT = pygame.font.Font("freesansbold.ttf", 24)  # Font for best score


# --- Database Setup ---
conn = sqlite3.connect("2048_scores.db")  # Connect to the database (or create it)
cursor = conn.cursor()

# Create the users table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
""")

# Create the scores table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        score INTEGER NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
""")
conn.commit()


# --- Helper Functions ---

def create_grid(size):
    """Creates an empty game grid of the specified size."""
    return [[0] * size for _ in range(size)]


def add_new_tile(grid):
    """Adds a new tile (2 or 4) to a random empty cell in the grid."""
    empty_cells = [(r, c) for r in range(len(grid)) for c in range(len(grid[0])) if grid[r][c] == 0]
    if not empty_cells:
        return False  # Grid is full
    row, col = random.choice(empty_cells)
    grid[row][col] = 2 if random.random() > 0.1 else 4  # 90% chance of 2, 10% of 4
    return True


def get_max_tile_value(grid):
    """Finds the maximum tile value in the grid."""
    max_value = 0
    for row in grid:
        for tile in row:
            max_value = max(max_value, tile)
    return max_value


def draw_tile(surface, value, x, y, animation_value=None):
    """Draws a tile with the given value at the specified position.

    Args:
        surface: The Pygame surface to draw on.
        value: The tile's numerical value (0, 2, 4, ..., 2048).
        x: The x-coordinate of the tile's top-left corner.
        y: The y-coordinate of the tile's top-left corner.
        animation_value:  If not None, draw this value instead of the tile's value. Used for animation.
    """
    if value == 0:
        pygame.draw.rect(surface, EMPTY_CELL_COLOR, (x, y, TILE_SIZE, TILE_SIZE), border_radius=8)
        return

    # Use the actual tile value, or the animation value if provided.
    display_value = animation_value if animation_value is not None else value
    color = TILE_COLORS.get(value, TILE_COLORS['super'])  # Use 'super' for values > 2048
    pygame.draw.rect(surface, color, (x, y, TILE_SIZE, TILE_SIZE), border_radius=8)
    if display_value > 0:  # prevent drawing 0
        text = FONT.render(str(display_value), True, FONT_COLOR)
        text_rect = text.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
        surface.blit(text, text_rect)


def draw_grid(surface, grid, moving_tiles):
    """Draws the entire game grid on the surface.

        moving_tiles:  A dictionary of tiles that are currently moving. Each key
                        is (row, col) and the value is a tuple:
                        (original_value, x_start, y_start, x_end, y_end, start_time)
    """
    # 1. Draw the background for the entire grid
    surface.fill(GAME_BACKGROUND_COLOR)  # changed
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            x = c * TILE_SIZE + (c + 1) * MARGIN
            y = r * TILE_SIZE + (r + 1) * MARGIN
            pygame.draw.rect(surface, EMPTY_CELL_COLOR, (x, y, TILE_SIZE, TILE_SIZE),
                             border_radius=8)  # background is empty cell color

    # 2. Draw the moving tiles *on top*, at their animated positions
    for (start_r, start_c), tile_data in moving_tiles.items():
        # Check if the tile_data has the expected number of elements.
        if len(tile_data) == 6:
            original_value, x_start, y_start, x_end, y_end, start_time = tile_data
        else:
            print(f"Error: Unexpected tile_data format: {tile_data}")  # error message
            continue  # Skip this tile and go to the next one
        elapsed_time = time.time() - start_time
        animation_duration = 0.1  # Adjust for speed as needed

        # Calculate the current x, y position based on the animation progress
        t = elapsed_time / animation_duration
        current_x = x_start + (x_end - x_start) * t
        current_y = y_start + (y_end - y_start) * t

        # Draw the tile at its current position
        draw_tile(surface, original_value, current_x, current_y)

    # 3. Draw the static tiles
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            x = c * TILE_SIZE + (c + 1) * MARGIN
            y = r * TILE_SIZE + (r + 1) * MARGIN
            if grid[r][c] != 0:
                draw_tile(surface, grid[r][c], x, y)


def collapse_row_left(row):
    """Collapses a row to the left, merging like tiles."""
    new_row = [x for x in row if x != 0]
    merged_row = []
    i = 0
    while i < len(new_row):
        if i + 1 < len(new_row) and new_row[i] == new_row[i + 1]:
            merged_row.append(new_row[i] * 2)
            i += 2
        else:
            merged_row.append(new_row[i])
            i += 1
    merged_row += [0] * (len(row) - len(merged_row))
    return merged_row


def collapse_grid_left(grid):
    """Collapses the entire grid to the left."""
    new_grid = [collapse_row_left(row) for row in grid]
    moved = new_grid != grid
    return new_grid, moved


def rotate_grid(grid):
    """Rotates the grid 90 degrees clockwise."""
    return [list(row) for row in zip(*grid[::-1])]


def move_and_add_tile(grid, direction):
    """Moves the tiles in the given direction, merges where possible, and adds a new tile.
        Returns:
            (new_grid, moved, score)
            new_grid: The updated grid.
            moved: True if any tiles moved, False otherwise.
            score:  The score from the merge
    """
    score = 0
    if direction == 'left':
        new_grid, moved = collapse_grid_left(grid)
    elif direction == 'right':
        rotated_grid = [row[::-1] for row in grid]
        new_grid, moved = collapse_grid_left(rotated_grid)
        new_grid = [row[::-1] for row in new_grid]
    elif direction == 'up':
        rotated_grid = rotate_grid(grid)
        new_grid, moved = collapse_grid_left(rotated_grid)
        new_grid = rotate_grid(rotate_grid(rotate_grid(new_grid)))  # Rotate back 270 degrees
    elif direction == 'down':
        rotated_grid = rotate_grid(rotate_grid(grid))
        new_grid, moved = collapse_grid_left(rotated_grid)
        new_grid = rotate_grid(new_grid)

    # Calculate the score (sum of merged tiles)
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] != new_grid[r][c] and new_grid[r][c] != 0:
                score += new_grid[r][c]

    if moved:
        add_new_tile(new_grid)
    return new_grid, moved, score


def check_game_over(grid):
    """Checks if the game is over (no more possible moves)."""
    for row in grid:
        if 0 in row:
            return False  # There's an empty cell
        for i in range(len(row) - 1):
            if row[i] == row[i + 1]:
                return False  # There are adjacent equal tiles in a row
    for c in range(len(grid[0])):
        for r in range(len(grid) - 1):
            if grid[r][c] == grid[r + 1][c]:
                return False  # There are adjacent equal tiles in a column
    return True  # No possible moves left


def draw_menu(surface, menu_items, selected_index):
    """Draws the main menu."""
    surface.fill(MENU_BACKGROUND_COLOR)  # Clear the screen, changed

    title_text = MENU_FONT.render("2048", True, GAME_TITLE_COLOR)  # changed
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    surface.blit(title_text, title_rect)

    for i, item in enumerate(menu_items):
        if i == selected_index:
            text = MENU_FONT.render(item, True, (255, 0, 0))  # Highlight selected item
        else:
            text = MENU_FONT.render(item, True, FONT_COLOR)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50))
        surface.blit(text, text_rect)


def draw_button(surface, rect, color, text, font):
    """Draws a button on the surface"""
    # Create gradient
    for y in range(rect.height):
        # Calculate the color at the current height
        c1 = BUTTON_GRADIENT_COLOR_1
        c2 = BUTTON_GRADIENT_COLOR_2
        r = int(c1[0] + (c2[0] - c1[0]) * y / rect.height)
        g = int(c1[1] + (c2[1] - c1[1]) * y / rect.height)
        b = int(c1[2] + (c2[2] - c1[2]) * y / rect.height)
        gradient_color = (r, g, b)
        pygame.draw.line(surface, gradient_color, (rect.left, rect.top + y), (rect.right, rect.top + y))
    pygame.draw.rect(surface, color, rect, border_radius=8, width=2)  # added border
    pygame.draw.rect(surface, BUTTON_BORDER_COLOR, rect, border_radius=8, width=2)
    text_render = font.render(text, True, BUTTON_TEXT_COLOR)
    text_rect = text_render.get_rect(center=rect.center)
    surface.blit(text_render, text_rect)


def draw_input_box(surface, rect, text, font, color, text_color, border_color):
    """Draws an input box."""
    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, border_color, rect, 2)
    text_surface = font.render(text, True, text_color)
    surface.blit(text_surface, (rect.x + 5, rect.y + 5))


def draw_message(surface, text):
    """Draws a message on the screen."""
    message_text = MESSAGE_FONT.render(text, True, MESSAGE_COLOR)
    message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))  # Position at bottom
    surface.blit(message_text, message_rect)


def save_score(user_id, score):
    """Saves the user's score to the database."""
    try:
        cursor.execute("INSERT INTO scores (user_id, score) VALUES (?, ?)", (user_id, score))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error saving score: {e}")
        return False


def get_user_id(username):
    """Retrieves the user ID from the database based on the username."""
    try:
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    except Exception as e:
        print(f"Error getting user ID: {e}")
        return None


def register_user(username, password):
    """Registers a new user in the database."""
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Username already exists
    except Exception as e:
        print(f"Error registering user: {e}")
        return False


def login_user(username, password):
    """Logs in a user by verifying the username and password."""
    try:
        cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
        result = cursor.fetchone()
        if result:
            return result[0]  # Return user ID
        else:
            return None
    except Exception as e:
        print(f"Error logging in user: {e}")
        return None


def get_best_score(user_id):
    """Retrieves the user's best score from the database."""
    try:
        cursor.execute("SELECT MAX(score) FROM scores WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        if result and result[0] is not None:
            return result[0]
        else:
            return 0  # Return 0 if no scores found
    except Exception as e:
        print(f"Error getting best score: {e}")
        return 0


def draw_game_info(surface, score, best_score):
    """Draws the current score and best score on the game screen."""
    score_text = SCORE_FONT.render(f"Score: {score}", True, FONT_COLOR)
    score_rect = score_text.get_rect(topleft=(MARGIN, MARGIN))  # Position at top-left
    surface.blit(score_text, score_rect)

    best_score_text = BEST_SCORE_FONT.render(f"Best: {best_score}", True, FONT_COLOR)
    best_score_rect = best_score_text.get_rect(topleft=(MARGIN, MARGIN + 30))  # Position below score
    surface.blit(best_score_text, best_score_rect)


def main():
    """Main function to run the game."""
    global GRID_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, FONT

    GRID_SIZE = DEFAULT_GRID_SIZE
    SCREEN_WIDTH = GRID_SIZE * TILE_SIZE + (GRID_SIZE + 1) * MARGIN
    SCREEN_HEIGHT = GRID_SIZE * TILE_SIZE + (GRID_SIZE + 1) * MARGIN
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("2048")

    menu_state = "main"  # "main", "grid_size_input", "game", "game_over", "register", "login"
    menu_items = ["Start", "Register", "Login", "Quit"]  # removed start
    selected_index = 0
    game_over = False
    grid = []
    score = 0
    moving_tiles = {}
    message_text = ""
    current_user_id = None  # To store the logged-in user's ID
    best_score = 0

    # Define button rectangles for main menu
    start_button_rect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2,
                                    50)  # removed start
    register_button_rect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 60, SCREEN_WIDTH // 2,
                                     50)  # register
    login_button_rect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 120, SCREEN_WIDTH // 2,
                                     50)  # login
    quit_button_rect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 180, SCREEN_WIDTH // 2,
                                    50)  # quit

    # Define button rectangle for restart (game over screen)
    restart_button_rect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 120, SCREEN_WIDTH // 2,
                                     50)  # same rect as login initially

    start_button_color = BUTTON_COLOR  # removed start
    register_button_color = BUTTON_COLOR
    login_button_color = BUTTON_COLOR
    quit_button_color = BUTTON_COLOR
    restart_button_color = BUTTON_COLOR

    # Input box for grid size
    input_box_rect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3, SCREEN_WIDTH // 2, 50)
    input_text = ""
    input_active = True
    input_error = ""
    input_font = INPUT_FONT

    # Input boxes for register/login
    username_input_rect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3, SCREEN_WIDTH // 2, 50)
    password_input_rect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2, 50)
    username_text = ""
    password_text = ""
    register_button_rect_reg = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 120,
                                                                         SCREEN_WIDTH // 2, 50)
    login_button_rect_log = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 120, SCREEN_WIDTH // 2,
                                                                        50)

    # Game loop
    running = True
    while running:
        screen.fill(MENU_BACKGROUND_COLOR)  # Default background
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif menu_state == "main":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button_rect.collidepoint(event.pos):  # removed start
                        start_button_color = BUTTON_HOVER_COLOR
                        pygame.display.flip()
                        time.sleep(0.1)
                        menu_state = "grid_size_input"
                        start_button_color = BUTTON_COLOR  # reset
                    elif register_button_rect.collidepoint(event.pos):
                        register_button_color = BUTTON_HOVER_COLOR
                        pygame.display.flip()
                        time.sleep(0.1)
                        menu_state = "register"
                        register_button_color = BUTTON_COLOR
                    elif login_button_rect.collidepoint(event.pos):
                        login_button_color = BUTTON_HOVER_COLOR
                        pygame.display.flip()
                        time.sleep(0.1)
                        menu_state = "login"
                        login_button_color = BUTTON_COLOR
                    elif quit_button_rect.collidepoint(event.pos):
                        quit_button_color = BUTTON_HOVER_COLOR
                        pygame.display.flip()
                        time.sleep(0.1)
                        running = False
                        quit_button_color = BUTTON_COLOR
                elif event.type == pygame.MOUSEMOTION:  # hover effect
                    if start_button_rect.collidepoint(event.pos):  # removed start
                        start_button_color = BUTTON_HOVER_COLOR
                    else:
                        start_button_color = BUTTON_COLOR
                    if register_button_rect.collidepoint(event.pos):
                        register_button_color = BUTTON_HOVER_COLOR
                    else:
                        register_button_color = BUTTON_COLOR
                    if login_button_rect.collidepoint(event.pos):
                        login_button_color = BUTTON_HOVER_COLOR
                    else:
                        login_button_color = BUTTON_COLOR
                    if quit_button_rect.collidepoint(event.pos):
                        quit_button_color = BUTTON_HOVER_COLOR
                    else:
                        quit_button_color = BUTTON_COLOR
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        selected_index = (selected_index + 1) % len(menu_items)
                    elif event.key == pygame.K_UP:
                        selected_index = (selected_index - 1 + len(menu_items)) % len(menu_items)
                    elif event.key == pygame.K_RETURN:
                        if selected_index == 0:  # Start Game #removed start
                            menu_state = "grid_size_input"
                        elif selected_index ==1:  # register
                            menu_state = "register"
                        elif selected_index == 2:  # login
                            menu_state = "login"
                        elif selected_index == 3:  # Quit
                            running = False
            elif menu_state == "grid_size_input":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        try:
                            size = int(input_text)
                            if 2 <= size <= 10:  # Basic validation, adjust as needed
                                GRID_SIZE = size
                                SCREEN_WIDTH = GRID_SIZE * TILE_SIZE + (GRID_SIZE + 1) * MARGIN
                                SCREEN_HEIGHT = GRID_SIZE * TILE_SIZE + (GRID_SIZE + 1) * MARGIN
                                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # resize
                                FONT = pygame.font.Font("freesansbold.ttf",
                                                                                40)  # You might need to adjust font size
                                grid = create_grid(GRID_SIZE)
                                add_new_tile(grid)
                                add_new_tile(grid)
                                score = 0
                                moving_tiles = {}
                                game_over = False
                                menu_state = "game"
                                input_error = ""
                            else:
                                input_error = "Size must be between 2 and 10."
                        except ValueError:
                            input_error = "Invalid input.  Enter a number."
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_char = event.unicode
                        if input_char.isdigit():
                            input_text += input_char
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button_rect.collidepoint(event.pos):  # start button in input screen
                        try:
                            size = int(input_text)
                            if 2 <= size <= 10:  # Basic validation, adjust as needed
                                GRID_SIZE = size
                                SCREEN_WIDTH = GRID_SIZE * TILE_SIZE + (GRID_SIZE + 1) * MARGIN
                                SCREEN_HEIGHT = GRID_SIZE * TILE_SIZE + (GRID_SIZE + 1) * MARGIN
                                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # resize
                                FONT = pygame.font.Font("freesansbold.ttf",
                                                                                40)  # You might need to adjust font size
                                grid = create_grid(GRID_SIZE)
                                add_new_tile(grid)
                                add_new_tile(grid)
                                score = 0
                                moving_tiles = {}
                                game_over = False
                                menu_state = "game"
                                input_error = ""
                            else:
                                input_error = "Size must be between 2 and 10."
                        except ValueError:
                            input_error = "Invalid input.  Enter a number."
            elif menu_state == "game":
                if event.type == pygame.KEYDOWN:
                    # Record the starting positions of tiles before the move
                    old_grid = [row[:] for row in grid]  # make a copy
                    for r in range(GRID_SIZE):
                        for c in range(GRID_SIZE):
                            if grid[r][c] != 0:
                                moving_tiles[(r, c)] = (grid[r][c],
                                                                        c * TILE_SIZE + (c + 1) * MARGIN,
                                                                        r * TILE_SIZE + (r + 1) * MARGIN,
                                                                        c * TILE_SIZE + (c + 1) * MARGIN,
                                                                        r * TILE_SIZE + (r + 1) * MARGIN,
                                                                        time.time())
                    # Handle arrow key presses
                    if event.key == pygame.K_LEFT:
                        grid, moved, move_score = move_and_add_tile(grid, 'left')
                    elif event.key == pygame.K_RIGHT:
                        grid, moved, move_score = move_and_add_tile(grid, 'right')
                    elif event.key == pygame.K_UP:
                        grid, moved, move_score = move_and_add_tile(grid, 'down') #fixed
                    elif event.key == pygame.K_DOWN:
                        grid, moved, move_score = move_and_add_tile(grid, 'up') #fixed
                    else:
                        moved = False  # No move was made
                        move_score = 0

                    score += move_score

                    if not moved:
                        moving_tiles = {}  # Clear moving tiles
                    else:
                        # Update the target positions for moving tiles.
                        for r in range(GRID_SIZE):
                            for c in range(GRID_SIZE):
                                if old_grid[r][c] != grid[r][c]:
                                    # Find where this tile ended up
                                    for new_r in range(GRID_SIZE):
                                        for new_c in range(GRID_SIZE):
                                            if grid[new_r][new_c] == old_grid[r][c]:
                                                moving_tiles[(r, c)] = (old_grid[r][c],
                                                                                                        c * TILE_SIZE + (c + 1) * MARGIN,
                                                                                                        r * TILE_SIZE + (r + 1) * MARGIN,
                                                                                                        new_c * TILE_SIZE + (new_c + 1) * MARGIN,
                                                                                                        new_r * TILE_SIZE + (new_r + 1) * MARGIN,
                                                                                                        time.time())
                                                break  # found
                                        else:
                                            continue
                                        break

                    game_over = check_game_over(grid)
                    if game_over:
                        print("Game Over!")  # For debugging
                        if current_user_id:
                            save_score(current_user_id, score)
                        menu_state = "game_over"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if game_over:
                        if restart_button_rect.collidepoint(event.pos):
                            restart_button_color = BUTTON_HOVER_COLOR
                            pygame.display.flip()
                            time.sleep(0.1)
                            menu_state = "main"
                            selected_index = 0
                            restart_button_color = BUTTON_COLOR
            elif menu_state == "game_over":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button_rect.collidepoint(event.pos):
                        restart_button_color = BUTTON_HOVER_COLOR
                        pygame.display.flip()
                        time.sleep(0.1)
                        menu_state = "main"
                        selected_index = 0
                        restart_button_color = BUTTON_COLOR
                elif event.type == pygame.MOUSEMOTION:  # hover effect
                    if restart_button_rect.collidepoint(event.pos):
                        restart_button_color = BUTTON_HOVER_COLOR
                    else:
                        restart_button_color = BUTTON_COLOR
            elif menu_state == "register":  # register state
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if username_text and password_text:
                            if register_user(username_text, password_text):
                                message_text = "Registration successful! Please log in."
                                menu_state = "login"  # Go to login after successful registration
                                username_text = ""
                                password_text = ""
                            else:
                                message_text = "Username already exists."
                        else:
                            message_text = "Please enter username and password."
                    elif event.key == pygame.K_BACKSPACE:
                        if input_active == 0:  # username
                            username_text = username_text[:-1]
                        elif input_active == 1:  # password
                            password_text = password_text[:-1]
                    else:
                        input_char = event.unicode
                        if input_active == 0:
                            username_text += input_char
                        elif input_active == 1:
                            password_text += input_char
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if register_button_rect_reg.collidepoint(event.pos):
                        if username_text and password_text:
                            if register_user(username_text, password_text):
                                message_text = "Registration successful! Please log in."
                                menu_state = "login"  # Go to login after successful registration
                                username_text = ""
                                password_text = ""
                            else:
                                message_text = "Username already exists."
                        else:
                            message_text = "Please enter username and password."
                    elif username_input_rect.collidepoint(event.pos):
                        input_active = 0
                    elif password_input_rect.collidepoint(event.pos):
                        input_active = 1

            elif menu_state == "login":  # login state
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if username_text and password_text:
                            user_id = login_user(username_text, password_text)
                            if user_id:
                                message_text = f"Logged in as {username_text}!"
                                current_user_id = user_id
                                best_score = get_best_score(current_user_id)  # get best score
                                menu_state = "grid_size_input"  # Go to game setup
                                username_text = ""
                                password_text = ""
                            else:
                                message_text = "Invalid credentials. Please try again."
                        else:
                            message_text = "Please enter username and password."
                    elif event.key == pygame.K_BACKSPACE:
                        if input_active == 0:  # username
                            username_text = username_text[:-1]
                        elif input_active == 1:  # password
                            password_text = password_text[:-1]
                    else:
                        input_char = event.unicode
                        if input_active == 0:
                            username_text += input_char
                        elif input_active == 1:
                            password_text += input_char
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if login_button_rect_log.collidepoint(event.pos):
                        if username_text and password_text:
                            user_id = login_user(username_text, password_text)
                            if user_id:
                                message_text = f"Logged in as {username_text}!"
                                current_user_id = user_id
                                best_score = get_best_score(current_user_id)  # get best score
                                menu_state = "grid_size_input"  # Go to game setup.
                                username_text = ""
                                password_text = ""
                            else:
                                message_text = "Invalid credentials. Please try again."
                        else:
                            message_text = "Please enter username and password."
                    elif username_input_rect.collidepoint(event.pos):
                        input_active = 0
                    elif password_input_rect.collidepoint(event.pos):
                        input_active = 1

        # Draw based on the current menu state
        if menu_state == "main":
            draw_menu(screen, menu_items, selected_index)
            draw_button(screen, start_button_rect, start_button_color, "Start", MENU_FONT) # removed start
            draw_button(screen, register_button_rect, register_button_color, "Register", MENU_FONT)
            draw_button(screen, login_button_rect, login_button_color, "Login", MENU_FONT)
            draw_button(screen, quit_button_rect, quit_button_color, "Quit", MENU_FONT)
        elif menu_state == "grid_size_input":
            draw_input_box(screen, input_box_rect, input_text, input_font, INPUT_BOX_COLOR, INPUT_TEXT_COLOR,
                             INPUT_BOX_BORDER_COLOR)
            draw_button(screen, start_button_rect, start_button_color, "Start Game",
                             MENU_FONT)  # start button on input screen.
            if input_error:
                draw_message(screen, input_error)
        elif menu_state == "game":
            draw_grid(screen, grid, moving_tiles)
            draw_game_info(screen, score, best_score) #draw score
            if game_over:
                draw_message(screen, "Game Over!")
                draw_button(screen, restart_button_rect, restart_button_color, "Restart", MENU_FONT)
        elif menu_state == "register":  # register screen
            draw_input_box(screen, username_input_rect, username_text, INPUT_FONT, INPUT_BOX_COLOR,
                             INPUT_TEXT_COLOR, INPUT_BOX_BORDER_COLOR)
            draw_input_box(screen, password_input_rect, password_text, INPUT_FONT, INPUT_BOX_COLOR,
                             INPUT_TEXT_COLOR, INPUT_BOX_BORDER_COLOR)
            draw_button(screen, register_button_rect_reg, register_button_color, "Register", MENU_FONT)
            draw_message(screen, message_text)  # display message
            # draw labels
            username_label = INPUT_FONT.render("Username:", True, FONT_COLOR)
            password_label = INPUT_FONT.render("Password:", True, FONT_COLOR)
            screen.blit(username_label, (username_input_rect.x - 120, username_input_rect.y + 10))
            screen.blit(password_label, (password_input_rect.x - 120, password_input_rect.y + 10))
        elif menu_state == "login":  # login screen
            draw_input_box(screen, username_input_rect, username_text, INPUT_FONT, INPUT_BOX_COLOR,
                             INPUT_TEXT_COLOR, INPUT_BOX_BORDER_COLOR)
            draw_input_box(screen, password_input_rect, password_text, INPUT_FONT, INPUT_BOX_COLOR,
                             INPUT_TEXT_COLOR, INPUT_BOX_BORDER_COLOR)
            draw_button(screen, login_button_rect_log, login_button_color, "Login", MENU_FONT)
            draw_message(screen, message_text)
            # draw labels.
            username_label = INPUT_FONT.render("Username:", True, FONT_COLOR)
            password_label = INPUT_FONT.render("Password:", True, FONT_COLOR)
            screen.blit(username_label, (username_input_rect.x - 120, username_input_rect.y + 10))
            screen.blit(password_label, (password_input_rect.x - 120, password_input_rect.y + 10))

        pygame.display.flip()

    pygame.quit()
    conn.close()


if __name__ == "__main__":
    main()
