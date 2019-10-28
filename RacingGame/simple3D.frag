
varying vec4 v_normal;
varying vec4 v_s;
varying vec4 v_h;
varying vec2 v_uv;

uniform vec4 u_light_diffuse;
uniform vec4 u_light_specular;

uniform vec4 u_mat_diffuse;
uniform vec4 u_mat_specular;
uniform float u_mat_shininess;

uniform sampler2D u_skybox;

void main(void)
{	
	vec4 mat_diffuse = u_mat_diffuse * texture2D(u_skybox, v_uv);
    // vector going from point that im drawing, to the light
	float lambert = max(dot(v_normal, v_s), 0.0);
	float phong = max(dot(v_normal, v_h), 0.0);

	gl_FragColor = u_light_diffuse * mat_diffuse * lambert 
			    + u_light_specular * u_mat_specular * pow(phong, u_mat_shininess);

    gl_FragColor.r = gl_FragColor.r * v_uv.x;

}