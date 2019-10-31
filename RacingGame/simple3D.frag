
varying vec4 v_normal;
varying vec4 v_s;
varying vec4 v_h;
varying vec2 v_uv;

uniform vec4 u_light_diffuse;
uniform vec4 u_light_specular;

uniform vec4 u_mat_diffuse;
uniform vec4 u_mat_specular;
uniform float u_mat_shininess;

uniform sampler2D u_diffuse_texture;
uniform sampler2D u_specular_texture;
 
void main(void)
{	
	vec4 mat_diffuse = u_mat_diffuse * texture2D(u_diffuse_texture, v_uv);
	vec4 mat_specular = u_mat_specular * texture2D(u_specular_texture, v_uv);
	float opacity = texture2D(u_diffuse_texture, v_uv).r;


	float lambert = max(dot(v_normal, v_s), 0.0);
	float phong = max(dot(v_normal, v_h), 0.0);

	gl_FragColor = u_light_diffuse * mat_diffuse * lambert 
			    + u_light_specular * mat_specular * pow(phong, u_mat_shininess);
	gl_FragColor.a = opacity;
}