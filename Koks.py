class TreeNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []

    def add_child(self, child_state):
        child_node = TreeNode(child_state, self)
        self.children.append(child_node)
        return child_node

# Function to generate all possible next moves
def generate_moves(symbols, player):
    moves = []
    for i in range(len(symbols)-1):
        if player == "O":
            if symbols[i] == "X" and symbols[i+1] == "X":
                new_symbols = symbols.copy()
                new_symbols[i] = player
                new_symbols.pop(i+1)
                moves.append(new_symbols)
            elif symbols[i] == "X" and symbols[i+1] == "O":
                new_symbols = symbols.copy()
                new_symbols[i] = player
                new_symbols.pop(i+1)
                moves.append(new_symbols)
        else:
            if symbols[i] == "O" and symbols[i+1] == "O":
                new_symbols = symbols.copy()
                new_symbols[i] = player
                new_symbols.pop(i+1)
                moves.append(new_symbols)
            elif symbols[i] == "O" and symbols[i+1] == "X":
                new_symbols = symbols.copy()
                new_symbols[i] = player
                new_symbols.pop(i+1)
                moves.append(new_symbols)
    return moves
    
# Recursive function to build the game tree
def build_game_tree(node, player):
    current_symbols = node.state
    next_player = "O" if player == "X" else "X"

    moves = generate_moves(current_symbols, player)
    for move in moves:
        child_node = node.add_child(move)
        build_game_tree(child_node, next_player)


# Initial symbols list
initial_symbols = ["O","X","O","X","X","O","X","X","O"]

# Create the root node with the initial board state
root = TreeNode(initial_symbols)

# Build the game tree
build_game_tree(root, "O")

# Print the initial symbols and the first level of child moves
print("Initial symbols:")
print(initial_symbols)

for child in root.children:
    print("Child symbols after one move:")
    print(child.state)
    print()
    for grandchild in child.children:
        print("Grandchild symbols after one move:")
        print(grandchild.state)
        print()
        print("Greatgrandchild symbols after one move:")
        for greatgrandchild in grandchild.children:
            print(greatgrandchild.state)
            print()