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
window.title("Knight Security Agent: BBot")  # Set title of window as the name of the App

# ***** Create the reinforcement learning environment - 'Board to Death Lumber top down 2D view' *****
num_rows = 6
num_cols = 10

'''
##################################### REPLACED REWARD LOOP ############################################## 
# THIS LINE WAS REPLACED BY THE REWARDS TABLE BELOW B/C WE NO LONGER WANTED '0' AS A REWARD IN THE CANVAS
# Create a list to give every square on our grid a reward value.
# This will be done with a data structure called a 2D list - its basically a list of lists
# For each inner list is a row of the grid, and each number in those lists is the reward for that square
#          >>>>>     rewards = [[0]* num_cols for _ in range(num_rows)]     <<<<<
##################################### REPLACED REWARD LOOP ##############################################  
'''
# Now that we have displayed the move information to the console to let our user know what is going on
# We also need to collect data for BBot to be able to learn from this experience
# We are going to collect the state, action, and the reward for this move and priont it to the console
# And save this data to a file for training our model later.
# Make the new reward in a 10 x 6 table
#    0 = normal square
#    1 = patrol square
#  -50 = isles we want to avoid
#  +50 = charging station to go when BBot is low
# +500 = burglar
rewards = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, -50, -50, -50, -50, -50, 1, 1, +50],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, -50, -50, -50, -50, -50, 1, 1, 1],
    [1, 1, 1, 1, 1, +500, 1, 1, 1, 1],
    [1, 1, -50, -50, -50, -50, -50, 1, 1, +50],
]

# Create a Q-Table to store the QValues for each state-action pair
# Qtables is a data structure that helps our robot learn which actions are 
    # best in each state based on the reward it recieves
# THis is BBots memory from learning and experiences in the environment
q_table = {}
for row in range(num_rows):
    for col in range(num_cols):
        # For each square, we will have a dictionary of actions and their corresponding Q-values
        q_table[(row, col)] = {"up": 0.0, "down": 0.0, "left": 0.0, "right": 0.0}
# Set the properties and Q-learning parameters for our robot
# Learning rate is how much BBot trust the new information vs what JoNot already knows
learning_rate = 0.1
# Discount facto is how much BBot cares about teh future rewards vs immediate rewards
# A value close to 1 means it cares a lot about the future, and 0 meanis it only cares about the immediate
discount_factor = 0.9

# Set the epsilon value for the exploration vs exploitation tradeoff
# Eplislon is the property that BBot will choose a random action (explore) vs the action with the highest Q-value now (exploit)
# Adjust this to make BBot more and less greedy
# At 0.3 = 30% exploration and 70% exploitation, at 0.7 = 70% exploration and 30% exploitation
epsilon = 0.7 

# Track how many times out robot visits every square
visit_count = [[0] * num_cols for _ in range(num_rows)]

cell_size = 70  # set the square size per cell
robot_row = 0   # Set agent current state - row
robot_col = 0   # Set agent current state - col



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

