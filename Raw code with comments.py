import OpenGL.GL as GL
import OpenGL.GLUT as GLUT
import math
import random
import time
from enum import Enum

import platform


if platform.system() == 'Windows':
    import winsound
else:
    import os

class GameState(Enum):
    PLAYING = 1
    PAUSED = 2
    GAME_OVER = 3


class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2

    def draw(self):
        # Midpoint line algorithm implementation
        dx = abs(self.x2 - self.x1)
        dy = abs(self.y2 - self.y1)

        x_step = 1 if self.x2 > self.x1 else -1
        y_step = 1 if self.y2 > self.y1 else -1

        x, y = self.x1, self.y1
        points = [(x, y)]

        if dx > dy:
            d = 2 * dy - dx
            while x != self.x2:
                x += x_step
                if d < 0:
                    d += 2 * dy
                else:
                    y += y_step
                    d += 2 * (dy - dx)
                points.append((x, y))
        else:
            d = 2 * dx - dy
            while y != self.y2:
                y += y_step
                if d < 0:
                    d += 2 * dx
                else:
                    x += x_step
                    d += 2 * (dx - dy)
                points.append((x, y))

        GL.glBegin(GL.GL_POINTS)
        for px, py in points:
            GL.glVertex2f(px, py)
        GL.glEnd()


class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.creation_time = time.time()

    def draw(self):
        #midpoint circle algorithm
        def draw_circle_points(cx, cy, x, y):
            points = [
                (cx + x, cy + y), (cx - x, cy + y),
                (cx + x, cy - y), (cx - x, cy - y),
                (cx + y, cy + x), (cx - y, cy + x),
                (cx + y, cy - x), (cx - y, cy - x)
            ]
            GL.glBegin(GL.GL_POINTS)
            for point in points:
                GL.glVertex2f(*point)
            GL.glEnd()

       
        GL.glColor3f(1.0, 0.84, 0.0)
        x = 0
        y = int(self.radius)
        d = 1 - y
        draw_circle_points(self.x, self.y, x, y)
        while x < y:
            if d < 0:
                d = d + 2 * x + 3
            else:
                d = d + 2 * (x - y) + 5
                y -= 1
            x += 1
            draw_circle_points(self.x, self.y, x, y)

        GL.glColor3f(0.9, 0.75, 0.0)
        inner_radius = self.radius - 2
        x = 0
        y = int(inner_radius)
        d = 1 - y
        draw_circle_points(self.x, self.y, x, y)
        while x < y:
            if d < 0:
                d = d + 2 * x + 3
            else:
                d = d + 2 * (x - y) + 5
                y -= 1
            x += 1
            draw_circle_points(self.x, self.y, x, y)

        # Draw "$" symbol
        GL.glColor3f(0.8, 0.65, 0.0)
        GL.glBegin(GL.GL_POINTS)
        # Vertical line
        for y in range(-4, 5):
            GL.glVertex2f(self.x, self.y + y)
        # Top curve
        for x in range(-3, 4):
            GL.glVertex2f(self.x + x, self.y + 4)
        # Bottom curve
        for x in range(-3, 4):
            GL.glVertex2f(self.x + x, self.y - 4)
        # Middle line
        for x in range(-3, 4):
            GL.glVertex2f(self.x + x, self.y)
        GL.glEnd()

class Diamond:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.creation_time = time.time()

    def draw(self):
        def fill_area(points):
            GL.glBegin(GL.GL_POINTS)
            for px, py in points:
                GL.glVertex2f(px, py)
            GL.glEnd()

        # Main outline points
        top = (self.x, self.y + self.radius)
        bottom = (self.x, self.y - self.radius)
        left = (self.x - self.radius, self.y)
        right = (self.x + self.radius, self.y)
        
        # Outer facets (light blue)
        GL.glColor3f(0.7, 1.0, 1.0)
        outer_points = []
        for i in range(int(self.radius)):
            for j in range(int(self.radius - i)):
                outer_points.extend([
                    (self.x + i, self.y + j),
                    (self.x - i, self.y + j),
                    (self.x + i, self.y - j),
                    (self.x - i, self.y - j)
                ])
        fill_area(outer_points)

        # Inner facets (darker blue)
        GL.glColor3f(0.4, 0.8, 0.8)
        inner_points = []
        for i in range(int(self.radius * 0.7)):
            for j in range(int((self.radius * 0.7) - i)):
                inner_points.extend([
                    (self.x + i, self.y + j),
                    (self.x - i, self.y + j),
                    (self.x + i, self.y - j),
                    (self.x - i, self.y - j)
                ])
        fill_area(inner_points)

        # Outline (bright cyan)
        GL.glColor3f(0.0, 1.0, 1.0)
        Line(top[0], top[1], right[0], right[1]).draw()
        Line(right[0], right[1], bottom[0], bottom[1]).draw()
        Line(bottom[0], bottom[1], left[0], left[1]).draw()
        Line(left[0], left[1], top[0], top[1]).draw()

