class TreeNode:
    def __init__(self, state, score, value=None, parent=None):
        self.state = state
        self.score = score #player score
        self.value = value #heuristic value
        self.parent = parent
        self.children = []

    def add_child(self, child_state, child_score):
        child_node = TreeNode(child_state, child_score, self)
        self.children.append(child_node)
        return child_node

# Function to generate all possible next moves
def generate_moves(symbols, score, player):
    moves = []
    for i in range(len(symbols)-1):
        temp_score = score.copy()
        if player == "O":
            if symbols[i] == "X" and symbols[i+1] == "X":
                new_symbols = symbols.copy()
                new_symbols[i] = player
                new_symbols.pop(i+1)
                temp_score[0]+=2
                move = [new_symbols,temp_score]
                moves.append(move)
            elif symbols[i] == "X" and symbols[i+1] == "O":
                new_symbols = symbols.copy()
                new_symbols[i] = player
                new_symbols.pop(i+1)
                temp_score[0]+=1
                move = [new_symbols,temp_score]
                moves.append(move)
        else:
            if symbols[i] == "O" and symbols[i+1] == "O":
                new_symbols = symbols.copy()
                new_symbols[i] = player
                new_symbols.pop(i+1)
                temp_score[1]+=2
                move = [new_symbols,temp_score]
                moves.append(move)
            elif symbols[i] == "O" and symbols[i+1] == "X":
                new_symbols = symbols.copy()
                new_symbols[i] = player
                new_symbols.pop(i+1)
                temp_score[1]+=1
                move = [new_symbols,temp_score]
                moves.append(move)
    return moves
    
# Recursive function to build the game tree
def build_game_tree(node, player):
    current_symbols = node.state
    current_score = node.score
    #current_value = node.value
    next_player = "O" if player == "X" else "X"

    moves = generate_moves(current_symbols, current_score, player)
    for move in moves:
        child_node = node.add_child(move[0],move[1])
        build_game_tree(child_node, next_player)


# Initial symbols list
initial_symbols = ["O","X","O","X","X","O","X","X","O"]
initial_score = [0,0]

# Create the root node with the initial board state
root = TreeNode(initial_symbols, initial_score)

# Build the game tree
build_game_tree(root, "O")

# Print the initial symbols and the first level of child moves
print("Initial symbols:")
print(initial_symbols)
print("Initial score:")
print(initial_score)

for child in root.children:
    print("Child symbols after one move:")
    print(child.state)
    print()
    print(child.score)
    print()
    for grandchild in child.children:
        print("Grandchild symbols after one move:")
        print(grandchild.state)
        print()
        print(grandchild.score)
        print()
        print("Greatgrandchild symbols after one move:")
        for greatgrandchild in grandchild.children:
            print(greatgrandchild.state)
            print()
            print(greatgrandchild.score)
            print()
#some change