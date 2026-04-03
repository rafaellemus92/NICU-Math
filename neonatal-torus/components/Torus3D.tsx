"use client";

import { useRef, useMemo, useState, useCallback } from "react";
import { Canvas, useFrame, useThree } from "@react-three/fiber";
import { OrbitControls, Text, Html } from "@react-three/drei";
import * as THREE from "three";
import { ABP_DOMAINS } from "@/lib/domains";

interface TorusConcept {
  id: number;
  name: string;
  slug: string;
  primary_domain: string;
  exam_relevance: number;
  ring1_identity: string | null;
}

interface TorusChunkDensity {
  domain: string;
  count: number;
}

interface Torus3DProps {
  concepts: TorusConcept[];
  chunkDensity: TorusChunkDensity[];
  onConceptClick?: (slug: string) => void;
}

// Map each domain to a position on the torus surface
// theta = angle around the tube (minor circle) — encodes "depth" (identity → edge)
// phi = angle around the ring (major circle) — encodes domain position
function domainToTorusPosition(
  domainIndex: number,
  totalDomains: number,
  R: number, // major radius
  r: number, // minor radius
  depth: number = 0 // 0-1, where on the minor circle
): [number, number, number] {
  const phi = (domainIndex / totalDomains) * Math.PI * 2;
  const theta = depth * Math.PI * 2;

  const x = (R + r * Math.cos(theta)) * Math.cos(phi);
  const y = (R + r * Math.cos(theta)) * Math.sin(phi);
  const z = r * Math.sin(theta);

  return [x, y, z];
}

// Domain label component on the torus surface
function DomainLabel({
  domain,
  position,
  color,
  count,
}: {
  domain: { id: string; abbrev: string; name: string; exam_percent: number };
  position: [number, number, number];
  color: string;
  count: number;
}) {
  return (
    <group position={position}>
      <Text
        fontSize={0.15}
        color={color}
        anchorX="center"
        anchorY="middle"
        font={undefined}
      >
        {domain.abbrev}
      </Text>
      <Text
        fontSize={0.08}
        color="#71717A"
        anchorX="center"
        anchorY="middle"
        position={[0, -0.18, 0]}
        font={undefined}
      >
        {domain.exam_percent}% | {count} chunks
      </Text>
    </group>
  );
}

// Concept dot on the torus surface
function ConceptDot({
  concept,
  position,
  color,
  onClick,
}: {
  concept: TorusConcept;
  position: [number, number, number];
  color: string;
  onClick?: () => void;
}) {
  const meshRef = useRef<THREE.Mesh>(null);
  const [hovered, setHovered] = useState(false);

  useFrame(() => {
    if (meshRef.current) {
      meshRef.current.scale.setScalar(hovered ? 1.8 : 1);
    }
  });

  const size = 0.03 + concept.exam_relevance * 0.05;

  return (
    <group position={position}>
      <mesh
        ref={meshRef}
        onClick={(e) => {
          e.stopPropagation();
          onClick?.();
        }}
        onPointerEnter={(e) => {
          e.stopPropagation();
          setHovered(true);
          document.body.style.cursor = "pointer";
        }}
        onPointerLeave={() => {
          setHovered(false);
          document.body.style.cursor = "default";
        }}
      >
        <sphereGeometry args={[size, 8, 8]} />
        <meshStandardMaterial
          color={color}
          emissive={color}
          emissiveIntensity={hovered ? 0.8 : 0.3}
        />
      </mesh>
      {hovered && (
        <Html distanceFactor={6} style={{ pointerEvents: "none" }}>
          <div className="bg-zinc-900 border border-zinc-700 rounded px-2 py-1 text-[10px] text-zinc-200 whitespace-nowrap shadow-xl">
            <div className="font-bold">{concept.name}</div>
            {concept.ring1_identity && (
              <div className="text-zinc-400 max-w-48 truncate">
                {concept.ring1_identity.substring(0, 60)}...
              </div>
            )}
          </div>
        </Html>
      )}
    </group>
  );
}

// Heat map segments on the torus surface
function HeatSegment({
  domainIndex,
  totalDomains,
  R,
  r,
  density,
  color,
}: {
  domainIndex: number;
  totalDomains: number;
  R: number;
  r: number;
  density: number; // 0-1 normalized
  color: string;
}) {
  const geometry = useMemo(() => {
    const phiStart = (domainIndex / totalDomains) * Math.PI * 2;
    const phiLength = (1 / totalDomains) * Math.PI * 2;

    const geo = new THREE.TorusGeometry(R, r * 1.01, 16, 32, phiLength);
    // Rotate to correct position
    geo.rotateZ(phiStart);
    return geo;
  }, [domainIndex, totalDomains, R, r]);

  return (
    <mesh geometry={geometry}>
      <meshStandardMaterial
        color={color}
        transparent
        opacity={0.08 + density * 0.25}
        side={THREE.DoubleSide}
      />
    </mesh>
  );
}

