'''
Making use of the A* algorithm to find the shortest path from a beginning point to an end-goal point in a maze. 
This program has the user define the size of the maze and the starting and end points. The obstacles are represented by 1's. 0's are permitted positions to move through. Diagonal movement is allowed. 
'''

import random

# Create a Node class for all positioning
class Node():

    def __init__(self, position=None, parent=None):
        self.position = position
        self.parent = parent

        # create h,g, and f values to calculate path costs
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


'''
A* algorithm. The functon returns a tuple of 
coordinates we have traveled from the starting coordinate
to the end coordinate
'''
def astar(maze,start,end):

    # First check that the start and end points are within the maze
    if start[0] > len(maze) or start[1] > len(maze):
        print("Start point not within maze specified. Please try again with a different end point.") 
        return

    if end[0] > len(maze) or end[1] > len(maze):
        print("End point not within maze specified. Please try again with a different end point.") 
        return

    # Create the start and end nodes
    start_node = Node(start, None)
    start_node.f = start_node.g = start_node.h = 0
    end_node = Node(end, None)
    end_node.f = end_node.g = end_node.h = 0

    # Initialize open and closed lists
    open_list = []
    closed_list = []

    # Add the start node to the open list
    open_list.append(start_node)

    # Go through the open list
    while len(open_list) > 0:

        # Get current node
        current_node = open_list[0]
        current_index = 0
        
        # Go to node with smallest f values (g + h) 
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
    
        # Pop the current_node off the open (currently searching nodes)
        # and add it to the closed list which will eventually become our path
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Check if we've found the goal before we start traveling again
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Show path from beginning to end

        # Generate the childen nodes
        children = []

        # Create the valid moves. Allowing for diagnonal movement. 
        # Allowing for diagonal movement will return mostly diagonal moves, but
        # it is the least costly path. Obstacles (1's) will help mitigate that we don't 
        # just return a diagonal line.
        
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            

            # Get the next node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # make sure that the position is valid
            if (node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze) - 1]) - 1) or node_position[1] < 0):
                continue
            
            # Skip obstacles. Obstacles in maze carry a '1' value 
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Make the node for this position
            new_node = Node(node_position, current_node)

            # Append this new node to the children list
            children.append(new_node)

        # add f,g, and h values and add the child node to the open list

        for child in children:

            # Check if the child is on the closed list
            for closed_children in closed_list:
                if child == closed_children:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1

            # heuristic is pythagorean them or the manhattan distance
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            
            # Assign the total cost 
            child.f = child.g + child.h

            # Check if the child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add this node to the open list (possible movements)
            open_list.append(child)





# Have the user define the dimensions of the maze. Also have user define start and end coordinates

# The obstacles are randomly generated making use of the 'random' library.

# Output the maze and the path.

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
