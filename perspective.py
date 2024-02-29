import numpy
import pygame
import math

#   setting   ------------------------------------------------
width = 1000  # screen size
height = 600
bg_color = (0, 0, 0)

scale = 80
pos = [width/2, height/2]  # center of cube
vertex_color = (255, 255, 255)
vertex_size = 5
line_color = (0, 144, 128)
line_size = 2

angle_x = 0  # initial angle
angle_x = 0
angle_x = 3.7
rotation = [0, 1, 0]
rot_speed = 0.00025

near = 50  # perspective
far = 60

#   matrix   ------------------------------------------------
vertices = []
for i in [-1, 1]:
    for j in [-1, 1]:
        for k in [-100, 1]:
            vertices.append(numpy.matrix([[i], [j], [k]]))

edges = [(0, 1), (0, 2), (0, 4),
         (3, 1), (3, 2), (3, 7),
         (6, 2), (6, 4), (6, 7),
         (5, 1), (5, 4), (5, 7)]

#   perspective   ------------------------------------------------


def perspective_proj(vertex: list[int, int]) -> list[int, int]:
    x, y, z = vertex

    x *= far / (z+far+near)
    y *= far / (z+far+near)

    return [x, y]


#   code   ------------------------------------------------
screen = pygame.display.set_mode((width, height))
_buff = []

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
        _v = rot_matrix * v
        proj = perspective_proj(_v.A1) * scale
        x = proj[0] * scale + pos[0]
        y = proj[1] * scale + pos[1]

        _buff.append((x, y))  # save for later to

        pygame.draw.circle(
            screen,
            vertex_color,
            (x, y),
            vertex_size)

    for p0, p1 in edges:
        pygame.draw.line(
            screen,
            line_color,
            _buff[p0],
            _buff[p1],
            line_size)

    _buff.clear()

    # commit
    pygame.display.update()
