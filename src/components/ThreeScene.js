import React, { useRef } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";

const RotatingCube = () => {
  const cubeRef = useRef();

  // Rotate the cube continuously
  useFrame(() => {
    cubeRef.current.rotation.x += 0.01;
    cubeRef.current.rotation.y += 0.01;
  });

  return (
    <mesh ref={cubeRef}>
      <boxGeometry args={[2, 2, 2]} />
      <meshStandardMaterial color="hotpink" />
    </mesh>
  );
};

const ThreeScene = () => {
  return (
    <Canvas style={{ height: "300px", width: "100%" }}>
      <ambientLight />
      <pointLight position={[5, 5, 5]} />
      <RotatingCube />
      <OrbitControls />
    </Canvas>
  );
};

export default ThreeScene;
