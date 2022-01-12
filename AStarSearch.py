import random

'''
A* (star) Pathfinding// Initialize both open and closed list
let the openList equal empty list of nodes
let the closedList equal empty list of nodes// Add the start node
put the startNode on the openList (leave it's f at zero)// Loop until you find the end
while the openList is not empty    // Get the current node
    let the currentNode equal the node with the least f value
    remove the currentNode from the openList
    add the currentNode to the closedList    // Found the goal
    if currentNode is the goal
        Congratz! You've found the end! Backtrack to get path    // Generate children
    let the children of the currentNode equal the adjacent nodes
    
    for each child in the children        // Child is on the closedList
        if child is in the closedList
            continue to beginning of for loop        // Create the f, g, and h values
        child.g = currentNode.g + distance between child and current
        child.h = distance from child to end
        child.f = child.g + child.h        // Child is already in openList
        if child.position is in the openList's nodes positions
            if the child.g is higher than the openList node's g
                continue to beginning of for loop        // Add the child to the openList
        add the child to the openList'''

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Check that the start and end points are within the maze
    if start[0] > len(maze) or start[1] > len(maze):
        print("Start point not within maze specified. Please try again with a different end point.") 
        return

    if end[0] > len(maze) or end[1] > len(maze):
        print("End point not within maze specified. Please try again with a different end point.") 
        return

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares. We can allow for Diagonal movement by adding:  (-1, -1), (-1, 1), (1, -1), (1, 1)

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)


def main():
    
    # Create maze
    inputRows = int(input("\nPlease enter the amount of rows you'd like for the maze: ")) 
    inputColumns = int(input("Please enter the amount of columns you'd like for the maze: ")) 
   
    mazeInput = []
    for i in range(inputRows):
        mazeInput.append([0]*inputColumns)


    # Create obstacles randomly 
    j = 0
    while j < inputColumns:
        randomObstacle = random.randint(1,inputRows - 1)
        mazeInput[randomObstacle][j] = 1
        j += 1


    # Get starting coordinates and goal coordinates
    startInput = input("\nPlease enter the coordinate for the starting point, only separated by a comma ( i.e. - 0,0 ): " )
    endInput = input("Please enter the coordinate for the end point, only separated by a comma ( i.e. - 0,0 ): " )

    
    startList = [ int(x.strip()) for x in startInput.split(",") if x.strip() ]
    endList = [ int(x.strip()) for x in endInput.split(",") if x.strip() ]

    # convert to tuple for immutability
    start = tuple(startList)
    end = tuple(endList)

    print("\n\nstarting position: ", start)
    print("goal position: ", end)

    
    print("\n Maze")
    for r in mazeInput:
        print("\n", r)

    # initialize astar algorithm
    path = astar(mazeInput, start, end)
    print("\n\n Path",path)


if __name__ == '__main__':
    main()