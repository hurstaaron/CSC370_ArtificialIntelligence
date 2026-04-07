###################################################################
#   1) Adding red lettering for the rewards on teh canvas
#   2) Removing [ ] around the reward numbers
#   CSC370 Artificial Intelligence
#   Professor Hinton
#   By Aaron Hurst
#   07Apr26
###################################################################

# import packages for the app
from shutil import move
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

# Create a list to give every square on our grid a reward value.
# This will be done with a data structure called a 2D list - its basically a list of lists
# For each inner list is a row of the grid, and each number in those lists is the reward for that square
rewards = [[0]* num_cols for _ in range(num_rows)]

# ***** Create canvas for the environment *****
canvas = tk.Canvas(window, width=num_cols * cell_size, height=num_rows * cell_size, bg="white")
canvas.pack()   # Add canvas to GUI window

# ***** Function for the grid system on screen *****
def draw_grid():
    # Draw horizontal gridlines
    for i in range(num_rows + 1):
        canvas.create_line(0, i * cell_size, num_cols * cell_size, i * cell_size, fill="black")
    # Draw vertical gridlines
    for i in range(num_cols + 1):
        canvas.create_line(i * cell_size, 0, i * cell_size, num_rows * cell_size, fill="black")
    for row in range(num_rows):
        for col in range(num_cols):
            x = col * cell_size + cell_size / 2
            y = row * cell_size + cell_size / 2
            canvas.create_text(x, y + 30, text="Row" + str(row) + ",Col" + str(col), fill="gray")

