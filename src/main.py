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

        self.window.grid_rowconfigure(0, weight=3)
        for i in range(1, 6):
            # makes row expandable
            self.window.grid_rowconfigure(0, weight=1) # make canvas expand to fill window
            # makes column expandable
            self.window.grid_columnconfigure(0, weight=1)   # make canvas expand to fill window 
 
        # Canvas setup
        self.canvas_height = 600
        self.canvas_width = 600
        self.canvas = tk.Canvas(self.window, bg="white", height=self.canvas_height, width=self.canvas_width)
        self.canvas.grid(column=0, row=0, columnspan=6, sticky="nsew")

        self.turtle = TurtleSimulator(self.window, self.canvas, self.canvas_height, self.canvas_width)
        # Prompt for initial line colour and width
        initial_colour = simpledialog.askstring("Initial Colour", "Enter initial line colour:",
                                                parent=self.window)
        initial_width = simpledialog.askinteger("Initial Width", "Enter initial line width:",
                                                parent=self.window)
        # Set initial colour and width if user entered them
        if initial_colour and initial_colour.lower() in ['black', 'red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'brown', 'white', 'cyan', 'magenta', 'grey']:
            self.turtle.set_colour(initial_colour)
        else:
            print("Invalid colour entered. Defaulting to black.")
            self.turtle.set_colour("black")
        
        if initial_width:
            self.turtle.set_width(initial_width)

        self.create_menu_bar(window = self.window)
        self.button_display()
        self.keyboard_and_mouse_events(window = self.window, canvas = self.canvas, turtle = self.turtle)
        


    def button_display(self):
        # colour dropdown menu
        colour_button = tk.Menubutton(self.window, text="Colour")
        colour_button.grid(column=3, row=3, sticky="nsew")
        colour_menu = tk.Menu(colour_button, tearoff=0)
        colour_button["menu"] = colour_menu
        colour_menu.add_command(label="Black", command=lambda: self.turtle.set_colour("black"))
        colour_menu.add_command(label="Red", command=lambda: self.turtle.set_colour("red"))
        colour_menu.add_command(label="Blue", command=lambda: self.turtle.set_colour("blue"))
        colour_menu.add_command(label="Green", command=lambda: self.turtle.set_colour("green"))
        colour_menu.add_command(label="Yellow", command=lambda: self.turtle.set_colour("yellow"))
        colour_menu.add_command(label="Orange", command=lambda: self.turtle.set_colour("orange"))
        colour_menu.add_command(label="Purple", command=lambda: self.turtle.set_colour("purple"))
        colour_menu.add_command(label="Pink", command=lambda: self.turtle.set_colour("pink"))
        colour_menu.add_command(label="Brown", command=lambda: self.turtle.set_colour("brown"))
        colour_menu.add_command(label="White", command=lambda: self.turtle.set_colour("white"))
        colour_menu.add_command(label="Cyan", command=lambda: self.turtle.set_colour("cyan"))
        colour_menu.add_command(label="Magenta", command=lambda: self.turtle.set_colour("magenta"))
        colour_menu.add_command(label="Grey", command=lambda: self.turtle.set_colour("grey"))

        # width dropdown menu
        width_button = tk.Menubutton(self.window, text="Width")
        width_button.grid(column=4, row=3, sticky="nsew")
        width_menu = tk.Menu(width_button, tearoff=0)
        width_button["menu"] = width_menu
        width_menu.add_command(label="1", command=lambda: self.turtle.set_width(1))
        width_menu.add_command(label="2", command=lambda: self.turtle.set_width(2))
        width_menu.add_command(label="3", command=lambda: self.turtle.set_width(3))
        width_menu.add_command(label="4", command=lambda: self.turtle.set_width(4))
        width_menu.add_command(label="5", command=lambda: self.turtle.set_width(5))
        width_menu.add_command(label="6", command=lambda: self.turtle.set_width(6))
        width_menu.add_command(label="7", command=lambda: self.turtle.set_width(7))

        # direction buttons
        tk.Button(self.window, text="↑", command=self.turtle.move_up).grid(column=1, row=1, sticky="nsew")
        tk.Button(self.window, text="↓", command=self.turtle.move_down).grid(column=1, row=2, sticky="nsew")
        tk.Button(self.window, text="←", command=self.turtle.move_left).grid(column=0, row=2, sticky="nsew")
        tk.Button(self.window, text="→", command=self.turtle.move_right).grid(column=2, row=2, sticky="nsew")
        tk.Button(self.window, text="↰", command=self.turtle.turn_left).grid(column=0, row=1, sticky="nsew")
        tk.Button(self.window, text="↱", command=self.turtle.turn_right).grid(column=2, row=1, sticky="nsew")
        
        # pen up/down buttons
        tk.Button(self.window, text="Pen Up", command=self.turtle.set_pen_up).grid(column=1, row=3, sticky="nsew")
        tk.Button(self.window, text="Pen Down", command=self.turtle.set_pen_down).grid(column=2, row=3, sticky="nsew")

        # undo/redo buttons
        tk.Button(self.window, text="Undo", command=self.turtle.undo).grid(column=4, row=1, sticky="nsew")
        tk.Button(self.window, text="Redo", command=self.turtle.redo).grid(column=5, row=1, sticky="nsew")

        tk.Button(self.window, text="Clear", command=self.turtle.clear).grid(column=5, row=2, sticky="nsew")

    def create_menu_bar(self, window):
        menu_bar = tk.Menu(window)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)  
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_drawing)
        file_menu.add_command(label="Save as Image", command=self.save_as_image)
        file_menu.add_command(label="Load Image", command=self.load_image)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=window.quit)

        menu_bar.add_cascade(label="File", menu=file_menu)

        # Edit menu
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command= self.about) 
        menu_bar.add_cascade(label="Help", menu=help_menu)

        # shapes menu
        shapes_menu = tk.Menu(menu_bar, tearoff=0)
        shapes_menu.add_command(label="Circle", command=self.draw_circle)
        shapes_menu.add_command(label="Rectangle", command=self.draw_rectangle)
        shapes_menu.add_command(label="Complex Shape", command=self.draw_complex_shape)
        menu_bar.add_cascade(label="Shapes", menu=shapes_menu)

        window.config(menu=menu_bar)

    def keyboard_and_mouse_events(self, window, canvas, turtle):
        # Bind keyboard events
        # for arrow keys to move the turtle
        window.bind("<Up>", lambda e: turtle.move_up())
        window.bind("<Down>", lambda e: turtle.move_down())
        window.bind("<Left>", lambda e: turtle.move_left())
        window.bind("<Right>", lambda e: turtle.move_right())

        # to change the colour of line drawn by the turtle
        window.bind("B", lambda e: turtle.set_colour("black"))
        window.bind("r", lambda e: turtle.set_colour("red"))
        window.bind("g", lambda e: turtle.set_colour("green"))
        window.bind("y", lambda e: turtle.set_colour("yellow"))
        window.bind("o", lambda e: turtle.set_colour("orange"))
        window.bind("p", lambda e: turtle.set_colour("purple"))
        window.bind("b", lambda e: turtle.set_colour("blue"))

        # to change the pen state
        window.bind("u", lambda e: turtle.set_pen_up())
        window.bind("d", lambda e: turtle.set_pen_down())

        #to change the turtle width
        window.bind("1", lambda e: turtle.set_width(1))
        window.bind("2", lambda e: turtle.set_width(2))
        window.bind("3", lambda e: turtle.set_width(3))
        window.bind("4", lambda e: turtle.set_width(4))

        # Bind mouse events
        canvas.bind("<Button-1>", lambda e: turtle.mouse_move(e.x, e.y))

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

    def load_image(self):
        #  get file path from user
        file_path = tk.filedialog.askopenfilename(filetypes=[
        ("PNG Images", "*.png"),
        ("JPEG Images", "*.jpeg"),
        ("JPG Images", "*.jpg")
        ])
        #
        if file_path:
            # load image and display on canvas
            self.image = Image.open(file_path)
            self.photo = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, image=self.photo, anchor='nw')
            self.turtle.turtle_icon_parts = self.turtle._create_turtle_icon(self.turtle.x, self.turtle.y)
            self.turtle._update_turtle_icon()

        # TODO: Fix to prevent interaction with turtle after loading image

    def draw_circle(self):
        radius = simpledialog.askinteger("Input", "Enter radius:", parent=self.window)
        if radius:
            self.turtle.draw_circle(radius)

    def draw_rectangle(self):
        width = simpledialog.askinteger("Input", "Enter width:", parent=self.window)
        height = simpledialog.askinteger("Input", "Enter height:", parent=self.window)
        if width and height:
            self.turtle.draw_rectangle(width, height)

    def draw_complex_shape(self):
        sides = simpledialog.askinteger("Input", "Enter number of sides:", parent=self.window)
        length = simpledialog.askinteger("Input", "Enter length of each side:", parent=self.window)
        if sides and length:
            self.turtle.draw_complex_shape(sides, length)

    def about(self):
        tk.messagebox.showinfo("About", "Turtle Simulator\nVersion 1.0\nCreated by Abdulbaasit Sanusi")

    def run(self):
        self.turtle.start_new_shape()
        self.turtle.draw_circle(50)
        # self.turtle.fill_last_shape("red")
        # self.window.resizable(False, False) # prevent resizing of window (setting window to fixed size for now)
        self.window.title("Turtle Simulator")
        self.window.mainloop()


if __name__ == "__main__":
    app = TurtleSimulatorAppUI()
    app.run()
