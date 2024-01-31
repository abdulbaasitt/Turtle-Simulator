"""
*******************************************************
 * author = 'Abdulbaasit Sanusi'
 * email  = 'abdulbaasitsanusi@gmail.com'
 * date   = '30-01-2024'
 * class  = 'Shapes'
 * description = 'This script contains the Shapes class
 *******************************************************
"""

import math
import time

class Shapes:
    def __init__ (self, canvas):
        self.canvas = canvas
        self.current_shape_vertices = []
        self.last_shape_type = None

    def are_all_vertices_within_canvas(self, vertices):
        """Check if all vertices of a polygon are within the canvas boundaries."""
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        return all(0 <= x <= canvas_width and 0 <= y <= canvas_height for x, y in vertices)

    def animation(self, delay_time = 0.1):
        """
        Animates the turtle.
        delay_time: Delay time between each action.
        """
        self.canvas.update()
        time.sleep(delay_time)

    def start_new_shape(self):
        """
        Starts a new shape.
        """
        self.current_shape_vertices.clear()
    
    def fill_rectangle_square(self, fill_color):
        """
        Fills the last rectangle drawn.
        """
        if self.last_shape_type not in ['rectangle', 'square']:
            print("No rectangle/square to fill")
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

    def fill_polygon(self, fill_color):
        """
        Fills the last polygon drawn.
        """
        if self.last_shape_type not in ['triangle','pentagon', 'hexagon',
                                        'heptagon', 'octagon', 'nonagon', 'polygon'] :
            print("No polygon to fill")
            return

        if not self.current_shape_vertices:
            print("No shape to fill")
            return
        
        self.canvas.create_polygon(self.current_shape_vertices, fill=fill_color, outline="")

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

        if self.are_all_vertices_within_canvas(self.current_shape_vertices):
            # Create an overlay shape with fill color
            self.canvas.create_oval(min_x, min_y, max_x, max_y, fill=fill_color, outline="")
        else:
            print("Circle is outside the canvas area. Cannot fill.")

    def fill_last_shape(self, fill_color):
        """
        Fills the last shape drawn.
        """

        print(f"Last Shape Type: {self.last_shape_type}")   
        if self.last_shape_type == 'circle' and len(self.current_shape_vertices) > 0:
            self.fill_circle(fill_color)

        elif (self.last_shape_type == 'rectangle' or self.last_shape_type == "square") and len(self.current_shape_vertices) > 0:
            self.fill_rectangle_square(fill_color)
        
        elif (self.last_shape_type in ['triangle','pentagon', 'hexagon','heptagon', 'octagon', 'nonagon', 'polygon'] )and len(self.current_shape_vertices) > 0:
            self.fill_polygon(fill_color)
        else:
            print("No shape to fill")
            return
        
    def draw_rectangle_square(self, width, height):
        """
        Draws a rectangle with a given width and height.
        width: Width of the rectangle.
        height: Height of the rectangle.
        """
        if width == height:
            self.last_shape_type = 'square'
        else:
            self.last_shape_type = 'rectangle'

        self.start_new_shape()
        self.current_shape_vertices.append((self.x, self.y))

        for _ in range(2):
            # self._move(self.x + width, self.y)
            self.move_at_angle(width) # move right
            self.turn_at_90(90)
            self.animation(0.1)
            self.current_shape_vertices.append((self.x, self.y))
            self.move_at_angle(height) # move down
            self.turn_at_90(90)
            self.animation(0.1)
            self.current_shape_vertices.append((self.x, self.y))
            print(f"Current Shape Vertices: {self.current_shape_vertices}")
    
    def draw_polygon(self, num_sides, side_length = 3):
        """
        Draws a polygon with a given side length.
        side_length: Length of each side of the polygon.
        """
        self.start_new_shape()

        if num_sides == 3:
            self.last_shape_type = 'triangle'
        elif num_sides == 5:
            self.last_shape_type = 'pentagon'
        elif num_sides == 6:
            self.last_shape_type = 'hexagon'
        elif num_sides == 7:
            self.last_shape_type = 'heptagon'
        elif num_sides == 8:
            self.last_shape_type = 'octagon'
        elif num_sides == 9:
            self.last_shape_type = 'nonagon'
        else:
            self.last_shape_type = 'polygon'

        angle = 360 / num_sides

        for _ in range(num_sides):
            self.move_at_angle(side_length)
            self.current_shape_vertices.append((self.x, self.y))
            self.turn_at_90(angle)
            self.animation()

    def draw_circle(self, radius):  
        """
        Draws a circle with a given radius.
        radius: Radius of the circle.
       """
        circumference = 2 * math.pi * radius
        n = 18
        segment_length = circumference / n
        angle = 360 / n
        self.last_shape_type = 'circle'

        self.start_new_shape()

        for _ in range(n):
            self.move_at_angle(segment_length)
            self.turn_at_90(angle)
            self.current_shape_vertices.append((self.x, self.y))
            self.animation()