# ***** Function to create Agent BBot *****
def draw_robot():
    canvas.delete('all')    # Delete everything on our canvas each time and redraw it
    
    # Right after we draw the grid, we want to draw a heat map
    # EXAMPLE: Make the hot squares get more red and the cold will stay white
    max_visits = max(visit_count[r][c] for r in range(num_rows) for c in range(num_cols)) or 1
    # Walk BBot through the grid and each color square based on how many times it has been visited
    # Paint each square with a color that gets more red the more it has been visited, 
    # and stays white if it has  never been visited
    for row in range(num_rows):
        for col in range(num_cols):
            # heat will b e avalue from 0 to 200, where 0 is never visited and
            # 200 is the most visited square
            # We can use the heat value to calculate the color of the square
            heat = int((visit_count[row][col] / max_visits) * 200)
            # Makes the squres get more red the hotter they get
            # and less green and blue to make the color more red and less white
            g = 255 - heat
            b = 255 - heat
            # This is the hex color code so if you wanted a green heat map
            # We could use different values
            color = f"#ff{g:02x}{b:02x}"
            # Calculate the x and y position of the square we want to color
            x1 = col * cell_size
            y1 = row * cell_size
            canvas.create_rectangle(x1, y1, x1 + cell_size, y1 + cell_size, fill=color, outline="")
    
    # draw new grid
    draw_grid() 
    # Here let loop through every square and draw the reward value for that square in the middle of it
    # so user can see the reward values for each square as they watch our robot move 
    for row in range(num_rows):
        for col in range(num_cols):
            # Calculate the x and y pos for thetest to be in the middle of the square
            rx = col * cell_size + 5
            ry = row * cell_size + 5
            # Draw the reward value for this 
            canvas.create_text(rx, ry, anchor="nw", text=str(rewards[row][col]), fill="red", font=("Arial", 10, "bold"))

    # Calculate positon for Agent BBot (state)
    x1 = robot_col * cell_size # x position
    y1 = robot_row * cell_size # y position
    
    # right side
    x2 = x1 + cell_size 
    y2 = y1 + cell_size

    canvas.create_rectangle(x1, y1, x2, y2, fill="blue") # Agent BBot is now blue
    canvas.create_text(x1 + cell_size //2, y1 + cell_size //2, text="BBot", fill="white", font=("Arial", 12, "bold"))

# ***** Function to move BBot randomly (everything starts randomly_use Random) *****
def move_robot(move_num=0, total_moves=0):
    # track robot state using the following variables 
    global robot_row, robot_col             

    ##### Start Epsilon / Greedy Decision ##### 
    # This determins if BBot will explore (Epsilon) or exploit (Greedy)  
    directions = ["up", "down", "left", "right"]    # BBot can move Up, Down, Left, Right - NOT diagnally

    # Ensure BBot will stay in the environment. We don't want him to move outside the grid
    # This keeps BBot from wasting moves by trying to break free of the environment (off canvas)
    moved = False
    while not moved:
        if random.random() < epsilon:
            ##### EXPLORE #####
            direction = random.choice(directions)  # BBot explores
            # tell the user what is happening
            print(f"Move {move_num} of {total_moves}: BBot is EXPLORING using a Random 'policy' and chose to move {direction}")
        else:
            ##### EXPLOIT #####
            # Here BBot is going to look up the Q-values from the Q-table for its current state and 
                # choose the action with the highest Q-value
            # Think of the Q-table as a memory bank BBot has learned from prior exploration experiences
            state = (robot_row, robot_col)
            direction = max(directions, key=lambda d: q_table[state][d]) # BBot exploits
            # tell the user what is happening
            print(f"Move {move_num} of {total_moves}: BBot is EXPLOITING using the Q-table to find it's best known move, aka action, and chose to move {direction}")
        
        # Check if this move would take BBot outside of the environment BEFORE BBot moves
        new_row, new_col = robot_row, robot_col
        if direction == "up": 
            new_row -= 1
        elif direction == "down":
            new_row += 1
        elif direction == "left":
            new_col -= 1
        elif direction == "right":
            new_col += 1

        # Check if the new position is actually different and not hitting a wall of our environment
        # If the new position is the same as the old position, then we know we are trying to move
        # outside the grid and we just skip this move and try again with a new random move.
        if 0 <= new_row < num_rows and 0 <= new_col < num_cols:
            # This is a valid move and we update BBot's position and exit the loop
            moved = True
        
    # Now that we have a valid move, let's apply the move for real
    robot_row = new_row
    robot_col = new_col

    # Count each visit BBot makes to the square here
    visit_count[robot_row][robot_col] += 1
    
    ''' CAN DELETE THIS B/C OF THE WHILE LOOP - 
        Hanging on to this for eductional purposes    
    # Evaluate the direction BBot chose to move randomly
    if direction == "up":                               # Up                        
        robot_row = max(0, robot_row - 1)
    elif direction == "down":                           # Down                        
        robot_row = min(num_rows - 1, robot_row + 1)
    elif direction == "left":                           # Left                         
        robot_col = max(0, robot_col - 1)
    elif direction == "right":                          # Right                        
        robot_col = min(num_cols - 1, robot_col + 1)
    '''   

    # Draw robot at the new position(state) it moved to
    draw_robot()

    # Keep user informed of BBot's state by printing to the console (GUI in our case)
    print(f"Move {move_num} of {total_moves}: Knight Security BBot moved {direction} to position: Row {robot_row}, Column {robot_col}")

    # Do a look up in the rewards table above and get the reward value
    # for the square BBot just landed on. Remember the square is the state, 
    # BBot is the agent
    reward = rewards[robot_row][robot_col]

    # Save where we are now the new stat after the move
    new_state = (robot_row, robot_col)
    # Now figure out the old state where we were before the move
    # Figure this out by reversing the move we just made
    old_row, old_col = robot_row, robot_col
    if direction == "up": old_row += 1
    elif direction == "down": old_row -= 1
    elif direction == "left": old_col += 1
    elif direction == "right": old_col -= 1

    # Handle the edge cases on the border of the grid where we can't move outside the grid
    # We need to make sure we dont gout out of bounds when calculating old state
    # Clamp the values witin the grid
    old_row = max(0, min(num_rows - 1, old_row))
    old_col = max(0, min(num_cols - 1, old_col))
    old_state = (old_row, old_col)

    # Find the best future score from the new squares aka state
    # By looking up the Q-values for the new state and taking the max points route
    best_future = max(q_table[new_state].values())

    # This is the best practice tried and true Q-learning formula used in Reinforcment learning
    # This is the magic formula
    # old_value + learning_rate * (reward + discount_factor * best_future - old_value)
    old_value = q_table[old_state][direction]
    q_table[old_state][direction] = old_value + learning_rate * (reward + discount_factor * best_future - old_value)
    
    # Tell the user what is going on: what is being learned by B-Bot in realtime
    print(f" >> Updated Q-table: state {old_state}, action '{direction}': {old_value:.2f} -> {q_table[old_state][direction]:.2f}")  

    # Now we print the state, action, and reward to console. Remember in this case the state is 
    # the robot's position in the environment (grid), the action is the direction moved, 
    # and the reward is the what we just calculated.
    print(f"State: (Row {robot_row}, Column {robot_col}, Action: {direction}, Reward: {reward})")
    # Open a text file in append mode to log the data for where BBot goes this episode.
    global log_file
    log_file =  open("data_store.txt", "w") 
    log_file.write(f"Move {move_num} of {total_moves}: State: (Row {robot_row}, Column {robot_col}, Action: {direction}, Reward: {reward})\n")
    # Close the file
    log_file.close()
    
TOTAL_MOVES = 50        # Constant to track number of moves BBot will make per episode
''' -- MOVE_DELAY_MS = 50      # Set delay between each of the moves in milisecs -- '''

# We changed the hard coded MOVE_DELAY_MS and went with a dictionaly of different speeds for BBot 
# The user will be able to select speeds from the GUI
speed_options = {
    "Slow (1 sec/move)": 1000,          #  1 sec delay
    "Medium (.5 sec/move)": 500,        # .5 sec delay this is the default
    "Fast (.2 sec/move)": 200,          # .2 sec delay
    "Boom, Boom (.05 sec/move)": 50,    # .05 sec delay
}

MOVE_DELAY_MS = 500     # This is the default

current_move = 0 # Track BBot's current move

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

# Let the user know what the speed options are
speed_label = tk.Label(window, text="Animations Speed:", font=("Arial", 12, "bold"), fg="darkblue")
# Add label so it appears in the window
speed_label.pack()

# Create string var to hold the selected speed option from the dropdown menu
speed_var = tk.StringVar(window)
# Set the default values to the "Medium" or must match one of the keys in the speed_options dict exactly
speed_var.set("Medium (.5 sec/move)")

# Create the dropdown menu for speed selection, we use the keys from the speed_options
# dictionary as the options for the dropdown
speed_menu = tk.OptionMenu(window, speed_var, *speed_options.keys())
# Set properties of the dropdown menus to make it look nice
speed_menu.config(font=("Arial", 12), width=25, bg="lightblue", fg="black")
# Add the dropdown menu to the window
speed_menu.pack()


# ***** Method that we can call over and over to run our episode and animate BBot *****
def run_episode():
    global current_move # keep track of BBot's current move

    # Evaluate if BBot has used all his moves for the episode
    if current_move >= TOTAL_MOVES:
        # Episode is over, now let user know
        info_label.config(text=f"BBot is all done and took {TOTAL_MOVES} random moves. Press RESET Button to restart.", fg="green" ) 
        # Re-enable the reset button now that the episode is finished
        reset_btn.config(state="normal")
        return  # Exit so the robot doesn't move anymore

    # If BBot has more moves left, then we are going to use them up starting here
    # Add one to the current move
    current_move += 1
    # Call move_robot() 
    move_robot(move_num=current_move, total_moves=TOTAL_MOVES)

    # Lets update the info for our user with the new position info
    info_label.config(text=f"Move {current_move} of {TOTAL_MOVES} | BBot is at Row {robot_row}, Col {robot_col}", fg="darkblue")

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
    # Read the selected speed from the dropdown and update MOVE_DELAY_MS
    global MOVE_DELAY_MS
    MOVE_DELAY_MS = speed_options[speed_var.get()]

    # Reset the move counter to 0
    current_move = 0
    # Disable the start and reset buttons during the simulation
    start_btn.config(state="disabled")
    reset_btn.config(state="disabled")
    # update the button to let our user know the robot is exploring 
    info_label.config(text="BBot is exploring...", fg="purple")
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
    # Redraw BBot
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

# On Startup lest draw BBot
draw_robot()

# Most importantly for the app to work
window.mainloop()











