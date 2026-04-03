"use client";

import { useRef, useMemo, useState, useEffect } from "react";
import { Canvas, useFrame, useThree } from "@react-three/fiber";
import { OrbitControls, Text, Html } from "@react-three/drei";
/* eslint-disable react-hooks/exhaustive-deps */
import * as THREE from "three";
import { ABP_DOMAINS } from "@/lib/domains";

// ── Types ──────────────────────────────────────────────────────────

export interface TorusConcept {
  id: number;
  name: string;
  slug: string;
  primary_domain: string;
  secondary_domains?: string | null;
  exam_relevance: number;
  ring1_identity: string | null;
  ring2_taxonomy?: string | null;
  ring3_associations?: string | null;
  ring4_distinctions?: string | null;
  ring5_edge?: string | null;
  board_pearls?: string | null;
  timeline?: string | null;
}

export interface TorusEdge {
  source_id: number;
  target_id: number;
  relation_type: string;
  weight: number;
  explanation: string | null;
}

export interface TorusDensity {
  domain: string;
  count: number;
}

export interface TraversalPathData {
  conceptIds: number[];
  currentStep: number;
  relation: string;
}

export interface ConceptTorusProps {
  concepts: TorusConcept[];
  edges: TorusEdge[];
  chunkDensity: TorusDensity[];
  focusConceptId: number | null;
  activeDomain: string | null;
  traversalPath: TraversalPathData | null;
  onConceptSelect: (concept: TorusConcept) => void;
  onDomainSelect: (domain: string | null) => void;
  onFiberHover: (info: FiberHoverInfo | null) => void;
}

export interface FiberHoverInfo {
  relationType: string;
  weight: number;
  sourceName: string;
  targetName: string;
  explanation: string | null;
  screenPos: { x: number; y: number };
}

// ── Timeline positions ─────────────────────────────────────────────

const TIMELINE_BANDS = [
  { key: "prenatal", label: "Prenatal", theta: 0.0, color: "#818CF8" },
  { key: "delivery", label: "Delivery Room", theta: 0.15, color: "#F87171" },
  { key: "minutes", label: "First Minutes", theta: 0.25, color: "#FB923C" },
  { key: "24h", label: "First 24h", theta: 0.4, color: "#FBBF24" },
  { key: "days", label: "Days 2-7", theta: 0.55, color: "#34D399" },
  { key: "weeks", label: "Weeks 2-12", theta: 0.7, color: "#3B82F6" },
  { key: "longterm", label: "Long-term", theta: 0.85, color: "#A855F7" },
];

// ── Geometry helpers ───────────────────────────────────────────────

const R = 2.2; // major radius
const r = 0.7; // minor radius

function torusXYZ(
  phi: number, // major angle (domain position)
  theta: number, // minor angle (timeline/depth)
): [number, number, number] {
  const x = (R + r * Math.cos(theta * Math.PI * 2)) * Math.cos(phi);
  const y = (R + r * Math.cos(theta * Math.PI * 2)) * Math.sin(phi);
  const z = r * Math.sin(theta * Math.PI * 2);
  return [x, y, z];
}

function domainPhi(domainId: string): number {
  const idx = ABP_DOMAINS.findIndex((d) => d.id === domainId);
  if (idx < 0) return 0;
  return (idx / ABP_DOMAINS.length) * Math.PI * 2;
}

// Deterministic hash for concept positioning
function hashCode(s: string): number {
  let h = 0;
  for (let i = 0; i < s.length; i++) {
    h = ((h << 5) - h + s.charCodeAt(i)) | 0;
  }
  return Math.abs(h);
}

// ── Fiber line styles ──────────────────────────────────────────────

const FIBER_STYLES: Record<string, { dash: number; gap: number; label: string }> = {
  association: { dash: 0, gap: 0, label: "Association" },
  distinction: { dash: 0.05, gap: 0.05, label: "Distinction" },
  treatment: { dash: 0.15, gap: 0.02, label: "Treatment" },
  mechanism: { dash: 0, gap: 0, label: "Mechanism" },
  genetic: { dash: 0.08, gap: 0.04, label: "Genetic" },
  temporal: { dash: 0.1, gap: 0.06, label: "Timeline" },
};

// ── Domain Band ────────────────────────────────────────────────────

