import tkinter as tk
from turtle_simulator import TurtleSimulator

import tkinter.messagebox # for about section


def new_file():
    pass

def open_file():
    file_path = tk.filedialog.askopenfilename()
    if file_path:
        pass


def about():
    tk.messagebox.showinfo("About", "Turtle Simulator\nVersion 1.0\nCreated by Abdulbaasit Sanusi")



def create_menu_bar(window):
    menu_bar = tk.Menu(window)

    # File menu
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="New", command=new_file)  
    file_menu.add_command(label="Open", command=open_file)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=window.quit)
    menu_bar.add_cascade(label="File", menu=file_menu)

    # Edit menu
    edit_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Edit", menu=edit_menu)

    # Help menu
    help_menu = tk.Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="About", command= about) 
    menu_bar.add_cascade(label="Help", menu=help_menu)

    window.config(menu=menu_bar)

def keyboard_and_mouse_events(window, canvas, turtle):
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


def main():
    window = tk.Tk()
    canvas_height = 600
    canvas_width = 600

    create_menu_bar(window)

    canvas = tk.Canvas(window, bg="white", height=canvas_height, width=canvas_width)
    canvas.grid(column=0, row=0, columnspan=6)



    turtle = TurtleSimulator(window, canvas, canvas_height, canvas_width)
    turtle.button_display()
    keyboard_and_mouse_events(window, canvas, turtle)



    
    window.mainloop()

if __name__ == "__main__":
    main()
