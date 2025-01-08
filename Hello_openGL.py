from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

shooter_x = 400
shooter_y = 40
shooter_radius = 20

fireBall = [] 
fall_circles= [] 
score = 0

fireRadius = 8
fireSpeed = 5

missedFire = 0

paused = False
gameOver = False

lives = 3
shooter_color = (1.0, 1.0, 0.0)

def draw_points(x, y):
    glPointSize(4.0) #je point size ei draw krtesi
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def findzone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    if abs(dx) > abs(dy):
        if dx >= 0 and dy >= 0:
            zone = 0
        elif dx >= 0 and dy < 0:
            zone = 7
        elif dx < 0 and dy >= 0:
            zone = 3
        elif dx < 0 and dy < 0:
            zone = 4
    else:
        if dx >= 0 and dy >= 0:
            zone = 1
        elif dx >= 0 and dy < 0:
            zone = 6
        elif dx < 0 and dy >= 0:
            zone = 2
        elif dx < 0 and dy < 0:
            zone = 5

    return zone
 
def convertToZone0(zone, x, y): #abar zone converstion krtesi
    if zone == 0:
        return (x, y)
    elif zone == 1:
        return (y, x)
    elif zone == 2:
        return (y, -x)
    elif zone == 3:
        return (-x, y)
    elif zone == 4:
        return (-x, -y)
    elif zone == 5:
        return (-y, -x)
    elif zone == 6:
        return (-y, x)
    elif zone == 7:
        return (x, -y)
 
def originalZone(zone, x, y): #original zone e back krtesi
    if zone == 0:
        return (x, y)
    elif zone == 1:
        return (y, x)
    elif zone == 2:
        return (-y, x)
    elif zone == 3:
        return (-x, y)
    elif zone == 4:
        return (-x, -y)
    elif zone == 5:
        return (-y, -x)
    elif zone == 6:
        return (y, -x)
    elif zone == 7:
        return (x, -y)
 
def midpoint_line(zone, x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    d =   2 * dy - dx
    dNE = 2 * (dy - dx)
    dE =  2 * dy
 
    x, y = x1, y1
 
    while x <= x2:
        cx, cy = originalZone(zone, x, y)
        draw_points(cx, cy)
        if d <= 0:      # choose E
            x = x + 1
            d = d + dE            
        else:           # choose NE
            x = x + 1
            y = y + 1
            d = d + dNE
 
def midpoint_line_8way(x1, y1, x2, y2): #kn zone ei asi find kre zone 0 te antesi to  put midpoint line draw
    zone = findzone(x1, y1, x2, y2)
    x1, y1 = convertToZone0(zone, x1, y1)
    x2, y2 = convertToZone0(zone, x2, y2)
    midpoint_line(zone, x1, y1, x2, y2)

def circle_points(x, y, cx, cy): #center and ekta point nicchi to draw, based on algo
    draw_points(x + cx, y + cy)
    draw_points(y + cx, x + cy)
    
    draw_points(y + cx, -x + cy)
    draw_points(x + cx, -y + cy)

    draw_points(-x + cx, -y + cy)
    draw_points(-y + cx, -x + cy)

    draw_points(-y + cx, x + cy)
    draw_points(-x + cx, y + cy)
 
def midpoint_circle(cx, cy, r):
    d = 1 - r
    x = 0
    y = r
 
    circle_points(x, y, cx, cy)
 
    while x <= y:
        if d < 0:       # choose E
            d = d + 2*x + 3
            x = x + 1
        else:           # choose SE
            d = d + 2*x - 2*y + 5
            x = x + 1
            y = y - 1

        circle_points(x, y, cx, cy)
def draw_triangle(x, y, size):
    
    glColor3f(1.0, 1.0, 0.0)  # yellow colour

    top = (x, y + size)
    left = (x - size, y)
    right = (x + size, y)

    glBegin(GL_POINTS)
    
    
    for i in range(int(left[0]), int(right[0]) + 4): #x cordinate iteration er jnno
        for j in range(int(y), int(top[1]) + 4): #y cordinate iteration er jnno
            
            if (j - y) <= (i - left[0]) * (top[1] - y) / (top[0] - left[0]) and (j - y) <= (right[0] - i) * (top[1] - y) / (right[0] - top[0]):
                glVertex2f(i, j)

    glEnd()

def draw_rectangle(x, y, width, height):
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_POINTS)
    for i in range(int(x - width /3), int(x + width/3) + 4): #x cordinate iteration er jnno
        for j in range(int(y - height/2 ), int(y + height /2) + 4): #y cordinate iteration er jnno
            glVertex2f(i, j)
    glEnd()

