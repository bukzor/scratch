import { useEffect } from "react";

import styles from "../components/SampleLayout.module.css";

import { onLoad } from "../two_cubes";

import "./styles.css";

export type SampleInit = (params: {
  canvas: HTMLCanvasElement;
}) => void | Promise<void>;

export const SampleLayout = () => {
  //window.onload = onLoad;
  useEffect(onLoad);

  return (
    <main>
      <div className={styles.canvasContainer}>
        <canvas />
      </div>
    </main>
  );
};

const RotatingCube: () => JSX.Element = () => <SampleLayout />;

export default RotatingCube;
