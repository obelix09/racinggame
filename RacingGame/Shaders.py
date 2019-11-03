
from OpenGL.GL import *
from math import * # trigonometry

import sys

from Base3DObjects import *

class Shader3D:
    def __init__(self):
        vert_shader = glCreateShader(GL_VERTEX_SHADER)
        shader_file = open(sys.path[0] + "/simple3D.vert")
        glShaderSource(vert_shader,shader_file.read())
        shader_file.close()
        glCompileShader(vert_shader)
        result = glGetShaderiv(vert_shader, GL_COMPILE_STATUS)
        if (result != 1): # shader didn't compile
            print("Couldn't compile vertex shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(vert_shader)))

        frag_shader = glCreateShader(GL_FRAGMENT_SHADER)
        shader_file = open(sys.path[0] + "/simple3D.frag")
        glShaderSource(frag_shader,shader_file.read())
        shader_file.close()
        glCompileShader(frag_shader)
        result = glGetShaderiv(frag_shader, GL_COMPILE_STATUS)
        if (result != 1): # shader didn't compile
            print("Couldn't compile fragment shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(frag_shader)))

        self.renderingProgramID = glCreateProgram()
        glAttachShader(self.renderingProgramID, vert_shader)
        glAttachShader(self.renderingProgramID, frag_shader)
        glLinkProgram(self.renderingProgramID)

        self.positionLoc			= glGetAttribLocation(self.renderingProgramID, "a_position")
        glEnableVertexAttribArray(self.positionLoc)

        self.normalLoc			= glGetAttribLocation(self.renderingProgramID, "a_normal")
        glEnableVertexAttribArray(self.normalLoc)

        self.uvLoc			= glGetAttribLocation(self.renderingProgramID, "a_uv")
        glEnableVertexAttribArray(self.uvLoc)

        self.modelMatrixLoc			= glGetUniformLocation(self.renderingProgramID, "u_model_matrix")
        self.viewMatrixLoc			= glGetUniformLocation(self.renderingProgramID, "u_view_matrix")
        self.projectionMatrixLoc			= glGetUniformLocation(self.renderingProgramID, "u_projection_matrix")

        self.eyePosLoc                 = glGetUniformLocation(self.renderingProgramID, "u_eye_position")
        # Each light position
        self.light1PosLoc               = glGetUniformLocation(self.renderingProgramID, "u_light_1_position")
        self.light1DiffuseLoc           = glGetUniformLocation(self.renderingProgramID, "u_light_1_diffuse")
        self.light1SpecularLoc          = glGetUniformLocation(self.renderingProgramID, "u_light_1_specular")
        self.light2PosLoc               = glGetUniformLocation(self.renderingProgramID, "u_light_2_position")
        self.light2DiffuseLoc           = glGetUniformLocation(self.renderingProgramID, "u_light_2_diffuse")
        self.light2SpecularLoc          = glGetUniformLocation(self.renderingProgramID, "u_light_2_specular")
        self.light3PosLoc               = glGetUniformLocation(self.renderingProgramID, "u_light_3_position")
        self.light3DiffuseLoc           = glGetUniformLocation(self.renderingProgramID, "u_light_3_diffuse")
        self.light3SpecularLoc          = glGetUniformLocation(self.renderingProgramID, "u_light_3_specular")
        # Material and global cordinates
        self.materialDiffuseLoc        = glGetUniformLocation(self.renderingProgramID, "u_mat_diffuse")
        self.materialSpecularLoc       = glGetUniformLocation(self.renderingProgramID, "u_mat_specular")
        self.materialShininessLoc      = glGetUniformLocation(self.renderingProgramID, "u_mat_shininess")
        self.materialAmbientLoc       = glGetUniformLocation(self.renderingProgramID, "u_mat_ambient")
        self.lightAmbientLoc           = glGetUniformLocation(self.renderingProgramID, "u_light_ambient")

        # texture stuff
        self.diffuseTextureLoc = glGetUniformLocation(self.renderingProgramID, "u_diffuse_texture")
        self.specularTextureLoc = glGetUniformLocation(self.renderingProgramID, "u_specular_texture")

    def use(self):
        try:
            glUseProgram(self.renderingProgramID)   
        except OpenGL.error.GLError:
            print(glGetProgramInfoLog(self.renderingProgramID))
            raise

    def set_model_matrix(self, matrix_array):
        glUniformMatrix4fv(self.modelMatrixLoc, 1, True, matrix_array)

    def set_view_matrix(self, matrix_array):
        glUniformMatrix4fv(self.viewMatrixLoc, 1, True, matrix_array)
    
    def set_projection_matrix(self, matrix_array):
        glUniformMatrix4fv(self.projectionMatrixLoc, 1, True, matrix_array)

    def set_position_attribute(self, vertex_array):
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 0, vertex_array)

    def set_normal_attribute(self, vertex_array):
        glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 0, vertex_array)

    def set_uv_attribute(self, vertex_array):
        glVertexAttribPointer(self.uvLoc, 2, GL_FLOAT, False, 0, vertex_array)

    def set_eye_position(self, pos):
        glUniform4f(self.eyePosLoc, pos.x, pos.y, pos.z, 1.0)
    
    def set_light_1_position(self, pos):
        glUniform4f(self.light1PosLoc, pos.x, pos.y, pos.z, 1.0)
    
    def set_light_1_diffuse(self, red, green, blue):
        glUniform4f(self.light1DiffuseLoc, red, green, blue, 1.0)
    
    def set_light_1_specular(self, red, green, blue):
        glUniform4f(self.light1SpecularLoc, red, green, blue, 1.0)

    def set_light_2_position(self, pos):
        glUniform4f(self.light2PosLoc, pos.x, pos.y, pos.z, 1.0)
    
    def set_light_2_diffuse(self, red, green, blue):
        glUniform4f(self.light2DiffuseLoc, red, green, blue, 1.0)
    
    def set_light_2_specular(self, red, green, blue):
        glUniform4f(self.light2SpecularLoc, red, green, blue, 1.0)

    def set_light_3_position(self, pos):
        glUniform4f(self.light3PosLoc, pos.x, pos.y, pos.z, 1.0)
    
    def set_light_3_diffuse(self, red, green, blue):
        glUniform4f(self.light3DiffuseLoc, red, green, blue, 1.0)
    
    def set_light_3_specular(self, red, green, blue):
        glUniform4f(self.light3SpecularLoc, red, green, blue, 1.0)
    
    def set_material_diffuse(self, red, green, blue, alpha=1.0):
        glUniform4f(self.materialDiffuseLoc, red, green, blue, alpha)
    
    def set_material_shininess(self, shininess):
        glUniform1f(self.materialShininessLoc, shininess)
    
    def set_material_specular(self, red, green, blue):
        glUniform4f(self.materialSpecularLoc, red, green, blue, 1.0)

    def set_light_ambient(self, red, green, blue):
        glUniform4f(self.lightAmbientLoc, red, green, blue, 1.0)

    def set_material_ambient(self, red, green, blue):
        glUniform4f(self.materialAmbientLoc, red, green, blue, 1.0)
    
    def set_diffuce_tex(self, number):
        glUniform1i(self.diffuseTextureLoc, number)

    def set_specular_tex(self, number):
        glUniform1i(self.specularTextureLoc, number)