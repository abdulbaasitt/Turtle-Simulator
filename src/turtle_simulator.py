""""This script contains the TurtleSimulator class
    and all related functions for the turtle simulator.
"""
import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import math
import time

class Shapes:
    def __init__ (self, canvas):
        self.canvas = canvas
        self.current_shape_vertices = []
        self.last_shape_type = None

    def start_new_shape(self):
        """
        Starts a new shape.
        """
        self.current_shape_vertices = []
        self.last_shape_type = None
    
    def fill_circle(self, fill_color):
        """
        Fills the last circle drawn.
        """
        if self.last_shape_type != 'circle':
            print("No circle to fill")
            return

        if not self.current_shape_vertices:
            print("No shape to fill")
            return

        # Calculate the bounding box
        min_x = min(self.current_shape_vertices, key=lambda x: x[0])[0]
        min_y = min(self.current_shape_vertices, key=lambda x: x[1])[1]
        max_x = max(self.current_shape_vertices, key=lambda x: x[0])[0]
        max_y = max(self.current_shape_vertices, key=lambda x: x[1])[1]

        # Create an overlay shape with fill color
        self.canvas.create_oval(min_x, min_y, max_x, max_y, fill=fill_color, outline="")

    def fill_rectangle(self, fill_color):
        """
        Fills the last rectangle drawn.
        """
        if self.last_shape_type != 'rectangle':
            print("No rectangle to fill")
            return

        if not self.current_shape_vertices:
            print("No shape to fill")
            return

        # Calculate the bounding box
        min_x = min(self.current_shape_vertices, key=lambda x: x[0])[0]
        min_y = min(self.current_shape_vertices, key=lambda x: x[1])[1]
        max_x = max(self.current_shape_vertices, key=lambda x: x[0])[0]
        max_y = max(self.current_shape_vertices, key=lambda x: x[1])[1]

        # Create an overlay shape with fill color
        self.canvas.create_rectangle(min_x, min_y, max_x, max_y, fill=fill_color, outline="")

    def fill_last_shape(self, fill_color):
        """
        Fills the last shape drawn.
        """

        print(f"Last Shape Type: {self.last_shape_type}")   
        if self.last_shape_type == 'circle' and len(self.current_shape_vertices) > 0:
            self.fill_circle(fill_color)

        elif self.last_shape_type == 'rectangle' and len(self.current_shape_vertices) > 0:
            pass
            # self.fill_rectangle(fill_color)
        
        elif self.last_shape_type == 'complex' and len(self.current_shape_vertices) > 0:
            pass
            # self.fill_complex_shape(fill_color)

        elif self.last_shape_type == 'polygon' and len(self.current_shape_vertices) > 0:
            pass
            # self.fill_polygon(fill_color)
        else:
            print("No shape to fill")
            return
        
    def draw_circle(self, radius):  
        """
        Draws a circle with a given radius.
        radius: Radius of the circle.
       """
        circumference = 2 * math.pi * radius
        n = 100
        segment_length = circumference / n
        angle = 360 / n
        self.last_shape_type = 'circle'

        delay_time = 0.01

        for _ in range(n):
            self.move_at_angle(segment_length)
            self.turn_right(angle)
            self.current_shape_vertices.append((self.x, self.y))
            self.canvas.update()
            time.sleep(delay_time)

    def draw_rectangle(self, width, height):
        """
        Draws a rectangle with a given width and height.
        width: Width of the rectangle.
        height: Height of the rectangle.
        """

        for _ in range(2):
            self._move(self.x + width, self.y)
            self.turn_right(90)
            self._move(self.x, self.y + height)
            self.turn_right(90)

    def draw_complex_shape(self, sides, length):
        """
        Draws a complex shape with a given number of sides and length.
        sides: Number of sides of the shape.
        length: Length of each side of the shape.
        """

        angle = 360 / sides
        for _ in range(sides):
            self._move(self.x + length, self.y)
            self.turn_right(angle)