def shooter():
     
    glColor3f(*shooter_color)
    draw_triangle(shooter_x, shooter_y, shooter_radius)
    draw_rectangle(shooter_x, shooter_y-15, shooter_radius, shooter_radius+10)
    draw_triangle(shooter_x, shooter_y-35, shooter_radius)


def drawFire(fire_x, fire_y):
    glColor3f(1.0, 0.0, 0.0)
    midpoint_circle(fire_x, fire_y, fireRadius)

def drawFallingCircle(circle):
    x, y, r, color = circle
    glColor3f(*color)
    midpoint_circle(x, y, r)



def update_fires(value):
    global fireBall, fall_circles, score, gameOver, shooter_color, lives, missedFire

    if gameOver or paused:
        glutPostRedisplay()
        glutTimerFunc(16, update_fires, 0)
        return  # early exit krtesi jodi game over hoi
    
    
    for fire in fireBall: 
        fire['y'] += fireSpeed 
   
    new_fires = []
    for fire in fireBall:
        if fire['y'] - fireRadius <= 840: #boundary er baire gele miss hoye jabe 
            new_fires.append(fire)
        else:
            missedFire += 1

    fireBall = new_fires

    
    for circle in fall_circles:
        circle[1] -= 3 # 3 unit namacchi
    
    #eikhaner collisions check fire ball ar circle er sthe
    for fire in fireBall:
        fx, fy = fire['x'], fire['y']
        for circle in fall_circles:
            cx, cy, cr, _ = circle
            if ((fx - cx) ** 2 + (fy - cy) ** 2) <= (fireRadius + cr) ** 2:
                score += 1
                print(f"Score: {score}") 
                fireBall.remove(fire)
                fall_circles.remove(circle)
                break

    #eikhaner collisions check fire ball ar shooter er sthe
    for circle in fall_circles:
        cx, cy, cr, i = circle
        if ((shooter_x - cx) ** 2 + (shooter_y - cy) ** 2) <= (shooter_radius + cr) ** 2:
            shooter_color = (1.0, 0.0, 0.0)  
            gameOver = True
            print("Game Over! Final Score:", score)
            glutPostRedisplay()  
            return  

    #check miss krle 
    for circle in fall_circles:
        if circle[1] - circle[2] <= 0:  
            lives -= 1 
            print(f"Remaining lives: {lives}")
            fall_circles.remove(circle)
            if lives == 0:
                gameOver = True
                shooter_color = (1.0, 0.0, 0.0)
                print("Game Over! Final Score:", score)
                glutPostRedisplay() 
                return

    if missedFire >= 3:
        shooter_color = (1.0, 0.0, 0.0)
        gameOver = True
        print("Game Over! Final Score:", score)
        glutPostRedisplay()
        return

    glutPostRedisplay()
    glutTimerFunc(20, update_fires, 0)

def keyboard(key, x, y):
    global shooter_x

    if gameOver or paused:
        return

    if key == b'a':
        shooter_x -= 20
        if shooter_x - shooter_radius < 0:
            shooter_x = shooter_radius

    elif key == b'd':
        shooter_x += 20
        if shooter_x + shooter_radius > 800:
            shooter_x = 800 - shooter_radius

    if key == b' ':
        
        fireBall.append({'x': shooter_x, 'y': shooter_y + shooter_radius})

    glutPostRedisplay()


def add_falling_circle(value):
    if not paused and not gameOver:
        x = random.randint(10, 780)
        y = 750
        r = random.randint(15, 40)
        color = (random.uniform(0.5, 1.0), random.uniform(0.5, 1.0), random.uniform(0.5, 1.0))
        fall_circles.append([x, y, r, color])

    # Schedule the next falling circle
    glutTimerFunc(1500, add_falling_circle, 0) #milisec

