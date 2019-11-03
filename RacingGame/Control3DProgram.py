
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
        self.screen = pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)

        self.shader = Shader3D()
        self.shader.use()

        self.model_matrix = ModelMatrix()
        self.view_matrix_1 = ViewMatrix()
        self.view_matrix_2 = ViewMatrix()

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

        # Shared racecar variables
        self.max_speed = 20
        self.acceleration = 10
        self.turn_speed = 160
        
        # Sound
        # pygame.mixer.music.play()
        pygame.mixer.music.load('./sounds/ghostBusters.mp3')
        # pygame.display.set_caption('Ghostboxters')

        # Collision coordinates outer racetrack circle 
        self.outer_collision_points = []

        # Collision coordinates inner racetrack circle 
        self.inner_collision_points = []

        # model matrix
        self.goal_collision_points = []

        # Goal line
        self.goal_line = 0

        # Camera variables
        self.distance_from_player = 5
        self.camera_pitch = 150 # Degrees
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
        self.texture_id10 = self.load_texture("/textures/redLight.jpg")
        self.texture_id11 = self.load_texture("/textures/yellowLight.jpg")
        self.texture_id12 = self.load_texture("/textures/greenLight.jpg")

        self.resetGame()

    def resetGame(self):
        pygame.mixer.music.load(sys.path[0] + '/sounds/ghostBusters.mp3')
        pygame.mixer.music.play()
        # Timer
        self.start_ticks = pygame.time.get_ticks()
        self.endTime = 0
        # Racecar 1 variables
        self.car1_pos = Point(26, 1, 3)
        self.car1_motion = Vector(0, 0, 0)
        self.car1_angle = 0
        self.current_driving_speed1 = 0
        self.current_turn_speed1 = 0
        self.total_turn1 = 0
        self.round1 = 0
        self.car1_real_motion = Vector(0,0,0)
        # model matrix for car1
        self.model_matrix_car1 = 0
        # Collision coordinates car1
        self.car1_collision_points = []

        # Racecar 2 variables
        self.car2_pos = Point(22, 1, 3)
        self.car2_motion = Vector(0, 0, 0)
        self.car2_angle = 0
        self.current_driving_speed2 = 0
        self.current_turn_speed2 = 0
        self.total_turn2 = 0
        self.round2 = 0
        self.car2_real_motion = Vector(0,0,0)
        # model matrix for car2
        self.model_matrix_car2 = 0
        # Collision coordinates car2
        self.car2_collision_points = []

        # Racecar 1 Movement keys
        self.W_key_down = False
        self.S_key_down = False
        self.A_key_down = False
        self.D_key_down = False

        # Racecar 2 Movement keys
        self.UP_key_down = False
        self.DOWN_key_down = False
        self.LEFT_key_down = False
        self.RIGHT_key_down = False


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
    
    def detectBorderCollision(self, delta_time):
        length = len(self.outer_collision_points)
        for i in range(length):
            if (i == length-1):
                line = Line(self.outer_collision_points[i], self.outer_collision_points[0])
            else:
                line = Line(self.outer_collision_points[i], self.outer_collision_points[i+1])
            for point in self.car1_collision_points: 
                p_hit = line.detect_collision(point, self.car1_real_motion, delta_time)
                if p_hit:
                    self.new_motion = Vector(line.point_2.x - line.point_1.x, line.point_2.y - line.point_1.y, line.point_2.z - line.point_1.z) * delta_time
                    self.car1_pos -= self.car1_motion * delta_time
                    self.car1_pos += self.new_motion * self.current_driving_speed1 * delta_time
                    break
            for point in self.car2_collision_points: 
                p_hit = line.detect_collision(point, self.car2_real_motion, delta_time)
                if p_hit:
                    self.new_motion = Vector(line.point_2.x - line.point_1.x, line.point_2.y - line.point_1.y, line.point_2.z - line.point_1.z) * delta_time
                    self.car2_pos -= self.car2_motion * delta_time
                    self.car2_pos += self.new_motion * self.current_driving_speed2 * delta_time
                    break

        
        length = len(self.inner_collision_points)
        for i in range(length):
            if (i == length-1):
                line = Line(self.inner_collision_points[i], self.inner_collision_points[1])
            else:
                line = Line(self.inner_collision_points[i], self.inner_collision_points[i+1])
            for point in self.car1_collision_points: 
                p_hit = line.detect_collision(point, self.car1_real_motion, delta_time)
                if p_hit:
                    self.new_motion = Vector(line.point_2.x - line.point_1.x, line.point_2.y - line.point_1.y, line.point_2.z - line.point_1.z) * delta_time
                    self.car1_pos -= self.car1_motion * delta_time
                    self.car1_pos += self.new_motion * self.current_driving_speed1 * delta_time
                    break
            for point in self.car2_collision_points: 
                p_hit = line.detect_collision(point, self.car2_real_motion, delta_time)
                if p_hit:
                    self.new_motion = Vector(line.point_2.x - line.point_1.x, line.point_2.y - line.point_1.y, line.point_2.z - line.point_1.z) * delta_time
                    self.car2_pos -= self.car2_motion * delta_time
                    self.car2_pos += self.new_motion * self.current_driving_speed2 * delta_time
                    break


    def detectCarCollision(self, delta_time):
        # check collision for car1
        for point in self.car1_collision_points:
            lines = []
            lines.append(Line(self.car2_collision_points[0], self.car2_collision_points[1]))
            lines.append(Line(self.car2_collision_points[1], self.car2_collision_points[2]))
            lines.append(Line(self.car2_collision_points[2], self.car2_collision_points[3]))
            lines.append(Line(self.car2_collision_points[3], self.car2_collision_points[0]))
            for line in lines:
                p_hit = line.detect_collision(point, self.car1_real_motion, delta_time)
                if p_hit:
                    self.new_motion = Vector(line.point_2.x - line.point_1.x, line.point_2.y - line.point_1.y, line.point_2.z - line.point_1.z) * delta_time
                    self.car1_pos -= self.car1_motion * delta_time
                    self.car1_pos += self.new_motion * delta_time * self.current_driving_speed1
                    break
        
        # check collision for car2
        for point in self.car2_collision_points:
            lines = []
            lines.append(Line(self.car1_collision_points[0], self.car1_collision_points[1]))
            lines.append(Line(self.car1_collision_points[1], self.car1_collision_points[2]))
            lines.append(Line(self.car1_collision_points[2], self.car1_collision_points[3]))
            lines.append(Line(self.car1_collision_points[3], self.car1_collision_points[0]))
            for line in lines:
                p_hit = line.detect_collision(point, self.car2_real_motion, delta_time)
                if p_hit:
                    self.new_motion = Vector(line.point_2.x - line.point_1.x, line.point_2.y - line.point_1.y, line.point_2.z - line.point_1.z) * delta_time
                    self.car2_pos -= self.car2_motion * delta_time
                    self.car2_pos += self.new_motion * self.current_driving_speed2 * delta_time
                    break

    def detectGoal(self, delta_time):
        car1_real_pos = self.racecar.get_global_point(self.car1_pos, self.model_matrix_car1)
        car2_real_pos = self.racecar.get_global_point(self.car2_pos, self.model_matrix_car2)

        # check car 1 
        p_hit = self.goal_line.detect_collision(car1_real_pos, self.car1_real_motion, delta_time)
        if p_hit:
            print("Racecar 1 collision detection")
            self.round1 += 1
            if (self.round1 == 3): 
                pygame.mixer.music.load(sys.path[0] + '/sounds/winner.mp3')
                pygame.mixer.music.play()
                print("Racecar 1 wins")
                self.endTime = self.timer + 5
                
        # Check car 2
        p_hit = self.goal_line.detect_collision(car2_real_pos, self.car2_real_motion, delta_time)
        if p_hit:
            print("Racecar 2 collision detection")
            self.round2 += 1
            if (self.round2 == 3): 
                pygame.mixer.music.load(sys.path[0] + '/sounds/winner.mp3')
                pygame.mixer.music.play()
                print("Racecar 2 wins")
                self.endTime = self.timer + 5


    def update(self):
        self.timer = ((pygame.time.get_ticks() - self.start_ticks) / 1000)
        delta_time = self.clock.tick() / 1000.0

        # Check if game has ended (someone won)
        if (self.endTime != 0 and self.timer >= self.endTime):
            self.resetGame()

        if(13 < self.timer):
            ########### Car controls 1 ############
            #go left or right
            if (self.LEFT_key_down):
                if(self.current_driving_speed1 > 0):
                    self.current_turn_speed1 = self.turn_speed * self.current_driving_speed1/20
                elif(self.current_driving_speed1 < 0):
                    self.current_turn_speed1 = self.turn_speed * self.current_driving_speed1/20 
            elif (self.RIGHT_key_down):
                if(self.current_driving_speed1 > 0):
                    self.current_turn_speed1 = -self.turn_speed * self.current_driving_speed1/20 
                elif(self.current_driving_speed1 < 0):
                    self.current_turn_speed1 = -self.turn_speed * self.current_driving_speed1/20
            else:
                self.current_turn_speed1 = 0 
            # go forward
            if self.UP_key_down:
                if (self.current_driving_speed1 < self.max_speed):
                    self.current_driving_speed1 += self.acceleration * delta_time
            else: 
                if (not self.DOWN_key_down and self.current_driving_speed1 > 0):
                    self.current_driving_speed1 -= self.acceleration * delta_time
            if self.DOWN_key_down:
                if (self.current_driving_speed1 > -self.max_speed):
                    self.current_driving_speed1 += -self.acceleration * delta_time
            else: 
                if (not self.UP_key_down and self.current_driving_speed1 < 0):
                    self.current_driving_speed1 += self.acceleration * delta_time
                    
            self.total_turn1 += self.current_turn_speed1 * delta_time
            distance = self.current_driving_speed1 

            self.car1_motion.x = distance * sin(self.total_turn1 * pi/180)
            self.car1_motion.z = distance * cos(self.total_turn1 * pi/180)
            self.car1_pos += self.car1_motion * delta_time

        ########### Car controls 2 ############
            #go left or right
            if (self.A_key_down):
                if(self.current_driving_speed2 > 0):
                    self.current_turn_speed2 = self.turn_speed * self.current_driving_speed2/20
                elif(self.current_driving_speed2 < 0):
                    self.current_turn_speed2 = self.turn_speed * self.current_driving_speed2/20 
            elif (self.D_key_down):
                if(self.current_driving_speed2 > 0):
                    self.current_turn_speed2 = -self.turn_speed * self.current_driving_speed2/20 
                elif(self.current_driving_speed2 < 0):
                    self.current_turn_speed2 = -self.turn_speed * self.current_driving_speed2/20
            else:
                self.current_turn_speed2 = 0 
            # go forward
            if self.W_key_down:
                if (self.current_driving_speed2 < self.max_speed):
                    self.current_driving_speed2 += self.acceleration * delta_time
            else: 
                if (not self.S_key_down and self.current_driving_speed2 > 0):
                    self.current_driving_speed2 -= self.acceleration * delta_time
            if self.S_key_down:
                if (self.current_driving_speed2 > -self.max_speed):
                    self.current_driving_speed2 += -self.acceleration * delta_time
            else: 
                if (not self.W_key_down and self.current_driving_speed2 < 0):
                    self.current_driving_speed2 += self.acceleration * delta_time
                    
            self.total_turn2 += self.current_turn_speed2 * delta_time
            distance = self.current_driving_speed2

            self.car2_motion.x = distance * sin(self.total_turn2 * pi/180)
            self.car2_motion.z = distance * cos(self.total_turn2 * pi/180)
            self.car2_pos += self.car2_motion * delta_time
            if (self.model_matrix_car1 != 0 and self.model_matrix_car2 != 0):
                # Detect collision between cars
                self.car1_real_motion = self.racecar.get_global_vector(self.car1_motion, self.model_matrix_car1)
                self.car2_real_motion = self.racecar.get_global_vector(self.car2_motion, self.model_matrix_car2)
                self.car1_collision_points = self.racecar.get_collision_points(self.model_matrix_car1)
                self.car2_collision_points = self.racecar.get_collision_points(self.model_matrix_car2)
                self.detectCarCollision(delta_time) 
            
                # Detect collision on racetrack boarders
                self.detectBorderCollision(delta_time)
                # Detect goal collision
                self.detectGoal(delta_time)

        # Calculate camera1 position
        self.camera1_pos.x = self.car1_pos.x - (self.horizontal_distance * sin(self.total_turn1 * pi/180))
        self.camera1_pos.y = -(self.car1_pos.y + self.vertical_distance)
        self.camera1_pos.z = self.car1_pos.z - (self.horizontal_distance * cos(self.total_turn1 * pi/180))

        # Calculate camera2 position
        self.camera2_pos.x = self.car2_pos.x - (self.horizontal_distance * sin(self.total_turn2 * pi/180))
        self.camera2_pos.y = -(self.car2_pos.y + self.vertical_distance)
        self.camera2_pos.z = self.car2_pos.z - (self.horizontal_distance * cos(self.total_turn2 * pi/180))

    def displayScreen(self):

        # Setting up the light positions:
        # Every object has the same specular and ambient for their material
        self.shader.set_light_ambient(0.3, 0.3, 0.3)
        self.shader.set_material_ambient(0.3, 0.3, 0.3)
        self.shader.set_material_diffuse(1.0, 1.0, 1.0)
        self.shader.set_material_specular(0.0, 0.0, 0.0)
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
        self.model_matrix.push_matrix()
        self.model_matrix.add_scale(400,0.5,400)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()

        self.circle_2D.set_vertices(self.shader)
        # Outer boarder
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id08)
        self.shader.set_diffuce_tex(0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(0.5, 0.4, 0.8)
        self.model_matrix.add_scale(2.1, 0.5, 4.1)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        if (self.outer_collision_points == []):
            self.outer_collision_points = self.circle_2D.get_collision_points(self.model_matrix.matrix)
        self.circle_2D.draw(self.shader)
        self.model_matrix.pop_matrix()

        # Track
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id05)
        self.shader.set_diffuce_tex(0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(0.5, 0.5, 0.8)
        self.model_matrix.add_scale(2, 0.5, 4)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.circle_2D.draw(self.shader)
        self.model_matrix.pop_matrix()

        # Inner boarder
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id08)
        self.shader.set_diffuce_tex(0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(0.5, 0.6, 0.8)
        self.model_matrix.add_scale(1.1, 0.5, 3.1)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        if (self.inner_collision_points == []):
            self.inner_collision_points = self.circle_2D.get_collision_points(self.model_matrix.matrix)
        self.circle_2D.draw(self.shader)
        self.model_matrix.pop_matrix()

        # Inner boarder with grass 
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id03)
        self.shader.set_diffuce_tex(0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(0.5, 0.7, 0.8)
        self.model_matrix.add_scale(1, 0.5, 3)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.circle_2D.draw(self.shader)
        self.model_matrix.pop_matrix()

        # Goal
        glActiveTexture(GL_TEXTURE0)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glBindTexture(GL_TEXTURE_2D, self.texture_id09)
        self.shader.set_diffuce_tex(0)
        self.cube_2D.set_vertices(self.shader)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(23.4, 0.4, 0.8)
        self.model_matrix.add_scale(13.4, 0.5, 1)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        if (self.goal_line == 0):
            goal_collision_points = self.cube_2D.get_collision_points(self.model_matrix.matrix)
            self.goal_line = Line(goal_collision_points[0], goal_collision_points[1])
        self.cube_2D.draw(self.shader)
        self.model_matrix.pop_matrix()

        #Racecars
        self.shader.set_material_diffuse(1.0, 1.0, 1.0)
        self.shader.set_material_specular(1.0, 1.0, 1.0)
        self.racecar.set_vertices(self.shader)

        # Racecar 1
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id06)
        self.shader.set_diffuce_tex(0)
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
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(self.car2_pos.x, 1, self.car2_pos.z)
        self.model_matrix.add_rotate_y(self.total_turn2 * pi/180)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.model_matrix_car2 = self.model_matrix.matrix
        self.racecar.draw(self.shader)
        self.model_matrix.pop_matrix()

        # Popup start light
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.cube.set_vertices(self.shader)
        self.shader.set_material_diffuse(1.0, 1.0, 1.0, 0.5)
        if(self.timer < 8):
            getReadyTexture = self.texture_id10
        elif(8 < self.timer and self.timer < 13):
            getReadyTexture = self.texture_id11
        else:
            getReadyTexture = self.texture_id12
        if (self.timer < 15):
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, getReadyTexture)
            self.shader.set_diffuce_tex(0)
            self.model_matrix.push_matrix()
            self.model_matrix.add_translation(23.4, 1, 6)
            self.model_matrix.add_scale(10, 5, 2)
            self.shader.set_model_matrix(self.model_matrix.matrix)
            self.cube.draw(self.shader)
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