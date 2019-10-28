
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

        self.view_matrix = ViewMatrix()
        self.view_matrix.look(Point(0, 0, 3), Point(0, 0, 0), Vector(0, 1, 0))
        self.shader.set_view_matrix(self.view_matrix.get_matrix())

        self.projection_matrix = ProjectionMatrix()
        self.projection_matrix.set_perspective(pi/2, 800/600, 0.5, 120)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.skybox = Skybox()
        self.cube = Cube()
        self.sphere = Sphere()

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

        # Walking speed 
        self.walk_speed = 3

        self.texture_id01 = self.load_texture("/textures/spacesky.webp")
        self.texture_id02 = self.load_texture("/textures/box2.png")
        self.texture_id03 = self.load_texture("/textures/grass.jpg")

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

        # Slide forward, backward
        if self.W_key_down:
            self.view_matrix.slide(0, 0, delta_time * -self.walk_speed)
        if self.S_key_down:
            self.view_matrix.slide(0, 0, delta_time * self.walk_speed)

        # Slide left, right
        if self.D_key_down:
            self.view_matrix.slide(delta_time * self.walk_speed, 0, 0)
        if self.A_key_down:
            self.view_matrix.slide(delta_time * -self.walk_speed, 0, 0)

        # YAW (rotate camera left and right) 
        if self.LEFT_key_down:
            self.view_matrix.yaw(-pi * delta_time)
        if self.RIGHT_key_down:
            self.view_matrix.yaw(pi * delta_time)

    def display(self):
        glEnable(GL_DEPTH_TEST) 
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glViewport(0, 0, 800, 600)

        self.shader.set_view_matrix(self.view_matrix.get_matrix())
        self.shader.set_eye_position(self.view_matrix.eye)
        self.shader.set_light_position(self.view_matrix.eye)
        self.shader.set_light_diffuse(1.0, 1.0, 1.0)
        
        # self.shader.set_light_position(Point(10.0, 1.0, 10.0))
        # self.shader.set_light_diffuse(1.0, 1.0, 1.0)
        # self.shader.set_light_specular(1.0, 1.0, 1.0)

        self.model_matrix.load_identity()
        self.skybox.set_vertices(self.shader)

        glBindTexture(GL_TEXTURE_2D, self.texture_id01)
        self.shader.set_material_diffuse(1.0, 1.0, 1.0)
        # self.shader.set_material_specular(0.1, 0.8, 0.1)
        self.model_matrix.push_matrix()
        self.model_matrix.add_scale(100,100,100)
        # self.model_matrix.add_rotate_y(self.angle * 0.5)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.skybox.draw(self.shader)
        self.model_matrix.pop_matrix()

        glBindTexture(GL_TEXTURE_2D, self.texture_id02)
        self.cube.set_vertices(self.shader)
        self.shader.set_material_diffuse(1.0, 1.0, 1.0)
        # self.shader.set_material_specular(0.1, 0.8, 0.1)
        self.model_matrix.push_matrix()
        # self.model_matrix.add_rotate_x(self.angle * 0.5)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()

        glBindTexture(GL_TEXTURE_2D, self.texture_id03)
        self.cube.set_vertices(self.shader)
        self.shader.set_material_diffuse(1.0, 1.0, 1.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(0,-2,0)
        self.model_matrix.add_scale(50,0.5,50)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()

        pygame.display.flip()

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