""""This script contains the TurtleSimulator class
    and all related functions for the turtle simulator.
"""
import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import math

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
        self.angle = 0 
        self.pen_down = True
        turtleImage = Image.open("../Assets/turtle_white_background.png")
        self.turtle_image = ImageTk.PhotoImage(turtleImage)
        self.turtle_icon = self.canvas.create_image(self.x, self.y, image=self.turtle_image)
        self.turtleImage = turtleImage

    def _rotate_turtle_icon(self, angle):
        """
        Rotates the turtle icon.
        angle: Angle to rotate the turtle icon.
        """
        center = self.turtleImage.size[0] / 2, self.turtleImage.size[1] / 2
        rotated_image = self.turtleImage.rotate(angle, center=center, expand=True)
        self.turtle_image = ImageTk.PhotoImage(rotated_image)
        self.canvas.itemconfig(self.turtle_icon, image=self.turtle_image)
        self.canvas.coords(self.turtle_icon, self.x, self.y)


    def _update_turtle_icon(self):
        """
        Updates the turtle icon on the canvas.
        """
        self._rotate_turtle_icon(-self.angle)
        self.canvas.coords(self.turtle_icon,self.x, self.y)


    def set_pen_up(self):
        """
        Lifts the pen up.
        """
        self.pen_down = False
    
    def set_pen_down(self):
        """
        Puts the pen down.
        """
        self.pen_down = True


    def _move(self, new_x, new_y):
        """
        Moves the turtle to a new position and draws.
        new_x: New x-coordinate.
        new_y: New y-coordinate.
        """
        if self.pen_down:
            self.canvas.create_line(self.x, self.y, new_x, new_y, fill="black", width=1)
        self.x, self.y = new_x, new_y
        self._update_turtle_icon()
        self.canvas.update()

    def move_at_angle(self, distance):
        """
        Moves the turtle at a given angle(for turning left and right).
        distance: Distance to move.
        """
        radian_angle = math.radians(self.angle)
        new_x = self.x + distance * math.cos(radian_angle)
        new_y = self.y - distance * math.sin(radian_angle)
        if self.pen_down:
            self.canvas.create_line(self.x, self.y, new_x, new_y, fill="black", width=1)
        self.x, self.y = new_x, new_y
        self._update_turtle_icon()


    def move_up(self):
        """
        Moves the turtle up.
        """
        self.angle = 270
        self._move(self.x, self.y - 10)
        self._update_turtle_icon()

    def move_down(self):
        """
        Moves the turtle down.
        """
        self.angle = 90
        self._move(self.x, self.y + 10)
        self._update_turtle_icon()

    def move_left(self):
        """
        Moves the turtle left.
        """
        self.angle = 180
        self._move(self.x - 10, self.y)
        self._update_turtle_icon()  

    def move_right(self):
        """
        Moves the turtle right.
        """
        self.angle = 0
        self._move(self.x + 10, self.y)
        self._update_turtle_icon()

    def turn_left(self):
        self.angle = (self.angle + 90) % 360
        self.move_at_angle(10)

    def turn_right(self):
        self.angle = (self.angle + 90) % 360
        self.move_at_angle(10)


    def button_display(self):
        tk.Button(self.window, text="↑", command=self.move_up).grid(column=0, row=1)
        tk.Button(self.window, text="↓", command=self.move_down).grid(column=1, row=1)
        tk.Button(self.window, text="←", command=self.move_left).grid(column=2, row=1)
        tk.Button(self.window, text="→", command=self.move_right).grid(column=3, row=1)
        tk.Button(self.window, text="↰", command=self.turn_left).grid(column=1, row=2)
        tk.Button(self.window, text="↱", command=self.turn_right).grid(column=2, row=2)
        tk.Button(self.window, text="Pen Up", command=self.set_pen_up).grid(column=1, row=3)
        tk.Button(self.window, text="Pen Down", command=self.set_pen_down).grid(column=2, row=3)


