import numpy as np
import pygame
import math
import threading

#   setting   ------------------------------------------------

# screen
width = 1000.0
height = 600.0
bg_color = (0, 0, 0)

# basic
xyz = [6, 3.5, 0]
scale = 80
angle = [0, -55, 0]  # degree
rotation = [0, 3, 0]  # apply local rotation

# visual
vertex_size = 5
vertex_color = (255, 255, 255)
line_size = 2
line_color = (0, 144, 128)
line_color1 = (8, 8, 8)
line_color2 = (64, 64, 64)

# camera
near = 1
far = 100
FOV = 80
cam_pos = [0, 0, -100]

# #   icosahedron   ------------------------------------------------
# vertices = []
# golden = (1 + 5 ** 0.5) / 2
# for a in [-1, 1]:
#     for b in [-1, 1]:
#         vertices.append(np.matrix([0, a, b*golden, 1]).reshape(4, 1)*scale)
#         vertices.append(np.matrix([a, b*golden, 0, 1]).reshape(4, 1)*scale)
#         vertices.append(np.matrix([b*golden, 0, a, 1]).reshape(4, 1)*scale)

# edges = {}  # meh can use a better method
# for i in range(len(vertices)):
#     for j in range(len(vertices)):
#         if (i == j):
#             continue
#         v = vertices[i]
#         other = vertices[j]
#         dist = math.sqrt(
#             (v[0]-other[0])**2 +
#             (v[1]-other[1]) ** 2 +
#             (v[2]-other[2])**2)
#         if (j, i) not in edges.keys():
#             if (dist == 2*scale):
#                 edges[(i, j)] = dist

#   long cube   ------------------------------------------------
vertices = []
for i in [-1, 1]:
    for j in [-1, 1]:
        for k in [-100, 1]:
            vertices.append(
                np.matrix([[i * scale], [j * scale], [k * scale], [scale]]))

edges = {(0, 1): 1, (0, 2): 1, (0, 4): 1,
         (3, 1): 1, (3, 2): 1, (3, 7): 1,
         (6, 2): 1, (6, 4): 1, (6, 7): 1,
         (5, 1): 1, (5, 4): 1, (5, 7): 1}


#   projection   ------------------------------------------------
orthogonal_proj = np.matrix([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
])

f = 1 / np.tan(np.radians(FOV) / 2)
perspective_proj = np.array([
    [f / (width / height), 0, 0, 0],
    [0, f, 0, 0],
    [0, 0, (near + far) / (near - far), -1],
    [0, 0, near * far / (near - far) * 2, 0]
])


# Camera position
cam_pos_ = np.array(cam_pos)  # Example position
# Create a translation matrix for moving the scene opposite to camera movement
view_matrix = np.eye(4)
view_matrix[:3, 3] = -cam_pos_
# This translation_matrix can act as a simple view matrix for moving the camera/scene

#   translate   ------------------------------------------------
translation_matrix = np.array([
    [1, 0, 0, xyz[0]],
    [0, 1, 0, xyz[1]],
    [0, 0, 1, xyz[2]],
    [0, 0, 0, 1]])

#   input   ------------------------------------------------
user_input = None


def HandleConsoleInput():
    global user_input
    if user_input:
        cmd = user_input.split()
        try:
            if cmd[0] == "translation":
                translation_matrix[0, 3] = float(cmd[1])
                translation_matrix[1, 3] = float(cmd[2])
                translation_matrix[2, 3] = float(cmd[3])
            if cmd[0] == "rotation":
                rotation[0] = float(cmd[1])
                rotation[1] = float(cmd[2])
                rotation[2] = float(cmd[3])
        except:
            pass
        finally:
            user_input = None


def GetInput():
    global user_input
    while True:
        user_input = input()


thread = threading.Thread(target=GetInput)
thread.daemon = True
thread.start()


#   update   ------------------------------------------------
screen = pygame.display.set_mode((width, height))
_buff = []

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            # keyboard
            if event.key == pygame.K_a:
                rot_speed *= 1.15
            elif event.key == pygame.K_d:
                rot_speed /= 1.15
            elif event.key == pygame.K_SPACE:
                if (rot_speed != 0):
                    temp = rot_speed
                    rot_speed = 0
                else:
                    rot_speed = temp

    HandleConsoleInput()

    #   update  ------------------------------------------------

    sinX = math.sin(np.radians(angle[0]))
    cosX = math.cos(np.radians(angle[0]))
    sinY = math.sin(np.radians(angle[1]))
    cosY = math.cos(np.radians(angle[1]))
    sinZ = math.sin(np.radians(angle[2]))
    cosZ = math.cos(np.radians(angle[2]))

    angle[0] += rotation[0] * 0.01  # otherwise too fast
    angle[1] += rotation[1] * 0.01
    angle[2] += rotation[2] * 0.01

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
        proj = np.dot(orthogonal_proj, proj)
        # proj = np.dot(view_matrix, proj)
        # proj = np.dot(perspective_proj, proj)
        # proj /= proj[3]

        x = proj.A1[0]
        y = proj.A1[1]

        _buff.append((x, y))  # save for later to

        pygame.draw.circle(
            screen,
            vertex_color,
            (x, y),
            vertex_size)

    for key in edges:
        # if (edges[key] == 2):
        #     color = line_color
        # elif (edges[key] == 2*golden):
        #     color = line_color1
        # else:
        #     color = line_color2

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
