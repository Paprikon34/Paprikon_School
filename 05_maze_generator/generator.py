import random
import sys

# Increase recursion limit (just in case a huge maze is generated)
sys.setrecursionlimit(5000)

# Maze size (must be odd numbers, e.g., 31 and 15)
WIDTH = 31
HEIGHT = 15

# Define how walls and paths will look (we use 2 characters for each, to make a nice square)
WALL = "██"
PATH = "  "

def create_empty_maze():
    """ 
    Creates a map that is completely filled with soil (walls everywhere).
    Returns a 2D list of walls.
    """
    maze_map = []
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            row.append(WALL)
        maze_map.append(row)
    return maze_map

def dig_tunnel(x, y, maze_map):
    """
    This is the main FUNCTION (the mole). It digs a hole, randomly looks around and goes further.
    """
    # Mark the current spot as a dug path (empty)
    maze_map[y][x] = PATH
    
    # 4 directions where the mole can dig (Up, Down, Left, Right)
    # We always jump by 2 cells! This is to always leave a thin wall between paths.
    # The layout is: (jump_amount_on_X, jump_amount_on_Y)
    directions = [
        (0, -2), # Up (y decreases by 2)
        (0, 2),  # Down (y increases by 2)
        (-2, 0), # Left (x decreases by 2)
        (2, 0)   # Right (x increases by 2)
    ]
    
    # Shuffle the directions! That's why every maze is different - the mole has a different plan every time.
    random.shuffle(directions)
    
    # The mole tries all 4 directions sequentially in random order
    for step_x, step_y in directions:
        next_x = x + step_x
        next_y = y + step_y
        
        # We check two important things:
        # 1. Did we go off the map?
        # 2. Is there still soil (a wall) in the new place? (If there's already a path, we don't dig there)
        if 0 < next_x < WIDTH - 1 and 0 < next_y < HEIGHT - 1:
            if maze_map[next_y][next_x] == WALL:
                # We found a spot! 
                # We also smash through the wall we "jumped over", connecting both places
                maze_map[y + step_y // 2][x + step_x // 2] = PATH
                
                # RECURSION: (The most complex step - difficulty 5)
                # We call the same function again to continue from the NEW spot. 
                # When the mole finishes in the new corridor and has nowhere to go (dead end), 
                # the program steps back from the recursion here and the mole tries the next direction.
                dig_tunnel(next_x, next_y, maze_map)

# --- MAIN PROGRAM SECTION ---
if __name__ == "__main__":
    print("Running the maze generator program (Algorithm: Recursive Backtracker/Mole)...\n")

    # 1. Prepare the soil (walls)
    our_maze = create_empty_maze()

    # 2. Release the mole from the top left corner (coordinates 1, 1 inside the soil)
    dig_tunnel(1, 1, our_maze)

    # 3. From the mole's burrow, we make an Entrance and an Exit at the edges of the map to make it a playable maze
    our_maze[1][0] = PATH # Entrance is on the left
    our_maze[HEIGHT-2][WIDTH-1] = PATH # Exit is on the bottom right

    # 4. Print it nicely on the screen row by row
    for row in our_maze:
        # Convert the array of characters into a single string for the whole row
        print("".join(row))

    print("\nSuccessfully generated! Can you solve it in your head?")
