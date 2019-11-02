
import random
from random import *

from OpenGL.GL import *
from OpenGL.GLU import *

import math
from math import *


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __len__(self):
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
    
    def normalize(self):
        length = self.__len__()
        self.x /= length
        self.y /= length
        self.z /= length

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector(self.y*other.z - self.z*other.y, self.z*other.x - self.x*other.z, self.x*other.y - self.y*other.x)

class Cube:
    def __init__(self):
        self.position_array = [
                            #Back
                            0.5, -0.5, -0.5,
                            0.5, 0.5, -0.5,
                            -0.5, 0.5, -0.5,
                            -0.5, -0.5, -0.5,
                            #Front
                            -0.5, -0.5, 0.5,
                            -0.5, 0.5, 0.5,
                            0.5, 0.5, 0.5,
                            0.5, -0.5, 0.5,
                            #Down
                            -0.5, -0.5, -0.5,
                            -0.5, -0.5, 0.5,
                            0.5, -0.5, 0.5,
                            0.5, -0.5, -0.5,
                            #Up
                            -0.5, 0.5, 0.5,
                            -0.5, 0.5, -0.5,
                            0.5, 0.5, -0.5,
                            0.5, 0.5, 0.5,
                            #Left
                            -0.5, -0.5, -0.5,
                            -0.5, 0.5, -0.5,
                            -0.5, 0.5, 0.5,
                            -0.5, -0.5, 0.5,
                            #Right
                            0.5, -0.5, 0.5,
                            0.5, 0.5, 0.5,
                            0.5, 0.5, -0.5,
                            0.5, -0.5, -0.5]
        self.normal_array = [
                            #Back
                            0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            #Front
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            #Down
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,
                            #Up
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            #Left 
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            #Right
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0]
        self.uv_array = [
                        # back 
                        0.0, 0.0,
                        0.0, 1.0, 
                        1.0, 1.0, 
                        1.0, 0.0,
                        # front 
                        0.0, 0.0,
                        0.0, 1.0, 
                        1.0, 1.0, 
                        1.0, 0.0,
                        # down
                        0.0, 0.0,
                        0.0, 1.0, 
                        1.0, 1.0, 
                        1.0, 0.0,
                        # up
                        0.0, 0.0,
                        0.0, 10.0, 
                        5.0, 5.0, 
                        5.0, 0.0,
                        # left
                        0.0, 0.0,
                        0.0, 1.0, 
                        1.0, 1.0, 
                        1.0, 0.0,
                        # right (DONE)
                        0.0, 0.0,
                        0.0, 1.0, 
                        1.0, 1.0, 
                        1.0, 0.0]               
    
    def set_vertices(self, shader):
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)
        shader.set_uv_attribute(self.uv_array)

    def draw(self, shader):
        glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 4, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 8, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 12, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 16, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 20, 4)

class Track:
        def __init__(self, x, y , z,  radius = 10, sides = 19):
            self.fullCircle = 2.2 * pi
            self.vertices = []
            self.miniVertices = []
            self.normals = [] 
            self.uv_array = [] 

            self.nrOfVertices = sides + 1
            self.vertices.append(x)
            self.vertices.append(y)
            self.vertices.append(z)
            self.normals.append(0)
            self.normals.append(1)
            self.normals.append(0)
            self.uv_array.append(0)
            self.uv_array.append(2)
            self.uv_array.append(0)
            for count in range(sides):
                self.vertices.append(x + ( radius * cos( count *  self.fullCircle / sides )))
                self.vertices.append(y)
                self.vertices.append(z + ( radius * sin( count * self.fullCircle / sides )) * 3)
                self.normals.append(0)
                self.normals.append(1)
                self.normals.append(0)
                self.uv_array.append(0)
                self.uv_array.append(2)
                self.uv_array.append(0)

        def set_vertices(self, shader):
            shader.set_position_attribute(self.vertices)
            shader.set_normal_attribute(self.normals)
            shader.set_uv_attribute(self.uv_array)

        def draw(self, shader):
            glDrawArrays( GL_TRIANGLE_FAN, 0, self.nrOfVertices)


class innerCircle:
        def __init__(self, x, y , z,  radius = 5, sides = 19):
            self.fullCircle = 2.2 * pi
            self.miniVertices = []
            self.normals = []
            self.uv_array = [] 

            self.nrOfVertices = sides + 1
            self.miniVertices.append(x)
            self.miniVertices.append(y)
            self.miniVertices.append(z)
            self.normals.append(0)
            self.normals.append(1)
            self.normals.append(0)
            self.uv_array.append(0)
            self.uv_array.append(2)
            self.uv_array.append(0)
            for count in range(sides):
                self.miniVertices.append( + ( radius * cos( count *  self.fullCircle / sides )))
                self.miniVertices.append(y / 2)
                self.miniVertices.append(z + ( radius * sin( count *  self.fullCircle / sides )) * 3)
                self.normals.append(0)
                self.normals.append(1)
                self.normals.append(0)
                self.uv_array.append(0)
                self.uv_array.append(2)
                self.uv_array.append(0)

        def set_vertices(self, shader):
            shader.set_position_attribute(self.miniVertices)
            shader.set_normal_attribute(self.normals)
            shader.set_uv_attribute(self.uv_array)

        def draw(self, shader):
            glDrawArrays( GL_TRIANGLE_FAN, 0, self.nrOfVertices)


