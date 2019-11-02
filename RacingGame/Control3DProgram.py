
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
        self.circle_2D = Circle_2D(0, 0, 0)
        self.cube = Cube()
        self.cube_2D = Cube_2D()
        self.racecar = Racecar()
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

        # model matrix for car1
        self.model_matrix_car1 = 0
        # Collision coordinates car1
        self.car1_collision_points = []

        # Racecar 2 variables
        self.car2_pos = Point(0, 1, 0)
        self.car2_motion = Vector(0, 0, 0)
        self.car2_angle = 0
        self.driving_speed2 = 20
        self.turn_speed2 = 160
        self.current_driving_speed2 = 0
        self.current_turn_speed2 = 0
        self.total_turn2 = 0

        # model matrix for car1
        self.model_matrix_car2 = 0
        # Collision coordinates car1
        self.car2_collision_points = []

        # Camera variables
        self.distance_from_player = 5
        self.camera_pitch = 250 # Degrees
        self.horizontal_distance = self.distance_from_player * cos(self.camera_pitch)
        self.vertical_distance = self.distance_from_player * sin(self.camera_pitch)
        self.camera1_pos = Point(0, 1, 0)
        self.camera2_pos = Point(0, 1, 0)

        # Textures
        self.texture_id01 = self.load_texture("/textures/spacesky.webp")
        self.texture_id03 = self.load_texture("/textures/grass.jpg")
        self.texture_id05 = self.load_texture("/textures/concrete.jpg")
        self.texture_id06 = self.load_texture("/textures/blue.jpg")
        self.texture_id07 = self.load_texture("/textures/red.jpg")
        self.texture_id08 = self.load_texture("/textures/boarder.jpg")
        self.texture_id09 = self.load_texture("/textures/goal.jpg")


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
    
    def detectCarCollision(self):
        # self.car1_collision_points
        # self.car2_collision_points
        car1_collision = False
        car2_collision = False

        # Check collision on car1
        for point1 in self.car1_collision_points:
            # If point in car1 is between car2-minX and car2-maxX and between car2-minZ and car2-maxZ = collision
            if (point1.x >= self.car2_collision_points[0].x and point1.x <= self.car2_collision_points[3].x):
                if (point1.z >= self.car2_collision_points[0].z and point1.z <= self.car2_collision_points[3].z):
                    car1_collision = True
                    print("YAY1")
        
        # Check collision on car2
        for point2 in self.car2_collision_points:
            # If point in car1 is between car1-minX and car1-maxX and between car1-minZ and car1-maxZ = collision
            if (point2.x >= self.car1_collision_points[0].x and point2.x <= self.car1_collision_points[3].x):
                if (point2.z >= self.car1_collision_points[0].z and point2.z <= self.car1_collision_points[3].z):
                    car2_collision = True
                    print("YAY2")
     
        if (not car1_collision and not car2_collision):
            print("NO")


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
        self.car1_pos.z += distance * cos(self.total_turn1 * pi/180)

        # Calculate camera1 position
        self.camera1_pos.x = self.car1_pos.x - (self.horizontal_distance * sin(self.total_turn1 * pi/180))
        self.camera1_pos.y = -(self.car1_pos.y + self.vertical_distance)
        self.camera1_pos.z = self.car1_pos.z - (self.horizontal_distance * cos(self.total_turn1 * pi/180))

       ########### Car controls 2 ############
        #go left or right
        if (self.A_key_down):
            if(self.current_driving_speed2 > 0):
                self.current_turn_speed2 = self.turn_speed2 * self.current_driving_speed2/20
            elif(self.current_driving_speed2 < 0):
                self.current_turn_speed2 = self.turn_speed2 * self.current_driving_speed2/20 
        elif (self.D_key_down):
            if(self.current_driving_speed2 > 0):
                self.current_turn_speed2 = -self.turn_speed2 * self.current_driving_speed2/20 
            elif(self.current_driving_speed2 < 0):
                self.current_turn_speed2 = -self.turn_speed2 * self.current_driving_speed2/20
        else:
            self.current_turn_speed2 = 0 
        # go forward
        if self.W_key_down:
            if (self.current_driving_speed2 < self.max_speed):
                self.current_driving_speed2 += self.driving_speed2 * delta_time
        else: 
            if (not self.S_key_down and self.current_driving_speed2 > 0):
                self.current_driving_speed2 -= self.driving_speed2 * delta_time
        if self.S_key_down:
            if (self.current_driving_speed2 > -self.max_speed):
                self.current_driving_speed2 += -self.driving_speed2 * delta_time
        else: 
            if (not self.S_key_down and self.current_driving_speed2 < 0):
                self.current_driving_speed2 += self.driving_speed2 * delta_time
                
        self.total_turn2 += self.current_turn_speed2 * delta_time
        distance = self.current_driving_speed2 * delta_time

        self.car2_pos.x += distance * sin(self.total_turn2 * pi/180)
        self.car2_pos.z += distance * cos(self.total_turn2 * pi/180)

        # Calculate camera2 position
        self.camera2_pos.x = self.car2_pos.x - (self.horizontal_distance * sin(self.total_turn2 * pi/180))
        self.camera2_pos.y = -(self.car2_pos.y + self.vertical_distance)
        self.camera2_pos.z = self.car2_pos.z - (self.horizontal_distance * cos(self.total_turn2 * pi/180))

        # Detect collision between cars
        if (self.model_matrix_car1 != 0):
            self.car1_collision_points = self.racecar.get_collision_points(self.model_matrix_car1)
            self.car2_collision_points = self.racecar.get_collision_points(self.model_matrix_car2)
            self.detectCarCollision()
           

    def displayScreen(self):
        # Setting up the light positions:
        # Every object has the same specular and ambient for their material
        self.shader.set_light_ambient(0.3, 0.3, 0.3)
        self.shader.set_material_ambient(0.3, 0.3, 0.3)
        self.shader.set_material_specular(0.4, 0.4, 0.4)
        self.shader.set_material_shininess(15)

        # Light 1 (Racer 1):
        self.shader.set_light_1_position(self.view_matrix_1.eye)
        self.shader.set_light_1_diffuse(0.4, 0.4, 0.4)
        self.shader.set_light_1_specular(0.4, 0.4, 0.4)

        # Light 2 (Racer 2):
        self.shader.set_light_2_position(self.view_matrix_2.eye)
        self.shader.set_light_2_diffuse(0.4, 0.4, 0.4)
        self.shader.set_light_2_specular(0.4, 0.4, 0.4)
        
        # Light 3:
        self.shader.set_light_3_position(Point(4.0, 4.0, 4.0))
        self.shader.set_light_3_diffuse(1.0, 1.0, 1.0)
        self.shader.set_light_3_specular(1.0, 1.0, 1.0)
        
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
        self.model_matrix.add_scale(600,0.5,600)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()

        # Outer boarder
        glActiveTexture(GL_TEXTURE0)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glBindTexture(GL_TEXTURE_2D, self.texture_id08)
        self.shader.set_diffuce_tex(0)
        self.circle_2D.set_vertices(self.shader)
        self.shader.set_material_diffuse(1.0, 1.0, 1.0)
        self.shader.set_material_specular(0.0, 0.0, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(0.5, 0.4, 0.8)
        self.model_matrix.add_scale(2.1, 0.5, 4.1)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.circle_2D.draw(self.shader)
        self.model_matrix.pop_matrix()

        # Track
        glActiveTexture(GL_TEXTURE0)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glBindTexture(GL_TEXTURE_2D, self.texture_id05)
        self.shader.set_diffuce_tex(0)
        self.circle_2D.set_vertices(self.shader)
        self.shader.set_material_diffuse(1.0, 1.0, 1.0)
        self.shader.set_material_specular(0.0, 0.0, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(0.5, 0.5, 0.8)
        self.model_matrix.add_scale(2, 0.5, 4)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.circle_2D.draw(self.shader)
        self.model_matrix.pop_matrix()

        # Goal
        glActiveTexture(GL_TEXTURE0)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glBindTexture(GL_TEXTURE_2D, self.texture_id09)
        self.shader.set_diffuce_tex(0)
        self.cube_2D.set_vertices(self.shader)
        self.shader.set_material_diffuse(1.0, 1.0, 1.0)
        self.shader.set_material_specular(0.0, 0.0, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(23.4, 0.4, 0.8)
        self.model_matrix.add_scale(13.4, 0.5, 1)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube_2D.draw(self.shader)
        self.model_matrix.pop_matrix()

        # Inner boarder
        glActiveTexture(GL_TEXTURE0)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glBindTexture(GL_TEXTURE_2D, self.texture_id08)
        self.shader.set_diffuce_tex(0)
        self.circle_2D.set_vertices(self.shader)
        self.shader.set_material_diffuse(1.0, 1.0, 1.0)
        self.shader.set_material_specular(0.0, 0.0, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(0.5, 0.6, 0.8)
        self.model_matrix.add_scale(1.1, 0.5, 3.1)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.circle_2D.draw(self.shader)
        self.model_matrix.pop_matrix()

        # Inner boarder with grass or smallerTrack
        glActiveTexture(GL_TEXTURE0)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glBindTexture(GL_TEXTURE_2D, self.texture_id03)
        self.shader.set_diffuce_tex(0)
        self.circle_2D.set_vertices(self.shader)
        self.shader.set_material_diffuse(1.0, 1.0, 1.0)
        self.shader.set_material_specular(0.0, 0.0, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(0.5, 0.7, 0.8)
        self.model_matrix.add_scale(1, 0.5, 3)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.circle_2D.draw(self.shader)
        self.model_matrix.pop_matrix()

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Racecar 1
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id06)
        self.shader.set_diffuce_tex(0)
        self.racecar.set_vertices(self.shader)
        self.shader.set_material_diffuse(1.0, 1.0, 1.0, 0.5)
        self.shader.set_material_specular(1.0, 1.0, 1.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(self.car1_pos.x, 1, self.car1_pos.z)
        self.model_matrix.add_rotate_y(self.total_turn1 * pi/180)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.model_matrix_car1 = self.model_matrix.matrix
        self.racecar.draw(self.shader)
        self.model_matrix.pop_matrix()

        # Racecar 2
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id07)
        self.shader.set_diffuce_tex(0)
        self.racecar.set_vertices(self.shader)
        self.shader.set_material_diffuse(1.0, 1.0, 1.0, 0.5)
        self.shader.set_material_specular(1.0, 1.0, 1.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(self.car2_pos.x, 1, self.car2_pos.z)
        self.model_matrix.add_rotate_y(self.total_turn2 * pi/180)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.model_matrix_car2 = self.model_matrix.matrix
        self.racecar.draw(self.shader)
        self.model_matrix.pop_matrix()

        glDisable(GL_BLEND)

    def display(self):
        glEnable(GL_DEPTH_TEST)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        # Player 1 camera
        self.view_matrix_1.look(self.camera1_pos, self.car1_pos, Vector(0, 1, 0))
        self.shader.set_view_matrix(self.view_matrix_1.get_matrix())
        glViewport(0, 0, 800, 300)
        self.displayScreen()

        # Player 2 camera
        self.view_matrix_2.look(self.camera2_pos, self.car2_pos, Vector(0, 1, 0))
        self.shader.set_view_matrix(self.view_matrix_2.get_matrix())
        glViewport(0, 300, 800, 300)
        self.displayScreen()

        pygame.display.flip()

    # def goalEntered(self):
    #     temp_ang = 0
    #     while temp_ang < 2 * pi:
    #         x1 = self.view_matrix_1.eye.x + self.collision_radius * cos(temp_ang)
    #         y1 = self.view_matrix_1.eye.y
    #         z1 = self.view_matrix_1.eye.z + self.collision_radius * sin(temp_ang)
    #         x2 = self.view_matrix_2.eye.x + self.collision_radius * cos(temp_ang)
    #         y2 = self.view_matrix_2.eye.y
    #         z2 = self.view_matrix_2.eye.z + self.collision_radius * sin(temp_ang)
    #         temp_ang += (pi * 2)/16
    #         point1 = Point(x1, y1, z1) 
    #         point2 = Point(x2, y2, z2) 
    #         if point1.x >= self.cube_collision_points[0] and point1.x <= self.cube_collision_points[1] or point2.x >= self.cube_collision_points[0] and point2.x <= self.cube_collision_points[1]:
    #                 if point.z >= self.cube_collision_points[2] and point.z <= self.cube_collision_points[3] or point.z >= self.cube_collision_points[2] and point.z <= self.cube_collision_points[3]:
    #                     self.view_matrix_1.look(Point(0, 0, 3), Point(0, 0, 0), Vector(0, 1, 0))
    #                     self.view_matrix_2.look(Point(0, 0, 3), Point(0, 0, 0), Vector(0, 1, 0))

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