import numpy
import pygame
import math

#   setting   ------------------------------------------------
width = 1000  # screen size
height = 600
bg_color = (0, 0, 0)

scale = 85
pos = [width/2, height/2]  # center of cube
vertex_color = (255, 255, 255)
vertex_size = 5
line_color = (0, 144, 128)
line_size = 2

angle_x = 0  # initial rotation
angle_x = 0
angle_x = 0
rotation = [1, 2, 0.2]
rot_speed = 0.00035

#   matrix   ------------------------------------------------
vertices = []
vertices.append(numpy.matrix([[-1], [-1], [1]]))
vertices.append(numpy.matrix([[2], [-2], [2]]))
vertices.append(numpy.matrix([[1], [1], [1]]))
vertices.append(numpy.matrix([[-1], [1], [1]]))
vertices.append(numpy.matrix([[-1], [-1], [-1]]))
vertices.append(numpy.matrix([[1], [-1], [-1]]))
vertices.append(numpy.matrix([[1], [1], [-1]]))
vertices.append(numpy.matrix([[-2], [2], [-2]]))


# project
proj_matrix = numpy.matrix([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 0]])


#   code   ------------------------------------------------
screen = pygame.display.set_mode((width, height))
last_vertex = (0, 0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            # input
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

    # angel
    sin_x = math.sin(angle_x)
    cos_x = math.cos(angle_x)
    sin_y = math.sin(angle_x)
    cos_y = math.cos(angle_x)
    sin_z = math.sin(angle_x)
    cos_z = math.cos(angle_x)
    angle_x += rotation[0]*rot_speed
    angle_x += rotation[1]*rot_speed
    angle_x += rotation[2]*rot_speed

    # rotation matrix
    rot_matrix = numpy.matrix([
        [cos_y*cos_z, sin_x*sin_y*cos_z-cos_x *
            sin_z, cos_x*sin_y*cos_z+sin_x*sin_z],
        [cos_y*sin_z, sin_x*sin_y*sin_z+cos_x *
            cos_z, cos_x*sin_y*sin_z-sin_x*cos_z],
        [-sin_y, sin_x*cos_y, cos_x*cos_y]
    ])

    # update
    screen.fill(bg_color)

    for v in vertices:
        proj = proj_matrix * rot_matrix * v
        x = proj.A1[0] * scale + pos[0]
        y = proj.A1[1] * scale + pos[1]

        pygame.draw.circle(
            screen,
            vertex_color,
            (x, y),
            vertex_size)

        pygame.draw.line(
            screen,
            line_color,
            (x, y),
            last_vertex,
            line_size)

        last_vertex = (x, y)

    # commit
    pygame.display.update()
