export function canvasRightSize(canvas, drawFn, ...args) {
  function onResize(entries) {
    for (const entry of entries) {
      canvas.width = entry.devicePixelContentBoxSize[0].inlineSize;
      canvas.height = entry.devicePixelContentBoxSize[0].blockSize;
      drawFn(canvas, ...args)
    }
  }

  const resizeObserver = new ResizeObserver(onResize);
  resizeObserver.observe(canvas, { box: "content-box" });
}
