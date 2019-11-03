varying vec4 v_normal;

// For lambert and phong for each colour
varying vec4 v_s_1;
varying vec4 v_s_2;
varying vec4 v_s_3;
varying vec4 v_h_1;
varying vec4 v_h_2;
varying vec4 v_h_3;

varying vec2 v_uv;

// Each light diffuse and specular colour
uniform vec4 u_light_1_diffuse;
uniform vec4 u_light_1_specular;
uniform vec4 u_light_2_diffuse;
uniform vec4 u_light_2_specular;
uniform vec4 u_light_3_diffuse;
uniform vec4 u_light_3_specular;

// Material colour
uniform vec4 u_mat_diffuse;
uniform vec4 u_mat_specular;
uniform float u_mat_shininess;

// Texture
uniform sampler2D u_diffuse_texture;
uniform sampler2D u_specular_texture;
 
// Global light
uniform vec4 u_light_ambient;
uniform vec4 u_mat_ambient;

void main(void)
{	
	// Using global variables to 
	vec4 mat_diffuse = u_mat_diffuse * texture2D(u_diffuse_texture, v_uv);
	vec4 mat_specular = u_mat_specular * texture2D(u_specular_texture, v_uv);

	// Calculating each light its specular and diffuse
    float lambert_1 = max(dot(v_normal, normalize(v_s_1)), 0.0);
    float phong_1 = max(dot(v_normal, normalize(v_h_1)), 0.0);
    vec4 diffuseColor_1 = u_light_1_diffuse * mat_diffuse * lambert_1;
    vec4 specularColor_1 = u_light_1_specular * mat_specular * pow(phong_1, u_mat_shininess);
    vec4 light1CalculatedColor = diffuseColor_1 + specularColor_1;
	
	float lambert_2 = max(dot(v_normal, normalize(v_s_2)), 0.0);
    float phong_2 = max(dot(v_normal, normalize(v_h_2)), 0.0);
    vec4 diffuseColor_2 = u_light_2_diffuse * mat_diffuse * lambert_2;
    vec4 specularColor_2 = u_light_2_specular * mat_specular * pow(phong_2, u_mat_shininess);
    vec4 light2CalculatedColor = diffuseColor_2 + specularColor_2;

    float lambert_3 = max(dot(v_normal, normalize(v_s_3)), 0.0);
    float phong_3 = max(dot(v_normal, normalize(v_h_3)), 0.0);
    vec4 diffuseColor_3 = u_light_3_diffuse * mat_diffuse * lambert_3;
    vec4 specularColor_3 = u_light_3_specular * mat_specular * pow(phong_3, u_mat_shininess);
    vec4 light3CalculatedColor = diffuseColor_3 + specularColor_3;


	// Adding the lights together for the combined colour
	gl_FragColor = u_light_ambient * u_mat_ambient + light1CalculatedColor + light2CalculatedColor + light3CalculatedColor;
	gl_FragColor.a = u_mat_diffuse.a;
}