class TurtleNavigation:
    def __init__(self, canvas, x, y, angle = 0):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.angle = angle
        self.pen_down = True

    def _move(self, new_x, new_y):
        """
        Moves the turtle to a new position and draws.
        new_x: New x-coordinate.
        new_y: New y-coordinate.
        """
        start_pos = (self.x, self.y)

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

    def move_at_angle(self, distance):
        """
        Moves the turtle at a given angle(for turning left and right).
        distance: Distance to move.
        """
        radian_angle = math.radians(self.angle)
        new_x = self.x + distance * math.cos(radian_angle)
        new_y = self.y - distance * math.sin(radian_angle)
        if self.pen_down:
            line_id = self.canvas.create_line(self.x, self.y, new_x, new_y, fill=self.line_colour, width=self.line_width)
            action = {'type': 'move', 'start': (self.x, self.y), 'end': (new_x, new_y), 'color': self.line_colour, 'width': self.line_width, 'line_id': line_id, 'pen_down': self.pen_down}
        else:
            action = {'type': 'move', 'start': (self.x, self.y), 'end': (new_x, new_y), 'color': self.line_colour, 'width': self.line_width, 'pen_down': self.pen_down}
        
        self.actions.append(action) 
        self.x, self.y = new_x, new_y
        self._update_turtle_icon()
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

    # OLD TURN LEFT
    # def turn_left(self, angle=90):
    #     self.angle = (self.angle + 90) % 360
    #     self.move_at_angle(10)
    
    def turn_left(self, angle=90):
        self.angle = (self.angle + angle) % 360
        self.move_at_angle(angle)

    # OLD TURN RIGHT
    # def turn_right(self, angle=90):
    #     self.angle = (self.angle + 90) % 360
    #     self.move_at_angle(10)

    def turn_right(self, angle=90):
        self.angle = (self.angle + angle) % 360
        self.move_at_angle(angle)

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
        self.line_colour = "black"
        self.line_width = 1
        self.angle = 0 
        self.pen_down = True
        # turtleImage = Image.open("../Assets/turtle_white_background.png") #TODO:  add file not found exception(FileNotFoundError:g)
        # # turtleImage = Image.open("../Assets/roamer_robot_small.png")
        # self.turtle_image = ImageTk.PhotoImage(turtleImage)
        # self.turtle_icon = self.canvas.create_image(self.x, self.y, image=self.turtle_image)
        self.turtle_icon_parts = self._create_turtle_icon(self.x, self.y)
        # self.turtleImage = turtleImage
        self.actions = []
        self.undone_actions = []

        #  TODO: Rotate turtle icon for Image. Set it up on Screen
        # def _rotate_turtle_icon(self, angle):
        #     """
        #     Rotates the turtle icon.
        #     angle: Angle to rotate the turtle icon.
        #     """
        #     center = self.turtleImage.size[0] / 2, self.turtleImage.size[1] / 2
        #     rotated_image = self.turtleImage.rotate(angle, center=center, expand=True)
        #     self.turtle_image = ImageTk.PhotoImage(rotated_image)
        #     self.canvas.itemconfig(self.turtle_icon, image=self.turtle_image)
        #     self.canvas.coords(self.turtle_icon, self.x, self.y)

        #  TODO: Update turtle icon for Image. Set it up on Screen
        # def _update_turtle_icon(self):
        #     """
        #     Updates the turtle icon on the canvas.
        #     """
        #     self._rotate_turtle_icon(-self.angle)
        #     self.canvas.coords(self.turtle_icon,self.x, self.y)

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
                    rect = self.canvas.create_rectangle(rect_x1, rect_y1, rect_x2, rect_y2, fill="black") # TODO:  change to turtle colour to be slected from menu  
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

    def _rotate_turtle_icon(self, angle):
        """
        Rotates the turtle icon around its center by the given angle.
        """
        self.angle = (self.angle + angle) % 360
        # Delete the current turtle icon
        for rect in self.turtle_icon_parts:
            self.canvas.delete(rect)
        self.turtle_icon_parts = self._create_turtle_icon(self.x, self.y)
    
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
                    # self.canvas.delete(self.canvas.find_withtag(tk.ALL)[-1])
                    if 'line_id' in action:
                        self.canvas.delete(action['line_id'])
                    self.canvas.update()
                elif action['type'] == 'pen':
                    self.pen_down = not self.pen_down
                elif action['type'] == 'color':
                    self.line_colour = action['color']
                elif action['type'] == 'width':
                    self.line_width = action['width']
                
                if not self.canvas.find_withtag(self.turtle_icon):
                    self.turtle_icon = self.canvas.create_image(self.x, self.y, image=self.turtle_image)
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
                        new_line_id = self.canvas.create_line(action['start'][0], action['start'][1], action['end'][0], action['end'][1], fill= action['color'], width=action['width'])
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
        # TODO:  fix this so that it doesn't create a new turtle icon every time
        # Temporary fix for turtle icon not showing up
        # self.turtle_icon = self.canvas.create_image(self.x, self.y, image=self.turtle_image)
        self.turtle_icon_parts = self._create_turtle_icon(self.x, self.y)
        self._update_turtle_icon()

    def clear(self):
        """Delete all drawings and reset the turtle."""
        self.canvas.delete("all")
        # self._update_turtle_icon()
        self.x = self.canvas.winfo_width() / 2
        self.y = self.canvas.winfo_height() / 2
        self.angle = 0
        self.turtle_icon_parts = self._create_turtle_icon(self.x, self.y)
        self._update_turtle_icon()

