import sys
from collections import deque
from datetime import datetime

# Structure of a node
class Node:
    def __init__(self, state, action, g, d, parent,h=0,f=0):
        self.state = state  # The state of the puzzle
        self.action = action  # The action taken
        self.g = g  # The cost so far to reach n
        self.d = d  # The depth 
        self.parent = parent  # A reference to the parent node
        self.h = h # The heuristic value
        self.f = f # The evaluation value
# Keep tracking the stats
class Statistics:
    def __init__(self):
        self.nodes_popped = 0
        self.nodes_expanded = 0
        self.nodes_generated = 0
        self.max_fringe_size = 0
############### Functions ######################################################
# Extract the initi tile and the goal tile
def read_puzzle_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    puzzle = []
    for line in lines:
        if line.strip() == "END OF FILE":
            break
        puzzle.append([int(num) for num in line.strip().split()])
    return puzzle
# Print result
def print_result(result):
    print(f"Solution Found at depth {result.d} with cost of {result.g}")
    # Backtrack from result node to the start node
    steps = []
    while result.parent is not None:
        steps.append(result.action)
        result = result.parent
    # print in the correct order
    print("Steps:")
    for step in reversed(steps):
        print("\t"+ step)
# Find vaild successors
def successor_fn(state):
    successors = []

    # Find the position of the blank tile in the current state
    blank_row = 0
    blank_col = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                blank_row = i
                blank_col = j
    # Define possible moves (up, down, right, left)
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Generate successor actions & results
    for move_row, move_col in moves:
        new_row = blank_row + move_row
        new_col = blank_col + move_col

        # Is new position valid?
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            # copy the current state
            new_state = [row[:] for row in state]

            # Swap the blank tile with the adjacent tile
            new_state[blank_row][blank_col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[blank_row][blank_col]

            # Determine the direction
            direction = ''
            if move_row == 1:
                direction = 'Up'
            elif move_row == -1:
                direction = 'Down'
            elif move_col == 1:
                direction = 'Left'
            elif move_col == -1:
                direction = 'Right'

            action = f"Move {state[new_row][new_col]} {direction}"

            # Add the action & the resulting state
            successors.append((action, new_state))

    return successors
# Return a set of vaild successors
def expand_node(node):
    successors = []

    # Generate successor actions & results
    for action, result in successor_fn(node.state):
        # Create a new Node
        successor = Node(state=result, action=action, g=0, d=0, parent=node)

        # Calculate g and d for the successor based on the parent node
        successor.g = node.g + int(action.split()[-2])
        successor.d = node.d + 1

        successors.append(successor)
    
    return successors
# Find a heuristic value
def heuristic(state, goal):
    h = 0 

    # store the positions
    current_loc = {}
    goal_loc = {}

    # Populate the dictionaries with tile positions
    for i in range(3):
        for j in range(3):
            current_loc[state[i][j]] = (i, j)
            goal_loc[goal[i][j]] = (i, j)

    # Calculate the Manhattan distance for each tile and accumulate the total heuristic value
    for tile in range(1, 9):  # Tiles 1 to 8
        current_pos = current_loc[tile]
        goal_pos = goal_loc[tile]
        h += tile*(abs(current_pos[0] - goal_pos[0]) + abs(current_pos[1] - goal_pos[1]))

    return h
############### Methods ########################################################
def BFS(problem,goal,fringe,closed,file_flag,f):
    #initialize 
    stat = Statistics()
    init_node = Node(problem, "Start", 0, 0, None)
    stat.nodes_generated += 1
    fringe.append(init_node)

    while True:

        # is noting in the fringe?
        if len(fringe) == 0:
            print("No solution found.")
            return False

        # update the max fringe size
        if len(fringe) > stat.max_fringe_size:
            stat.max_fringe_size = len(fringe)

        # pop a node from fringe
        node = fringe.popleft()
        stat.nodes_popped += 1

        # is the node match the goal?
        if node.state == goal:
            print(f"Nodes Popped: {stat.nodes_popped}\nNodes Expanded: {stat.nodes_expanded}\nNodes Generated: {stat.nodes_generated}\nMax Fringe Size: {stat.max_fringe_size}")
            if file_flag == 1:
                f.write(f"\tNodes Popped: {stat.nodes_popped}\n\tNodes Expanded: {stat.nodes_expanded}\n\tNodes Generated: {stat.nodes_generated}\n\tMax Fringe Size: {stat.max_fringe_size}")
            return node
        
        # is the node in the closed?
        if node.state not in closed:
            closed.append(node.state)
        
        # Expand the current node and generate successors
            successors = expand_node(node)
            stat.nodes_expanded += 1
            # Adding successors to the fringe
            for successor in successors:
                fringe.append(successor)
                stat.nodes_generated += 1

            if file_flag == 1:
                f.write(f"Generating successors to < state = {node.state}, action = {node.action} g(n) = {node.g}, d = {node.d}, Parent = Pointer to {node.parent} >\n")
                f.write(f"\t{len(successors)} successors generated\n")
                f.write(f"\tClosed: {list(closed)}\n")
                f.write(f"\tFringe: [\n")
                for x in fringe:
                    f.write(f"\t\t\t< state = {x.state}, action = {x.action} g(n) = {x.g}, d = {x.d}, Parent = Pointer to {x.parent} >\n")
def UCS(problem,goal,fringe,closed,file_flag,f):
    #initialize 
    stat = Statistics()
    init_node = Node(problem, "Start", 0, 0, None)
    stat.nodes_generated += 1
    fringe.append(init_node)
    
    while True:

        # noting in the fringe
        if len(fringe) == 0:
            print("No solution found.")
            return False
        
        # update the max fringe size
        if len(fringe) > stat.max_fringe_size:
            stat.max_fringe_size = len(fringe)

        # pop a node from fringe
        node = fringe.popleft()
        stat.nodes_popped += 1

        # is the node match the goal?
        if node.state == goal:
            print(f"Nodes Popped: {stat.nodes_popped}\nNodes Expanded: {stat.nodes_expanded}\nNodes Generated: {stat.nodes_generated}\nMax Fringe Size: {stat.max_fringe_size}")
            if file_flag == 1:
                f.write(f"\tNodes Popped: {stat.nodes_popped}\n\tNodes Expanded: {stat.nodes_expanded}\n\tNodes Generated: {stat.nodes_generated}\n\tMax Fringe Size: {stat.max_fringe_size}")
            return node
        
        # is the node in the closed?
        if node.state not in closed:
            closed.append(node.state)

            # Expand the current node and generate successors
            successors = expand_node(node)
            stat.nodes_expanded += 1
            # Adding successors to the fringe
            for successor in successors:
                fringe.append(successor)
                stat.nodes_generated += 1
            # Sorting by cost
            fringe = deque(sorted(list(fringe), key=lambda x: x.g))

            if file_flag == 1:
                f.write(f"Generating successors to < state = {node.state}, action = {node.action} g(n) = {node.g}, d = {node.d}, Parent = Pointer to {node.state} >\n")
                f.write(f"\t{len(successors)} successors generated\n")
                f.write(f"\tClosed: {list(closed)}\n")
                f.write(f"\tFringe: [\n")
                for x in fringe:
                    f.write(f"\t\t\t< state = {x.state}, action = {x.action} g(n) = {x.g}, d = {x.d}, Parent = Pointer to {x.parent} >\n")
def GREEDY(problem,goal,fringe,closed,file_flag,f):
    #initialize 
    stat = Statistics()
    init_node = Node(problem, "Start", 0, 0, None, heuristic(problem,goal))
    stat.nodes_generated += 1
    fringe.append(init_node)
    
    while True:

        # noting in the fringe
        if len(fringe) == 0:
            print("No solution found.")
            return False
        
        # update the max
        if len(fringe) > stat.max_fringe_size:
            stat.max_fringe_size = len(fringe)

        # pop a node from fringe
        node = fringe.popleft()
        stat.nodes_popped += 1
        
        # is the node match the goal?
        if node.state == goal:
            print(f"Nodes Popped: {stat.nodes_popped}\nNodes Expanded: {stat.nodes_expanded}\nNodes Generated: {stat.nodes_generated}\nMax Fringe Size: {stat.max_fringe_size}")
            if file_flag == 1:
                f.write(f"\tNodes Popped: {stat.nodes_popped}\n\tNodes Expanded: {stat.nodes_expanded}\n\tNodes Generated: {stat.nodes_generated}\n\tMax Fringe Size: {stat.max_fringe_size}")
            return node
        
        # is the node in the closed?
        if node.state not in closed:
            closed.append(node.state)
            # Expand the current node and generate successors
            successors = expand_node(node)
            stat.nodes_expanded += 1
            # Adding successors to the fringe
            for successor in successors:
                successor.h = heuristic(successor.state, goal)
                fringe.append(successor)
                stat.nodes_generated += 1
            # sort by the value of heuristic
            fringe = deque(sorted(list(fringe), key=lambda x: x.h))
            if file_flag == 1:
                f.write(f"Generating successors to < state = {node.state}, action = {node.action} g(n) = {node.g}, d = {node.d}, h = {node.h}, Parent = Pointer to {node.parent} >\n")
                f.write(f"\t{len(successors)} successors generated\n")
                f.write(f"\tClosed: {list(closed)}\n")
                f.write(f"\tFringe: [\n")
                for x in fringe:
                    f.write(f"\t\t\t< state = {x.state}, action = {x.action} g(n) = {x.g}, d = {x.d}, h = {x.h}, Parent = Pointer to {x.parent} >\n")
def A_STAR(problem,goal,fringe,closed,file_flag,f):
    #initialize 
    stat = Statistics()
    init_node = Node(problem, "Start", 0, 0, None, heuristic(problem,goal), heuristic(problem,goal))
    stat.nodes_generated += 1
    fringe.append(init_node)

    while True:

        # is noting in the fringe?
        if len(fringe) == 0:
            print("No solution found.")
            return False

        # update the max fringe size
        if len(fringe) > stat.max_fringe_size:
            stat.max_fringe_size = len(fringe)

        # pop a node from fringe
        node = fringe.popleft()
        stat.nodes_popped += 1
 
        # is the node match the goal?
        if node.state == goal:
            print(f"Nodes Popped: {stat.nodes_popped}\nNodes Expanded: {stat.nodes_expanded}\nNodes Generated: {stat.nodes_generated}\nMax Fringe Size: {stat.max_fringe_size}")
            if file_flag == 1:
                f.write(f"\tNodes Popped: {stat.nodes_popped}\n\tNodes Expanded: {stat.nodes_expanded}\n\tNodes Generated: {stat.nodes_generated}\n\tMax Fringe Size: {stat.max_fringe_size}")
            return node
        
        # is the node in the closed?
        if node.state not in closed:
            closed.append(node.state)
            # Expand the current node and generate successors
            successors = expand_node(node)
            stat.nodes_expanded += 1
            # Adding successors to the fringe
            for successor in successors:
                successor.h = heuristic(successor.state,goal)
                successor.f = successor.h + successor.g
                fringe.append(successor)
                stat.nodes_generated += 1
            # sort by the value of evaluation (f(n))
            fringe = deque(sorted(list(fringe), key=lambda x: x.f))
            if file_flag == 1:
                f.write(f"Generating successors to < state = {node.state}, action = {node.action} g(n) = {node.g}, d = {node.d}, f(n) = {node.f}, Parent = Pointer to {node.parent} >\n")
                f.write(f"\t{len(successors)} successors generated\n")
                f.write(f"\tClosed: {list(closed)}\n")
                f.write(f"\tFringe: [\n")
                for x in fringe:
                    f.write(f"\t\t\t< state = {x.state}, action = {x.action} g(n) = {x.g}, d = {x.d}, f(n) = {x.f}, Parent = Pointer to {x.parent} >\n")
def DFS(problem,goal,fringe,closed,file_flag,f):
    #initialize 
    stat = Statistics()
    init_node = Node(problem, "Start", 0, 0, None)
    stat.nodes_generated += 1
    fringe.append(init_node)

    while True:
        # is noting in the fringe?
        if len(fringe) == 0:
            print("No solution found.")
            return False

        # update the max fringe size
        if len(fringe) > stat.max_fringe_size:
            stat.max_fringe_size = len(fringe)

        # pop a node from fringe
        node = fringe.pop()
        stat.nodes_popped += 1
 
        # is the node match the goal?
        if node.state == goal:
            print(f"Nodes Popped: {stat.nodes_popped}\nNodes Expanded: {stat.nodes_expanded}\nNodes Generated: {stat.nodes_generated}\nMax Fringe Size: {stat.max_fringe_size}")
            if file_flag == 1:
                f.write(f"\tNodes Popped: {stat.nodes_popped}\n\tNodes Expanded: {stat.nodes_expanded}\n\tNodes Generated: {stat.nodes_generated}\n\tMax Fringe Size: {stat.max_fringe_size}")
            return node
        

        # is the node in the closed?
        if node.state not in closed:
            closed.append(node.state)
            # Expand the current node and generate successors
            successors = expand_node(node)
            stat.nodes_expanded += 1
            # Adding successors to the fringe
            for successor in successors:
                fringe.append(successor)
                stat.nodes_generated += 1

            if file_flag == 1:
                f.write(f"Generating successors to < state = {node.state}, action = {node.action} g(n) = {node.g}, d = {node.d}, Parent = Pointer to {node.parent} >\n")
                f.write(f"\t{len(successors)} successors generated\n")
                f.write(f"\tClosed: {list(closed)}\n")
                f.write(f"\tFringe: [\n")
                for x in fringe:
                    f.write(f"\t\t\t< state = {x.state}, action = {x.action} g(n) = {x.g}, d = {x.d}, Parent = Pointer to {x.parent} >\n")
def DLS(problem,goal,fringe,closed,depth_limit,file_flag,f):
    #initialize 
    stat = Statistics()
    init_node = Node(problem, "Start", 0, 0, None)
    stat.nodes_generated += 1
    fringe.append(init_node)
    

    while True:
        # Is noting in the fringe?
        if len(fringe) == 0:
            print("No solution found.")
            return False

        # Update the max fringe size
        if len(fringe) > stat.max_fringe_size:
            stat.max_fringe_size = len(fringe)

        # Pop a node from fringe
        node = fringe.pop()
        stat.nodes_popped += 1
        
        # Is the node match the goal?
        if node.state == goal:
            print(f"Nodes Popped: {stat.nodes_popped}\nNodes Expanded: {stat.nodes_expanded}\nNodes Generated: {stat.nodes_generated}\nMax Fringe Size: {stat.max_fringe_size}")
            if file_flag == 1:
                f.write(f"\tNodes Popped: {stat.nodes_popped}\n\tNodes Expanded: {stat.nodes_expanded}\n\tNodes Generated: {stat.nodes_generated}\n\tMax Fringe Size: {stat.max_fringe_size}")
            return node
        
   
        # Is the node not in the closed and not over the depth_limit?
        if node.state not in closed:
            closed.append(node.state)
            # Expand the current node and generate successors
            if node.d < depth_limit:
                successors = expand_node(node)
                stat.nodes_expanded += 1
                # Adding successors to the fringe
                for successor in successors:
                    fringe.append(successor)
                    stat.nodes_generated += 1

                if file_flag == 1:
                    f.write(f"Generating successors to < state = {node.state}, action = {node.action} g(n) = {node.g}, d = {node.d}, Parent = Pointer to {node.parent} >\n")
                    f.write(f"\t{len(successors)} successors generated\n")
                    f.write(f"\tClosed: {list(closed)}\n")
                    f.write(f"\tFringe: [\n")
                    for x in fringe:
                        f.write(f"\t\t\t< state = {x.state}, action = {x.action} g(n) = {x.g}, d = {x.d}, Parent = Pointer to {x.parent} >\n")
def IDS(problem,goal,fringe,closed,file_flag,f):
    # Base case l = 0
    depth_limit = 0

    while True:
        # Initialize 
        stat = Statistics()
        init_node = Node(problem, "Start", 0, 0, None)
        stat.nodes_generated += 1
        closed = []
        fringe.append(init_node)
        while len(fringe):
            # Update the max fringe size
            if len(fringe) > stat.max_fringe_size:
                stat.max_fringe_size = len(fringe)

            # Pop a node from fringe
            node = fringe.pop()
            stat.nodes_popped += 1
            # Is the node match the goal?
            if node.state == goal:
                print(f"Nodes Popped: {stat.nodes_popped}\nNodes Expanded: {stat.nodes_expanded}\nNodes Generated: {stat.nodes_generated}\nMax Fringe Size: {stat.max_fringe_size}")
                if file_flag == 1:
                    f.write(f"\tNodes Popped: {stat.nodes_popped}\n\tNodes Expanded: {stat.nodes_expanded}\n\tNodes Generated: {stat.nodes_generated}\n\tMax Fringe Size: {stat.max_fringe_size}")
                return node
            

            # Is the node not in the closed and not over the depth_limit?
            if node.state not in closed:
                closed.append(node.state)
                # Expand the current node and generate successors
                if node.d < depth_limit:
                    successors = expand_node(node)
                    stat.nodes_expanded += 1
                    # Adding successors to the fringe
                    for successor in successors:
                        fringe.append(successor)
                        stat.nodes_generated += 1

                    if file_flag == 1:
                        f.write(f"Generating successors to < state = {node.state}, action = {node.action} g(n) = {node.g}, d = {node.d}, Parent = Pointer to {node.parent} >\n")
                        f.write(f"\t{len(successors)} successors generated\n")
                        f.write(f"\tClosed: {list(closed)}\n")
                        f.write(f"\tFringe: [\n")
                        for x in fringe:
                            f.write(f"\t\t\t< state = {x.state}, action = {x.action} g(n) = {x.g}, d = {x.d}, Parent = Pointer to {x.parent} >\n")
        # if d reaches the limit +1                
        depth_limit += 1
############### Main ############################################################ 
# check arguments
if len(sys.argv) < 3 or len(sys.argv) > 5:
    print("format: expense_8_puzzle.py <start-file> <goal-file> [<method>] [<dump-flag>]")
    sys.exit(1)

# Extract the command line
start_file = sys.argv[1]
goal_file = sys.argv[2]

if len(sys.argv) == 3:
    method = "a*"
else:
    method = sys.argv[3]

# Is <dump-flag> true or false?
if len(sys.argv) == 3 or len(sys.argv) == 4:
    dump_flag = "false"
else:
    dump_flag = sys.argv[4]
file_flag = 0
f = 0
if dump_flag == "true":
    # Current date and time
    now = datetime.now()
    dt_string = now.strftime("%m_%d_%Y-%H_%M_%S")
    f = open (f"trace-" + dt_string + ".txt", "w+")
    file_flag = 1
elif dump_flag != "false" and dump_flag != "true":
    print("Please type true or false for [<dump-flag>]")
    sys.exit(1)

if file_flag == 1:
    f.write("Command-Line Arguments : " + start_file + " " + goal_file + " " + method + " " + dump_flag + "\n")
    f.write("Method Selected : " + method + "\n")

# Read the start and goal puzzles from the files
start_puzzle = read_puzzle_file(start_file)
goal_puzzle = read_puzzle_file(goal_file)

# Initialize
fringe = deque()
closed = deque()

if method == "bfs":
    if file_flag == 1:
        f.write("Running : " + method + "\n")
    result = BFS(start_puzzle,goal_puzzle,fringe,closed,file_flag,f)
    if result:
        print_result(result)
elif method == "ucs":
    if file_flag == 1:
        f.write("Running : " + method + "\n")
    result = UCS(start_puzzle,goal_puzzle,fringe,closed,file_flag,f)
    if result:
        print_result(result)
elif method == "greedy":
    if file_flag == 1:
        f.write("Running : " + method + "\n")
    result = GREEDY(start_puzzle,goal_puzzle,fringe,closed,file_flag,f)
    if result:
        print_result(result)
elif method == "a*":
    if file_flag == 1:
        f.write("Running : " + method + "\n")
    result = A_STAR(start_puzzle,goal_puzzle,fringe,closed,file_flag,f)
    if result:
        print_result(result)
elif method == "dfs":
    if file_flag == 1:
        f.write("Running : " + method + "\n")
    result = DFS(start_puzzle,goal_puzzle,fringe,closed,file_flag,f)
    if result:
        print_result(result)
elif method == "dls":
    depth_limit = int(input("Enter the depth limit: "))
    if depth_limit < 0:
        print("Depth limit must be >= 0")
        sys.exit(1)
    if file_flag == 1:
        f.write("Running : " + method + "\n")
    result = DLS(start_puzzle,goal_puzzle,fringe,closed,depth_limit,file_flag,f)
    if result:
        print_result(result)
elif method == "ids":
    if file_flag == 1:
        f.write("Running : " + method + "\n")
    result = IDS(start_puzzle,goal_puzzle,fringe,closed,file_flag,f)
    if result:
        print_result(result)
else:
    print("please type another method (bfs/ucs/greedy/a\*/dfs/dls/ids)")
#################################################################################