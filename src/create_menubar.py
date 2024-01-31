"""
*******************************************************
 * author = 'Abdulbaasit Sanusi'
 * email  = 'abdulbaasitsanusi@gmail.com'
 * date   = '30-01-2024'
 * class  = 'CreateMenuBar'
 * description = 'This script contains the CreateMenuBar class
 *******************************************************
"""

import tkinter as tk
import time # for saving canvas as image
import json # for saving and loading files
from PIL import ImageGrab # for saving canvas as image
from tkinter import simpledialog # for drawing shapes

class CreateMenuBar:
    def __init__(self, window, canvas, turtle):
        self.create_menu_bar(window = self.window)

    def create_menu_bar(self, window):
        menu_bar = tk.Menu(window)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        labels = [("New", self.new_file), ("Open", self.open_file), ("Save", self.save_drawing), 
                  ("Save as Image", self.save_as_image), ("Exit", window.quit)]
        for label in labels:
            if label[0] == "Exit":
                file_menu.add_separator()
            self.add_command_to_menu(file_menu, label[0], label[1])    
        menu_bar.add_cascade(label="File", menu=file_menu)

        # shapes menu
        shapes_menu = tk.Menu(menu_bar, tearoff=0)
        shapes = [("Triangle", lambda: self.draw_shape(3)),("Square", self.draw_rectangle),("Rectangle", self.draw_rectangle),
                ("Circle", self.draw_circle), ("Pentagon", lambda: self.draw_shape(5)), ("Hexagon", lambda: self.draw_shape(6)), 
                ("Heptagon", lambda: self.draw_shape(7)), ("Octagon", lambda: self.draw_shape(8)), 
                ("Nonagon", lambda: self.draw_shape(9)), ("Polygon", self.draw_polygon)]
     
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
        menu_bar.add_cascade(label="Line Width", menu=width_menu)

        # Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command= self.about) 
        menu_bar.add_cascade(label="Help", menu=help_menu)

        window.config(menu=menu_bar)

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
        try:
            if length:
                length = int(length)
            else:
                length = None
        except ValueError:
            length = None
            print("ValueError: Invalid length entered, Please enter a valid number")
             
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
