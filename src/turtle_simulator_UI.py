"""
*******************************************************
 *
 *                  _____     ____
 *                 /      \  |  o | 
 *                |        |/ ___\| 
 *                |_________/     
 *                |_|_| |_|_|
 *                |_|_| |_|_| 
 * author = 'Abdulbaasit Sanusi'
 * email  = 'abdulbaasitsanusi@gmail.com'
 * date   = '30-01-2024'
 * class  = 'TurtleSimulatorAppUI'
 * description = 'This script contains the TurtleSimuatorAppUI class
 *******************************************************
"""

import tkinter as tk
from turtle_simulator import TurtleSimulator
from create_buttons import CreateButtons
from create_menubar import CreateMenuBar

class TurtleSimulatorAppUI(CreateButtons, CreateMenuBar):
    def __init__(self):
        # Window setup
        self.window = tk.Tk()
        self.window.title("Turtle Simulator")

        # Set window size
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        self.window.geometry(f"{screen_width}x{screen_height}+0+0")
        self.window.grid_rowconfigure(0, weight=1)

        # Canvas setup
        self.canvas_height = self.window.winfo_height()
        self.canvas_width = self.window.winfo_width()
        self.canvas = tk.Canvas(self.window, bg="white", height=self.canvas_height, width=self.canvas_width)
        self.canvas.grid(column=0, row=0, columnspan=7, sticky="nsew")
        
        # Turtle setup
        self.turtle = TurtleSimulator(self.window, self.canvas, self.canvas_height, self.canvas_width)

        # Initialise the buttons and menu bar
        CreateButtons.__init__(self, self.window, self.canvas, self.turtle)
        CreateMenuBar.__init__(self, self.window, self.canvas, self.turtle)
        
        self.demo_running = False

    def change_canvas_bg_color(self, color):
        """Change the background color of the canvas."""
        self.canvas.config(bg=color)
    
    def handle_canvas_click(self, event):
        # Only act on mouse click if interaction is enabled
        if self.mouse_interaction_enabled:
            self.turtle.set_pen_up()
            self.turtle.mouse_move(event.x, event.y)
    
    def keyboard_bind_helper(self, key, func):
        self.window.bind(key, func)
    
    def stop_demo(self):    
        self.demo_running = False

    def keyboard_and_mouse_events(self, window, canvas, turtle):
        # Bind keyboard events for arrow keys to move the turtle
        arrow_keys = [("<Up>", lambda e: turtle.move_up()), ("<Down>", lambda e: turtle.move_down()), 
                      ("<Left>", lambda e: turtle.move_left()), ("<Right>", lambda e: turtle.move_right())]
        for key, function in arrow_keys:
            self.keyboard_bind_helper(key, function)

        # to change the colour of line drawn by the turtle
        colour_keys = [("b", lambda e: turtle.set_colour("black")), ("r", lambda e: turtle.set_colour("red")), 
                       ("g", lambda e: turtle.set_colour("green")), ("y", lambda e: turtle.set_colour("yellow")), 
                       ("o", lambda e: turtle.set_colour("orange")), ("p", lambda e: turtle.set_colour("purple")), 
                       ("l", lambda e: turtle.set_colour("blue"))]
        for key, function in colour_keys:
            self.keyboard_bind_helper(key, function)

        # to change the pen state
        window.bind("u", lambda e: turtle.set_pen_up())
        window.bind("d", lambda e: turtle.set_pen_down())

        #to change the turtle width
        width_keys = [("1", lambda e: turtle.set_width(1)), ("2", lambda e: turtle.set_width(2)), 
                      ("3", lambda e: turtle.set_width(3)), ("4", lambda e: turtle.set_width(4)), 
                      ("5", lambda e: turtle.set_width(5)), ("6", lambda e: turtle.set_width(6)), 
                      ("7", lambda e: turtle.set_width(7)), ("8", lambda e: turtle.set_width(8)), 
                      ("9", lambda e: turtle.set_width(9)), ("0", lambda e: turtle.set_width(10))]
        for key, function in width_keys:
            self.keyboard_bind_helper(key, function)

        # to stop the demo
        window.bind("q", lambda e: self.stop_demo())

    def demo(self):
        self.demo_running = True
        # Reset the canvas and turtle position
        self.turtle.clear()
        
        # Set a thicker pen width for better visibility
        self.turtle.set_width(5)

        # list of colors for the shapes
        colors = ["blue", "green", "yellow", "red", "purple", "orange", "pink", "cyan", "magenta"]

        # Set initial position for the turtle
        start_x = self.canvas.winfo_width() / 2 - 300  # done to center the shapes
        start_y = self.canvas.winfo_height() / 2 - 200 

        # a list of functions to draw the shapes
        shape_functions = [
            (self.turtle.draw_polygon, 3, 50),  # Triangle
            (self.turtle.draw_rectangle_square, 50, 50),  # Square
            (self.turtle.draw_rectangle_square, 80, 50),  # Rectangle
            (self.turtle.draw_circle, 25),  # Circle
            (self.turtle.draw_polygon, 5, 40),  # Pentagon
            (self.turtle.draw_polygon, 6, 35),  # Hexagon
            (self.turtle.draw_polygon, 7, 30),  # Heptagon
            (self.turtle.draw_polygon, 8, 25),  # Octagon
            (self.turtle.draw_polygon, 9, 20)   # Nonagon
        ]

        for i, (draw_func, *args) in enumerate(shape_functions):

            if not self.demo_running:
                break
            
            # Move the turtle to the starting position
            start_x += 100
            self.turtle.move_to(start_x, start_y)
            self.turtle.set_pen_down()

            # Draw and fill the shape
            draw_func(*args)
            self.turtle.fill_last_shape(colors[i])

            # Move to the next line or to the right after drawing
            if i % 3 == 2:  # After every three shapes, move down to start a new line
                start_x = self.canvas.winfo_width() / 2 - 300  # Reset x position
                start_y += 200  # Move down
            else:
                start_x += 100  # Move right
            
            self.turtle.set_pen_up()

        # Move the turtle away from the last drawn shape
        self.turtle.move_to(start_x + 100, start_y)

    def run(self):

        self.window.title("Turtle Simulator")
        self.window.update_idletasks()
        self.canvas_width = self.window.winfo_width()
        self.canvas_height = self.window.winfo_height()
        self.canvas.config(width=self.canvas_width, height=self.canvas_height)
        self.turtle.x = self.canvas_width/2 + 5
        self.turtle.y = self.canvas_height/2 - 80
        self.turtle.turtle_icon_parts = self.turtle._create_turtle_icon(self.turtle.x, self.turtle.y)
        self.turtle._update_turtle_icon()

        self.canvas.bind("<Button-1>", self.handle_canvas_click)
        self.window.mainloop()
