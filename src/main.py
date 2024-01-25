import tkinter as tk
from turtle_simulator import TurtleSimulator

def main():
    window = tk.Tk()
    canvas_height = 600
    canvas_width = 600

    canvas = tk.Canvas(window, bg="white", height=canvas_height, width=canvas_width)
    canvas.grid(column=0, row=0, columnspan=6)

    turtle = TurtleSimulator(window, canvas, canvas_height, canvas_width)
    turtle.button_display()

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
    window.bind("u", lambda e: turtle.pen_up())
    window.bind("d", lambda e: turtle.pen_down())

    #to change the turtle width
    window.bind("1", lambda e: turtle.set_width(1))
    window.bind("2", lambda e: turtle.set_width(2))
    window.bind("3", lambda e: turtle.set_width(3))
    window.bind("4", lambda e: turtle.set_width(4))

    # Bind mouse events
    canvas.bind("<Button-1>", lambda e: turtle.mouse_move(e.x, e.y))

    
    window.mainloop()

if __name__ == "__main__":
    main()
