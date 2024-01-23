import tkinter as tk
from turtle_simulator import TurtleSimulator

def main():
    window = tk.Tk()
    coords = [150, 150]

    canvas = tk.Canvas(window, bg="white", height=300, width=300)
    canvas.grid(column=0, row=0, columnspan=4)

    turtle = TurtleSimulator(window, canvas)
    turtle.button_display()
    
    window.mainloop()

if __name__ == "__main__":
    main()
