""""This script contains the TurtleSimulator class
    and all related functions for the turtle simulator.
"""
import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import math

class TurtleSimulator:
    def __init__(self, window, canvas, canvas_width, canvas_height, color="black"):
        """
        Initialise the turtle with a starting position, colour, and state.
        canvas: tkinter canvas object where the turtle will draw.
        window: tkinter window object for button placement.
        start_x: Starting x-coordinate.
        start_y: Starting y-coordinate.
        color: Initial colour of the line.
        """
        self.canvas = canvas
        self.window = window
        self.x = canvas_width//2
        self.y = canvas_height //2
        self.line_colour = "black"
        self.line_width = 1
        self.angle = 0 
        self.pen_down = True
        turtleImage = Image.open("../Assets/turtle_white_background.png") #TODO:  add file not found exception(FileNotFoundError:g)
        # turtleImage = Image.open("../Assets/roamer_robot_small.png")
        self.turtle_image = ImageTk.PhotoImage(turtleImage)
        self.turtle_icon = self.canvas.create_image(self.x, self.y, image=self.turtle_image)
        self.turtleImage = turtleImage
        self.actions = []
        self.undone_actions = []    

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

        self.x, self.y = new_x, new_y
        self._update_turtle_icon()
        self.canvas.update()


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
        # colour dropdown menu
        colour_button = tk.Menubutton(self.window, text="Colour")
        colour_button.grid(column=3, row=3)
        colour_menu = tk.Menu(colour_button, tearoff=0)
        colour_button["menu"] = colour_menu
        colour_menu.add_command(label="Black", command=lambda: self.set_colour("black"))
        colour_menu.add_command(label="Red", command=lambda: self.set_colour("red"))
        colour_menu.add_command(label="Blue", command=lambda: self.set_colour("blue"))
        colour_menu.add_command(label="Green", command=lambda: self.set_colour("green"))
        colour_menu.add_command(label="Yellow", command=lambda: self.set_colour("yellow"))
        colour_menu.add_command(label="Orange", command=lambda: self.set_colour("orange"))
        colour_menu.add_command(label="Purple", command=lambda: self.set_colour("purple"))
        colour_menu.add_command(label="Pink", command=lambda: self.set_colour("pink"))
        colour_menu.add_command(label="Brown", command=lambda: self.set_colour("brown"))
        colour_menu.add_command(label="White", command=lambda: self.set_colour("white"))
        colour_menu.add_command(label="Cyan", command=lambda: self.set_colour("cyan"))
        colour_menu.add_command(label="Magenta", command=lambda: self.set_colour("magenta"))
        colour_menu.add_command(label="Grey", command=lambda: self.set_colour("grey"))

        # width dropdown menu
        width_button = tk.Menubutton(self.window, text="Width")
        width_button.grid(column=4, row=3)
        width_menu = tk.Menu(width_button, tearoff=0)
        width_button["menu"] = width_menu
        width_menu.add_command(label="1", command=lambda: self.set_width(1))
        width_menu.add_command(label="2", command=lambda: self.set_width(2))
        width_menu.add_command(label="3", command=lambda: self.set_width(3))
        width_menu.add_command(label="4", command=lambda: self.set_width(4))

        # direction buttons
        tk.Button(self.window, text="↑", command=self.move_up).grid(column=0, row=1)
        tk.Button(self.window, text="↓", command=self.move_down).grid(column=1, row=1)
        tk.Button(self.window, text="←", command=self.move_left).grid(column=2, row=1)
        tk.Button(self.window, text="→", command=self.move_right).grid(column=3, row=1)
        tk.Button(self.window, text="↰", command=self.turn_left).grid(column=1, row=2)
        tk.Button(self.window, text="↱", command=self.turn_right).grid(column=2, row=2)
        
        # pen up/down buttons
        tk.Button(self.window, text="Pen Up", command=self.set_pen_up).grid(column=1, row=3)
        tk.Button(self.window, text="Pen Down", command=self.set_pen_down).grid(column=2, row=3)

        # undo/redo buttons
        tk.Button(self.window, text="Undo", command=self.undo).grid(column=4, row=1)
        tk.Button(self.window, text="Redo", command=self.redo).grid(column=5, row=1)
