import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 1440
HEIGHT = 500
FPS = 30
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

CIRCLE = "O"
CROSS = "X"


# Function to draw text on the screen
def draw_text(surface, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)


# Function to generate the initial string of symbols
def generate_symbols(length):
    symbols = [
        CROSS if random.random() < 0.5 else CIRCLE for _ in range(length)
    ]
    return symbols


# Function to draw symbols on the screen and return rectangles around each symbol
def draw_symbols(symbols):
    symbol_size = 40
    x_offset = 50  # Left align symbols
    y = HEIGHT // 2
    symbol_rects = []  # List to store rectangles around symbols
    for index, symbol in enumerate(symbols):
        if symbol == CROSS:
            pygame.draw.line(
                screen,
                BLACK,
                (x_offset + 5, y - 5),
                (x_offset + symbol_size - 5, y + symbol_size - 5),
                3,
            )
            pygame.draw.line(
                screen,
                BLACK,
                (x_offset + symbol_size - 5, y - 5),
                (x_offset + 5, y + symbol_size - 5),
                3,
            )
        elif symbol == CIRCLE:
            pygame.draw.circle(
                screen,
                RED,
                (x_offset + symbol_size // 2, y + symbol_size // 2),
                symbol_size // 2 - 5,
                3,
            )
        symbol_rects.append(
            pygame.Rect(x_offset + 20, y, symbol_size, symbol_size))
        x_offset += symbol_size + 10  # Increase x_offset for next symbol
    return symbol_rects


# Function to draw scores on the screen
def draw_scores(player_points):
    font = pygame.font.SysFont(None, 24)
    text1 = font.render(f"Circles: {player_points[0]}", True, RED)
    text2 = font.render(f"Crosses: {player_points[1]}", True, BLUE)
    screen.blit(text1, (10, 10))  # Circles score in top left corner
    screen.blit(text2, (WIDTH - text2.get_width() - 10,
                        10))  # Crosses score in top right corner


# Function to display the player turn on the screen
def display_player_turn(player):
    font = pygame.font.SysFont(None, 36)
    if player == 0:
        text = font.render("Player's Turn: Circles", True, RED)
    else:
        text = font.render("Player's Turn: Crosses", True, BLUE)
    screen.blit(text, (WIDTH // 2 - 200, 50))  # Display at the top center

    # Additional text below player's turn display
    gameinfo_text = font.render(
        "Press between two valid symbols to make a turn", True, BLACK)
    screen.blit(gameinfo_text, (WIDTH // 2 - 280, 100))


# Function to make a move and update points
def make_move(symbols, player_points, current_player, clicked_symbol):
    # Check if the clicked symbols are within the bounds of the current symbol array
    if clicked_symbol < len(symbols) - 1:
        if current_player == 0:  # Circles
            if (symbols[clicked_symbol] == CROSS
                    and symbols[clicked_symbol + 1] == CROSS):
                symbols[clicked_symbol] = CIRCLE
                symbols.pop(clicked_symbol + 1)
                player_points[0] += 2
                return True
            elif (symbols[clicked_symbol] == CROSS
                  and symbols[clicked_symbol + 1] == CIRCLE):
                symbols[clicked_symbol] = CIRCLE
                symbols.pop(clicked_symbol + 1)
                player_points[0] += 1
                return True
        elif current_player == 1:  # Crosses
            if (symbols[clicked_symbol] == CIRCLE
                    and symbols[clicked_symbol + 1] == CIRCLE):
                symbols[clicked_symbol] = CROSS
                symbols.pop(clicked_symbol + 1)
                player_points[1] += 2
                return True
            elif (symbols[clicked_symbol] == CIRCLE
                  and symbols[clicked_symbol + 1] == CROSS):
                symbols[clicked_symbol] = CROSS
                symbols.pop(clicked_symbol + 1)
                player_points[1] += 1
                return True
    return False  # Invalid move


# Function to check if the game is over
def is_game_over(symbols, current_player):
    if len(symbols) == 1:
        return True  # If only one symbol left, the game is over
    if current_player == 0:  # Circles
        for i in range(len(symbols) - 1):
            if (symbols[i] == CROSS and symbols[i + 1] == CROSS) or (
                    symbols[i] == CROSS and symbols[i + 1] == CIRCLE):
                return False  # If XX or XO combination is found, the game is not over
    elif current_player == 1:  # Crosses
        for i in range(len(symbols) - 1):
            if (symbols[i] == CIRCLE and symbols[i + 1] == CIRCLE) or (
                    symbols[i] == CIRCLE and symbols[i + 1] == CROSS):
                return False  # If OO or OX combination is found, the game is not over
    return True  # If no more moves can be made, the game is over


# Function to display the winner and provide options to restart or quit
def display_winner(screen, player_points):
    font = pygame.font.SysFont(None, 48)
    if player_points[0] > player_points[1]:
        text = font.render("Player with circles wins!", True, RED)
    elif player_points[0] < player_points[1]:
        text = font.render("Player with crosses wins!", True, BLUE)
    else:
        text = font.render("It's a tie!", True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2,
                       HEIGHT // 3 - text.get_height() // 2))

    # Buttons for restarting or quitting
    restart_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 50, 300, 50)
    quit_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 120, 300, 50)
    pygame.draw.rect(screen, GREEN, restart_button)
    pygame.draw.rect(screen, RED, quit_button)
    draw_text(
        screen,
        "Restart Game",
        font,
        BLACK,
        restart_button.centerx,
        restart_button.centery,
    )
    draw_text(screen, "Quit", font, BLACK, quit_button.centerx,
              quit_button.centery)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    return True  # Restart game
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()


# Function to initialize the game
def start_game():
    symbol_length = 0
    input_box = pygame.Rect(100, HEIGHT // 2 - 20, 200, 40)
    font = pygame.font.Font(None, 32)
    color_inactive = pygame.Color("lightskyblue3")
    color_active = pygame.Color("dodgerblue2")
    color = color_inactive
    active = False
    text = ""
    running = True
    current_player = 0  # 0 for circles, 1 for crosses
    player_points = [0, 0]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        try:
                            symbol_length = int(text)
                            if not 15 <= symbol_length <= 25:
                                raise ValueError
                            running = False
                        except ValueError:
                            print(
                                "Invalid input! Length must be between 15 and 25."
                            )
                        text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill(WHITE)
        pygame.draw.rect(screen, color, input_box, 2)
        draw_text(
            screen,
            "Enter the length of the symbol string (15-25):",
            font,
            BLACK,
            100,
            HEIGHT // 2 - 50,
        )
        draw_text(screen, text, font, BLACK, input_box.x + 100,
                  input_box.y + 5)
        input_box.w = max(200, font.size(text)[0] + 10)
        pygame.display.flip()

    symbols = generate_symbols(symbol_length)
    symbol_rects = draw_symbols(symbols)  # Get rectangles between symbols

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if any symbol was clicked
                for symbols_clicked, rect in enumerate(symbol_rects):
                    if rect.collidepoint(event.pos):
                        print("Symbol clicked:", symbols_clicked)
                        if make_move(symbols, player_points, current_player,
                                     symbols_clicked):
                            current_player = (
                                current_player + 1
                            ) % 2  # Switch to next player only if move is valid
                        break  # Exit the loop after processing the click

        # Draw everything
        screen.fill(WHITE)
        draw_symbols(symbols)
        draw_scores(player_points)  # Draw scores
        display_player_turn(current_player)

        # Check for game over
        if is_game_over(symbols, current_player):
            restart = display_winner(screen, player_points)
            if restart:
                return  # Restart game
            else:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(FPS)


# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Symbol Game")
clock = pygame.time.Clock()

# Start the game
start_game()
