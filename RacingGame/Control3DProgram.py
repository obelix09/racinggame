
# from OpenGL.GL import *
# from OpenGL.GLU import *
from math import *

import pygame
from pygame.locals import *

import sys
import time

from Shaders import *
from Matrices import *

class GraphicsProgram3D:
    def __init__(self):

        pygame.init() 
        pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)

        self.shader = Shader3D()
        self.shader.use()

        self.model_matrix = ModelMatrix()
        self.collision_radius = 0.5

        self.view_matrix_1 = ViewMatrix()
        self.view_matrix_2 = ViewMatrix()
        # Cam position - looking at - upVector
        self.view_matrix_1.look(Point(0, 1, 3), Point(0, 0, 0), Vector(0, 1, 0))
        self.view_matrix_2.look(Point(3, 1, 0), Point(0, 0, 0), Vector(0, 1, 0))

        self.projection_matrix = ProjectionMatrix()
        self.projection_matrix.set_perspective(pi/3, 800/300, 0.5, 500)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.skybox = Skybox()
        self.trackPosition = 1
        self.track = Track(self.trackPosition / 2, self.trackPosition / 2, 0)
        self.innerCircle = innerCircle(self.trackPosition, self.trackPosition, 0)
        self.cube = Cube()
        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.angle = 0

       # Movement keys
        self.W_key_down = False
        self.S_key_down = False
        self.A_key_down = False
        self.D_key_down = False

        # Rotation keys (pitch & yaw)
        self.UP_key_down = False
        self.DOWN_key_down = False
        self.LEFT_key_down = False
        self.RIGHT_key_down = False

        # Max speed 
        self.max_speed = 20
        self.max_turn = pi / 2
        # Car speed per second
        self.speed1 = 0
        self.speed2 = 0
        self.turn1 = 0
        self.turn2 = 0
        # Turn speed
        self.turn_speed = 1
        # Acceleration
        self.acceleration = 4 

        self.texture_id01 = self.load_texture("/textures/spacesky.webp")
        self.texture_id02 = self.load_texture("/textures/box2.png")
        self.texture_id03 = self.load_texture("/textures/grass.jpg")
        self.texture_id04 = self.load_texture("/textures/raindrops.jpg")
        self.texture_id05 = self.load_texture("/textures/concrete.jpg")

    def load_texture(self, path_string):
        skybox = pygame.image.load(sys.path[0] + path_string)
        tex_string = pygame.image.tostring(skybox, "RGBA", 1)
        width = skybox.get_width()
        height = skybox.get_height()
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, tex_string)
        return tex_id

    def update(self):
        delta_time = self.clock.tick() / 1000.0
        self.angle += pi * delta_time
        ########### Car controls 1 ############
              # go forward
        if self.UP_key_down:
            if (self.speed1 < self.max_speed):
                self.speed1 += self.acceleration * delta_time
            self.view_matrix_1.slide(0, 0, delta_time * -self.speed1)
        else:
            if (self.speed1 > 0):
                self.speed1 -= self.acceleration * delta_time * 2
            self.view_matrix_1.slide(0, 0, delta_time * -self.speed1)
            if (self.speed1 < 0):
                self.speed1 = 0

        # If press right, turn right
        # YAW (rotate camera left and right) 
        if self.LEFT_key_down:
            self.turn1 = delta_time * -pi * self.speed1/20
            self.view_matrix_1.yaw(self.turn1 * self.turn_speed)
        if self.RIGHT_key_down:
            self.turn1 = delta_time * pi * self.speed1/20
            self.view_matrix_1.yaw(self.turn1 * self.turn_speed)

        ########### Car controls 2 ############
        # go forward
        if self.W_key_down:
            if (self.speed2 < self.max_speed):
                self.speed2 += self.acceleration * delta_time
            self.view_matrix_2.slide(0, 0, delta_time * -self.speed2)
        else:
            if (self.speed2 > 0):
                self.speed2 -= self.acceleration * delta_time * 2
            self.view_matrix_2.slide(0, 0, delta_time * -self.speed2)
            if (self.speed2 < 0):
                self.speed2 = 0

        # If press right, turn right
        # YAW (rotate camera left and right) 
        if self.A_key_down:
            self.turn2 = delta_time * -pi * self.speed2/20
            self.view_matrix_2.yaw(self.turn2 * self.turn_speed)
        if self.D_key_down:
            self.turn2 = delta_time * pi * self.speed2/20
            self.view_matrix_2.yaw(self.turn2 * self.turn_speed)
        delta_time = self.clock.tick() / 1000.0

    def displayScreen(self):
        self.shader.set_light_position(Point(4.0, 4.0, 4.0))
        self.shader.set_light_diffuse(1.0, 1.0, 1.0)
        self.shader.set_light_specular(1.0, 1.0, 1.0)

        self.model_matrix.load_identity()

        # Skybox
        self.skybox.set_vertices(self.shader)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id01)
        self.shader.set_diffuce_tex(0)

        self.shader.set_material_diffuse(1.0, 1.0, 1.0)
        self.shader.set_material_specular(0.0, 0.0, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_scale(600,600,600)
        # self.model_matrix.add_rotate_y(self.angle * 0.5)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.skybox.draw(self.shader)
        self.model_matrix.pop_matrix()

        # Track
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id05)
        self.shader.set_diffuce_tex(0)
        self.track.set_vertices(self.shader)
        self.shader.set_material_diffuse(1.0, 1.0, 1.0)
        self.shader.set_material_specular(0.0, 0.0, 0.0)
        self.model_matrix.push_matrix()
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.track.draw(self.shader)
        self.model_matrix.pop_matrix()

        # Inner Circle or Track
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id03)
        self.shader.set_diffuce_tex(0)
        self.innerCircle.set_vertices(self.shader)
        self.shader.set_material_diffuse(1.0, 1.0, 1.0)
        self.shader.set_material_specular(0.0, 0.0, 0.0)
        self.model_matrix.push_matrix()
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.innerCircle.draw(self.shader)
        self.model_matrix.pop_matrix()
        

    def display(self):
        glEnable(GL_DEPTH_TEST)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        # Player 1 camera
        self.shader.set_view_matrix(self.view_matrix_1.get_matrix())
        glViewport(0, 0, 800, 300)
        self.displayScreen()

        # Player 2 camera
        self.shader.set_view_matrix(self.view_matrix_2.get_matrix())
        glViewport(0, 300, 800, 300)
        self.displayScreen()

        pygame.display.flip()

    def goalEntered(self):
        temp_ang = 0
        while temp_ang < 2 * pi:
            x1 = self.view_matrix_1.eye.x + self.collision_radius * cos(temp_ang)
            y1 = self.view_matrix_1.eye.y
            z1 = self.view_matrix_1.eye.z + self.collision_radius * sin(temp_ang)
            x2 = self.view_matrix_2.eye.x + self.collision_radius * cos(temp_ang)
            y2 = self.view_matrix_2.eye.y
            z2 = self.view_matrix_2.eye.z + self.collision_radius * sin(temp_ang)
            temp_ang += (pi * 2)/16
            point1 = Point(x1, y1, z1) 
            point2 = Point(x2, y2, z2) 
            if point1.x >= self.cube_collision_points[0] and point1.x <= self.cube_collision_points[1] or point2.x >= self.cube_collision_points[0] and point2.x <= self.cube_collision_points[1]:
                    if point.z >= self.cube_collision_points[2] and point.z <= self.cube_collision_points[3] or point.z >= self.cube_collision_points[2] and point.z <= self.cube_collision_points[3]:
                        self.view_matrix_1.look(Point(0, 0, 3), Point(0, 0, 0), Vector(0, 1, 0))
                        self.view_matrix_2.look(Point(0, 0, 3), Point(0, 0, 0), Vector(0, 1, 0))

    def program_loop(self):
        exiting = False
        while not exiting:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quitting!")
                    exiting = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        print("Escaping!")
                        exiting = True
                    if event.key == K_w:
                        self.W_key_down  = True
                    if event.key == K_s:
                        self.S_key_down = True
                    if event.key == K_a:
                        self.A_key_down = True
                    if event.key == K_d:
                        self.D_key_down = True
                    if event.key == K_UP:
                        self.UP_key_down = True
                    if event.key == K_DOWN:
                        self.DOWN_key_down = True
                    if event.key == K_LEFT:
                        self.LEFT_key_down = True
                    if event.key == K_RIGHT:
                        self.RIGHT_key_down = True
                    if event.key == K_SPACE:
                        self.SPACE_key_down = True
                elif event.type == pygame.KEYUP:
                    if event.key == K_w:
                        self.W_key_down  = False
                    if event.key == K_s:
                        self.S_key_down = False
                    if event.key == K_a:
                        self.A_key_down = False
                    if event.key == K_d:
                        self.D_key_down = False
                    if event.key == K_UP:
                        self.UP_key_down = False
                    if event.key == K_DOWN:
                        self.DOWN_key_down = False
                    if event.key == K_LEFT:
                        self.LEFT_key_down = False
                    if event.key == K_RIGHT:
                        self.RIGHT_key_down = False
                    if event.key == K_SPACE:
                        self.SPACE_key_down = False
            
            self.update()
            self.display()

        #OUT OF GAME LOOP
        pygame.quit()

    def start(self):
        self.program_loop()

if __name__ == "__main__":
    GraphicsProgram3D().start()