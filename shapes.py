import numpy as np
import math


#   'cube'   ------------------------------------------------
def not_a_cube(scale):

    vertices = []

    # 3 <-- 2
    #       ^
    #       |
    # 0 --> 1

    vertices.append([-1, -1, 1, 1])
    vertices.append([2, -2, 2, 1])
    vertices.append([1, 1, 1, 1])
    vertices.append([-1, 1, 1, 1])
    vertices.append([-1, -1, -1, 1])
    vertices.append([1, -1, -1, 1])
    vertices.append([1, 1, -1, 1])
    vertices.append([-2, 2, -2, 1])

    for i in range(len(vertices)):  # scale & np format shananigans
        vertices[i] = np.matrix(vertices[i]).reshape(4, 1) * scale
        vertices[i][3] = 1  # reset w to 1 AFTER scaling

    edges = {}

    for i in range(1, len(vertices)):
        edges[(i-1, i)] = -1

    faces = [(0, 1, 2), (5, 6, 7)]

    return vertices, edges, faces


#   icosahedron   ------------------------------------------------

golden = (1 + 5 ** 0.5) / 2


def icosahedron(scale):

    vertices = []

    for a in [-1, 1]:
        for b in [-golden, golden]:
            vertices.append([0, a, b, 1])
            vertices.append([a, b, 0, 1])
            vertices.append([b, 0, a, 1])

    # do the edge before scaling mess up float precision
    edges = {}

    for i in range(len(vertices)):  # meh can really use a better way but this only run once
        for j in range(len(vertices)):
            if (i == j):
                continue
            v1 = vertices[i]
            v2 = vertices[j]
            dist = math.sqrt((v1[0]-v2[0])**2 +
                             (v1[1]-v2[1])**2 +
                             (v1[2]-v2[2])**2)
            if (j, i) not in edges.keys():
                if (dist == 2):  # outer = 2, inner-center = 2*golden, inner-diagonal = 2*golden^2
                    edges[(i, j)] = dist

    # scale & np format shananigans
    for i in range(len(vertices)):
        vertices[i] = np.matrix(vertices[i]).reshape(4, 1) * scale*1.5
        vertices[i][3] = 1

    faces = [(0, 1, 2)]

    return vertices, edges, faces


#   long cube   ------------------------------------------------

def long_cube(scale):

    vertices = []

    for x in [-1, 1]:
        for y in [-2, 2]:
            for z in [-1, 1]:
                vertices.append([x, y, z, 1])

    for x in range(len(vertices)):
        vertices[x] = np.matrix(vertices[x]).reshape(4, 1) * scale
        vertices[x][3] = 1

    edges = {(0, 1): 0, (0, 2): 0, (0, 4): 0,
             (3, 1): 0, (3, 2): 0, (3, 7): 0,
             (6, 2): 0, (6, 4): 0, (6, 7): 0,
             (5, 1): 0, (5, 4): 0, (5, 7): 0}

    faces = [(0, 1, 5, 4)]

    return vertices, edges, faces
