import { useEffect, useRef, useState } from 'react'
import gsap from 'gsap'
import { useGSAP } from '@gsap/react'
import * as THREE from 'three'

// Three.js: one spinning shape drawn into a canvas.
function Scene({ onReady }) {
  const canvasRef = useRef(null)

  useEffect(() => {
    const canvas = canvasRef.current
    let renderer
    try {
      renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true })
    } catch {
      onReady(false)
      return
    }
    const scene = new THREE.Scene()
    const camera = new THREE.PerspectiveCamera(50, 1, 0.1, 100)
    camera.position.z = 4

    const shape = new THREE.Mesh(
      new THREE.TorusKnotGeometry(1, 0.32, 160, 24),
      new THREE.MeshStandardMaterial({ color: 0x38bdf8, metalness: 0.4, roughness: 0.25 }),
    )
    scene.add(shape)
    scene.add(new THREE.AmbientLight(0xffffff, 0.6))
    const light = new THREE.DirectionalLight(0xffffff, 2.5)
    light.position.set(3, 4, 5)
    scene.add(light)

    const resize = () => {
      const { clientWidth: w, clientHeight: h } = canvas
      renderer.setSize(w, h, false)
      camera.aspect = w / h
      camera.updateProjectionMatrix()
    }
    resize()
    window.addEventListener('resize', resize)

    renderer.setAnimationLoop((t) => {
      shape.rotation.x = t / 2000
      shape.rotation.y = t / 1400
      renderer.render(scene, camera)
    })
    onReady(true)

    return () => {
      window.removeEventListener('resize', resize)
      renderer.setAnimationLoop(null)
      renderer.dispose()
    }
  }, [onReady])

  return <canvas ref={canvasRef} className="h-72 w-full sm:h-96" />
}

export default function App() {
  const root = useRef(null)
  const [gsapDone, setGsapDone] = useState(false)
  const [threeOk, setThreeOk] = useState(null)

  // GSAP: fade and slide the hero text in.
  useGSAP(
    () => {
      gsap.from('.reveal', {
        y: 40,
        opacity: 0,
        duration: 0.8,
        stagger: 0.15,
        ease: 'power3.out',
        onComplete: () => setGsapDone(true),
      })
    },
    { scope: root },
  )

  const checks = [
    ['React', true],
    ['Tailwind CSS', true],
    ['GSAP', gsapDone],
    ['Three.js', threeOk === true],
  ]

  return (
    <main ref={root} className="min-h-screen bg-slate-950 px-4 py-10 text-slate-100">
      <div className="mx-auto grid max-w-5xl items-center gap-8 md:grid-cols-2">
        <section>
          <p className="reveal text-sm font-semibold uppercase tracking-widest text-sky-400">
            Web design environment
          </p>
          <h1 className="reveal mt-3 text-4xl font-bold leading-tight sm:text-5xl">
            React, Tailwind, GSAP and Three.js are running.
          </h1>
          <p className="reveal mt-4 text-slate-300">
            This is the test page. Edit <code className="text-sky-300">src/App.jsx</code> and the
            preview reloads by itself.
          </p>
          <ul className="reveal mt-6 grid grid-cols-2 gap-3" data-testid="checks">
            {checks.map(([name, ok]) => (
              <li
                key={name}
                data-ok={ok}
                className={`rounded-lg border px-3 py-2 text-sm ${
                  ok ? 'border-emerald-500/50 bg-emerald-500/10 text-emerald-300' : 'border-slate-700 text-slate-400'
                }`}
              >
                {ok ? 'OK' : '...'} {name}
              </li>
            ))}
          </ul>
        </section>
        <Scene onReady={setThreeOk} />
      </div>
    </main>
  )
}
