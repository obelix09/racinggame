// For the object
attribute vec3 a_position;
attribute vec3 a_normal;
attribute vec2 a_uv;

uniform mat4 u_model_matrix;
uniform mat4 u_view_matrix;
uniform mat4 u_projection_matrix;

// Position of eye and each light
uniform vec4 u_light_1_position;
uniform vec4 u_light_2_position;
uniform vec4 u_light_3_position;
uniform vec4 u_eye_position;

varying vec4 v_normal;

// For lambert and phong for each colour
varying vec4 v_s_1;
varying vec4 v_s_2;
varying vec4 v_s_3;
varying vec4 v_h_1;
varying vec4 v_h_2;
varying vec4 v_h_3;

varying vec2 v_uv;

void main(void)
{
	vec4 position = vec4(a_position.x, a_position.y, a_position.z, 1.0);
	vec4 normal = vec4(a_normal.x, a_normal.y, a_normal.z, 0.0);

	// UV coords sent into per-pixel use
	v_uv = a_uv;

	position = u_model_matrix * position;
	v_normal = normalize(u_model_matrix * normal);

	// vector going from point that im drawing, to the light
	//global coordinates
    // Used diffuse light in lambert
    v_s_1 = normalize(u_light_1_position - position);
    v_s_2 = normalize(u_light_2_position - position);
    v_s_3 = normalize(u_light_3_position - position);

	// Used for specular light in phong
    vec4 v = normalize(u_eye_position - position);
    v_h_1 = normalize(v_s_1 + v);
    v_h_2 = normalize(v_s_2 + v);
    v_h_3 = normalize(v_s_3 + v);

 	// Multiply position with view matrix for eye coordinates,
    // then projection matrix for clip coordinates
	position = u_view_matrix * position;
	position = u_projection_matrix * position;

	gl_Position = position;
}