import * as W from './lib/webgl.js';


export async function webgl_demo(canvas, slider_x, slider_y) {
  var webgl = canvas.getContext("webgl");
  if (!webgl) {
    canvas.outerHTML = 'No webgl for you. t.t';
    return false;
  }

  var vert = W.fetchShader(webgl, 'index.vert')
  var frag = W.fetchShader(webgl, 'index.frag')

  var shaders = await Promise.all([vert, frag])
  var program = W.createProgram(webgl, ...shaders)
  initialize(webgl, program)

  var grey = Math.random();
  var color = [Math.random(), Math.random(), Math.random(), 1];

  var redraw = () => draw(webgl, program, x, y, grey, color)
  W.rightSize(webgl, redraw)
  x.oninput = x.onchange = redraw
  y.oninput = y.onchange = redraw
}

// Fill the buffer with texture coordinates for the F.
function setTexcoords(gl) {
  gl.bufferData(
    gl.ARRAY_BUFFER,
    new Float32Array([
      // rectangle
      0, 0,
      0, 1,
      1, 0,
      0, 1,
      1, 1,
      1, 0,
    ]),
    gl.STATIC_DRAW,
  );

  // Create a texture.
  var texture = gl.createTexture();
  gl.bindTexture(gl.TEXTURE_2D, texture);
  
  // Fill the texture with a 1x1 blue pixel.
  gl.texImage2D(
    gl.TEXTURE_2D, 0,
    gl.RGBA, 1, 1, 0,
    gl.RGBA,
    gl.UNSIGNED_BYTE,
    new Uint8Array([0, 0, 255, 255]),
  );
  
  // Asynchronously load an image
  var image = new Image();
  image.src = "resources/f-texture.png";
  image.addEventListener('load', function() {
    // Now that the image has loaded make copy it to the texture.
    gl.bindTexture(gl.TEXTURE_2D, texture);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA,gl.UNSIGNED_BYTE, image);
    gl.generateMipmap(gl.TEXTURE_2D);
  });
}


function initialize(webgl, program) {
  var a_position = webgl.getAttribLocation(program, "a_position");
  webgl.enableVertexAttribArray(a_position);

  // Create a buffer for texcoords.
  var a_texcoords = gl.getAttribLocation(program, "a_texcoords");
  gl.enableVertexAttribArray(a_texcoords);

  // We'll supply texcoords as floats.
  gl.vertexAttribPointer(a_texcoords, 2, gl.FLOAT, false, 0, 0);

  // Set Texcoords.
  setTexcoords(gl);

  var ab_position = webgl.createBuffer();
  webgl.bindBuffer(webgl.ARRAY_BUFFER, ab_position);

  // ab_position = three 2d points
  var positions = [
    -0.3, -0.3,
    0, 0.5,
    0.7, 0,
  ];
  webgl.bufferData(webgl.ARRAY_BUFFER, new Float32Array(positions), webgl.STATIC_DRAW);

  // Tell the attribute how to get data out of ab_position (ARRAY_BUFFER)
  var size = 2;          // 2 components per iteration
  var type = webgl.FLOAT;   // the data is 32bit floats
  var normalize = false; // don't normalize the data
  var stride = 0;        // 0 = move forward size * sizeof(type) each iteration to get the next position
  var offset = 0;        // start at the beginning of the buffer
  webgl.vertexAttribPointer(a_position, size, type, normalize, stride, offset)

  // Tell it to use our program (pair of shaders)
  webgl.useProgram(program);
}

function slider_max(slider, max) {
  if (slider.max == "") {
    slider.max = max
    slider.value = slider.value * max / 100;
  }
}

function draw(webgl, program, x_slider, y_slider, grey, color) {
  var w = webgl.canvas.width
    , h = webgl.canvas.height;

  slider_max(x_slider, w * 2 / 3);
  slider_max(y_slider, h * 8 / 9);

  webgl.viewport(0, 0, w, h);

  // Clear the canvas to grey.
  webgl.clearColor(grey, grey, grey, 0.0);
  webgl.clear(webgl.COLOR_BUFFER_BIT);

  var translation = [
    parseInt(x_slider.value),
    parseInt(y_slider.value),
  ]

  // lookup uniforms
  var u_resolution = webgl.getUniformLocation(program, "u_resolution");
  var u_color = webgl.getUniformLocation(program, "u_color");

  // Setup a rectangle
  W.setRectangle(webgl, translation[0], translation[1], w/3, h/9);

  // set the resolution
  webgl.uniform2f(u_resolution, w, h);

  // set the color
  webgl.uniform4fv(u_color, color);

  // Draw the rectangle.
  var primitiveType = webgl.TRIANGLES;
  var offset = 0;
  var count = 6;
  webgl.drawArrays(primitiveType, offset, count);
}