function DomainBand({
  domainIndex,
  domain,
  density,
  maxDensity,
  isActive,
  isFaded,
  onClick,
}: {
  domainIndex: number;
  domain: (typeof ABP_DOMAINS)[number];
  density: number;
  maxDensity: number;
  isActive: boolean;
  isFaded: boolean;
  onClick: () => void;
}) {
  const meshRef = useRef<THREE.Mesh>(null);
  const [hovered, setHovered] = useState(false);

  const geometry = useMemo(() => {
    // Scale arc length by exam weight to make heavier domains wider
    const weightScale = domain.exam_percent / 5; // 5% = baseline width
    const baseAngle = (1 / ABP_DOMAINS.length) * Math.PI * 2;
    const phiLength = baseAngle * Math.min(weightScale, 1.6); // cap scaling
    const phiStart =
      (domainIndex / ABP_DOMAINS.length) * Math.PI * 2 -
      phiLength / 2 +
      baseAngle / 2;

    const geo = new THREE.TorusGeometry(R, r * 1.01, 12, 24, phiLength);
    geo.rotateZ(phiStart);
    return geo;
  }, [domainIndex, domain.exam_percent]);

  const normalizedDensity = maxDensity > 0 ? density / maxDensity : 0;
  const baseOpacity = 0.05 + normalizedDensity * 0.2;
  const opacity = isFaded ? baseOpacity * 0.15 : isActive ? baseOpacity + 0.15 : baseOpacity;

  return (
    <mesh
      ref={meshRef}
      geometry={geometry}
      onClick={(e) => {
        e.stopPropagation();
        onClick();
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
      <meshStandardMaterial
        color={domain.color}
        transparent
        opacity={hovered ? opacity + 0.1 : opacity}
        side={THREE.DoubleSide}
      />
    </mesh>
  );
}

// ── Domain Label ───────────────────────────────────────────────────

function DomainLabel({
  domain,
  domainIndex,
  count,
  isFaded,
  isActive,
}: {
  domain: (typeof ABP_DOMAINS)[number];
  domainIndex: number;
  count: number;
  isFaded: boolean;
  isActive: boolean;
}) {
  const phi = (domainIndex / ABP_DOMAINS.length) * Math.PI * 2;
  const labelR = R + r + 0.25;
  const x = labelR * Math.cos(phi);
  const y = labelR * Math.sin(phi);

  return (
    <group position={[x, y, 0]}>
      <Text
        fontSize={isActive ? 0.16 : 0.12}
        color={isFaded ? "#3f3f46" : domain.color}
        anchorX="center"
        anchorY="middle"
        font={undefined}
      >
        {domain.abbrev}
      </Text>
      {!isFaded && (
        <Text
          fontSize={0.06}
          color="#52525B"
          anchorX="center"
          anchorY="middle"
          position={[0, -0.15, 0]}
          font={undefined}
        >
          {domain.exam_percent}% | {count}
        </Text>
      )}
    </group>
  );
}

// ── Timeline Ring ──────────────────────────────────────────────────

function TimelineRing() {
  return (
    <group>
      {TIMELINE_BANDS.map((band) => {
        // Place labels along the tube (minor circle) at phi=0
        const pos = torusXYZ(0, band.theta);
        return (
          <group key={band.key}>
            {/* Faint ring around torus at this theta */}
            <mesh rotation={[Math.PI / 2, 0, 0]}>
              <torusGeometry
                args={[R + r * Math.cos(band.theta * Math.PI * 2), 0.003, 4, 64]}
              />
              <meshBasicMaterial color={band.color} transparent opacity={0.08} />
            </mesh>
            {/* Label at outer edge */}
            <group position={[pos[0] + 0.4, pos[1], pos[2]]}>
              <Text
                fontSize={0.05}
                color={band.color}
                anchorX="left"
                anchorY="middle"
                font={undefined}
              >
                {band.label}
              </Text>
            </group>
          </group>
        );
      })}
    </group>
  );
}

// ── Concept Node ───────────────────────────────────────────────────

function ConceptNode({
  concept,
  position,
  color,
  isFocus,
  isFaded,
  isConnected,
  onClick,
}: {
  concept: TorusConcept;
  position: [number, number, number];
  color: string;
  isFocus: boolean;
  isFaded: boolean;
  isConnected: boolean;
  onClick: () => void;
}) {
  const meshRef = useRef<THREE.Mesh>(null);
  const glowRef = useRef<THREE.Mesh>(null);
  const [hovered, setHovered] = useState(false);

  useFrame((_, delta) => {
    if (!meshRef.current) return;
    const targetScale = isFocus ? 2.5 : hovered ? 1.6 : 1;
    const s = meshRef.current.scale.x;
    meshRef.current.scale.setScalar(s + (targetScale - s) * delta * 8);

    if (glowRef.current && isFocus) {
      glowRef.current.scale.setScalar(
        3 + Math.sin(Date.now() * 0.003) * 0.4
      );
    }
  });

  const baseSize = 0.025 + concept.exam_relevance * 0.04;
  const opacity = isFaded ? 0.08 : isConnected ? 0.9 : 0.5;
  const emissiveIntensity = isFocus ? 1.0 : hovered ? 0.6 : isConnected ? 0.4 : 0.15;

  return (
    <group position={position}>
      {/* Glow ring for focus concept */}
      {isFocus && (
        <mesh ref={glowRef}>
          <ringGeometry args={[baseSize * 2, baseSize * 3, 32]} />
          <meshBasicMaterial
            color={color}
            transparent
            opacity={0.15}
            side={THREE.DoubleSide}
          />
        </mesh>
      )}

      <mesh
        ref={meshRef}
        onClick={(e) => {
          e.stopPropagation();
          onClick();
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
        <sphereGeometry args={[baseSize, 12, 12]} />
        <meshStandardMaterial
          color={color}
          emissive={color}
          emissiveIntensity={emissiveIntensity}
          transparent
          opacity={opacity}
        />
      </mesh>

      {/* Hover tooltip */}
      {hovered && !isFocus && (
        <Html distanceFactor={5} style={{ pointerEvents: "none" }}>
          <div className="bg-zinc-900/95 border border-zinc-700 rounded-lg px-3 py-2 text-[10px] text-zinc-200 whitespace-nowrap shadow-xl backdrop-blur-sm">
            <div className="font-bold text-xs mb-0.5">{concept.name}</div>
            <div className="text-zinc-500">{domainName(concept.primary_domain)}</div>
            {concept.ring1_identity && (
              <div className="text-zinc-400 max-w-52 truncate mt-1">
                {concept.ring1_identity.substring(0, 80)}
              </div>
            )}
            <div className="text-zinc-600 mt-1">
              Relevance: {Math.round(concept.exam_relevance * 100)}%
            </div>
          </div>
        </Html>
      )}
    </group>
  );
}

// ── Fiber (connection line) ────────────────────────────────────────

function Fiber({
  from,
  to,
  edge,
  color,
  isFaded,
}: {
  from: [number, number, number];
  to: [number, number, number];
  edge: TorusEdge;
  color: string;
  isFaded: boolean;
  onHover: (info: FiberHoverInfo | null) => void;
  sourceName: string;
  targetName: string;
}) {
  const curvePoints = useMemo(() => {
    const curve = new THREE.QuadraticBezierCurve3(
      new THREE.Vector3(...from),
      new THREE.Vector3(
        (from[0] + to[0]) / 2,
        (from[1] + to[1]) / 2,
        (from[2] + to[2]) / 2 +
          (edge.relation_type === "temporal" ? 0.5 : 0.15) * edge.weight
      ),
      new THREE.Vector3(...to)
    );
    return curve.getPoints(20).flatMap((p) => [p.x, p.y, p.z]);
  }, [from, to, edge]);

  const geometry = useMemo(() => {
    const geo = new THREE.BufferGeometry();
    geo.setAttribute(
      "position",
      new THREE.Float32BufferAttribute(curvePoints, 3)
    );
    return geo;
  }, [curvePoints]);

  const opacity = isFaded ? 0.03 : 0.15 + edge.weight * 0.5;
  const lineWidth = 1 + edge.weight * 3;

  // Use primitive to avoid JSX <line> vs SVG conflict
  const lineObj = useMemo(() => {
    const mat = new THREE.LineBasicMaterial({
      color,
      transparent: true,
      opacity,
      linewidth: lineWidth,
    });
    return new THREE.Line(geometry, mat);
  }, [geometry, color, opacity, lineWidth]);

  // Update material reactively
  useEffect(() => {
    if (lineObj.material instanceof THREE.LineBasicMaterial) {
      lineObj.material.opacity = opacity;
      lineObj.material.color.set(color);
    }
  }, [lineObj, opacity, color]);

  return <primitive object={lineObj} />;
}

// ── Main Scene ─────────────────────────────────────────────────────

function TorusScene({
  concepts,
  edges,
  chunkDensity,
  focusConceptId,
  activeDomain,
  traversalPath,
  onConceptSelect,
  onDomainSelect,
  onFiberHover,
}: ConceptTorusProps) {
  const groupRef = useRef<THREE.Group>(null);
  const targetRotation = useRef(0);
  const { camera } = useThree();

  // Build lookup maps
  const conceptMap = useMemo(
    () => new Map(concepts.map((c) => [c.id, c])),
    [concepts]
  );

  const densityMap = useMemo(
    () => new Map(chunkDensity.map((d) => [d.domain, d.count])),
    [chunkDensity]
  );
  const maxDensity = useMemo(
    () => Math.max(...chunkDensity.map((d) => d.count), 1),
    [chunkDensity]
  );

  // Traversal state
  const traversalIds = useMemo(
    () => new Set(traversalPath?.conceptIds || []),
    [traversalPath]
  );
  const isTraversing = traversalPath && traversalPath.conceptIds.length > 1;
  const traversalCurrentId = isTraversing
    ? traversalPath.conceptIds[traversalPath.currentStep]
    : null;

  // Connected concept IDs (direct neighbors of focus)
  const connectedIds = useMemo(() => {
    if (!focusConceptId) return new Set<number>();
    const ids = new Set<number>();
    for (const e of edges) {
      if (e.source_id === focusConceptId) ids.add(e.target_id);
      if (e.target_id === focusConceptId) ids.add(e.source_id);
    }
    return ids;
  }, [focusConceptId, edges]);

  // Position each concept on torus surface
  const conceptPositions = useMemo(() => {
    const positions = new Map<number, [number, number, number]>();
    for (const c of concepts) {
      const h = hashCode(c.slug + c.name);
      const basePhi = domainPhi(c.primary_domain);
      // Jitter within domain sector
      const sectorWidth = (1 / ABP_DOMAINS.length) * Math.PI * 2;
      const jitter = ((h % 1000) / 1000 - 0.5) * sectorWidth * 0.7;
      const phi = basePhi + jitter;
      // Theta based on hash (timeline position if available, else scatter)
      const theta = ((h % 777) / 777) * 0.4 + 0.05;
      positions.set(c.id, torusXYZ(phi, theta));
    }
    return positions;
  }, [concepts]);

  // Compute target rotation to bring focus/traversal concept to front
  useEffect(() => {
    const targetId = traversalCurrentId || focusConceptId;
    if (targetId) {
      const c = conceptMap.get(targetId);
      if (c) {
        const phi = domainPhi(c.primary_domain);
        targetRotation.current = -phi + Math.PI / 2;
      }
    }
  }, [focusConceptId, traversalCurrentId, conceptMap]);

  // Animate rotation toward target
  useFrame((_, delta) => {
    if (!groupRef.current) return;

    if (focusConceptId) {
      // Smoothly rotate to focus
      const diff = targetRotation.current - groupRef.current.rotation.z;
      // Wrap angle difference
      const wrapped =
        ((diff + Math.PI) % (Math.PI * 2)) - Math.PI;
      groupRef.current.rotation.z += wrapped * delta * 3;
    } else {
      // Gentle auto-rotation when no focus
      groupRef.current.rotation.z += delta * 0.03;
    }
  });

  // Camera setup
  useMemo(() => {
    camera.position.set(0, -1.5, 5.5);
    camera.lookAt(0, 0, 0);
  }, [camera]);

  // Which edges to render
  const visibleEdges = useMemo(() => {
    if (isTraversing) {
      // In traversal: show edges between traversal nodes
      return edges.filter(
        (e) => traversalIds.has(e.source_id) && traversalIds.has(e.target_id)
      );
    }
    if (!focusConceptId) return edges.slice(0, 50);
    return edges.filter(
      (e) =>
        e.source_id === focusConceptId ||
        e.target_id === focusConceptId
    );
  }, [focusConceptId, edges, isTraversing, traversalIds]);

  return (
    <group ref={groupRef}>
      {/* Base torus wireframe — subtle terrain */}
      <mesh>
        <torusGeometry args={[R, r, 24, 48]} />
        <meshStandardMaterial
          color="#18181B"
          wireframe
          transparent
          opacity={0.06}
        />
      </mesh>

      {/* Solid torus shell — translucent */}
      <mesh>
        <torusGeometry args={[R, r * 0.99, 32, 64]} />
        <meshStandardMaterial
          color="#0A0A0A"
          transparent
          opacity={0.3}
          side={THREE.BackSide}
        />
      </mesh>

      {/* Domain bands */}
      {ABP_DOMAINS.map((domain, i) => (
        <DomainBand
          key={domain.id}
          domainIndex={i}
          domain={domain}
          density={densityMap.get(domain.id) || 0}
          maxDensity={maxDensity}
          isActive={activeDomain === domain.id}
          isFaded={
            !!(activeDomain && activeDomain !== domain.id) ||
            !!(
              focusConceptId &&
              !connectedIds.has(focusConceptId) &&
              !concepts.some(
                (c) =>
                  c.primary_domain === domain.id &&
                  (c.id === focusConceptId || connectedIds.has(c.id))
              )
            )
          }
          onClick={() =>
            onDomainSelect(activeDomain === domain.id ? null : domain.id)
          }
        />
      ))}

      {/* Domain labels */}
      {ABP_DOMAINS.map((domain, i) => {
        const isDomainRelevant =
          !focusConceptId ||
          concepts.some(
            (c) =>
              c.primary_domain === domain.id &&
              (c.id === focusConceptId || connectedIds.has(c.id))
          );
        return (
          <DomainLabel
            key={domain.id}
            domain={domain}
            domainIndex={i}
            count={densityMap.get(domain.id) || 0}
            isFaded={!isDomainRelevant && !!focusConceptId}
            isActive={activeDomain === domain.id}
          />
        );
      })}

      {/* Timeline overlay */}
      <TimelineRing />

      {/* Fibers (connection lines) */}
      {visibleEdges.map((edge) => {
        const fromPos = conceptPositions.get(edge.source_id);
        const toPos = conceptPositions.get(edge.target_id);
        if (!fromPos || !toPos) return null;

        const targetConcept =
          edge.source_id === focusConceptId
            ? conceptMap.get(edge.target_id)
            : conceptMap.get(edge.source_id);

        const targetDomain = targetConcept?.primary_domain;
        const color = ABP_DOMAINS.find((d) => d.id === targetDomain)?.color || "#71717A";

        const isPathEdge =
          isTraversing &&
          traversalIds.has(edge.source_id) &&
          traversalIds.has(edge.target_id);

        const isFaded = isTraversing
          ? !isPathEdge
          : !!focusConceptId &&
            edge.source_id !== focusConceptId &&
            edge.target_id !== focusConceptId;

        return (
          <Fiber
            key={`${edge.source_id}-${edge.target_id}-${edge.relation_type}`}
            from={fromPos}
            to={toPos}
            edge={isPathEdge ? { ...edge, weight: Math.max(edge.weight, 0.7) } : edge}
            color={isPathEdge ? "#F59E0B" : color}
            isFaded={isFaded}
            onHover={onFiberHover}
            sourceName={conceptMap.get(edge.source_id)?.name || "?"}
            targetName={conceptMap.get(edge.target_id)?.name || "?"}
          />
        );
      })}

      {/* Concept nodes */}
      {concepts.map((concept) => {
        const pos = conceptPositions.get(concept.id);
        if (!pos) return null;

        const color =
          ABP_DOMAINS.find((d) => d.id === concept.primary_domain)?.color ||
          "#71717A";

        const isOnPath = traversalIds.has(concept.id);
        const isCurrentTraversalNode = concept.id === traversalCurrentId;
        const isFocus = concept.id === focusConceptId || isCurrentTraversalNode;
        const isConnected = connectedIds.has(concept.id) || isOnPath;
        const isFaded = isTraversing
          ? !isOnPath && !isFocus
          : !!focusConceptId && !isFocus && !isConnected;

        // Domain filter (skip in traversal mode for path nodes)
        if (
          activeDomain &&
          concept.primary_domain !== activeDomain &&
          !isFocus &&
          !isConnected &&
          !isOnPath
        ) {
          return null;
        }

        return (
          <ConceptNode
            key={concept.id}
            concept={concept}
            position={pos}
            color={color}
            isFocus={isFocus}
            isFaded={isFaded}
            isConnected={isConnected}
            onClick={() => onConceptSelect(concept)}
          />
        );
      })}
    </group>
  );
}

// ── Helper ─────────────────────────────────────────────────────────

function domainName(id: string) {
  return ABP_DOMAINS.find((d) => d.id === id)?.name || id;
}

// ── Exported Component ─────────────────────────────────────────────

export default function ConceptTorus(props: ConceptTorusProps) {
  return (
    <Canvas
      camera={{ position: [0, -1.5, 5.5], fov: 45 }}
      gl={{ antialias: true, alpha: true }}
      style={{ background: "transparent" }}
    >
      <ambientLight intensity={0.35} />
      <pointLight position={[4, 4, 5]} intensity={0.6} />
      <pointLight position={[-4, -2, 4]} intensity={0.25} color="#818CF8" />
      <pointLight position={[0, 0, -3]} intensity={0.15} color="#F87171" />

      <TorusScene {...props} />

      <OrbitControls
        enableDamping
        dampingFactor={0.08}
        minDistance={2.5}
        maxDistance={8}
        enablePan={false}
        rotateSpeed={0.5}
      />
    </Canvas>
  );
}