# ***** Function to create Agent JoBot *****
def draw_robot():
    canvas.delete('all')    # Delete everything on our canvas each time and redraw it
    draw_grid()             # draw new grid

    # Here let loop through every square and draw the reward value for that square in the middle of it
        # so user can see the reward values for each square as they watch our robot move 
    for row in range(num_rows):
        for col in range(num_cols):
            # Calculate the x and y pos for thetest to be in the middle of the square
            rx = col * cell_size + 5
            ry = row * cell_size + 5
            # Draw the reward value for this 
            canvas.create_text(rx, ry, anchor="nw", text=str(rewards[row][col]), fill="red", font=("Arial", 10, "bold"))

    # Calculate positon for Agent JoBot (state)
    x1 = robot_col * cell_size # x position
    y1 = robot_row * cell_size # y position
    
    # right side
    x2 = x1 + cell_size 
    y2 = y1 + cell_size

    canvas.create_rectangle(x1, y1, x2, y2, fill="blue") # Agent JoBot is now blue
    canvas.create_text(x1 + cell_size //2, y1 + cell_size //2, text="JoBot", fill="white", font=("Arial", 12, "bold"))

# ***** Function to move JoBot randomly (everything starts randomly_use Random) *****
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

    # Now that we have displayed the move information to the console to let our user know what is going on
    # We also need to collect data for JoBot to be able to learn from this experience
    # We are going to collect the state, action, and the reward for this move and priont it to the console
    # And save this data to a file for training our model later.
    
    
    # Make the new reward in a 10 x 6 table
    #    0 = normal square
    #    1 = patrol square
    #  -50 = isles we want to avoid
    #  +50 = charging station to go when Jobot is low
    # +500 = burglar
    rewards = [
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [[1], [1], [-50], [-50], [-50], [-50], [-50], [1], [1], [+50]],
        [[1], [1], [1], [1], [1], [1], [1], [1], [1], [1]],
        [[1], [1], [-50], [-50], [-50], [-50], [-50], [1], [1], [1]],
        [[1], [1], [1], [1], [1], [+500], [1], [1], [1], [1]],
        [[1], [1], [-50], [-50], [-50], [-50], [-50], [1], [1], [+50]],
    ]
    
    # Do a look up in the rewards table above and get the reward value
    # for the square JoBot just landed on. Remember the square is the state, 
    # JoBot is the agent
    reward = rewards[robot_row][robot_col]


    # Now we print the state, action, and reward to console. Remember in this case the state is 
    # the robot's position in the environment (grid), the action is the direction moved, 
    # and the reward is the what we just calculated.
    print(f"State: (Row {robot_row}, Column {robot_col}, Action: {direction}, Reward: {reward})")
    # Open a text file in append mode to log the data for where JoBot goes this episode.
    global log_file
    log_file =  open("data_store.txt", "a") 
    log_file.write(f"Move {move_num} of {total_moves}: State: (Row {robot_row}, Column {robot_col}, Action: {direction}, Reward: {reward})\n")
    # Close the file
    log_file.close()

TOTAL_MOVES = 50 # Constant to track number of moves JoBot will make per episode

MOVE_DELAY_MS = 500    # Set delay between each of the moves in milisecs

current_move = 0 # Track JoBot's current move

# ***** Create a label to keep the user informed with info and status *****
info_label = tk.Label(window, text="Press Start to begin!", font=("Arial", 12, "bold"), fg="darkblue", bg="lightyellow", pady=5)
info_label.pack(fill="x") # Pack label on canvas
 
# ***** Create label to tell the user they can enter the number of moves *****
moves_label = tk.Label(window, text="Number of moves? ", font=("Arial", 12, "bold"), fg="darkblue")
moves_label.pack() # Pack label on canvas

# Now we need a text box so our user can type in the number of moves JopBot will be trained on
moves_entry = tk.Entry(window, font=("Arial", 12), width=6, justify="center")
# Still lets use a default value of what we set above
moves_entry.insert(0,"50")
# Add our moves textbox onto the form
moves_entry.pack()

# ***** Create frame to group the buttons *****
button_frame = tk.Frame(window, pady=5)
button_frame.pack()

# ***** Method that we can call over and over to run our episode and animate JoBot *****
def run_episode():
    global current_move # keep track of JoBot's current move

    # Evaluate if JoBot has used all his moves for the episode
    if current_move >= TOTAL_MOVES:
        # Episode is over, now let user know
        info_label.config(text=f"Jobot is all done and took {TOTAL_MOVES} random moves. Press RESET Button to restart.", fg="green" ) 
        # Re-enable the reset button now that the episode is finished
        reset_btn.config(state="normal")
        return  # Exit so the robot doesn't move anymore

    # If JoBot has more moves left, then we are going to use them up starting here
    # Add one to the current move
    current_move += 1
    # Call move_robot() 
    move_robot(move_num=current_move, total_moves=TOTAL_MOVES)

    # Lets update the info for our user with the new position info
    info_label.config(text=f"Move {current_move} of {TOTAL_MOVES} | JoBot is at Row {robot_row}, Col {robot_col}", fg="darkblue")

    # Call this function after the delay so the human can see what is going on
    window.after(MOVE_DELAY_MS, run_episode)

# ***** Time to have fun and start the episode ***** 
def start_simulation():
    # Reset the global position and counter back to the starting place
    global robot_row
    global robot_col
    global current_move
    # Let's mnake the starting place the top left square right now
    robot_row = 0
    robot_col = 0
    # Read the users number of moves they want
    global TOTAL_MOVES
    # Convert from string to int
    TOTAL_MOVES = int(moves_entry.get())
   
    # Reset the move counter
    current_move = 0
    # Disable the start and reset buttons during the simulation
    start_btn.config(state="disabled")
    reset_btn.config(state="disabled")
    # update the button to let our user know the robot is exploring 
    info_label.config(text="JoBot is exploring...", fg="purple")
    # Let's draw the robot at the first postion before the first move
    draw_robot()
    # Now finally kick off the animation loop with a delay
    window.after(MOVE_DELAY_MS, run_episode)

# ***** When user clicks reset button it will raise the reset event *****
# Handle that event here with this fucntion
def reset_simulation():
    # reset the global postion and counter to 0
    global robot_row
    global robot_col
    global current_move
    # Redraw JoBot
    draw_robot()

    # update the button to let our user know the robot is exploring
    info_label.config(text="Environment is reset, press start to run again", fg="darkblue")
    # Enable the start button and disable the reset button b/c there is nothing to reset
    start_btn.config(state="normal")
    reset_btn.config(state="disabled")

# ***** Now let's create the buttons *****
# Start button
start_btn=tk.Button(button_frame, text="START", font=("Arial", 12, "bold"), bg="green", fg="white", padx=14, pady=4, command=start_simulation)
# Now place the button
start_btn.pack(side="left", padx=10)

# Reset button
reset_btn=tk.Button(button_frame, text="RESET", font=("Arial", 12, "bold"), bg="grey", fg="white", padx=14, pady=4, command=reset_simulation)
# Now place the button
reset_btn.pack(side="left", padx=10)

# On Startup lest draw JoBot
draw_robot()

# Most importantly for the app to work
window.mainloop()











