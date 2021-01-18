export function canvasRightSize(canvas, drawFn) {
  function onResize(entries) {
    for (const entry of entries) {
      canvas.width = entry.devicePixelContentBoxSize[0].inlineSize;
      canvas.height = entry.devicePixelContentBoxSize[0].blockSize;
      drawFn(canvas)
    }
  }

  const resizeObserver = new ResizeObserver(onResize);
  resizeObserver.observe(canvas, { box: "content-box" });
}

export function webglRightSize(webgl, drawFn) {
  canvasRightSize(webgl.canvas, canvas => drawFn(webgl));
}
