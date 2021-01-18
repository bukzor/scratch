import {webglRightSize} from './canvas_rightsize.js';


export function webgl_demo(canvas) {
  console.log('canvas:', canvas);

  var webgl = canvas.getContext("webgl");
  if (!webgl) {
    canvas.outerHTML = 'No webgl for you. t.t';
    return false;
  }

  console.log('webgl:', webgl);
  var vertexShader = fetch('index.vert')
    .then(response => response.text())
    .then(source => createShader(webgl, webgl.VERTEX_SHADER, source));

  var fragmentShader = fetch('index.frag')
    .then(response => response.text())
    .then(source => createShader(webgl, webgl.FRAGMENT_SHADER, source));

  return Promise.all([vertexShader, fragmentShader])
    .then(shaders => createProgram(webgl, ...shaders))
    .then(program => initialize(webgl, program))
    .then(() => webglRightSize(webgl, draw));
}

function initialize(webgl, program) {
  var positionAttributeLocation = webgl.getAttribLocation(program, "a_position");

  webgl.enableVertexAttribArray(positionAttributeLocation);

  var positionBuffer = webgl.createBuffer();

  webgl.bindBuffer(webgl.ARRAY_BUFFER, positionBuffer);

  // three 2d points
  var positions = [
    -0.3, -0.3,
    0, 0.5,
    0.7, 0,
  ];
  webgl.bufferData(webgl.ARRAY_BUFFER, new Float32Array(positions), webgl.STATIC_DRAW);

  // Tell the attribute how to get data out of positionBuffer (ARRAY_BUFFER)
  var size = 2;          // 2 components per iteration
  var type = webgl.FLOAT;   // the data is 32bit floats
  var normalize = false; // don't normalize the data
  var stride = 0;        // 0 = move forward size * sizeof(type) each iteration to get the next position
  var offset = 0;        // start at the beginning of the buffer
  webgl.vertexAttribPointer(positionAttributeLocation, size, type, normalize, stride, offset)

  // Tell it to use our program (pair of shaders)
  webgl.useProgram(program);
}

function draw(webgl) {
  console.log('webgl(2):', webgl);
  webgl.viewport(0, 0, webgl.canvas.width, webgl.canvas.height);

  // Clear the canvas
  webgl.clearColor(0, 0, 0, 0);
  webgl.clear(webgl.COLOR_BUFFER_BIT);

  var primitiveType = webgl.TRIANGLES;
  var offset = 0;
  var count = 3;
  webgl.drawArrays(primitiveType, offset, count);
}

function createShader(webgl, type, source) {
  var shader = webgl.createShader(type);
  webgl.shaderSource(shader, source);
  webgl.compileShader(shader);
  var success = webgl.getShaderParameter(shader, webgl.COMPILE_STATUS);
  if (success) {
    return shader;
  } else {
    var error = webgl.getShaderInfoLog(shader);
    webgl.deleteShader(shader);
    throw error;
  }
}


function createProgram(webgl, vertexShader, fragmentShader) {
  var program = webgl.createProgram();
  webgl.attachShader(program, vertexShader);
  webgl.attachShader(program, fragmentShader);
  webgl.linkProgram(program);
  var success = webgl.getProgramParameter(program, webgl.LINK_STATUS);
  if (success) {
    return program;
  } else {
    var error = webgl.getProgramInfoLog(program)
    webgl.deleteProgram(program);
    throw error;
  }
}
