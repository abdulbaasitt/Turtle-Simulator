import tkinter as tk
from turtle_simulator import TurtleSimulator
import time # for saving canvas as image

import tkinter.messagebox # for about section
import tkinter.filedialog # for open file
import json # for saving and loading files
from PIL import ImageGrab # for saving canvas as image
from PIL import Image, ImageTk # for loading image

class TurtleSimulatorAppUI:
    def __init__(self):
        self.window = tk.Tk()
        self.canvas_height = 600
        self.canvas_width = 600
        self.canvas = tk.Canvas(self.window, bg="white", height=self.canvas_height, width=self.canvas_width)
        self.canvas.grid(column=0, row=0, columnspan=6)
        self.turtle = TurtleSimulator(self.window, self.canvas, self.canvas_height, self.canvas_width)
        self.create_menu_bar(window = self.window)
        self.turtle.button_display()
        self.keyboard_and_mouse_events(window = self.window, canvas = self.canvas, turtle = self.turtle)


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

        # TODO: Fix to prevent interaction with turtle after loading image   


    def about(self):
        tk.messagebox.showinfo("About", "Turtle Simulator\nVersion 1.0\nCreated by Abdulbaasit Sanusi")

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = TurtleSimulatorAppUI()
    app.run()
