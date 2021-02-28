precision mediump float;

// Passed in from the vertex shader.
varying vec2 v_texcoord;

uniform vec4 u_color;
// The texture.
uniform sampler2D u_texture;

void main() {
  gl_FragColor = texture2D(u_texture, v_texcoord);

}
