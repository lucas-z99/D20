import numpy as np
import pygame
import math
import threading
import shapes


#   setting   ------------------------------------------------

# screen
width = 1000.0
height = 600.0
bg_color = (0, 0, 0)

# basic
xyz = [0, -5, 0]
scale = 11
angle = [0, 0, 0]
rotation = [0.33, 30, 0.33]  # local rotation

# visual
vertex_size = 5
vertex_color = (255, 255, 255)
line_size = 2
line_color = (0, 144, 128)
line_color1 = (8, 8, 8)
line_color2 = (64, 64, 64)
face_color = (3, 45, 84)
# face_color = (170, 223, 195)
# face_color = (233, 116, 81)

# perstective
use_perspective = 1
near: float = 0.1
far: float = 5000
FOV = 80
cam_dist = 60


#   shape   ------------------------------------------------
vertices, edges, faces = shapes.not_a_cube(scale)
# vertices, edges, faces = shapes.icosahedron(scale)
# vertices, edges, faces = shapes.long_cube(scale)


#   cache   ------------------------------------------------
half_width = width/2
half_height = height/2

#   projection matrix   ------------------------------------------------
orthographic_matrix = np.matrix([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
])

S = 1.0 / np.tan(np.radians(FOV/2))  # scale x,y by distance
perspective_matrix = np.array([
    [S * height/width, 0, 0, 0],
    [0, S, 0, 0],
    [0, 0, (far+near) / (far-near), -2*far*near / (far-near)],
    [0, 0, 1, 0]
])

#   translate   ------------------------------------------------
translation_matrix = np.array([
    [1, 0, 0, xyz[0]],
    [0, 1, 0, xyz[1]],
    [0, 0, 1, xyz[2] + cam_dist],
    [0, 0, 0, 1.0]])

#   console input   ------------------------------------------------
user_input = None


def HandleConsoleInput():
    global user_input, vertices, edges, faces
    if user_input:
        cmd = user_input.split()
        try:
            if cmd[0].lower() == "cube":
                vertices, edges, faces = shapes.not_a_cube(scale)
            if cmd[0].lower() == "long":
                vertices, edges, faces = shapes.long_cube(scale)
            if cmd[0].lower() == "d20":
                vertices, edges, faces = shapes.icosahedron(scale)
        except:
            print("Invalid input")
        finally:
            user_input = None


def GetInput():
    global user_input
    while True:
        user_input = input()


thread = threading.Thread(target=GetInput)
thread.daemon = True
thread.start()


def HandleKeyboard():

    global rot_speed
    key_down = pygame.key.get_pressed()
    if key_down[pygame.K_e]:
        rot_speed *= 1.005
    elif key_down[pygame.K_q]:
        rot_speed /= 1.005
    elif key_down[pygame.K_w]:
        translation_matrix[1, 3] += 0.1
    elif key_down[pygame.K_s]:
        translation_matrix[1, 3] -= 0.1
    elif key_down[pygame.K_a]:
        translation_matrix[0, 3] -= 0.1
    elif key_down[pygame.K_d]:
        translation_matrix[0, 3] += 0.1


#   update   ------------------------------------------------
screen = pygame.display.set_mode((width, height))
_buff = []
rot_speed = 1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if (rot_speed != 0):
                temp = rot_speed
                rot_speed = 0
            else:
                rot_speed = temp

    HandleKeyboard()
    HandleConsoleInput()

    #   update  ------------------------------------------------

    sinX = math.sin(np.radians(angle[0]))
    cosX = math.cos(np.radians(angle[0]))
    sinY = math.sin(np.radians(angle[1]))
    cosY = math.cos(np.radians(angle[1]))
    sinZ = math.sin(np.radians(angle[2]))
    cosZ = math.cos(np.radians(angle[2]))

    angle[0] += rotation[0] * 0.001 * rot_speed  # otherwise too fast
    angle[1] += rotation[1] * 0.001 * rot_speed
    angle[2] += rotation[2] * 0.001 * rot_speed

    rotation_matrix = np.matrix([
        [cosY*cosZ, sinX*sinY*cosZ - cosX*sinZ, cosX*sinY*cosZ + sinX*sinZ, 0],
        [cosY*sinZ, sinX*sinY*sinZ + cosX*cosZ, cosX*sinY*sinZ - sinX*cosZ, 0],
        [-sinY,     sinX*cosY,                  cosX*cosY,                  0],
        [0,         0,                          0,                          1]])

    TR_matrix = np.dot(translation_matrix, rotation_matrix)

    # update
    screen.fill(bg_color)
    for v in vertices:

        proj = np.dot(TR_matrix, v)

        if (not use_perspective):
            proj = np.dot(orthographic_matrix, proj)
        else:
            proj = np.dot(perspective_matrix, proj)
            proj /= proj.A1[3]  # apply w
            x = (proj.A1[0] + 1) * half_width  # get screen pos
            y = (1 - proj.A1[1]) * half_height

        pygame.draw.circle(
            screen,
            vertex_color,
            (x, y),
            vertex_size)

        _buff.append((x, y))  # for drawing edges

    for f in faces:
        poly = ()
        for v in f:
            poly += (_buff[v],)
        pygame.draw.polygon(screen, face_color, poly)

    for key in edges:
        color = line_color
        pygame.draw.line(
            screen,
            color,
            _buff[key[0]],
            _buff[key[1]],
            line_size)

    _buff.clear()

    # display
    pygame.display.update()