class Bike:
    def __init__(self, x, height):
        self.x = x
        self.y = height
        self.width = 15  
        self.height = 30 
        self.speed = 250  

    def update(self, dt):
        self.y -= self.speed * dt 

    def draw(self):
        def fill_area(x1, y1, x2, y2):
            GL.glBegin(GL.GL_POINTS)
            for x in range(int(x1), int(x2) + 1):
                for y in range(int(y1), int(y2) + 1):
                    GL.glVertex2f(x, y)
            GL.glEnd()

        def fill_circle(cx, cy, radius):
            GL.glBegin(GL.GL_POINTS)
            for x in range(int(cx - radius), int(cx + radius + 1)):
                for y in range(int(cy - radius), int(cy + radius + 1)):
                    if (x - cx) * (x - cx) + (y - cy) * (y - cy) <= radius * radius:
                        GL.glVertex2f(x, y)
            GL.glEnd()

        # Wheels (larger for motorcycle)
        GL.glColor3f(0.1, 0.1, 0.1)  # Black tires
        fill_circle(self.x, self.y - 12, 8)  # Back wheel
        fill_circle(self.x, self.y + 12, 8)  # Front wheel

        # Wheel rims
        GL.glColor3f(0.8, 0.8, 0.8)  # Silver
        fill_circle(self.x, self.y - 12, 5)  # Back rim
        fill_circle(self.x, self.y + 12, 5)  # Front rim

        # Main body (Red for visibility)
        GL.glColor3f(0.8, 0.0, 0.0)
        fill_area(self.x - 3, self.y - 8, self.x + 3, self.y + 8)  # Body

        # Handlebars
        GL.glColor3f(0.7, 0.7, 0.7)
        fill_area(self.x - 8, self.y + 8, self.x + 8, self.y + 10)

        # Rider
        GL.glColor3f(0.3, 0.3, 0.3)
        fill_circle(self.x, self.y, 6)  # Rider's body
        fill_circle(self.x, self.y + 8, 4)  # Rider's head

        # Headlight
        GL.glColor3f(1.0, 1.0, 0.0)
        fill_circle(self.x, self.y + 15, 3)

class Shield:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self):
        
        GL.glColor3f(0.0, 0.5, 1.0)  
        GL.glBegin(GL.GL_LINES)

        # Top arc (semi-circle)
        for i in range(50):
            angle = math.pi * i / 50  # Half-circle (0 to π)
            px1 = self.x + self.radius * math.cos(angle)
            py1 = self.y + self.radius * math.sin(angle)
            px2 = self.x + self.radius * math.cos(angle + math.pi / 50)
            py2 = self.y + self.radius * math.sin(angle + math.pi / 50)
            GL.glVertex2f(px1, py1)
            GL.glVertex2f(px2, py2)

        # Bottom V-shape
        px_bottom_left = self.x - self.radius * 0.7
        py_bottom_left = self.y - self.radius * 1.2
        px_bottom_right = self.x + self.radius * 0.7
        py_bottom_right = self.y - self.radius * 1.2
        GL.glVertex2f(self.x - self.radius, self.y)  # Connect to bottom left
        GL.glVertex2f(px_bottom_left, py_bottom_left)
        GL.glVertex2f(px_bottom_left, py_bottom_left)
        GL.glVertex2f(px_bottom_right, py_bottom_right)
        GL.glVertex2f(px_bottom_right, py_bottom_right)
        GL.glVertex2f(self.x + self.radius, self.y)  # Connect back to top arc
        GL.glEnd()

       
        GL.glColor3f(0.0, 0.7, 0.9) 
        GL.glBegin(GL.GL_POINTS)
        for i in range(200):  
            angle = 2 * math.pi * i / 200
            for r in range(int(self.radius / 2), int(self.radius)): 
                px = self.x + r * math.cos(angle)
                py = self.y + r * math.sin(angle)
                if py <= self.y + self.radius * math.sin(angle) and py >= py_bottom_left:
                    GL.glVertex2f(px, py)
        GL.glEnd()

        # Decorative cross inside the shield
        GL.glColor3f(1.0, 1.0, 1.0)  # White for the cross
        GL.glBegin(GL.GL_LINES)
        # Vertical line
        GL.glVertex2f(self.x, self.y + self.radius * 0.4)
        GL.glVertex2f(self.x, self.y - self.radius * 0.8)
        # Horizontal line
        GL.glVertex2f(self.x - self.radius * 0.3, self.y - self.radius * 0.2)
        GL.glVertex2f(self.x + self.radius * 0.3, self.y - self.radius * 0.2)
        GL.glEnd()


class FastPowerUp(Circle):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.creation_time = time.time()

    def draw(self):
        # Draw the outer ring using GL_POINTS for a rough circle approximation
        GL.glColor3f(0.0, 1.0, 0.0)  # Green color for the fast effect
        for i in range(100):
            angle = 2 * math.pi * i / 100
            px = self.x + self.radius * math.cos(angle)
            py = self.y + self.radius * math.sin(angle)
            GL.glBegin(GL.GL_POINTS)
            GL.glVertex2f(px, py)
            GL.glEnd()

        # Draw a lightning bolt (fast power-up logo)
        GL.glColor3f(1.0, 1.0, 0.0)  # Yellow color for the lightning bolt
        GL.glBegin(GL.GL_LINES)
        # Top diagonal
        GL.glVertex2f(self.x - 5, self.y + 10)
        GL.glVertex2f(self.x + 5, self.y - 10)
        # Middle diagonal
        GL.glVertex2f(self.x + 5, self.y - 10)
        GL.glVertex2f(self.x - 5, self.y - 5)
        # Bottom diagonal
        GL.glVertex2f(self.x - 5, self.y - 5)
        GL.glVertex2f(self.x + 5, self.y - 15)
        GL.glEnd()

        # Add some sparkles around the lightning bolt
        GL.glColor3f(1.0, 1.0, 1.0)  # White color for sparkles
        GL.glBegin(GL.GL_POINTS)
        for i in range(20):
            angle = 2 * math.pi * i / 20
            px = self.x + (self.radius + 5) * math.cos(angle)
            py = self.y + (self.radius + 5) * math.sin(angle)
            GL.glVertex2f(px, py)
        GL.glEnd()

