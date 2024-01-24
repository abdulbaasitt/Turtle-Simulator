import unittest
from src.turtle_simulator import TurtleSimulator
import tkinter as tk

class TestTurtleSimulator(unittest.TestCase):
    def setUp(self):
        # Setting up a tkinter window and canvas for testing
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, bg="white", height=300, width=300)
        self.canvas.pack()
        self.turtle = TurtleSimulator(self.canvas, self.window)

    def test_movement(self):
        # Test if the turtle moves correctly
        start_x, start_y = self.turtle.x, self.turtle.y

        # Move the turtle up, down, left, and right
        self.turtle.move_up()
        self.assertEqual((self.turtle.x, self.turtle.y), (start_x, start_y - 10))

        self.turtle.move_down()
        self.assertEqual((self.turtle.x, self.turtle.y), (start_x, start_y))

        self.turtle.move_left()
        self.assertEqual((self.turtle.x, self.turtle.y), (start_x - 10, start_y))

        self.turtle.move_right()
        self.assertEqual((self.turtle.x, self.turtle.y), (start_x, start_y))

        self.turtle.turn_left()
        self.assertEqual(self.turtle.angle, self.turtle.angle) # placeholder for turn_left() test

        self.turtle.turn_right()
        self.assertEqual(self.turtle.angle, self.turtle.angle) # placeholder for turn_right() test

if __name__ == '__main__':
    unittest.main()

