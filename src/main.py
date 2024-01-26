import tkinter as tk
from turtle_simulator import TurtleSimulator

import tkinter.messagebox # for about section
import tkinter.filedialog # for open file


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
        pass

    def open_file(self):
        file_path = tk.filedialog.askopenfilename()
        if file_path:
            pass


    def about(self):
        tk.messagebox.showinfo("About", "Turtle Simulator\nVersion 1.0\nCreated by Abdulbaasit Sanusi")

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = TurtleSimulatorAppUI()
    app.run()
