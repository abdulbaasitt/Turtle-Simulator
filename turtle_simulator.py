""""This script contains the TurtleSimulator class
    and all related functions for the turtle simulator.
"""
import tkinter as tk

class TurtleSimulator:
    def __init__(self, window, canvas, start_x=150, start_y=150, color="black"):
        """
        Initialise the turtle with a starting position, color, and state.
        canvas: tkinter canvas object where the turtle will draw.
        window: tkinter window object for button placement.
        start_x: Starting x-coordinate.
        start_y: Starting y-coordinate.
        color: Initial color of the line.
        """
        self.canvas = canvas
        self.window = window
        self.x = start_x
        self.y = start_y

    def move_up(self):
        self.canvas.create_line(self.x, self.y, self.x, self.y + 10, fill="black", width=1)
        self.y += 10


    def move_down(self):
        self.canvas.create_line(self.x, self.y, self.x, self.y - 10, fill="black", width=1)
        self.y -= 10


    def move_left(self):
        self.canvas.create_line(self.x, self.y, self.x - 10,self.y, fill="black", width=1)
        self.x -= 10


    def move_right(self):
        self.canvas.create_line(self.x, self.y, self.x + 10,self.y, fill="black", width=1)
        self.x += 10

    def turn_left(self):
        pass


    def turn_right(self):
        pass

    def button_display(self):
        tk.Button(self.window, text="↑", command=self.move_up).grid(column=0, row=1)
        tk.Button(self.window, text="↓", command=self.move_down).grid(column=1, row=1)
        tk.Button(self.window, text="←", command=self.move_left).grid(column=2, row=1)
        tk.Button(self.window, text="→", command=self.move_right).grid(column=3, row=1)
        tk.Button(self.window, text="↰", command=self.turn_left).grid(column=1, row=2)
        tk.Button(self.window, text="↱", command=self.turn_left).grid(column=2, row=2)