class SlowPowerUp(Circle):
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.creation_time = time.time()

    def draw(self):
        # Drawing the outer ring using GL_POINTS for a rough circle approximation
        GL.glColor3f(1.0, 0.0, 0.0)  # Red color for the slow effect
        for i in range(100):
            angle = 2 * math.pi * i / 100
            px = self.x + self.radius * math.cos(angle)
            py = self.y + self.radius * math.sin(angle)
            GL.glBegin(GL.GL_POINTS)
            GL.glVertex2f(px, py)
            GL.glEnd()

        # Draw minus sign
        GL.glColor3f(1.0, 1.0, 1.0)  # White color for the minus sign
        GL.glBegin(GL.GL_POINTS)
        # Horizontal line for minus sign
        for x in range(int(self.x - self.radius/2), int(self.x + self.radius/2) + 1):
            for y in range(int(self.y - 2), int(self.y + 3)):  # Thickness of 5 pixels
                GL.glVertex2f(x, y)
        GL.glEnd()

        # Add a light blue glow effect around the minus sign
        GL.glColor3f(0.0, 0.0, 1.0)  # Blue color for the glow
        GL.glBegin(GL.GL_POINTS)
        for x in range(int(self.x - self.radius/2 - 2), int(self.x + self.radius/2 + 3)):
            GL.glVertex2f(x, self.y - 3)  # Bottom glow
            GL.glVertex2f(x, self.y + 3)  # Top glow
        for y in range(int(self.y - 3), int(self.y + 4)):
            GL.glVertex2f(self.x - self.radius/2 - 2, y)  # Left glow
            GL.glVertex2f(self.x + self.radius/2 + 2, y)  # Right glow
        GL.glEnd()
        
class OpposingCar:
    def __init__(self, x, height):
        self.x = x
        self.y = height
        self.width = 30  # Car width for collision
        self.height = 60  # Car height for collision
        self.speed = 150  # Speed of opposing car

    def update(self, dt):
        self.y -= self.speed * dt  # Move down

    def draw(self):
        def fill_area(x1, y1, x2, y2):
            GL.glBegin(GL.GL_POINTS)
            for x in range(int(x1), int(x2) + 1):
                for y in range(int(y1), int(y2) + 1):
                    GL.glVertex2f(x, y)
            GL.glEnd()

        def fill_circle(cx, cy, radius):
            GL.glBegin(GL.GL_POINTS)
            for x in range(int(cx - radius), int(cx + radius + 1)):
                for y in range(int(cy - radius), int(cy + radius + 1)):
                    if (x - cx) * (x - cx) + (y - cy) * (y - cy) <= radius * radius:
                        GL.glVertex2f(x, y)
            GL.glEnd()

        # Main body (Blue)
        GL.glColor3f(0.0, 0.0, 0.8)
        # Center body
        fill_area(self.x - 15, self.y - 30, self.x + 15, self.y + 30)

        # Racing stripe (white)
        GL.glColor3f(0.9, 0.9, 0.9)
        fill_area(self.x - 4, self.y - 25, self.x + 4, self.y + 25)

        # Windshield (tinted)
        GL.glColor3f(0.2, 0.2, 0.2)
        fill_area(self.x - 10, self.y - 15, self.x + 10, self.y - 5)

        # Rear window
        fill_area(self.x - 10, self.y + 5, self.x + 10, self.y + 15)

        # Logo
        GL.glColor3f(0.9, 0.9, 0.0)
        fill_circle(self.x, self.y - 20, 3)

        # Wheels
        wheel_positions = [
            (self.x - 16, self.y - 20),
            (self.x + 16, self.y - 20),
            (self.x - 16, self.y + 20),
            (self.x + 16, self.y + 20),
        ]

        for wx, wy in wheel_positions:
            GL.glColor3f(0.1, 0.1, 0.1)
            fill_circle(wx, wy, 6)
            GL.glColor3f(0.8, 0.8, 0.8)
            fill_circle(wx, wy, 4)
            GL.glColor3f(0.9, 0.9, 0.0)
            fill_circle(wx, wy, 2)

        # Headlights
        GL.glColor3f(1.0, 1.0, 0.0)
        headlight_positions = [
            (self.x - 12, self.y + 28),
            (self.x + 12, self.y + 28),
        ]

        for hx, hy in headlight_positions:
            fill_circle(hx, hy, 4)
            GL.glColor3f(1.0, 1.0, 0.8)
            fill_circle(hx, hy, 2)