def pause():
    global paused
    paused = not paused
    if paused:
        print('Paused')
    else:
        print('Resumed')
    glutPostRedisplay()


def cross():
 
    global score
    
    glClear(GL_COLOR_BUFFER_BIT)  
    
    glColor3f(1.0, 0.0, 0.0)

    glRasterPos2f(300, 400)
    for char in "Goodbye!":
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))

    glRasterPos2f(320, 350)
    score_text = f"Your score is: {score}"
    for char in score_text:
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))

    glFlush() 
    time.sleep(2) 
    glutLeaveMainLoop()


def restart():
    global shooter_color, fireBall, fall_circles, score, gameOver, paused, lives, missedFire
    print("Starting Over")
    if gameOver:
        score = 0
        lives = 3
        missedFire = 0
        paused = False
        gameOver = False
        fall_circles.clear()
        fireBall.clear()
        shooter_color = (1.0, 1.0, 0.0)
        print(f"Score: {score}")
        glutPostRedisplay()
        glutTimerFunc(16, update_fires, 0)
    else:
        score = 0
        lives = 3
        missedFire = 0
        paused = False
        gameOver = False
        fall_circles.clear()
        fireBall.clear()
        shooter_color = (1.0, 1.0, 0.0)
        print(f"Score: {score}")
        glutPostRedisplay()
        return
        
    
def draw_button(color, shape):
    glColor3f(*color)
    if shape == 'play':
        midpoint_line_8way(385, 705, 420, 725)
        midpoint_line_8way(385, 745, 420, 725)
        midpoint_line_8way(385, 710, 390, 745)
    elif shape == 'pause':
        midpoint_line_8way(388, 705, 388, 745)
        midpoint_line_8way(412, 705, 412, 745)
    elif shape == 'left_arrow':
        midpoint_line_8way(55, 725, 75, 740)
        midpoint_line_8way(55, 725, 90, 725)
        midpoint_line_8way(55, 725, 75, 710)
    elif shape == 'cross':
        midpoint_line_8way(705, 705, 745, 745)
        midpoint_line_8way(745, 705, 705, 745)

def draw_buttons():
    draw_button((0.0, 1.0, 1.0), 'left_arrow')
    draw_button((1.0, 0.75, 0.0), 'pause' if not paused else 'play')
    draw_button((1.0, 0.0, 0.0), 'cross')

def inside(x, y, x1, y1, x2, y2):
    return x1 <= x <= x2 and y1 <= y <= y2

def mouse(button, state, x, y):
    global gameOver, paused, score, fireBall, fall_circles
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        y = 750 - y     
        if inside(x, y, 50, 700, 100, 750):  
            restart()
        elif inside(x, y, 375, 700, 425, 750):  
            pause()
        elif inside(x, y, 700, 700, 750, 750):  
           
            cross()
    



def iterate():
    glViewport(0, 0, 800, 750)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 800, 0.0, 750, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
 
def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()

    draw_buttons()
    if not gameOver:
        shooter()
        
        for fire in fireBall:
            drawFire(fire['x'], fire['y'])

        for circle in fall_circles:
            drawFallingCircle(circle)

        
        glColor3f(1.0, 0.1, 1.0)
        glRasterPos2f(20, 680)
        score_ = f"Score: {score}"
        for char in score_:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

        glRasterPos2f(20, 650)
        lives_ = f"Remaining lives: {lives}"
        for char in lives_:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
        
        glRasterPos2f(20, 620)
        missed_ = f"Missed Fire: {missedFire}"
        for char in missed_:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

    else:
        shooter()
        glColor3f(0.0, 1.0, 1.0)
        
        glRasterPos2f(340, 400)
        for char in "Game Over!":
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))
        
        glRasterPos2f(335, 370)
        score_text = f"Final Score: {score}"
        for char in score_text:
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))



    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(800, 750)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Shoot The Circles!")
glutDisplayFunc(showScreen)
glutMouseFunc(mouse)
glutKeyboardFunc(keyboard)

glutTimerFunc(0, update_fires, 0)
glutTimerFunc(0, add_falling_circle, 0)

glutMainLoop()