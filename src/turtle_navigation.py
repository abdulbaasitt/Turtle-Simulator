"""
*******************************************************
 *
 *                  _____     ____
 *                 /      \  |  o | 
 *                |        |/ ___\| 
 *                |_________/     
 *                |_|_| |_|_|
 *                |_|_| |_|_| 
 * author = 'Abdulbaasit Sanusi'
 * email  = 'abdulbaasitsanusi@gmail.com'
 * date   = '30-01-2024'
 * class  = 'TurtleNavigation'
 * description = 'This script contains the turtle navigation class
 *******************************************************
"""

import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import math
import time


class TurtleNavigation:
    def __init__(self, canvas, x, y, angle = 0):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.angle = angle
        self.pen_down = True

    def is_within_canvas(self, x, y):
        """Check if the given coordinates are within the canvas boundaries."""
        return 0 <= x <= self.canvas.winfo_width() and 0 <= y <= self.canvas.winfo_height()

    def _move(self, new_x, new_y):
        """
        Moves the turtle to a new position and draws.
        new_x: New x-coordinate.
        new_y: New y-coordinate.
        """
        start_pos = (self.x, self.y)
        if self.is_within_canvas(new_x, new_y):
            if self.pen_down:
                line_id = self.canvas.create_line(self.x, self.y, new_x, new_y, fill= self.line_colour, width=self.line_width)
                action = {'type': 'move', 'start': start_pos, 'end': (new_x, new_y), 'color': self.line_colour, 'width': self.line_width, 'line_id': line_id, 'pen_down': self.pen_down}
            else:
                action = {'type': 'move', 'start': start_pos, 'end': (new_x, new_y), 'color': self.line_colour, 'width': self.line_width, 'pen_down': self.pen_down}
            
            self.actions.append(action)
            self.current_shape_vertices.append((new_x, new_y))
            self.x, self.y = new_x, new_y
            self._update_turtle_icon()
            self.canvas.update()
    
    def move_to(self, new_x, new_y):
        """
        Moves the turtle to the specified coordinates without drawing.
        new_x: New x-coordinate to move to.
        new_y: New y-coordinate to move to.
        """
        if self.is_within_canvas(new_x, new_y):
            # Update the turtle's position
            self.set_pen_up()
            self.x = new_x
            self.y = new_y
            
            # Update the turtle's icon to the new position without drawing a line
            self._update_turtle_icon()

    def move_at_angle(self, distance):
        """
        Moves the turtle at a given angle(for turning left and right).
        distance: Distance to move.
        """
        radian_angle = math.radians(self.angle)
        new_x = self.x + distance * math.cos(radian_angle)
        new_y = self.y - distance * math.sin(radian_angle)
        if self.is_within_canvas(new_x, new_y):
            if self.pen_down:
                line_id = self.canvas.create_line(self.x, self.y, new_x, new_y, fill=self.line_colour, width=self.line_width)
                action = {'type': 'move', 'start': (self.x, self.y), 'end': (new_x, new_y), 'color': self.line_colour, 'width': self.line_width, 'line_id': line_id, 'pen_down': self.pen_down}
            else:
                action = {'type': 'move', 'start': (self.x, self.y), 'end': (new_x, new_y), 'color': self.line_colour, 'width': self.line_width, 'pen_down': self.pen_down}
            
            self.actions.append(action) 
            self.x, self.y = new_x, new_y
            self._update_turtle_icon()
            self.animation(0.0001)
            self.canvas.update()

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

    def mouse_move(self, new_x, new_y):
        """
        Moves the turtle to a new position based on mouse click.
        new_x: New x-coordinate.
        new_y: New y-coordinate.
        """

        start_pos = (self.x, self.y)
        print(f"Before Move: Start ({self.x}, {self.y})")
        if self.is_within_canvas(new_x, new_y):
            if self.pen_down:
                line_id = self.canvas.create_line(self.x, self.y, new_x, new_y, fill= self.line_colour, width=self.line_width)
                action = {'type': 'move', 'start': start_pos, 'end': (new_x, new_y), 'color': self.line_colour, 'width': self.line_width, 'line_id': line_id, 'pen_down': self.pen_down}
            else:
                action = {'type': 'move', 'start': start_pos, 'end': (new_x, new_y), 'color': self.line_colour, 'width': self.line_width, 'pen_down': self.pen_down}
            
            self.actions.append(action)
            print(f"Action Recorded: {action}")
            self.x, self.y = new_x, new_y
            self._update_turtle_icon()
            self.canvas.update()

    def turn_at_90(self, angle=90):
        self.angle = (self.angle + angle) % 360
        self.move_at_angle(angle)

    def move_to_origin(self):
        """
        Moves the turtle to the center of the canvas.
        """
        for part in self.turtle_icon_parts:
            self.canvas.delete(part)

        self.x = self.canvas.winfo_width() / 2
        self.y = self.canvas.winfo_height() / 2
        self.angle = 0
        self.turtle_icon_parts = self._create_turtle_icon(self.x, self.y)        
        self._update_turtle_icon()
        self.set_pen_down()
