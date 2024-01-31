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
        # a 2D matrix of 1s and 0s to represent the turtle icon
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
        half_size = len(self.turtle_matrix[0]) // 2 * size # Half the size of the turtle icon

        turtle_icon = []

        for i, row in enumerate(self.turtle_matrix):
            for j, val in enumerate(row):
                if val == 1: # calculate the coordinates of each square that makes up the turtle icon
                    rect_x1 = x - half_size + j * size # x-coordinate of the top left corner of the rectangle
                    rect_y1 = y - half_size + i * size  # y-coordinate of the top left corner of the rectangle
                    rect_x2 = rect_x1 + size # x-coordinate of the bottom right corner of the rectangle
                    rect_y2 = rect_y1 + size # y-coordinate of the bottom right corner of the rectangle
                    rect = self.canvas.create_rectangle(rect_x1, rect_y1, rect_x2, rect_y2, fill=self.turtle_colour)
                    turtle_icon.append(rect)

        return turtle_icon
    
    def _update_turtle_icon(self):
        """
        Updates the turtle icon on the canvas to a new position.
        """
        size = 2  # Size of each individual square
        half_size = len(self.turtle_matrix[0]) // 2 * size # Half the size of the turtle icon
        counter = 0

    
        for i, row in enumerate(self.turtle_matrix):
            for j, val in enumerate(row):
                if val == 1:
                    rect_id = self.turtle_icon_parts[counter] # get the rectangle id from the turtle_icon_parts list
                    counter += 1 

                    rect_x1 = self.x - half_size + j * size # x-coordinate of the top left corner of the rectangle
                    rect_y1 = self.y - half_size + i * size # y-coordinate of the top left corner of the rectangle
                    rect_x2 = rect_x1 + size # x-coordinate of the bottom right corner of the rectangle
                    rect_y2 = rect_y1 + size # y-coordinate of the bottom right corner of the rectangle
                    self.canvas.coords(rect_id, rect_x1, rect_y1, rect_x2, rect_y2) # update the coordinates of the rectangle

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
            if len(self.actions) > 0: # Check if there are any actions to undo 
                action = self.actions.pop() # Pop the last action from the actions list
                print(f"Undoing Action: {action}")
                self.undone_actions.append(action) # Add the action to the undone_actions list
                if action['type'] == 'move': # Check the type of action
                    self.x, self.y = action['start'] # Set the turtle coordinates to the start coordinates of the action    
                    self._update_turtle_icon() # Update the turtle icon
                    if 'line_id' in action: # Check if the action has a line_id
                        self.canvas.delete(action['line_id']) # Delete the line from the canvas
                    self.canvas.update() # Update the canvas   
                elif action['type'] == 'pen': # Check if the action is a pen action
                    self.pen_down = not self.pen_down # Toggle the pen state
                elif action['type'] == 'color': # Check if the action is a color action
                    self.line_colour = action['color'] # Set the line colour to the action colour
                elif action['type'] == 'width': # Check if the action is a width action
                    self.line_width = action['width'] # Set the line width to the action width
                
        except IndexError or KeyError or UnboundLocalError as e:
            print(e)
            print("No actions to undo.")

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
        self.canvas.delete("all") # Clear the canvas
        self._update_turtle_icon() # Update the turtle icon

        for action in actions: # Iterate through the actions
            if action['type'] == 'move':
            # Recreate the line on the canvas
                self.canvas.create_line(action['start'][0], action['start'][1],
                                    action['end'][0], action['end'][1],
                                    fill=action['color'], width=action['width'])
        self._update_turtle_icon()
        self.canvas.update()
        self.turtle_icon_parts = self._create_turtle_icon(self.x, self.y) # Recreate the turtle icon
        self._update_turtle_icon()

    def clear(self):
        """Delete all drawings and reset the turtle."""
        self.canvas.delete("all")
        self.actions.clear()
        self.x = self.canvas.winfo_width() / 2
        self.y = self.canvas.winfo_height() / 2
        self.angle = 0
        self.turtle_icon_parts = self._create_turtle_icon(self.x, self.y) # Recreate the turtle icon
        self._update_turtle_icon()

    def toggle_turtle_icon(self):
        """
        Toggles the visibility of the turtle icon.
        """
        if self.turtle_icon_visible: # Hide the turtle icon
            for part in self.turtle_icon_parts: # Hide each part of the turtle icon
                self.canvas.itemconfig(part, state='hidden') # Hide the turtle icon
            self.turtle_icon_visible = False # Set the turtle icon visibility to False
        else:
            for part in self.turtle_icon_parts:
                self.canvas.itemconfig(part, state='normal')  # Show each part of the turtle icon
            self.turtle_icon_visible = True # Set the turtle icon visibility to True