# class Ghost:
#     def __init__(self):
#         self.position_array = [0.0

#         ]

class Skybox:
    def __init__(self):
        self.position_array = [
                            #Back
                            0.5, -0.5, -0.5,
                            0.5, 0.5, -0.5,
                            -0.5, 0.5, -0.5,
                            -0.5, -0.5, -0.5,
                            #Front
                            -0.5, -0.5, 0.5,
                            -0.5, 0.5, 0.5,
                            0.5, 0.5, 0.5,
                            0.5, -0.5, 0.5,
                            #Down
                            -0.5, -0.5, -0.5,
                            -0.5, -0.5, 0.5,
                            0.5, -0.5, 0.5,
                            0.5, -0.5, -0.5,
                            #Up
                            -0.5, 0.5, 0.5,
                            -0.5, 0.5, -0.5,
                            0.5, 0.5, -0.5,
                            0.5, 0.5, 0.5,
                            #Left
                            -0.5, -0.5, -0.5,
                            -0.5, 0.5, -0.5,
                            -0.5, 0.5, 0.5,
                            -0.5, -0.5, 0.5,
                            #Right
                            0.5, -0.5, 0.5,
                            0.5, 0.5, 0.5,
                            0.5, 0.5, -0.5,
                            0.5, -0.5, -0.5]
        self.normal_array = [
                            #Back
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            #Front
                            0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            #Down
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            #Up
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,
                            #Left 
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            #Right
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0]
        self.uv_array = [
                        # back 
                        0.25, 0.334,
                        0.25, 0.665, 
                        0.5, 0.665, 
                        0.5, 0.334,
                        # front 
                        0.75, 0.334,
                        0.75, 0.665, 
                        1.0, 0.665, 
                        1.0, 0.334,
                        # down
                        0.75, 0.001,
                        0.75, 0.334, 
                        0.999, 0.334, 
                        0.999, 0.001,
                        # up
                        0.75, 0.665,
                        0.75, 0.99, 
                        0.99, 0.99, 
                        0.99, 0.665,
                        # left
                        0.5, 0.334,
                        0.5, 0.665, 
                        0.75, 0.665, 
                        0.75, 0.334,
                        # right
                        0.01, 0.334,
                        0.01, 0.665, 
                        0.25, 0.665, 
                        0.25, 0.334]
    
    def set_vertices(self, shader):
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)
        shader.set_uv_attribute(self.uv_array)

    def draw(self, shader):
        glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 4, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 8, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 12, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 16, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 20, 4)

class OptimizedCube:
    def __init__(self):
        self.position_array = [
                            #Back
                            0.5, -0.5, -0.5,
                            0.5, 0.5, -0.5,
                            -0.5, 0.5, -0.5,
                            -0.5, -0.5, -0.5,
                            #Front
                            -0.5, -0.5, 0.5,
                            -0.5, 0.5, 0.5,
                            0.5, 0.5, 0.5,
                            0.5, -0.5, 0.5,
                            #Down
                            -0.5, -0.5, -0.5,
                            -0.5, -0.5, 0.5,
                            0.5, -0.5, 0.5,
                            0.5, -0.5, -0.5,
                            #Up
                            -0.5, 0.5, 0.5,
                            -0.5, 0.5, -0.5,
                            0.5, 0.5, -0.5,
                            0.5, 0.5, 0.5,
                            #Left
                            -0.5, -0.5, -0.5,
                            -0.5, 0.5, -0.5,
                            -0.5, 0.5, 0.5,
                            -0.5, -0.5, 0.5,
                            #Right
                            0.5, -0.5, 0.5,
                            0.5, 0.5, 0.5,
                            0.5, 0.5, -0.5,
                            0.5, -0.5, -0.5]
        self.normal_array = [
                            #Back
                            0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            #Front
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            #Down
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,
                            #Up
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            #Left 
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            #Right
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0]
        self.uv_array = [
                        # back 
                        0.0, 0.0,
                        0.0, 1.0, 
                        1.0, 1.0, 
                        1.0, 0.0,
                        # front 
                        0.0, 0.0,
                        0.0, 1.0, 
                        1.0, 1.0, 
                        1.0, 0.0,
                        # down
                        0.0, 0.0,
                        0.0, 1.0, 
                        1.0, 1.0, 
                        1.0, 0.0,
                        # up
                        0.0, 0.0,
                        0.0, 1.0, 
                        1.0, 1.0, 
                        1.0, 0.0,
                        # left
                        0.0, 0.0,
                        0.0, 1.0, 
                        1.0, 1.0, 
                        1.0, 0.0,
                        # right (DONE)
                        0.0, 0.0,
                        0.0, 1.0, 
                        1.0, 1.0, 
                        1.0, 0.0]               
        
        # # gl gives me an id, 1 = one buffer
        # self.vertex_buffer_id = glGenBuffers(1)
        # # i want your glbuffer to be this buffer (idno)
        # glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer_id)
        # glBufferData(GL_ARRAY_BUFFER, numpy.array(vertex_array, dtype='float32'), GL_STATIC_DRAW)

    def set_vertices(self, shader):
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)
        shader.set_uv_attribute(self.uv_array)

    def draw(self, shader):
        glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 4, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 8, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 12, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 16, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 20, 4)