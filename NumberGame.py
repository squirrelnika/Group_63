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

# Function to draw text on the screen
def draw_text(surface, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

# Function to generate the initial string of symbols
def generate_symbols(length):
    symbols = [
        "X" if random.random() < 0.5 else "O" for _ in range(length)
    ]
    return symbols

# Function to draw symbols on the screen and return rectangles around each symbol
def draw_symbols(symbols):
    symbol_size = 40
    x_offset = 50  # Left align symbols
    y = HEIGHT // 2
    symbol_rects = []  # List to store rectangles around symbols
    for index, symbol in enumerate(symbols):
        if symbol == "X":
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
        elif symbol == "O":
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
    screen.blit(text2, (WIDTH - text2.get_width() - 10,10))  # Crosses score in top right corner

# Function to display the player turn on the screen
def display_player_turn(player):
    font = pygame.font.SysFont(None, 36)
    if player == "O":
        text = font.render("Player's Turn: Circles", True, RED)
    else:
        text = font.render("Player's Turn: Crosses", True, BLUE)
    screen.blit(text, (WIDTH // 2 - 200, 50))  # Display at the top center

    # Additional text below player's turn display
    gameinfo_text = font.render(
        "Press between two valid symbols to make a turn", True, BLACK)
    screen.blit(gameinfo_text, (WIDTH // 2 - 280, 100))

#Class to generate game tree
class TreeNode:
    def __init__(self, state, score, chosen_symbol=None, value=None, parent=None):
        self.state = state
        self.score = score #player score
        self.value = value #heuristic value
        self.chosen_symbol = chosen_symbol
        self.parent = parent
        self.children = []

    def add_child(self, child_state, child_score, chosen_symbol):
        child_node = TreeNode(child_state, child_score, chosen_symbol, self)
        self.children.append(child_node)
        return child_node
    
# Function to generate all possible next moves
def generate_moves(symbols, points, player):
    moves = []
    for i in range(len(symbols)-1):
        temp_score = points.copy() #japaskatas
        if player == "O":
            if symbols[i] == "X" and symbols[i+1] == "X":
                new_symbols = symbols.copy()
                new_symbols[i] = player
                new_symbols.pop(i+1)
                temp_score[0]+=2
                move = [new_symbols,temp_score, i]
                moves.append(move)
            elif symbols[i] == "X" and symbols[i+1] == "O":
                new_symbols = symbols.copy()
                new_symbols[i] = player
                new_symbols.pop(i+1)
                temp_score[0]+=1
                move = [new_symbols,temp_score, i]
                moves.append(move)
        else:
            if symbols[i] == "O" and symbols[i+1] == "O":
                new_symbols = symbols.copy()
                new_symbols[i] = player
                new_symbols.pop(i+1)
                temp_score[1]+=2
                move = [new_symbols,temp_score, i]
                moves.append(move)
            elif symbols[i] == "O" and symbols[i+1] == "X":
                new_symbols = symbols.copy()
                new_symbols[i] = player
                new_symbols.pop(i+1)
                temp_score[1]+=1
                move = [new_symbols,temp_score, i]
                moves.append(move)
    return moves

# Recursive function to build the game tree
def build_game_tree(node, player, depth):
    if depth == 0:
        return
    current_symbols = node.state
    current_score = node.score
    #current_value = node.value
    next_player = "O" if player == "X" else "X"

    moves = generate_moves(current_symbols, current_score, player)
    for move in moves:
        child_node = node.add_child(move[0],move[1],move[2])
        build_game_tree(child_node, next_player, depth-1)

#Function for player to make move
def player_move(clicked_symbol, game_path, level):
    for child in game_path[level].children:
        if child[2] == clicked_symbol:
            game_path.append(child)
            return True
        else:
            return False
        
#Function for computer to make move/ to be edited
def computer_move(level, game_path):
    for child in game_path[level].children: #gives all current level possible moves
        pass

# Function to make a move and update points
def make_move(symbols, player_points, current_player, clicked_symbol):
    # Check if the clicked symbols are within the bounds of the current symbol array
    if clicked_symbol < len(symbols) - 1:
        if current_player == "O":  # Circles
            if (symbols[clicked_symbol] == "X"
                    and symbols[clicked_symbol + 1] == "X"):
                symbols[clicked_symbol] = "O"
                symbols.pop(clicked_symbol + 1)
                player_points[0] += 2
                return True
            elif (symbols[clicked_symbol] == "X"
                  and symbols[clicked_symbol + 1] == "O"):
                symbols[clicked_symbol] = "O"
                symbols.pop(clicked_symbol + 1)
                player_points[0] += 1
                return True
        elif current_player == "X":  # Crosses
            if (symbols[clicked_symbol] == "O"
                    and symbols[clicked_symbol + 1] == "O"):
                symbols[clicked_symbol] = "X"
                symbols.pop(clicked_symbol + 1)
                player_points[1] += 2
                return True
            elif (symbols[clicked_symbol] == "O"
                  and symbols[clicked_symbol + 1] == "X"):
                symbols[clicked_symbol] = "X"
                symbols.pop(clicked_symbol + 1)
                player_points[1] += 1
                return True
    return False  # Invalid move

# Function to check if the game is over
def is_game_over(symbols, current_player):
    if len(symbols) == 1:
        return True  # If only one symbol left, the game is over
    if current_player == "O":  # Circles
        for i in range(len(symbols) - 1):
            if (symbols[i] == "X" and symbols[i + 1] == "X") or (
                    symbols[i] == "X" and symbols[i + 1] == "O"):
                return False  # If XX or XO combination is found, the game is not over
    elif current_player == "X":  # Crosses
        for i in range(len(symbols) - 1):
            if (symbols[i] == "O" and symbols[i + 1] == "O") or (
                    symbols[i] == "O" and symbols[i + 1] == "X"):
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
        restart_button.x,
        restart_button.y,
    )
    draw_text(screen, "Quit", font, BLACK, quit_button.x,
              quit_button.y)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    return start_game()  # Restart game
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
    current_player = "O"  # 0 for circles, 1 for crosses
    player_points = [0, 0]
    human = True
    level = 0
    game_path = []

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

    # Create the root node with the initial board state
    root = TreeNode(symbols, player_points)
    game_path.append(root)
    
    # Build the game tree 3 levels
    build_game_tree(root, current_player, 3)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            
            if human:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if any symbol was clicked
                    for symbols_clicked, rect in enumerate(symbol_rects):
                        if rect.collidepoint(event.pos):
                            print("Symbol clicked:", symbols_clicked)
                            if player_move(level, game_path, symbols_clicked):
                                level +=1
                                human = False
                            break  # Exit the loop after processing the click
            else:
                if computer_move(level, game_path):
                    level +=1
                    human = True
                break    
            

        # Draw everything
        screen.fill(WHITE)
        draw_symbols(symbols)
        draw_scores(player_points)  # Draw scores
        display_player_turn(current_player)

        # Check for game over
        if is_game_over(symbols, current_player):
            display_winner(screen, player_points)

        pygame.display.flip()
        clock.tick(FPS)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Symbol Game")
clock = pygame.time.Clock()

# Start the game
start_game()