class Tree:
    def __init__(self, x, y):
        self.x = x
        self.y = y - 20
        self.trunk_width = 8
        self.trunk_height = 25
        
    def draw(self):
        # Trunk (rectangle of points)
        GL.glColor3f(0.36, 0.25, 0.20)
        GL.glBegin(GL.GL_POINTS)
        for dx in range(-self.trunk_width // 2, self.trunk_width // 2 + 1, 2):
            for dy in range(0, self.trunk_height + 1, 2):
                GL.glVertex2f(self.x + dx, self.y + dy)
        GL.glEnd()

        # Leaves (triangle of points)
        GL.glColor3f(0.0, 0.6, 0.0)
        leaf_y = self.y + self.trunk_height
        
        GL.glBegin(GL.GL_POINTS)
        # Draw triangle shape using points
        height = 40
        base = 30
        for dy in range(height):
            width = base * (height - dy) / height
            for dx in range(int(-width), int(width) + 1, 2):
                GL.glVertex2f(self.x + dx, leaf_y + dy)
        GL.glEnd()

    def update_position(self, speed):
        self.y -= speed



class Game:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.reset_game()
        self.last_line_update = time.time()
        self.line_y = 0
        self.opposing_cars = []
        self.opposing_bikes = []  # New list for bikes
        self.last_car_spawn = time.time()
        self.last_bike_spawn = time.time()
        self.car_spawn_delay = 3.0
        self.bike_spawn_delay = 2.0
        self.shield_active = False
        self.shield_start_time = 0
        self.falling_shields = []
        self.trees = []
        self.generate_trees() 
        self.speed=2
        self.slow_power_up_active = False
        self.slow_power_up_start_time = 0
        self.falling_slow_power_ups = []
        self.fast_power_up_active = False
        self.fast_power_up_start_time = 0
        self.falling_fast_power_ups = []
        self.base_speed = 2  # Base speed of the game
        self.speed_multiplier = 1  # Speed multiplier for fast power-up
        self.rain_enabled = False
        self.night_mode = False

        
        

    def reset_game(self):
        self.state = GameState.PLAYING
        self.score = 0
        self.distance = 0  # Initialize distance
        self.missed_shots = 0
        self.car_x = self.width // 2
        self.car_y = 50
        self.falling_circles = []
        self.road_lines = []
        self.last_frame_time = time.time()
        self.pause_start_time = 0
        self.total_pause_time = 0
        self.opposing_cars = []
        self.last_car_spawn = time.time()
        self.opposing_bikes = []
        self.last_bike_spawn = time.time()
        self.falling_diamonds = []
    
    def generate_trees(self):
        for i in range(4):  # Reduced from 10 to 5 per side
            x_left = random.randint(50, 150)
            y = random.randint(30, self.height - 30)
            self.trees.append(Tree(x_left, y))

            x_right = random.randint(self.width - 150, self.width - 50)
            y = random.randint(50, self.height - 50)
            self.trees.append(Tree(x_right, y))


    def update_trees(self):
        if self.state != GameState.PLAYING:
            return
            
        for tree in self.trees:
            tree.update_position(self.speed)
            if tree.y < -50:
                if tree.x < self.width // 2:
                    tree.x = random.randint(50, 150)
                else:
                    tree.x = random.randint(self.width - 150, self.width - 50)
                tree.y = random.randint(self.height, self.height + 100)
    
    def draw_trees(self):
        for tree in self.trees:
            tree.draw()
    
    def toggle_rain(self):
        self.rain_enabled = not self.rain_enabled
        if self.rain_enabled:
            self.raindrops = [(random.randint(0, self.width), random.randint(0, self.height)) for _ in range(100)]

    def draw_rain(self):
        if not self.rain_enabled:
            return

        GL.glColor3f(0.5, 0.5, 1.0)  # Light blue for raindrops
        GL.glBegin(GL.GL_POINTS)
        for i in range(len(self.raindrops)):
            x, y = self.raindrops[i]
            y -= 20
            if y < 0:
                y = self.height
                x = random.randint(0, self.width)
            self.raindrops[i] = (x, y)
            for j in range(8):  # Create a line effect using 5 points
                GL.glVertex2f(x, y - j)
        GL.glEnd()

    def toggle_night(self):
        self.night_mode = not self.night_mode


    def spawn_bike(self):
        # Spawn bikes in slightly different positions than cars
        valid_x_positions = [x for x in range(240, 561, 80)]  # More positions due to smaller size
        x = random.choice(valid_x_positions)
        new_bike = Bike(x, self.height + 20)
        self.opposing_bikes.append(new_bike)

    def check_bike_collision(self, player_car, bike):
        # Collision box for player car
        player_left = player_car.car_x - 15
        player_right = player_car.car_x + 15
        player_top = player_car.car_y + 30
        player_bottom = player_car.car_y - 30

        # Collision box for bike (smaller)
        bike_left = bike.x - 8
        bike_right = bike.x + 8
        bike_top = bike.y + 15
        bike_bottom = bike.y - 15

        # Check for overlap
        return (player_left < bike_right and
                player_right > bike_left and
                player_top > bike_bottom and
                player_bottom < bike_top)

    def draw_car(self):
        if self.shield_active:
            GL.glColor3f(0.0, 1.0, 1.0)  # Light blue color for shield outline
        else:
            GL.glColor3f(0.8, 0.0, 0.0)  # Red color for car outline
        def fill_area(x1, y1, x2, y2):
            # Fills a rectangular area with points
            GL.glBegin(GL.GL_POINTS)
            for x in range(int(x1), int(x2) + 1):
                for y in range(int(y1), int(y2) + 1):
                    GL.glVertex2f(x, y)
            GL.glEnd()

        def fill_circle(cx, cy, radius):
            # Fills a circle using points
            GL.glBegin(GL.GL_POINTS)
            for x in range(int(cx - radius), int(cx + radius + 1)):
                for y in range(int(cy - radius), int(cy + radius + 1)):
                    if (x - cx) * (x - cx) + (y - cy) * (y - cy) <= radius * radius:
                        GL.glVertex2f(x, y)
            GL.glEnd()

        # Main body (Ferrari red)
        GL.glColor3f(0.8, 0.0, 0.0)
        # Center body
        fill_area(self.car_x - 15, self.car_y - 30, self.car_x + 15, self.car_y + 30)

        # Racing stripe (white)
        GL.glColor3f(0.9, 0.9, 0.9)
        fill_area(self.car_x - 4, self.car_y - 25, self.car_x + 4, self.car_y + 25)

        # Windshield (tinted)
        GL.glColor3f(0.2, 0.2, 0.2)
        fill_area(self.car_x - 10, self.car_y + 5, self.car_x + 10, self.car_y + 15)

        # Rear window
        fill_area(self.car_x - 10, self.car_y - 15, self.car_x + 10, self.car_y - 5)

        # Ferrari logo
        GL.glColor3f(0.9, 0.9, 0.0)
        fill_circle(self.car_x, self.car_y + 20, 3)

        # Wheels with detailed rims
        wheel_positions = [
            (self.car_x - 16, self.car_y - 20),  # Back left
            (self.car_x + 16, self.car_y - 20),  # Back right
            (self.car_x - 16, self.car_y + 20),  # Front left
            (self.car_x + 16, self.car_y + 20),  # Front right
        ]

        for wx, wy in wheel_positions:
            # Tire (black)
            GL.glColor3f(0.1, 0.1, 0.1)
            fill_circle(wx, wy, 6)

            # Rim (silver)
            GL.glColor3f(0.8, 0.8, 0.8)
            fill_circle(wx, wy, 4)

            # Center cap (gold)
            GL.glColor3f(0.9, 0.9, 0.0)
            fill_circle(wx, wy, 2)

        # Taillights
        GL.glColor3f(1.0, 0.0, 0.0)
        taillight_positions = [
            (self.car_x - 12, self.car_y - 28),
            (self.car_x + 12, self.car_y - 28),
        ]

        for tx, ty in taillight_positions:
            fill_circle(tx, ty, 4)
            GL.glColor3f(0.8, 0.0, 0.0)
            fill_circle(tx, ty, 2)

        # Side mirrors
        GL.glColor3f(0.8, 0.0, 0.0)
        mirror_positions = [
            (self.car_x - 20, self.car_y + 5),
            (self.car_x + 20, self.car_y + 5),
        ]

        for mx, my in mirror_positions:
            fill_circle(mx, my, 2)

        # Air intakes (using points for lines)
        GL.glColor3f(0.1, 0.1, 0.1)
        GL.glBegin(GL.GL_POINTS)
        # Left intake
        for i in range(5):
            GL.glVertex2f(self.car_x - 18 + i, self.car_y + i)
        # Right intake
        for i in range(5):
            GL.glVertex2f(self.car_x + 18 - i, self.car_y + i)
        GL.glEnd()

    def draw_left_arrow(self, x, y):

        arrow_lines = [
            Line(x, y, x + 10, y + 10),  # Top diagonal
            Line(x + 10, y + 10, x + 10, y + 5),  # Top vertical
            Line(x + 10, y + 5, x + 20, y + 5),  # Horizontal
            Line(x + 20, y + 5, x + 20, y - 5),  # Bottom vertical
            Line(x + 20, y - 5, x + 10, y - 5),  # Horizontal
            Line(x + 10, y - 5, x + 10, y - 10),  # Bottom diagonal
            Line(x, y, x + 10, y - 10),  # Bottom diagonal to tip
        ]

        for line in arrow_lines:
            line.draw()

    def draw_play_pause(self, x, y):
        if self.state == GameState.PAUSED:
            # symmetric play triangle
            play_lines = [
                Line(x - 10, y - 10, x - 10, y + 10),  # Left vertical
                Line(x - 10, y + 10, x + 10, y),  # Diagonal down
                Line(x + 10, y, x - 10, y - 10)  # Diagonal up
            ]
            for line in play_lines:
                line.draw()
        else:
            # pause bars
            pause_lines = [
                Line(x - 7, y - 10, x - 7, y + 10),  # Left bar
                Line(x - 5, y - 10, x - 5, y + 10),  # Left bar right edge
                Line(x + 3, y - 10, x + 3, y + 10),  # Right bar
                Line(x + 5, y - 10, x + 5, y + 10),  # Right bar left edge
            ]
            for line in pause_lines:
                line.draw()

    def draw_x_button(self, x, y):
        points = set()
        for i in range(-10, 11):
            for j in range(-10, 11):
                if abs(i - j) <= 3 or abs(i + j) <= 3:
                    points.add((x + i, y + j))

        GL.glBegin(GL.GL_POINTS)
        for px, py in points:
            GL.glVertex2f(px, py)
        GL.glEnd()

    def draw_moving_line(self):
        # Draw the moving vertical line at the center of the window

        # road dividing line 1 -

        vertical_line = Line(self.width // 2, self.line_y, self.width // 2,
                             self.line_y - 100)  # Move the line by 100 units
        GL.glColor3f(1.0, 1.0, 1.0)
        # Set color for the line (white in this case)
        vertical_line.draw()

        vertical_line = Line(self.width // 2 + 1, self.line_y, self.width // 2 + 1,
                             self.line_y - 100)  # Move the line by 100 units
        GL.glColor3f(1.0, 1.0, 1.0)
        # Set color for the line (white in this case)
        vertical_line.draw()

        vertical_line = Line(self.width // 2 + 2, self.line_y, self.width // 2 + 2,
                             self.line_y - 100)  # Move the line by 100 units
        GL.glColor3f(1.0, 1.0, 1.0)
        # Set color for the line (white in this case)
        vertical_line.draw()

    def draw_buttons(self):
        button_y = self.height - 30

        # Restart button (left arrow)
        GL.glColor3f(0.2, 0.8, 0.2)
        self.draw_left_arrow(25, button_y)

        # Play/Pause button
        GL.glColor3f(1.0, 0.65, 0.0)
        self.draw_play_pause(100, button_y)

        # Exit button (X)
        GL.glColor3f(1.0, 0.0, 0.0)
        self.draw_x_button(160, button_y)

    def create_falling_circle(self):
        if len(self.falling_circles) < 1 and random.random() < 0.5:
            x = random.randint(220, 580)
            radius = 11  # All circles now have the same radius
            circle = Circle(x, self.height - 20, radius)  # Remove is_special parameter
            self.falling_circles.append(circle)

    def create_falling_diamond(self):
        if len(self.falling_diamonds) < 1 and random.random() < 0.005:
            x = random.randint(220, 580)
            radius = 13  # Size of the diamond
            diamond = Diamond(x, self.height - 20, radius)
            self.falling_diamonds.append(diamond)

    def create_falling_shield(self):
        if len(self.falling_shields) < 1 and random.random() < 0.001:  # Rare spawn probability
            x = random.randint(220, 580)
            radius = 15  # Size of the shield
            shield = Shield(x, self.height - 20, radius)
            self.falling_shields.append(shield)

    def create_falling_slow_power_up(self):
        if len(self.falling_slow_power_ups) < 1 and random.random() < 0.001:  # Rare spawn probability
            x = random.randint(220, 580)
            radius = 15  # Size of the Slow power up
            slow_power_up = SlowPowerUp(x, self.height - 20, radius)
            self.falling_slow_power_ups.append(slow_power_up)
    
    def create_falling_fast_power_up(self):
        if len(self.falling_fast_power_ups) < 1 and random.random() < 0.001:  # Rare spawn probability
            x = random.randint(220, 580)
            radius = 15  # Size of the fast power-up
            fast_power_up = FastPowerUp(x, self.height - 20, radius)
            self.falling_fast_power_ups.append(fast_power_up)
    

    def spawn_opposing_car(self):
        # Spawn cars in the valid road area
        valid_x_positions = [x for x in range(220, 581, 120)]  # Discrete positions across the road
        x = random.choice(valid_x_positions)
        new_car = OpposingCar(x, self.height + 30)  # Start above screen
        self.opposing_cars.append(new_car)

    def check_car_collision(self, player_car, opposing_car):
        # Collision box for player car
        player_left = player_car.car_x - 15
        player_right = player_car.car_x + 15
        player_top = player_car.car_y + 30
        player_bottom = player_car.car_y - 30

        # Collision box for opposing car
        opp_left = opposing_car.x - 15
        opp_right = opposing_car.x + 15
        opp_top = opposing_car.y + 30
        opp_bottom = opposing_car.y - 30

        # Check for overlap
        return (player_left < opp_right and
                player_right > opp_left and
                player_top > opp_bottom and
                player_bottom < opp_top)

    def update(self):
        if self.state != GameState.PLAYING:
            return

        current_time = time.time()
        global dt
        dt = current_time - self.last_frame_time - (
            current_time - self.pause_start_time if self.pause_start_time > self.last_frame_time else 0)
        self.last_frame_time = current_time

        if current_time - self.last_car_spawn > self.car_spawn_delay:
            self.spawn_opposing_car()
            self.last_car_spawn = current_time

        if self.shield_active:
            current_time = time.time()
            if current_time - self.shield_start_time > 6:  # Shield duration
                print("Shield deactivated!")  # Print a message when the shield is deactivated
                self.shield_active = False

        # Update opposing cars
        for car in self.opposing_cars[:]:
            car.update(dt)
            if not self.shield_active and self.check_car_collision(self, car):
                self.game_over()
                return
            if car.y < -60:
                self.opposing_cars.remove(car)

        if current_time - self.last_bike_spawn > self.bike_spawn_delay:
            self.spawn_bike()
            self.last_bike_spawn = current_time

        #Update opposing bikes
        for bike in self.opposing_bikes[:]:
            bike.update(dt)
            if not self.shield_active and self.check_bike_collision(self, bike):
                self.game_over()
                return
            if bike.y < -30:
                self.opposing_bikes.remove(bike)

        self.score += 1 * dt  # Increase score by 1 every frame
        self.distance += dt  # Increase distance by 1 meter every second

        self.line_y -= 75 * dt  # Move the line down by 50 units per second
        if self.line_y < 0:
            self.line_y = self.height  # Reset the line position

        # car hitbox
        ship_left = self.car_x - 35
        ship_right = self.car_x + 35
        ship_bottom = self.car_y - 32
        ship_top = self.car_y + 20

        for circle in self.falling_circles[:]:
            circle.y -= 50 * dt

            # collision with car
            if (circle.x + circle.radius > ship_left and
                    circle.x - circle.radius < ship_right and
                    circle.y + circle.radius > ship_bottom and
                    circle.y - circle.radius < ship_top):
                self.score += 10  # Increase score by 50
                self.falling_circles.remove(circle)  # Remove the coin
                continue

            if circle.y < 0:
                self.falling_circles.remove(circle)

        self.create_falling_circle()
        
        # Update falling diamonds
        for diamond in self.falling_diamonds[:]:
            diamond.y -= 50 * dt
            if (diamond.x - diamond.radius < self.car_x + 15 and diamond.x + diamond.radius > self.car_x - 15 and
                    diamond.y + diamond.radius > self.car_y - 30 and
                    diamond.y - diamond.radius < self.car_y + 30):
                self.score += 50  # Award points for diamond collision
                self.falling_diamonds.remove(diamond)
                continue
            if diamond.y < 0:
                self.falling_diamonds.remove(diamond)
        self.create_falling_diamond()      

        # Update falling shields
        for shield in self.falling_shields[:]:
            shield.y -= 50 * dt
            if (shield.x - shield.radius < self.car_x + 15 and shield.x + shield.radius > self.car_x - 15 and
                    shield.y + shield.radius > self.car_y - 30 and
                    shield.y - shield.radius < self.car_y + 30):
                print("Shield collected!")  # Print a message when the shield is collected
                self.shield_active = True
                self.shield_start_time = time.time()
                self.falling_shields.remove(shield)
                continue
            if shield.y < 0:
                self.falling_shields.remove(shield)
        self.create_falling_shield()

        # Update falling Slow power ups
        for slow_power_up in self.falling_slow_power_ups[:]:
            slow_power_up.y -= 50 * dt
            if (slow_power_up.x - slow_power_up.radius < self.car_x + 15 and slow_power_up.x + slow_power_up.radius > self.car_x - 15 and
                    slow_power_up.y + slow_power_up.radius > self.car_y - 30 and
                    slow_power_up.y - slow_power_up.radius < self.car_y + 30):
                print("Slow power up collected!")  # Print a message when the Slow power up is collected
                self.slow_power_up_active = True
                self.slow_power_up_start_time = time.time()
                self.falling_slow_power_ups.remove(slow_power_up)
                continue
            if slow_power_up.y < 0:
                self.falling_slow_power_ups.remove(slow_power_up)

        # Check if Slow power up duration has expired
        if self.slow_power_up_active:
            if time.time() - self.slow_power_up_start_time > 6:  # Duration of the Slow power up
                print("Slow power up deactivated!")  # Print a message when the Slow power up is deactivated
                self.slow_power_up_active = False

        # Update opposing cars' speed if Slow power up is active
        if self.slow_power_up_active:
            for car in self.opposing_cars:
                car.speed = 70  # Slow down opposing cars
            for bike in self.opposing_bikes:
                bike.speed = 100  # Slow down opposing bikes
        else:
            for car in self.opposing_cars:
                car.speed = 150  # Reset to normal speed
            for bike in self.opposing_bikes:
                bike.speed = 250  # Reset to normal speed

        self.create_falling_slow_power_up()
    
     # Update falling fast power-ups
        for fast_power_up in self.falling_fast_power_ups[:]:
            fast_power_up.y -= 50 * dt
            if (fast_power_up.x - fast_power_up.radius < self.car_x + 15 and
                    fast_power_up.x + fast_power_up.radius > self.car_x - 15 and
                    fast_power_up.y + fast_power_up.radius > self.car_y - 30 and
                    fast_power_up.y - fast_power_up.radius < self.car_y + 30):
                print("Fast power up collected!")  # Print a message when the fast power up is collected
                self.fast_power_up_active = True
                self.fast_power_up_start_time = time.time()
                self.falling_fast_power_ups.remove(fast_power_up)
                continue
            if fast_power_up.y < 0:
                self.falling_fast_power_ups.remove(fast_power_up)

        # Check if fast power up duration has expired
        if self.fast_power_up_active:
            if time.time() - self.fast_power_up_start_time > 8:  # Duration of the fast power up
                print("Fast power up deactivated!")  # Print a message when the fast power up is deactivated
                self.fast_power_up_active = False

        # Update game speed if fast power up is active
        if self.fast_power_up_active:
            self.speed_multiplier = 4  # Increase speed multiplier
            for car in self.opposing_cars:
                car.speed = 240  # Speed up opposing cars
            for bike in self.opposing_bikes:
                bike.speed = 300  # speed up opposing bikes
            self.score += 4 * dt  # Increase score by 1 every frame
            self.distance += 4* dt  # Increase distance by 1 meter every second
            self.line_y -= 100 * dt  # Move the line down by 50 units per second
        else:
            self.speed_multiplier = 1  # Reset to normal speed

        self.speed = self.base_speed * self.speed_multiplier  # Update game speed
        self.create_falling_fast_power_up()


    def game_over(self):
        self.state = GameState.GAME_OVER
        if platform.system() == 'Windows':
           winsound.Beep(250, 100)  # 250Hz for 1 second
        else:
            os.system('tput bel')  # Unix-like systems
        print(f"Game Over! Final Score: {int(self.score)}")

    def handle_mouse(self, x, y):
        y = self.height - y

        if y > self.height - 45 and y < self.height - 15:
            if 15 <= x <= 45:
                print("Starting Over")
                self.reset_game()
            elif 85 <= x <= 115:
                current_time = time.time()
                if self.state == GameState.PLAYING:
                    self.state = GameState.PAUSED
                    self.pause_start_time = current_time
                    print("Game Paused")
                elif self.state == GameState.PAUSED:
                    self.state = GameState.PLAYING
                    self.total_pause_time += current_time - self.pause_start_time
                    self.last_frame_time = current_time
                    print("Game Resumed")
            elif 145 <= x <= 175:
                print(f"Goodbye! Final Score: {self.score}")
                GLUT.glutLeaveMainLoop()

    def handle_keyboard(self, key, x, y):
        if self.state != GameState.PLAYING:
            return

        if key == b'a' and self.car_x > 240:
            self.car_x -= 10
        elif key == b'd' and self.car_x < self.width - 240:
            self.car_x += 10
        elif key == b'w' and self.car_y < self.height - 50:
            self.car_y += 10
        elif key == b's' and self.car_y > 50:
            self.car_y -= 10
        if key == b'r':
            game.toggle_rain()
        if key == b'n':
            game.toggle_night()



import numpy as np


# Prepare the point data in advance (batch)
def prepare_points():
    points = []
    for x in range(200, 601):  # From x = 200 to x = 600
        for y in range(0, 601):  # From y = 0 to y = 600
            points.append((x, y))
    return np.array(points, dtype=np.float32)


# Prepare the point data (do this once during initialization)
point_data = prepare_points()


def display():
    GL.glClear(GL.GL_COLOR_BUFFER_BIT)

    # Draw road background
    GL.glColor3f(0.3, 0.3, 0.3)
    GL.glEnableClientState(GL.GL_VERTEX_ARRAY)
    GL.glVertexPointer(2, GL.GL_FLOAT, 0, point_data)
    GL.glDrawArrays(GL.GL_POINTS, 0, len(point_data))
    GL.glDisableClientState(GL.GL_VERTEX_ARRAY)

    # Draw road lines
    game.draw_moving_line()

    # Draw opposing vehicles
    for car in game.opposing_cars:
        car.draw()

    # Draw bikes
    for bike in game.opposing_bikes:
        bike.draw()

    # Draw falling shields
    for shield in game.falling_shields:
        shield.draw()
    
    for slow_power_up in game.falling_slow_power_ups:
        slow_power_up.draw()
    
    for fast_power_up in game.falling_fast_power_ups:
        fast_power_up.draw()

    # Draw player's car
    game.draw_car()

    # Draw coins/circles
    GL.glColor3f(1.0, 0.0, 0.0)
    GL.glPointSize(2.0)
    for circle in game.falling_circles:
        circle.draw()

    # Draw diamonds
    for diamond in game.falling_diamonds:
        diamond.draw()
    
    if game.night_mode:
        GL.glClearColor(0.1, 0.1, 0.2, 1.0)  # Night sky background
    else:
        GL.glClearColor(0.545, 0.271, 0.07, 1.0)  # Light blue sky background

    # Draw UI elements
    game.draw_buttons()
    
    game.update_trees()
    game.draw_trees()
    game.draw_rain()

    # Display the score
    GL.glColor3f(1.0, 1.0, 1.0)
    draw_text(f"Score: {int(game.score)}", game.width - 150, game.height - 30)
    draw_text(f"Distance: {int(game.distance)} m", game.width - 150, game.height - 50)

    # Display state messages in the middle of the screen
    if game.state == GameState.PAUSED:
        GL.glColor3f(1.0, 1.0, 0.0)  # Yellow color
        message = "Game is Paused!"
        # Calculate text position to center it
        text_width = len(message) * 9  # Approximate width of each character
        x = (game.width - text_width) // 2
        y = game.height // 2
        draw_text(message, x, y)
    elif game.state == GameState.GAME_OVER:
        GL.glColor3f(1.0, 0.0, 0.0)  # Red color
        message = "Game Over!"
        text_width = len(message) * 9
        x = (game.width - text_width) // 2
        y = game.height // 2
        draw_text(message, x, y)

    # Update game state
    game.update()
    GLUT.glutSwapBuffers()


def draw_text(text, x, y):
    GL.glRasterPos2f(x, y)
    for char in text:
        GLUT.glutBitmapCharacter(GLUT.GLUT_BITMAP_HELVETICA_18, ord(char))


def reshape(width, height):
    GL.glViewport(0, 0, width, height)
    GL.glMatrixMode(GL.GL_PROJECTION)
    GL.glLoadIdentity()
    GL.glOrtho(0, width, 0, height, -1, 1)
    GL.glMatrixMode(GL.GL_MODELVIEW)


def mouse_func(button, state, x, y):
    if button == GLUT.GLUT_LEFT_BUTTON and state == GLUT.GLUT_DOWN:
        game.handle_mouse(x, y)


def timer_func(value):
    GLUT.glutPostRedisplay()
    GLUT.glutTimerFunc(16, timer_func, 0)


game = Game()


def main():
    GLUT.glutInit()
    GLUT.glutInitDisplayMode(GLUT.GLUT_DOUBLE | GLUT.GLUT_RGB)
    GLUT.glutInitWindowSize(game.width, game.height)
    GLUT.glutCreateWindow(b"Dodge and Run! : 2D Driving Simulator")

    GL.glClearColor(0.545, 0.271, 0.07, 1.0)
    GL.glPointSize(2.0)

    GLUT.glutDisplayFunc(display)
    GLUT.glutReshapeFunc(reshape)
    GLUT.glutKeyboardFunc(game.handle_keyboard)
    GLUT.glutMouseFunc(mouse_func)
    GLUT.glutTimerFunc(0, timer_func, 0)

    GLUT.glutMainLoop()


if __name__ == "__main__":
    main()