import sys

def cal_points(state):
    if (state[0] == 0):
        return state[1] * 3
    elif (state[1] == 0):
        return state[0] * 2
    
def Minimax_Decision(state,version,alpha,beta):
    if version == "standard": # Computer maximizes the value among minimum values
        v, action = Max_Value(state,alpha,beta,version)
    elif version == "misere": # Computer minimizes the value among maximum values
        v, action = Min_Value(state,alpha,beta,version)
    return v, action

def Max_Value(state,alpha,beta,version):
    if (state[0] == 0 or state[1] == 0):
        return -1*cal_points(state), None
    v = float('-inf')
    action = None
    if version == "standard": # On standard mode, it picks blue first, then red
        for a,s in std_successors(state):
            v_new, _ = Min_Value(s,alpha,beta,version)
            if v_new > v:
                v = v_new
                action = a
            if v_new >= beta:
                return v, action
            if v_new > alpha:
                alpha = v_new
    elif version == "misere": # On misere mode, it picks red first, then blue
        for a,s in mj_successors(state):
            v_new, _ = Min_Value(s,alpha,beta,version)
            if v_new > v:
                v = v_new
                action = a
            if v_new >= beta:
                return v, action
            if v_new > alpha:
                alpha = v_new
    return v, action

def Min_Value(state,alpha,beta,version):
    if (state[0] == 0 or state[1] == 0):
        return cal_points(state), None
    v = float('inf')
    action = None
    if version == "standard": # On standard mode, it picks blue first, then red
        for a,s in std_successors(state):
            v_new, _ = Max_Value(s,alpha,beta,version)
            if v_new < v:
                v = v_new
                action = a
            if v_new <= alpha:
                return v, action
            if v_new < beta:
                beta = v_new
    elif version == "misere": # On misere mode, it picks red first, then blue
        for a,s in mj_successors(state):
            v_new, _ = Max_Value(s,alpha,beta,version)
            if v_new < v:
                v = v_new
                action = a
            if v_new <= alpha:
                return v, action
            if v_new < beta:
                beta = v_new
    return v, action
# Add red, and then blue
def mj_successors(state):
    actions = []
    if state[0] > 0:
        actions.append(("red", [state[0] - 1, state[1]]))
    if state[1] > 0:
        actions.append(("blue",[state[0],state[1]-1]))
    return actions
# Add blue, and then red
def std_successors(state):
    actions = []
    if state[1] > 0:
        actions.append(("blue",[state[0],state[1]-1]))
    if state[0] > 0:
        actions.append(("red", [state[0] - 1, state[1]]))
    return actions

def whos_winner(point,player,version):
    player_point = 0
    computer_point = 0
    winner = None
    # Who was the player when the program was terminated
    if player == "human": # player lose
        if version == "standard":
            player_point = -1 * point
            computer_point = point
            winner = "computer"
        elif version == "misere":
            player_point = point 
            computer_point = -1 * point
            winner = "human"
    else: # computer lose
        if version == "standard":
            player_point = point
            computer_point = -1 *point
            winner = "human"
        elif version == "misere":
            player_point = -1 * point 
            computer_point = point
            winner = "computer"
    # Print the result
    print("======== RESULT ========")
    print(f"Winner: {winner}")
    print("Player points: " + str(player_point))
    print("Computer points: " + str(computer_point))

#########################main#########################
# Number of arguments
n = len(sys.argv)
if (n < 3 or n > 5):
    print("format: red_blue_nim.py <num-red> <num-blue> <version> <first-player> <depth>")
    sys.exit(1)
 
# Number of red and blue marbles
red = int(sys.argv[1])
blue = int(sys.argv[2])
if red < 1 or blue < 1:
    print("The number of marbles should be more than 0 to play")
    sys.exit(1)

# Version
version = "standard"
if (n > 3):
    version = sys.argv[3]
if version != "standard" and version != "misere":
    print("Type vaild version. [standard/misere]")
    sys.exit(1)

# First-player
player = "computer"
if (n > 4):
    player = sys.argv[4]
if player != "computer" and player != "human":
    print("Type vaild first player. [computer/human]")

# Limite the depth
if (n > 5):
    depth = sys.argv[5]
# Print current status
print(f"red: {red}, blue: {blue}")
print(f"Version: {version}")
print(f"first player: {player}")
print("========================")

# Initial values
bowl = [red,blue]
alpha, beta = float('-inf'), float('inf')

# Loop until one of the marbles becomes 0
while (bowl[0] != 0 and bowl[1] != 0):
    # Print the state every time an action is taken.
    print("state = " + str(bowl))
    if player == "computer": # The computer use the minmax strategy
        v, action = Minimax_Decision(bowl, version, alpha, beta)
        print(f"Computer's action: {action}")
        if action == "red":
            bowl[0] -= 1
        elif action == "blue":
            bowl[1] -= 1
        player = "human"
    elif player == "human": # An user take input
        action = input("Your action: ")
        if action == "red":
            bowl[0] -= 1
        elif action == "blue":
            bowl[1] -= 1
        else:
            print(f"\"{action}\" is not a vaild command. [red/blue]")
            continue
        player = "computer"

# Print the final state
print("state = " + str(bowl))
# Caculate the point
point = cal_points(bowl)
# Decide who is the winner
whos_winner(point,player,version)