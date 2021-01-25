import {canvasRightSize} from './canvas_rightsize.js';

export function rightSize(webgl, drawFn, ...args) {
  canvasRightSize(webgl.canvas, canvas => drawFn(webgl, ...args));
};

export function fetchShader(webgl, path) {
  if (path.endsWith(".vert")) {
    var type = webgl.VERTEX_SHADER
  } else if (path.endsWith(".frag")) {
    var type = webgl.FRAGMENT_SHADER
  } else {
    throw "unrecognized shader type: " + path
  }

  return fetch(path)
    .then(response => response.text())
    .then(source => createShader(webgl, type, source))
}


export function createShader(webgl, type, source) {
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


export function createProgram(webgl, vertexShader, fragmentShader) {
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

// Fill the buffer with the values that define a rectangle.
export function setRectangle(webgl, x, y, width, height) {
  var x1 = x;
  var x2 = x + width;
  var y1 = y;
  var y2 = y + height;
  webgl.bufferData(
      webgl.ARRAY_BUFFER,
      new Float32Array([
          x1, y1,
          x2, y1,
          x1, y2,
          x1, y2,
          x2, y1,
          x2, y2,
      ]),
      webgl.STATIC_DRAW);
}
