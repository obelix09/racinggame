
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

        self.view_matrix_1 = ViewMatrix()
        self.view_matrix_2 = ViewMatrix()
        self.view_matrix_1.look(Point(1, 6, 0), Point(0, 0, 0), Vector(0, 1, 0))
        self.view_matrix_2.look(Point(0, 6, 1), Point(0, 0, 0), Vector(0, 1, 0))

        self.projection_matrix = ProjectionMatrix()
        self.projection_matrix.set_perspective(pi/3, 800/300, 0.5, 500)
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

        # Max speed 
        self.max_speed = 20

        # Racecar 1 variables
        self.car1_pos = Point(0, 1, 0)
        self.car1_motion = Vector(0, 0, 0)
        self.car1_angle = 0
        self.driving_speed1 = 20
        self.turn_speed1 = 160
        self.current_driving_speed1 = 0
        self.current_turn_speed1 = 0
        self.total_turn1 = 0

        # Racecar 2 variables
        self.car2_pos = Point(0, 1, 0)
        self.car2_motion = Vector(0, 0, 0)
        self.car2_angle = 0
        self.driving_speed2 = 2
        self.turn_speed2 = 160
        self.current_driving_speed2 = 0
        self.current_turn_speed2 = 0
        self.total_turn2 = 0

        # Camera variables
        self.distance_from_player = 5
        self.camera_pitch = 150 # Degrees
        self.horizontal_distance = self.distance_from_player * cos(self.camera_pitch)
        self.vertical_distance = self.distance_from_player * sin(self.camera_pitch)
        self.camera1_pos = Point(0, 1, 0)
        self.camera2_pos = Point(0, 1, 0)

        # Textures
        self.texture_id01 = self.load_texture("/textures/spacesky.webp")
        self.texture_id02 = self.load_texture("/textures/box2.png")
        self.texture_id03 = self.load_texture("/textures/grass.jpg")
        self.texture_id04 = self.load_texture("/textures/raindrops.jpg")
    

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

        ########### Car controls 1 ############
        #go left or right
        if (self.LEFT_key_down):
            if(self.current_driving_speed1 > 0):
                self.current_turn_speed1 = self.turn_speed1 * self.current_driving_speed1/20
            elif(self.current_driving_speed1 < 0):
                self.current_turn_speed1 = self.turn_speed1 * self.current_driving_speed1/20 
        elif (self.RIGHT_key_down):
            if(self.current_driving_speed1 > 0):
                self.current_turn_speed1 = -self.turn_speed1 * self.current_driving_speed1/20 
            elif(self.current_driving_speed1 < 0):
                self.current_turn_speed1 = -self.turn_speed1 * self.current_driving_speed1/20
        else:
            self.current_turn_speed1 = 0 
        # go forward
        if self.UP_key_down:
            if (self.current_driving_speed1 < self.max_speed):
                self.current_driving_speed1 += self.driving_speed1 * delta_time
        else: 
            if (not self.DOWN_key_down and self.current_driving_speed1 > 0):
                self.current_driving_speed1 -= self.driving_speed1 * delta_time
        if self.DOWN_key_down:
            if (self.current_driving_speed1 > -self.max_speed):
                self.current_driving_speed1 += -self.driving_speed1 * delta_time
        else: 
            if (not self.DOWN_key_down and self.current_driving_speed1 < 0):
                self.current_driving_speed1 += self.driving_speed1 * delta_time
                
        
        self.total_turn1 += self.current_turn_speed1 * delta_time
        distance = self.current_driving_speed1 * delta_time

        self.car1_pos.x += distance * sin(self.total_turn1 * pi/180)
        self.car1_pos.z += distance  * cos(self.total_turn1 * pi/180)

        # Calculate camera1 position
        self.camera1_pos.x = self.car1_pos.x - (self.horizontal_distance * sin(self.total_turn1 * pi/180))
        self.camera1_pos.y = -(self.car1_pos.y + self.vertical_distance)
        self.camera1_pos.z = self.car1_pos.z - (self.horizontal_distance * cos(self.total_turn1 * pi/180))

       ########### Car controls 2 ############
        #go left or right 
        if (self.A_key_down):
            if(self.W_key_down):
                self.current_turn_speed2 = self.turn_speed2
            elif(self.S_key_down):
                self.current_turn_speed2 = -self.turn_speed2 
        elif (self.D_key_down):
            if(self.W_key_down):
                self.current_turn_speed2 = -self.turn_speed2 
            elif(self.S_key_down):
                self.current_turn_speed2 = self.turn_speed2 
        else:
            self.current_turn_speed2 = 0
        # go forward
        if self.W_key_down:
            self.current_driving_speed2 = self.driving_speed2 
        elif self.S_key_down:
            self.current_driving_speed2 = -self.driving_speed2 
        else:
            self.current_driving_speed2 = 0
        
        self.total_turn2 += self.current_turn_speed2 * delta_time
        distance = self.current_driving_speed2 * delta_time
        self.car2_pos.x += distance * sin(self.total_turn2 * pi/180)
        self.car2_pos.z += distance  * cos(self.total_turn2 * pi/180)

        # Calculate camera2 position
        self.camera2_pos.x = self.car2_pos.x - (self.horizontal_distance * sin(self.total_turn2 * pi/180))
        self.camera2_pos.y = -(self.car2_pos.y + self.vertical_distance)
        self.camera2_pos.z = self.car2_pos.z - (self.horizontal_distance * cos(self.total_turn2 * pi/180))
           

    def displayScreen(self):
        self.shader.set_light_position(Point(4.0, 4.0, 4.0))
        self.shader.set_light_diffuse(1.0, 1.0, 1.0)
        self.shader.set_light_specular(1.0, 1.0, 1.0)
        self.model_matrix.load_identity()

        #Skybox
        self.skybox.set_vertices(self.shader)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id01)
        self.shader.set_diffuce_tex(0)
        self.shader.set_material_diffuse(1.0, 1.0, 1.0)
        self.shader.set_material_specular(0.0, 0.0, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_scale(600,600,600)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.skybox.draw(self.shader)
        self.model_matrix.pop_matrix()

        # Grassboi
        glActiveTexture(GL_TEXTURE0)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glBindTexture(GL_TEXTURE_2D, self.texture_id03)
        self.shader.set_diffuce_tex(0)
        self.cube.set_vertices(self.shader)
        self.shader.set_material_diffuse(1.0, 1.0, 1.0)
        self.shader.set_material_specular(0.0, 0.0, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(0,-2,0)
        self.model_matrix.add_scale(50,0.5,50)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # Racecar 1
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id02)
        self.shader.set_diffuce_tex(0)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id04)
        self.shader.set_specular_tex(1)
        self.cube.set_vertices(self.shader)
        self.shader.set_material_diffuse(1.0, 1.0, 1.0, 0.5)
        self.shader.set_material_specular(1.0, 1.0, 1.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(self.car1_pos.x, 0, self.car1_pos.z)
        self.model_matrix.add_rotate_y(self.total_turn1 * pi/180)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()

        # Racecar 2
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id02)
        self.shader.set_diffuce_tex(0)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id04)
        self.shader.set_specular_tex(1)
        self.cube.set_vertices(self.shader)
        self.shader.set_material_diffuse(1.0, 1.0, 1.0, 0.5)
        self.shader.set_material_specular(1.0, 1.0, 1.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(self.car2_pos.x, 0, self.car2_pos.z)
        self.model_matrix.add_rotate_y(self.total_turn2 * pi/180)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()
        
        glDisable(GL_BLEND)

    def display(self):
        glEnable(GL_DEPTH_TEST)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        self.view_matrix_1.look(self.camera1_pos, self.car1_pos, Vector(0, 1, 0))
        self.shader.set_view_matrix(self.view_matrix_1.get_matrix())
        glViewport(0, 0, 800, 300)
        self.displayScreen()

        self.view_matrix_2.look(self.camera2_pos, self.car2_pos, Vector(0, 1, 0))
        self.shader.set_view_matrix(self.view_matrix_2.get_matrix())
        glViewport(0, 300, 800, 300)
        self.displayScreen()
        
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