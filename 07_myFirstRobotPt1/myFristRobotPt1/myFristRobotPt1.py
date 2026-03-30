# import packages for the app
import tkinter as tk    # we will use the GUI 
import random           # so our agent moves randomly
import time             # so our agent slows down to human speed          

# ***** Make the GUI *****
window = tk.Tk()        # Create main app window
window.title("Agent JoBot: Knight Security Bot")  # Set title of window as the name of the App

# ***** Create the reinforcement learning environment - 'Board to Death Lumber top down 2D view' *****
num_rows = 6
num_cols = 10

cell_size = 70  # set the square size per cell
robot_row = 0   # Set agent current state - row
robot_col = 0   # Set agent current state - col

# ***** Create canvas for the environment *****
canvas = tk.Canvas(window, width=num_cols * cell_size, height=num_rows * cell_size, bg="white")
canvas.pack()   # Add canvas to GUI window

# Function for the grid system on screen
def draw_grid():
    for i in range(num_rows + 1):
        canvas.create_line(0, i * cell_size, num_cols * cell_size, i * cell_size, fill="black")
    for i in range(num_cols + 1):
        canvas.create_line(0, i * cell_size, num_rows * cell_size, i * cell_size, fill="black")
    for row in range(num_rows):
        for col in range(num_cols):
            x = col * cell_size + cell_size / 2
            y = row * cell_size + cell_size / 2
            canvas.create_text(x, y + 30, text="Row" + str(row) + ",Col" + str(col), fill="gray")

# Function to create Agent JoBot
def draw_robot():
    canvas.delete('all')    # Delete everything on our canvas each time and redraw it
    draw_grid()             # draw new grid

    # Calculate positon for Agent JoBot (state)
    x1 = robot_col * cell_size # x position
    y1 = robot_row * cell_size # y position
    
    # right side
    x2 = x1 + cell_size 
    y2 = y1 + cell_size

    canvas.create_rectangle(x1, y1, x2, y2, fill="blue") # Agent JoBot is now blue
    canvas.create_text(x1 + cell_size //2, y1 + cell_size //2, text="JoBot", fill="white", font=("Arial", 12, "bold"))

# Function to move JoBot randomly (everything starts randomly_use Random)
def move_robot(move_num=0, total_moves=0):
    global robot_row, robot_col                     # track robot state using the following variables
    directions = ["up", "down", "left", "right"]    # Jobot can move Up, Down, Left, Right - NOT diagnally
    direction = random.choice(directions)           # JoBot will move in a randlom direction from the list we made above

    # Evaluate the direction JoBot chose to move randomly
    if direction == "up":                               # Up                        
        robot_row = max(0, robot_row - 1)
    elif direction == "down":                           # Down                        
        robot_row = min(num_rows - 1, robot_row + 1)
    elif direction == "left":                           # Left                         
        robot_col = max(0, robot_col - 1)
    elif direction == "right":                          # Right                        
        robot_col = min(num_cols - 1, robot_col + 1)

    # Draw robot at the new position(state) it moved to
    draw_robot()

    # Keep user informed of JoBot's state by printing to the console (GUI in our case)
    print(f"Move {move_num} of {total_moves}: Knight Security JoBot moved {direction} to position: Row {robot_row}, Column {robot_col}")
        