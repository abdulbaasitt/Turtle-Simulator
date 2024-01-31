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
        self.keyboard_and_mouse_events(window = self.window, canvas = self.canvas, turtle = self.turtle)
        # toggle buttons initialization
        self.init_mouse_toggle_button()
        self.init_turtle_icon_toggle_button()
        self.init_pen_state_toggle_button()
        
    def add_command_to_menu(self, menu_name, label, command):
        menu_name.add_command(label = label, command = command)

    def add_direction_buttons(self, frame, button_style):
        direction_buttons = [("↑", self.turtle.move_up, 2, 1), ("↓", self.turtle.move_down,2,3), 
                             ("←", self.turtle.move_left,1,2), ("→", self.turtle.move_right,3,2)]
        for i, (text, command, column, row) in enumerate(direction_buttons):
            tk.Button(frame, text=text, command=command, **button_style).grid(column=column, row=row)

    
    def add_functional_buttons(self, frame, button_style):
        functional_buttons = [("Reset", self.turtle.clear, 2, 2), ("Demo", self.demo, 2, 1), 
                              ("Undo", self.turtle.undo, 1, 1), ("Origin", self.turtle.move_to_origin, 1, 2)]
        for i, (text, command, column, row) in enumerate(functional_buttons):
            tk.Button(frame, text=text, command=command, **button_style).grid(column=column, row=row)
    
    
    def init_mouse_toggle_button(self):
        self.mouse_button_frame = tk.Frame(self.window)
        self.mouse_button_frame.grid(column=2, row=1)
        self.mouse_toggle_button = tk.Button(self.mouse_button_frame, text="Enable Mouse", command=self.toggle_mouse_interaction)
        self.mouse_toggle_button.grid(column=2, row=1)

    def init_turtle_icon_toggle_button(self):
        self.show_turtle_button_frame = tk.Frame(self.window)
        self.show_turtle_button_frame.grid(column=1, row=1)
        self.turtle_icon_toggle_button = tk.Button(self.show_turtle_button_frame, text="Hide Turtle", command=self.toggle_turtle_icon_visibility)
        self.turtle_icon_toggle_button.grid(column=1, row=1)
    
    def init_pen_state_toggle_button(self):
        self.pen_state_button_frame = tk.Frame(self.window)
        self.pen_state_button_frame.grid(column=4, row=1)
        self.pen_state_toggle_button = tk.Button(self.pen_state_button_frame, text="Pen Up", command=self.toggle_pen_state)
        self.pen_state_toggle_button.grid(column=4, row=1)

    def toggle_turtle_icon_visibility(self):
        self.turtle.toggle_turtle_icon()  
        self.turtle_icon_visibility = not self.turtle_icon_visibility
        if self.turtle_icon_visibility:
            self.turtle_icon_toggle_button.config(text="Hide Turtle")
        else:
            self.turtle_icon_toggle_button.config(text="Show Turtle")

    def toggle_mouse_interaction(self):
        # Toggle the state
        self.mouse_interaction_enabled = not self.mouse_interaction_enabled 
        if self.mouse_interaction_enabled:
            self.mouse_toggle_button.config(text="Disable Mouse")
            self.turtle.set_pen_up()
            self.pen_state_toggle_button.config(text="Pen Down")
            
        else:
            self.mouse_toggle_button.config(text="Enable Mouse")
            self.turtle.set_pen_down()
            self.pen_state_toggle_button.config(text="Pen Up")
            # if self.mouse_interaction_enabled:
            self.mouse_interaction_enabled = False
            self.mouse_toggle_button.config(text="Enable Mouse")
    
    def toggle_pen_state(self):
        if self.turtle.pen_down:
            self.turtle.set_pen_up()
            self.pen_state_toggle_button.config(text="Pen Down")
            self.mouse_interaction_enabled = False
            self.mouse_toggle_button.config(text="Enable Mouse")
        else:
            self.turtle.set_pen_down()
            self.pen_state_toggle_button.config(text="Pen Up")

    def button_display(self):
        button_style = {"borderwidth": 2, "relief": "raised"}

        # direction buttons
        direction_button_frame = tk.Frame(self.window)
        self.add_direction_buttons(direction_button_frame, button_style)
        direction_button_frame.grid(column=3, row=1)
        
        # clear/demo/origin buttons
        clear_demo_origin_button_frame = tk.Frame(self.window)
        self.add_functional_buttons(clear_demo_origin_button_frame, button_style)    
        clear_demo_origin_button_frame.grid(column=5, row=1)
