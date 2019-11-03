
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
        return Vector(self.x/length, self.y/length, self.z/length)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector(self.y*other.z - self.z*other.y, self.z*other.x - self.x*other.z, self.x*other.y - self.y*other.x)

class Line():
    def __init__(self, point_1, point_2):
        self.point_1 = point_1
        self.point_2 = point_2
        self.vector = Vector(point_1.x - point_2.x, point_1.y - point_2.y, point_1.z - point_2.z)
        self.n_vector = Vector(self.vector.z, self.vector.y, -self.vector.x)
        self.unit_vector = self.n_vector.normalize()

    def detect_collision(self, point, motion , delta_time):
        b_a = self.point_1 - point
        n_b_a = self.unit_vector.dot(b_a)
        n_c = self.unit_vector.dot(motion)
        if (n_c != 0):
            t_hit = (n_b_a / n_c)
            if ((t_hit >= 0) and (t_hit <= delta_time)):
                #Calculate position
                p_hit = Point((point.x + (t_hit * motion.x)), point.y, (point.z + (t_hit * motion.z)))
                if (self.point_1.x == self.point_2.x) :
                    if (self.point_1.z >= self.point_2.z):
                        if ((p_hit.z >= self.point_2.z) and (p_hit.z <= self.point_1.z)):
                            return p_hit
                    else:
                        if ((p_hit.z <= self.point_2.z) and (p_hit.z >= self.point_1.z)):
                            return p_hit
                else :
                    if (self.point_1.x >= self.point_2.x):
                        if ((p_hit.x >= self.point_2.x) and (p_hit.x <= self.point_1.x)):
                            return p_hit
                    else :
                        if ((p_hit.x <= self.point_2.x) and (p_hit.x >= self.point_1.x)):
                            return p_hit
        return False

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
                        0.0, 5.0, 
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


class Cube_2D:
    def __init__(self):
        self.position_array = [
                           #Up
                            -0.5, 0.5, 0.5,
                            -0.5, 0.5, -0.5,
                            0.5, 0.5, -0.5,
                            0.5, 0.5, 0.5,]
        self.normal_array = [
                            #Up
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,]
        self.uv_array = [
                        # up
                        0.0, 0.0,
                        0.0, 1.0, 
                        5.0, 1.0, 
                        5.0, 0.0,]               
    
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

class Circle_2D:
        def __init__(self, x, y , z,  radius = 15, sides = 19):
            self.fullCircle = 2.2 * pi
            self.vertices = []
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
                self.vertices.append(z + ( radius * sin( count * self.fullCircle / sides )))
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

class Racecar:
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
    
    def get_collision_points(self, model_matrix):
        #first point
        pointX1 = -0.5 * model_matrix[0] + -0.5 * model_matrix[1] + -0.5 * model_matrix[2] + 1 * model_matrix[3] 
        pointZ1 = -0.5 * model_matrix[8] + -0.5 * model_matrix[9] + -0.5 * model_matrix[10] + 1 * model_matrix[11] 

        #second point
        pointX2 = -0.5 * model_matrix[0] + -0.5 * model_matrix[1] + -0.5 * model_matrix[2] + 1 * model_matrix[3] 
        pointZ2 = 0.5 * model_matrix[8] + 0.5 * model_matrix[9] + 0.5 * model_matrix[10] + 1 * model_matrix[11] 

        #third point
        pointX3 = 0.5 * model_matrix[0] + 0.5 * model_matrix[1] + 0.5 * model_matrix[2] + 1 * model_matrix[3] 
        pointZ3 = 0.5 * model_matrix[8] + 0.5 * model_matrix[9] + 0.5 * model_matrix[10] + 1 * model_matrix[11] 

        #forth point
        pointX4 = 0.5 * model_matrix[0] + 0.5 * model_matrix[1] + 0.5 * model_matrix[2] + 1 * model_matrix[3] 
        pointZ4 = -0.5 * model_matrix[8] + -0.5 * model_matrix[9] + -0.5 * model_matrix[10] + 1 * model_matrix[11] 

        return [Point(pointX1 , 0, pointZ1), Point(pointX2 , 0, pointZ2), Point(pointX3 , 0, pointZ3), Point(pointX4 , 0, pointZ4)]

    def get_global_vector(self, motion, model_matrix):
        vectorX = motion.x * model_matrix[0] + motion.x * model_matrix[1] + motion.x * model_matrix[2] + 0 * model_matrix[3]
        vectorZ = motion.z * model_matrix[8] + motion.z * model_matrix[9] + motion.z * model_matrix[10] + 0 * model_matrix[11]

        return Vector(vectorX, 0, vectorZ)

    def get_local_point(self, point, model_matrix):
        pointX = point.x / (model_matrix[0] + model_matrix[1] + model_matrix[2] + model_matrix[3])
        pointZ = point.z / (model_matrix[8] + model_matrix[9] + model_matrix[10] + model_matrix[11])

        return Point(pointX, point.y, pointZ)