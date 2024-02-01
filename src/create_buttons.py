"""
*******************************************************
 * author = 'Abdulbaasit Sanusi'
 * email  = 'abdulbaasitsanusi@gmail.com'
 * date   = '30-01-2024'
 * class  = 'CreateButtons'
 * description = 'This script contains the CreateButtons class
 *******************************************************
"""

import tkinter as tk

class CreateButtons:
    def __init__(self, window, canvas, turtle):

        self.button_display()
        self.mouse_interaction_enabled = False
        self.turtle_icon_visibility = True
        
        # toggle buttons initialization
        self.init_mouse_toggle_button()
        self.init_turtle_icon_toggle_button()
        self.init_pen_state_toggle_button()

    # function to add direction buttons
    def add_direction_buttons(self, frame, button_style):
        """Add the direction buttons to the given frame."""
        # list of tuples containing the text, command, column, and row of each button
        direction_buttons = [("↑", self.turtle.move_up, 2, 1), ("↓", self.turtle.move_down,2,3), 
                             ("←", self.turtle.move_left,1,2), ("→", self.turtle.move_right,3,2)]
        for i, (text, command, column, row) in enumerate(direction_buttons):
            tk.Button(frame, text=text, command=command, **button_style).grid(column=column, row=row) # add button to frame

    # functional buttons
    def add_functional_buttons(self, frame, button_style):
        """Add the functional buttons to the given frame."""
        # list of tuples containing the text, command, column, and row of each button
        functional_buttons = [("Reset", self.turtle.clear, 2, 2), ("Demo", self.demo, 2, 1), 
                              ("Undo", self.turtle.undo, 1, 1), ("Origin", self.turtle.move_to_origin, 1, 2)]
        for i, (text, command, column, row) in enumerate(functional_buttons):
            tk.Button(frame, text=text, command=command, **button_style).grid(column=column, row=row) # add button to frame
    
    def init_mouse_toggle_button(self):
        """Initialise the mouse toggle button."""
        self.mouse_button_frame = tk.Frame(self.window)    # create a frame to hold the button
        self.mouse_button_frame.grid(column=2, row=1) # add the frame to the window
        self.mouse_toggle_button = tk.Button(self.mouse_button_frame, 
                                             text="Enable Mouse", command=self.toggle_mouse_interaction)  # create the button
        self.mouse_toggle_button.grid(column=2, row=1)  # add the button to the frame

    def init_turtle_icon_toggle_button(self):
        """Initialise the turtle icon toggle button."""
        self.show_turtle_button_frame = tk.Frame(self.window) 
        self.show_turtle_button_frame.grid(column=1, row=1)
        self.turtle_icon_toggle_button = tk.Button(self.show_turtle_button_frame, 
                                                   text="Hide Turtle", command=self.toggle_turtle_icon_visibility)
        self.turtle_icon_toggle_button.grid(column=1, row=1)
    
    def init_pen_state_toggle_button(self):
        """Initialise the pen state toggle button."""
        self.pen_state_button_frame = tk.Frame(self.window)
        self.pen_state_button_frame.grid(column=4, row=1)
        self.pen_state_toggle_button = tk.Button(self.pen_state_button_frame, 
                                                 text="Set Pen Up", command=self.toggle_pen_state)
        self.pen_state_toggle_button.grid(column=4, row=1)

    def toggle_turtle_icon_visibility(self):
        """Toggle the visibility of the turtle icon."""
        self.turtle.toggle_turtle_icon()  # hides and recreates the turtle icon
        self.turtle_icon_visibility = not self.turtle_icon_visibility 
        if self.turtle_icon_visibility:
            self.turtle_icon_toggle_button.config(text="Hide Turtle")   
        else:
            self.turtle_icon_toggle_button.config(text="Show Turtle")

    def toggle_mouse_interaction(self):
        """Toggle the mouse interaction."""
        # Toggle the state
        self.mouse_interaction_enabled = not self.mouse_interaction_enabled 
        if self.mouse_interaction_enabled:
            self.mouse_toggle_button.config(text="Disable Mouse")  
            self.turtle.set_pen_up() # set the pen up so that the turtle doesn't draw when moving with the mouse
            self.pen_state_toggle_button.config(text="Set Pen Down") # toggle the state of the pen state button
            
        else:
            self.mouse_toggle_button.config(text="Enable Mouse")
            self.turtle.set_pen_down() # pen is down so that the turtle can draw when moving with the arrow keys
            self.pen_state_toggle_button.config(text="Set Pen Up")  # toggle the state of the pen state button
            self.mouse_interaction_enabled = False # ensure that the mouse interaction is disabled
            self.mouse_toggle_button.config(text="Enable Mouse") # update the text of the mouse toggle button
    
    def toggle_pen_state(self):
        """Toggle the pen state."""
        if self.turtle.pen_down:
            self.turtle.set_pen_up() 
            self.pen_state_toggle_button.config(text="Set Pen Down")
            self.mouse_interaction_enabled = False
            self.mouse_toggle_button.config(text="Enable Mouse")
        else:
            self.turtle.set_pen_down()
            self.pen_state_toggle_button.config(text="Set Pen Up")

    def button_display(self):
        """Display the buttons."""
        button_style = {"borderwidth": 2, "relief": "raised"}

        # direction buttons
        direction_button_frame = tk.Frame(self.window)
        self.add_direction_buttons(direction_button_frame, button_style)
        direction_button_frame.grid(column=3, row=1)
        
        # clear/demo/origin buttons
        clear_demo_origin_button_frame = tk.Frame(self.window)
        self.add_functional_buttons(clear_demo_origin_button_frame, button_style)    
        clear_demo_origin_button_frame.grid(column=5, row=1)