// Main torus scene
function TorusScene({
  concepts,
  chunkDensity,
  onConceptClick,
}: Torus3DProps) {
  const groupRef = useRef<THREE.Group>(null);
  const { camera } = useThree();

  // Slow auto-rotation
  useFrame((_, delta) => {
    if (groupRef.current) {
      groupRef.current.rotation.z += delta * 0.05;
    }
  });

  const R = 2; // major radius
  const r = 0.8; // minor radius

  // Build density map
  const maxDensity = Math.max(...chunkDensity.map((d) => d.count), 1);
  const densityMap = new Map(chunkDensity.map((d) => [d.domain, d.count]));

  // Position concepts on torus
  const conceptPositions = useMemo(() => {
    return concepts.map((concept) => {
      const domainIdx = ABP_DOMAINS.findIndex(
        (d) => d.id === concept.primary_domain
      );
      const idx = domainIdx >= 0 ? domainIdx : 0;

      // Scatter concepts slightly within their domain sector
      const jitterPhi =
        (Math.random() - 0.5) * (1 / ABP_DOMAINS.length) * Math.PI * 2 * 0.6;
      const depth = 0.1 + Math.random() * 0.3; // position on minor circle

      const phi =
        (idx / ABP_DOMAINS.length) * Math.PI * 2 + jitterPhi;
      const theta = depth * Math.PI * 2;

      const x = (R + r * Math.cos(theta)) * Math.cos(phi);
      const y = (R + r * Math.cos(theta)) * Math.sin(phi);
      const z = r * Math.sin(theta);

      return {
        concept,
        position: [x, y, z] as [number, number, number],
        color:
          ABP_DOMAINS.find((d) => d.id === concept.primary_domain)?.color ||
          "#71717A",
      };
    });
  }, [concepts]);

  // Set initial camera
  useMemo(() => {
    camera.position.set(0, -1, 5);
    camera.lookAt(0, 0, 0);
  }, [camera]);

  return (
    <group ref={groupRef}>
      {/* Base torus wireframe */}
      <mesh>
        <torusGeometry args={[R, r, 32, 64]} />
        <meshStandardMaterial
          color="#27272A"
          wireframe
          transparent
          opacity={0.15}
        />
      </mesh>

      {/* Heat segments per domain */}
      {ABP_DOMAINS.map((domain, i) => (
        <HeatSegment
          key={domain.id}
          domainIndex={i}
          totalDomains={ABP_DOMAINS.length}
          R={R}
          r={r}
          density={(densityMap.get(domain.id) || 0) / maxDensity}
          color={domain.color}
        />
      ))}

      {/* Domain labels */}
      {ABP_DOMAINS.map((domain, i) => {
        const pos = domainToTorusPosition(
          i,
          ABP_DOMAINS.length,
          R + r + 0.3,
          0
        );
        return (
          <DomainLabel
            key={domain.id}
            domain={domain}
            position={pos}
            color={domain.color}
            count={densityMap.get(domain.id) || 0}
          />
        );
      })}

      {/* Concept dots */}
      {conceptPositions.map(({ concept, position, color }) => (
        <ConceptDot
          key={concept.id}
          concept={concept}
          position={position}
          color={color}
          onClick={() => onConceptClick?.(concept.slug)}
        />
      ))}
    </group>
  );
}

export default function Torus3D({
  concepts,
  chunkDensity,
  onConceptClick,
}: Torus3DProps) {
  return (
    <div className="w-full h-[600px] bg-zinc-950 rounded-xl border border-zinc-800 overflow-hidden relative">
      <Canvas
        camera={{ position: [0, -1, 5], fov: 50 }}
        gl={{ antialias: true }}
      >
        <ambientLight intensity={0.4} />
        <pointLight position={[5, 5, 5]} intensity={0.8} />
        <pointLight position={[-5, -5, 5]} intensity={0.3} color="#818CF8" />

        <TorusScene
          concepts={concepts}
          chunkDensity={chunkDensity}
          onConceptClick={onConceptClick}
        />

        <OrbitControls
          enableDamping
          dampingFactor={0.05}
          minDistance={2}
          maxDistance={10}
          autoRotate={false}
        />
      </Canvas>

      {/* Legend overlay */}
      <div className="absolute bottom-4 left-4 bg-zinc-900/80 backdrop-blur-sm border border-zinc-800 rounded-lg p-3 text-[10px]">
        <div className="text-zinc-500 uppercase tracking-wider mb-1 font-bold">
          Torus Axes
        </div>
        <div className="text-zinc-400 space-y-0.5">
          <div>Ring (major) = ABP Domain position</div>
          <div>Tube (minor) = Depth: identity → edge</div>
          <div>Dot size = Exam relevance</div>
          <div>Heat = Chunk density</div>
        </div>
        <div className="text-zinc-600 mt-2">
          Drag to rotate / Scroll to zoom / Click concept to open
        </div>
      </div>
    </div>
  );
}
