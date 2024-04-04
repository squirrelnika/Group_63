import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 1200
HEIGHT = 600
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
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


# Function to generate the initial string of symbols
def generate_symbols(length):
    symbols = [CROSS if random.random() < 0.5 else CIRCLE for _ in range(length)]
    return symbols


# Function to draw symbols on the screen
def draw_symbols(symbols):
    symbol_size = 40
    x_offset = (WIDTH - (symbol_size * len(symbols))) // 2
    y = HEIGHT // 2
    for symbol in symbols:
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
        x_offset += symbol_size


# Function to draw scores on the screen
def draw_scores(player_points):
    font = pygame.font.SysFont(None, 24)
    text1 = font.render(f"Circles: {player_points[0]}", True, RED)
    text2 = font.render(f"Crosses: {player_points[1]}", True, BLUE)
    screen.blit(text1, (10, 10))  # Circles score in top left corner
    screen.blit(
        text2, (WIDTH - text2.get_width() - 10, 10)
    )  # Crosses score in top right corner


# Function to display the player turn on the screen
def display_player_turn(player):
    font = pygame.font.SysFont(None, 36)
    if player == 0:
        text = font.render("Player's Turn: Circles", True, RED)
    else:
        text = font.render("Player's Turn: Crosses", True, BLUE)
    screen.blit(text, (WIDTH // 2, 50))  # Display at the top center


# Function to make a move and update points
def make_move(symbols, player_points, current_player):
    # Find the first occurrence of XX=O or XO=O for circles
    if current_player == 0:  # Circles
        index = 0
        while index < len(symbols) - 1:
            if symbols[index] == CROSS and symbols[index + 1] == CROSS:
                symbols[index] = CIRCLE
                symbols.pop(index + 1)
                player_points[0] += 2
                return
            elif symbols[index] == CROSS and symbols[index + 1] == CIRCLE:
                symbols[index] = CIRCLE
                symbols.pop(index + 1)
                player_points[0] += 1
                return
            index += 1
    # Find the first occurrence of OO=X or OX=X for crosses
    elif current_player == 1:  # Crosses
        index = 0
        while index < len(symbols) - 1:
            if symbols[index] == CIRCLE and symbols[index + 1] == CIRCLE:
                symbols[index] = CROSS
                symbols.pop(index + 1)
                player_points[1] += 2
                return
            elif symbols[index] == CIRCLE and symbols[index + 1] == CROSS:
                symbols[index] = CROSS
                symbols.pop(index + 1)
                player_points[1] += 1
                return
            index += 1


# Function to check if the game is over
def is_game_over(symbols):
    return len(symbols) == 1


# Function to display the winner and provide options to restart or quit
def display_winner(screen, player_points):
    font = pygame.font.SysFont(None, 48)
    if player_points[0] > player_points[1]:
        text = font.render("Player with circles wins!", True, RED)
    elif player_points[0] < player_points[1]:
        text = font.render("Player with crosses wins!", True, BLUE)
    else:
        text = font.render("It's a tie!", True, BLACK)
    screen.blit(
        text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 3 - text.get_height() // 2)
    )

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
    draw_text(screen, "Quit", font, BLACK, quit_button.centerx, quit_button.centery)

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
    input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 20, 200, 40)
    font = pygame.font.Font(None, 32)
    color_inactive = pygame.Color("lightskyblue3")
    color_active = pygame.Color("dodgerblue2")
    color = color_inactive
    active = False
    text = ""
    running = True
    current_player = 0  # 0 for circles, 1 for crosses
    player_points = [0, 0]

    # Buttons for each player's moves
    circle_button1 = pygame.Rect(100, 100, 100, 50)
    cross_button1 = pygame.Rect(WIDTH - 200, 100, 100, 50)

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
                            print("Invalid input! Length must be between 15 and 25.")
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
            WIDTH // 2,
            HEIGHT // 2 - 50,
        )
        draw_text(screen, text, font, BLACK, input_box.x + 100, input_box.y + 5)
        input_box.w = max(200, font.size(text)[0] + 10)
        pygame.display.flip()

    symbols = generate_symbols(symbol_length)

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
                if current_player == 0:  # Circles
                    if circle_button1.collidepoint(event.pos):
                        make_move(symbols, player_points, current_player)
                        current_player = (current_player + 1) % 2
                elif current_player == 1:  # Crosses
                    if cross_button1.collidepoint(event.pos):
                        make_move(symbols, player_points, current_player)
                        current_player = (current_player + 1) % 2

        # Print current symbols to console
        print("Current symbols:", symbols)

        # Draw everything
        screen.fill(WHITE)
        draw_symbols(symbols)
        draw_scores(player_points)  # Draw scores

        # Check for game over
        if is_game_over(symbols):
            restart = display_winner(screen, player_points)
            if restart:
                return  # Restart game
            else:
                pygame.quit()
                sys.exit()

        display_player_turn(current_player)  # Display current player's turn
        # Draw buttons
        pygame.draw.rect(screen, RED, circle_button1)
        pygame.draw.rect(screen, BLUE, cross_button1)
        draw_text(
            screen, "Turn", font, BLACK, circle_button1.x + 50, circle_button1.y + 15
        )
        draw_text(
            screen, "Turn", font, BLACK, cross_button1.x + 50, cross_button1.y + 15
        )
        pygame.display.flip()
        clock.tick(FPS)


# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Symbol Game")
clock = pygame.time.Clock()

# Start the game
start_game()