import tkinter as tk
from turtle_simulator import TurtleSimulator
import time # for saving canvas as image

import tkinter.messagebox # for about section
import tkinter.filedialog # for open file
import json # for saving and loading files
from PIL import ImageGrab # for saving canvas as image
from PIL import Image, ImageTk # for loading image
from tkinter import simpledialog # for drawing shapes

class TurtleSimulatorAppUI:
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
        self.turtle = TurtleSimulator(self.window, self.canvas, self.canvas_height, self.canvas_width)
        self.create_menu_bar(window = self.window)
        self.button_display()
        self.mouse_interaction_enabled = False
        self.turtle_icon_visibility = True
        self.keyboard_and_mouse_events(window = self.window, canvas = self.canvas, turtle = self.turtle)

        # toggle buttons initialization
        self.init_mouse_toggle_button()
        self.init_turtle_icon_toggle_button()
        self.init_pen_state_toggle_button()
        
        self.demo_running = False

    def change_canvas_bg_color(self, color):
        """Change the background color of the canvas."""
        self.canvas.config(bg=color)
    
    def add_command_to_menu(self, menu_name, label, command):
        menu_name.add_command(label = label, command = command)

    def add_direction_buttons(self, frame, button_style):

        tk.Button(frame, text="↑", command=self.turtle.move_up, **button_style).grid(column=2, row=1)
        tk.Button(frame, text="↓", command=self.turtle.move_down, **button_style).grid(column=2, row=3)
        tk.Button(frame, text="←", command=self.turtle.move_left, **button_style).grid(column=1, row=2)
        tk.Button(frame, text="→", command=self.turtle.move_right, **button_style).grid(column=3, row=2)
    
    def add_clear_demo_origin_undo_buttons(self, frame, button_style):
        tk.Button(frame, text="Reset", command=self.turtle.clear, **button_style).grid(column=2, row=2)
        tk.Button(frame, text="Demo", command=self.demo, **button_style).grid(column=2, row=1)
        tk.Button(frame, text="Undo", command=self.turtle.undo, **button_style).grid(column=1, row=1)
        tk.Button(frame, text="Origin", command=self.turtle.move_to_origin, **button_style).grid(column=1, row=2)
    
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
        self.add_clear_demo_origin_undo_buttons(clear_demo_origin_button_frame, button_style)    
        clear_demo_origin_button_frame.grid(column=5, row=1)

    def create_menu_bar(self, window):
        menu_bar = tk.Menu(window)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        labels = [("New", self.new_file), ("Open", self.open_file), ("Save", self.save_drawing), ("Save as Image", self.save_as_image), ("Exit", window.quit)]
        for label in labels:
            if label[0] == "Exit":
                file_menu.add_separator()
            self.add_command_to_menu(file_menu, label[0], label[1])    
        menu_bar.add_cascade(label="File", menu=file_menu)

        # shapes menu
        shapes_menu = tk.Menu(menu_bar, tearoff=0)
        shapes = [("Triangle", lambda: self.draw_shape(3)),("Square", self.draw_rectangle),("Rectangle", self.draw_rectangle), ("Circle", self.draw_circle),
        ("Pentagon", lambda: self.draw_shape(5)), ("Hexagon", lambda: self.draw_shape(6)), ("Heptagon", lambda: self.draw_shape(7)), 
        ("Octagon", lambda: self.draw_shape(8)), ("Nonagon", lambda: self.draw_shape(9)),
        ("Polygon", self.draw_polygon)]
        for shape in shapes:
            self.add_command_to_menu(shapes_menu, shape[0], shape[1])
        menu_bar.add_cascade(label="Shapes", menu=shapes_menu)

        #colour menu
        colour_menu = tk.Menu(menu_bar, tearoff=0)
        colours = ["black", "red", "blue", "green", "yellow", "orange", "purple", "pink", "brown", "white", "cyan", "magenta", "grey"]
        for colour in colours:
            self.add_command_to_menu(colour_menu, colour, lambda colour=colour: self.turtle.set_colour(colour))
        menu_bar.add_cascade(label="Line Colour", menu=colour_menu)

        bg_colour_menu = tk.Menu(menu_bar, tearoff=0)
        for colour in colours:
            self.add_command_to_menu(bg_colour_menu, colour, lambda colour=colour: self.canvas.config(bg=colour))
        menu_bar.add_cascade(label="Background Colour", menu=bg_colour_menu)

        #width menu
        width_menu = tk.Menu(menu_bar, tearoff=0)
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,12]
        for number in numbers:
            self.add_command_to_menu(width_menu, number, lambda number=number: self.turtle.set_width(number))
        menu_bar.add_cascade(label="Width", menu=width_menu)

        # Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command= self.about) 
        menu_bar.add_cascade(label="Help", menu=help_menu)

        window.config(menu=menu_bar)
    
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

    def new_file(self):
        self.canvas.delete("all")
        self.turtle.actions.clear()
        self.turtle.undone_actions.clear()

    def open_file(self):
        file_path = tk.filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            with open(file_path, 'r') as file:
               actions = json.load(file)
               self.turtle.redraw(actions)

    def save_drawing(self):
        file_path = tk.filedialog.asksaveasfilename(defaultextension=".json")
        print("File saved at:", file_path)

        if file_path:
            with open(file_path, 'w') as file:
                json.dump(self.turtle.actions, file)

    def save_as_image(self):
        # file types to save as
        filetypes = [('PNG files', '*.png'), ('JPEG files', '*.jpeg;*.jpg')]

        # get file path from user
        file_path = tk.filedialog.asksaveasfilename(filetypes=filetypes)
        
        if not file_path:
            return # user cancelled save
        
        # Infer the file type from the file_path extension
        file_type = file_path.split('.')[-1].upper()

        # current size of canvas
        self.window.update_idletasks() 
        time.sleep(0.5)  # to prevent save dialog box
        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()
    
        try:
            # Grab the image of the canvas area and save it
            ImageGrab.grab().crop((x, y, x1, y1)).save(file_path, file_type)
            tk.messagebox.showinfo("Success", f"Image saved successfully as {file_type} at {file_path}")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error saving image as {file_type}: {e}")
            print("Error saving image:", e)

    def draw_circle(self):
        radius = simpledialog.askinteger("Input", "Enter radius:", parent=self.window)
        fill = simpledialog.askstring("Input", "Enter fill colour(optional):", parent=self.window)
        if radius:
            self.turtle.draw_circle(radius)
            if fill:
                self.turtle.fill_last_shape(fill)

    def draw_rectangle(self):
        width = simpledialog.askinteger("Input", "Enter width:", parent=self.window)
        height = simpledialog.askinteger("Input", "Enter height:", parent=self.window)
        fill = simpledialog.askstring("Input", "Enter fill colour(optional):", parent=self.window)
        if width and height:
            self.turtle.draw_rectangle_square(width, height)
            if fill:
                self.turtle.fill_last_shape(fill)

    def draw_shape(self, num_sides):
        length = simpledialog.askstring("Input", "Enter length of each side(optional):", parent=self.window)
        if length:
            length = int(length)
        else:
            length = None 
        fill = simpledialog.askstring("Input", "Enter fill colour(optional):", parent=self.window)
        if length:
            self.turtle.draw_polygon(num_sides = num_sides,side_length = length)
            if fill:
                self.turtle.fill_last_shape(fill)

    def draw_polygon(self):
        sides = simpledialog.askinteger("Input", "Enter number of sides:", parent=self.window)
        length = simpledialog.askstring("Input", "Enter length of each side(optional):", parent=self.window)
        if length:
            length = int(length)
        else:
            length = None 
        fill = simpledialog.askstring("Input", "Enter fill colour(optional):", parent=self.window)
        if sides and length:
            self.turtle.draw_polygon(sides, length)
            if fill:
                self.turtle.fill_last_shape(fill)
        elif sides:
            self.turtle.draw_polygon(sides)
            if fill:
                self.turtle.fill_last_shape(fill)
        
    def about(self):
        tk.messagebox.showinfo("About", "Turtle Simulator\nVersion 1.0\nCreated by Abdulbaasit Sanusi")

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


if __name__ == "__main__":
    app = TurtleSimulatorAppUI()
    app.run()
    
