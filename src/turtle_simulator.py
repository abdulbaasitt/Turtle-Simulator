"""
*******************************************************
 * author = 'Abdulbaasit Sanusi'
 * email  = 'abdulbaasitsanusi@gmail.com'
 * date   = '30-01-2024'
 * class  = 'TUrtleSimulator'
 * description = 'This script contains the TurtleSimulator class
 *******************************************************
"""

import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import math
import time
from turtle_navigation import TurtleNavigation
from shapes import Shapes


class TurtleSimulator(Shapes, TurtleNavigation):
    def __init__(self, window, canvas, canvas_width, canvas_height, color="black"):
        """
        Initialise the turtle with a starting position, colour, and state.
        canvas: tkinter canvas object where the turtle will draw.
        window: tkinter window object for button placement.
        start_x: Starting x-coordinate.
        start_y: Starting y-coordinate.
        color: Initial colour of the line.
        """
        TurtleNavigation.__init__(self, canvas, canvas_width//2, canvas_height//2)
        Shapes.__init__(self, canvas)
        self.canvas = canvas
        self.window = window
        self.x = canvas_width//2
        self.y = canvas_height //2
        self.line_colour = color
        self.line_width = 2
        self.angle = 0 
        self.pen_down = True
        self.actions = []
        self.undone_actions = []
        self.turtle_icon_visible = True
        self.turtle_colour = color

    def _create_turtle_icon(self, x, y):
        """
        Creates the turtle icon on the canvas using the turtle_matrix.
        x, y: Center coordinates of the turtle.
        """
        self.turtle_matrix = [
            [1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1],  
            [0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0],  
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],  
            [1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0],  
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  
            [1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0],  
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],  
            [0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0],  
            [1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1]   
            ]

        size = 2  # Size of each individual square
        half_size = len(self.turtle_matrix[0]) // 2 * size

        turtle_icon = []

        for i, row in enumerate(self.turtle_matrix):
            for j, val in enumerate(row):
                if val == 1:
                    rect_x1 = x - half_size + j * size
                    rect_y1 = y - half_size + i * size
                    rect_x2 = rect_x1 + size
                    rect_y2 = rect_y1 + size
                    rect = self.canvas.create_rectangle(rect_x1, rect_y1, rect_x2, rect_y2, fill=self.turtle_colour)
                    turtle_icon.append(rect)

        return turtle_icon
    
    def _update_turtle_icon(self):
        """
        Updates the turtle icon on the canvas to a new position.
        """
        size = 2  # Size of each individual square
        half_size = len(self.turtle_matrix[0]) // 2 * size
        counter = 0

    
        for i, row in enumerate(self.turtle_matrix):
            for j, val in enumerate(row):
                if val == 1:
                    rect_id = self.turtle_icon_parts[counter]
                    counter += 1

                    rect_x1 = self.x - half_size + j * size
                    rect_y1 = self.y - half_size + i * size
                    rect_x2 = rect_x1 + size
                    rect_y2 = rect_y1 + size
                    self.canvas.coords(rect_id, rect_x1, rect_y1, rect_x2, rect_y2)

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
    
    def set_angle(self, angle):
        """
        Sets the angle of the turtle.
        angle: Angle to set the turtle to.
        """
        self.angle = angle

    def undo(self):
        """
        Undoes the last action.
        """
        try :
            if len(self.actions) > 0:
                action = self.actions.pop()
                print(f"Undoing Action: {action}")
                self.undone_actions.append(action)
                if action['type'] == 'move':
                    self.x, self.y = action['start']
                    self._update_turtle_icon()
                    if 'line_id' in action:
                        self.canvas.delete(action['line_id'])
                    self.canvas.update()
                elif action['type'] == 'pen':
                    self.pen_down = not self.pen_down
                elif action['type'] == 'color':
                    self.line_colour = action['color']
                elif action['type'] == 'width':
                    self.line_width = action['width']
                
        except IndexError or KeyError or UnboundLocalError as e:
            print(e)
            print("No actions to undo.")

    def redo(self):
        """
        Redoes the last action.
        """
        try:
            if len(self.undone_actions) > 0:
                action = self.undone_actions.pop()
                print(f"Redoing Action: {action}")
                self.actions.append(action)
                if action['type'] == 'move':
                    self.x, self.y = action['end']
                    self._update_turtle_icon()
                    if action['pen_down']:
                        new_line_id = self.canvas.create_line(action['start'][0], action['start'][1], 
                                                              action['end'][0], action['end'][1], 
                                                              fill= action['color'], width=action['width'])
                        action['line_id'] = new_line_id
                    self.canvas.update()
                elif action['type'] == 'pen':
                    self.pen_down = not self.pen_down
                elif action['type'] == 'color':
                    self.line_colour = action['color']
                elif action['type'] == 'width':
                    self.line_width = action['width']
        except IndexError or KeyError or UnboundLocalError as e:
            print(e)
            print("No actions to redo.")

    def set_colour(self, colour):
        """
        Sets the colour of the line.
        colour: Colour of the line.
        """
        self.line_colour = colour
    
    def set_width(self, width):
        """
        Sets the width of the line.
        width: Width of the line.
        """
        self.line_width = width

    def redraw(self, actions):
        """
        Redraws the turtle on the canvas.
        """
        self.canvas.delete("all")
        self._update_turtle_icon()

        for action in actions:
            if action['type'] == 'move':
            # Recreate the line on the canvas
                self.canvas.create_line(action['start'][0], action['start'][1],
                                    action['end'][0], action['end'][1],
                                    fill=action['color'], width=action['width'])
        self._update_turtle_icon()
        self.canvas.update()
        self.turtle_icon_parts = self._create_turtle_icon(self.x, self.y)
        self._update_turtle_icon()

    def clear(self):
        """Delete all drawings and reset the turtle."""
        self.canvas.delete("all")
        self.actions.clear()
        self.x = self.canvas.winfo_width() / 2
        self.y = self.canvas.winfo_height() / 2
        self.angle = 0
        self.turtle_icon_parts = self._create_turtle_icon(self.x, self.y)
        self._update_turtle_icon()

    def toggle_turtle_icon(self):
        """
        Toggles the visibility of the turtle icon.
        """
        if self.turtle_icon_visible:
            for part in self.turtle_icon_parts:
                self.canvas.itemconfig(part, state='hidden')
            self.turtle_icon_visible = False
        else:
            for part in self.turtle_icon_parts:
                self.canvas.itemconfig(part, state='normal')
            self.turtle_icon_visible = True
