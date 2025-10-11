---
tags: [reference, api, patterns]
---

# Motion Canvas Comprehensive Cheatsheet

## Table of Contents
1. [Project Setup](#project-setup)
2. [Core Concepts](#core-concepts)
3. [Components](#components)
4. [Animation & Tweening](#animation--tweening)
5. [Signals & Reactive System](#signals--reactive-system)
6. [Layout System](#layout-system)
7. [Media Support](#media-support)
8. [Time Events](#time-events)
9. [Effects & Shaders](#effects--shaders)
10. [Easing Functions](#easing-functions)
11. [Configuration](#configuration)
12. [Common Patterns](#common-patterns)
13. [Troubleshooting](#troubleshooting)

---

## Project Setup

### Create New Project
```bash
npm init @motion-canvas@latest
```

### Basic Project Structure
```
my-animation/
├── package.json
├── public/
├── src/
│   ├── motion-canvas.d.ts
│   ├── project.ts
│   └── scenes/
│       └── example.tsx
├── tsconfig.json
└── vite.config.ts
```

### Project Configuration (`src/project.ts`)
```typescript
import { makeProject } from '@motion-canvas/core';
import example from './scenes/example?scene';
import audio from '../audio/voice.mp3';

export default makeProject({
  scenes: [example],
  audio: audio, // Optional audio track
});
```

### Vite Configuration (`vite.config.ts`)
```typescript
import { defineConfig } from 'vite';
import motionCanvas from '@motion-canvas/vite-plugin';

export default defineConfig({
  plugins: [
    motionCanvas({
      project: './src/project.ts',
      output: './output',
    }),
  ],
});
```

---

## Core Concepts

### Scene Structure
```typescript
import { makeScene2D } from '@motion-canvas/2d';
import { createRef, waitFor } from '@motion-canvas/core';

export default makeScene2D(function* (view) {
  // Scene content and animations
  // Generator function describes animation flow
});
```

### Coordinate System
- **Origin**: Center of the screen (0, 0)
- **X-axis**: Positive right, negative left
- **Y-axis**: Positive down, negative up
- **Units**: Pixels by default

### Generator Functions
```typescript
// yield* - delegates to another generator
yield* circle().scale(2, 1); // Wait for animation to complete

// yield - pause for one frame
yield;

// waitFor - pause for specific duration
yield* waitFor(2); // Wait 2 seconds
```

---

## Components

### Basic Shapes

#### Rectangle
```typescript
import { Rect } from '@motion-canvas/2d';

<Rect
  width={200}
  height={100}
  fill="#ff6b6b"
  stroke="#333"
  lineWidth={2}
  radius={10} // Rounded corners
  position={[0, 0]}
/>
```

#### Circle
```typescript
import { Circle } from '@motion-canvas/2d';

<Circle
  width={200}
  height={200}
  fill="#4ecdc4"
  stroke="#333"
  lineWidth={2}
  position={[0, 0]}
/>
```

#### Line
```typescript
import { Line } from '@motion-canvas/2d';

<Line
  points={[
    [0, -50],   // Start point
    [100, 0],   // Middle point
    [0, 50]     // End point
  ]}
  stroke="#333"
  lineWidth={3}
  startArrow={true}
  endArrow={true}
  arrowSize={15}
  radius={10} // Rounded corners
  closed={false} // Connect last to first point
/>
```

### Text
```typescript
import { Txt } from '@motion-canvas/2d';

<Txt
  text="Hello World"
  fontSize={48}
  fontFamily="Arial"
  fontWeight={700}
  fill="#333"
  position={[0, 0]}
  textAlign="center"
  lineHeight={60}
  letterSpacing={2}
/>

// Shortcuts for styling
<Txt.b text="Bold Text" />     // Bold
<Txt.i text="Italic Text" />   // Italic
```

### Layout Container
```typescript
import { Layout } from '@motion-canvas/2d';

<Layout
  direction="column" // or "row"
  gap={20}
  alignItems="center"
  justifyContent="center"
  padding={[20, 30]} // [vertical, horizontal]
>
  <Rect width={100} height={50} fill="red" />
  <Rect width={100} height={50} fill="blue" />
</Layout>
```

### Media Components

#### Image
```typescript
import { Img } from '@motion-canvas/2d';
import imageSrc from '../images/example.png';

<Img
  src={imageSrc}
  width={300}
  height={200}
  radius={10}
  scale={1}
/>
```

#### Video
```typescript
import { Video } from '@motion-canvas/2d';
import videoSrc from '../videos/example.mp4';

const videoRef = createRef<Video>();

<Video
  ref={videoRef}
  src={videoSrc}
  width={640}
  height={360}
/>

// Control video playback
videoRef().play();
videoRef().pause();
```

---

## Animation & Tweening

### Property Animation
```typescript
const circle = createRef<Circle>();

// Basic animation: property(targetValue, duration)
yield* circle().scale(2, 1);
yield* circle().position([100, 50], 0.5);
yield* circle().fill('#ff0000', 2);

// With easing
import { easeInOutCubic } from '@motion-canvas/core';
yield* circle().scale(2, 1, easeInOutCubic);
```

### Parallel Animations
```typescript
import { all } from '@motion-canvas/core';

// Run animations simultaneously
yield* all(
  circle().scale(2, 1),
  circle().fill('#ff0000', 1),
  circle().position([100, 0], 1)
);
```

### Sequential Animations
```typescript
// Chain animations
yield* circle().scale(1.5, 0.5);
yield* circle().position([200, 0], 1);
yield* circle().scale(1, 0.5);
```

### Custom Tween
```typescript
import { tween, map } from '@motion-canvas/core';

yield* tween(2, value => {
  const x = map(-300, 300, value);
  circle().position.x(x);
});
```

### Animation Chaining
```typescript
// Using .to() for chaining (Signal method)
yield* circle().scale(1.5, 1).to(0.8, 0.5).to(1, 0.3);
```

---

## Signals & Reactive System

### Creating Signals
```typescript
import { createSignal } from '@motion-canvas/core';

const radius = createSignal(50);
const area = createSignal(() => Math.PI * radius() * radius());

// Get value
console.log(radius()); // 50

// Set value
radius(100);

// Animate signal
yield* radius(150, 2); // Animate to 150 over 2 seconds
```

### Signal Types
```typescript
// Primitive signals
const count = createSignal(0);
const name = createSignal('Motion Canvas');

// Vector signals
import { Vector2 } from '@motion-canvas/core';
const position = Vector2.createSignal([0, 0]);

// Color signals
import { Color } from '@motion-canvas/core';
const color = Color.createSignal('#ff0000');
```

### Computed Signals
```typescript
import { createComputed } from '@motion-canvas/core';

const width = createSignal(100);
const height = createSignal(50);
const area = createComputed(() => width() * height());
```

### Effects
```typescript
import { createEffect } from '@motion-canvas/core';

const position = createSignal([0, 0]);

// React to signal changes
createEffect(() => {
  console.log('Position changed:', position());
});
```

---

## Layout System

### Flexbox Properties
```typescript
<Layout
  // Direction
  direction="row" | "column" | "row-reverse" | "column-reverse"
  
  // Alignment
  alignItems="flex-start" | "center" | "flex-end" | "stretch"
  justifyContent="flex-start" | "center" | "flex-end" | "space-between" | "space-around"
  
  // Spacing
  gap={20} // or [rowGap, columnGap]
  padding={[10, 20]} // [vertical, horizontal] or number
  margin={10}
  
  // Wrapping
  wrap="nowrap" | "wrap" | "wrap-reverse"
>
  {/* Children */}
</Layout>
```

### Child Properties
```typescript
<Rect
  // Flex properties
  grow={1}
  shrink={0}
  basis="auto" | "content" | number
  alignSelf="auto" | "flex-start" | "center" | "flex-end"
  
  // Size
  size={[width, height]} // or null for auto
  minWidth={100}
  maxWidth={500}
  minHeight={50}
  maxHeight={300}
/>
```

### Positioning
```typescript
<Rect
  position={[x, y]}
  
  // Anchor shortcuts
  top={100}        // Y position from top
  bottom={100}     // Y position from bottom
  left={50}        // X position from left
  right={50}       // X position from right
  
  // Corner shortcuts
  topLeft={[x, y]}
  topRight={[x, y]}
  bottomLeft={[x, y]}
  bottomRight={[x, y]}
  
  // Center
  middle={[x, y]}  // Same as position for centered nodes
/>
```

---

## Media Support

### Audio
```typescript
// In project.ts
import audio from '../audio/voice.mp3';

export default makeProject({
  scenes: [example],
  audio: audio, // Add to project
});
```

### Image Formats
- **Supported**: PNG, JPEG, GIF, WebP, SVG
- **Usage**: Import and use with `<Img>` component

### Video Formats  
- **Supported**: MP4, WebM, OGV
- **Usage**: Import and use with `<Video>` component
- **Control**: Use refs to play/pause/seek

---

## Time Events

### Time Markers
```typescript
import { waitUntil } from '@motion-canvas/core';

// Set marker
yield* waitUntil('intro-end');

// Wait for marker (useful for audio sync)
yield* waitUntil('beat-drop');
```

### Timeline Control
```typescript
// Wait for specific duration
yield* waitFor(2.5);

// Conditional waiting
if (condition) {
  yield* waitFor(1);
}
```

---

## Effects & Shaders

### Built-in Effects
```typescript
<Rect
  // Shadow
  shadowColor="#000000"
  shadowBlur={10}
  shadowOffset={[5, 5]}
  
  // Filters
  filters={{
    blur: 5,
    brightness: 1.2,
    contrast: 1.1,
    saturate: 1.5
  }}
/>
```

### Custom Shaders
```typescript
<Rect
  shaders={[
    {
      fragment: `
        uniform float time;
        vec4 main(vec2 coord) {
          return vec4(coord, sin(time), 1.0);
        }
      `,
      uniforms: { time: () => useTime() }
    }
  ]}
/>
```

---

## Easing Functions

### Built-in Easing
```typescript
import {
  linear,
  easeIn, easeOut, easeInOut,
  easeInCubic, easeOutCubic, easeInOutCubic,
  easeInQuint, easeOutQuint, easeInOutQuint,
  easeInExpo, easeOutExpo, easeInOutExpo,
  easeInBack, easeOutBack, easeInOutBack,
  easeInElastic, easeOutElastic, easeInOutElastic,
  easeInBounce, easeOutBounce, easeInOutBounce
} from '@motion-canvas/core';

// Usage
yield* circle().scale(2, 1, easeOutElastic);
```

### Custom Easing
```typescript
// Bezier curve
import { cubicBezier } from '@motion-canvas/core';
const customEase = cubicBezier(0.25, 0.46, 0.45, 0.94);

// Custom function
const bounce = (t: number) => {
  return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
};
```

---

## Configuration

### Editor Configuration
```typescript
// vite.config.ts
export default defineConfig({
  plugins: [
    motionCanvas({
      project: './src/project.ts',
      output: './output',
      bufferedAssets: /\.(wav|ogg)$/,
      editor: '@motion-canvas/ui',
      proxy: {
        allowedMimeTypes: ['image/*', 'video/*'],
        allowListHosts: ['example.com']
      }
    }),
  ],
});
```

### Project Settings
```typescript
// src/project.ts
export default makeProject({
  scenes: [scene1, scene2],
  name: 'My Animation',
  audio: audioFile,
  
  // Scene settings
  background: '#1a1a1a',
  size: [1920, 1080], // Resolution
});
```

---

## Common Patterns

### References Pattern
```typescript
const circle = createRef<Circle>();
const text = createRef<Txt>();

view.add(
  <>
    <Circle ref={circle} />
    <Txt ref={text} />
  </>
);

// Use references
yield* all(
  circle().scale(2, 1),
  text().opacity(1, 0.5)
);
```

### State Management
```typescript
// Save and restore state
circle().save();
yield* circle().scale(2, 1);
yield* circle().restore(1); // Restore with animation
```

### Multiple References
```typescript
import { createRefArray } from '@motion-canvas/core';

const circles = createRefArray<Circle>();

view.add(
  <Layout>
    {range(5).map(i => 
      <Circle ref={circles[i]} />
    )}
  </Layout>
);

// Animate all circles
yield* all(
  ...circles.map(circle => circle.scale(2, 1))
);
```

### Conditional Animations
```typescript
const shouldAnimate = true;

if (shouldAnimate) {
  yield* circle().scale(2, 1);
} else {
  circle().scale(2); // Set immediately
}
```

### Loop Animations
```typescript
import { loop } from '@motion-canvas/core';

yield* loop(3, () => 
  circle().scale(1.2, 0.5).to(1, 0.5)
);
```

### Scene Transitions
```typescript
import { slideTransition, Direction } from '@motion-canvas/core';

export default makeScene2D(function* (view) {
  yield* slideTransition(Direction.Right);
  // Scene content
});
```

---

## Troubleshooting

### Common Issues

#### Animation Not Working
- Ensure you're using `yield*` for animations
- Check that duration is > 0
- Verify property names are correct

#### TypeScript Errors
- Make sure to import types correctly
- Use proper generic types for refs: `createRef<Circle>()`
- Check motion-canvas.d.ts is present

#### Performance Issues
- Use `cache={true}` for complex static elements
- Avoid creating too many nodes in loops
- Use `composite={true}` for effects

#### Audio Sync Issues
- Use `.wav` format for best sync (not `.mp3`)
- Use `waitUntil()` with audio markers
- Check audio offset in editor

### Debugging Tips

#### Logging
```typescript
import { useLogger } from '@motion-canvas/core';

const logger = useLogger();
logger.info('Debug message', { data: someValue });
```

#### Visual Debugging
```typescript
// Show node bounds
<Rect stroke="red" lineWidth={1} fill={null} />

// Add debug text
<Txt text={`Position: ${circle().position()}`} />
```

#### Time Debugging
```typescript
import { useTime } from '@motion-canvas/core';

const time = useTime();
console.log('Current time:', time());
```

### Performance Tips
- Use `createRef()` instead of `useRef()` for better performance
- Cache complex calculations with signals
- Prefer Layout over manual positioning
- Use `shaders` for GPU-accelerated effects
- Enable caching for static complex elements

---

## Quick Reference

### Essential Imports
```typescript
// Core
import { 
  makeScene2D, createRef, all, waitFor, waitUntil,
  tween, map, linear, easeInOutCubic
} from '@motion-canvas/core';

// Components
import { 
  Rect, Circle, Line, Txt, Layout, Img, Video
} from '@motion-canvas/2d';
```

### Animation Patterns
```typescript
// Basic property animation
yield* node().property(value, duration);

// Parallel animations
yield* all(
  node1().scale(2, 1),
  node2().opacity(0, 1)
);

// Chained animations
yield* node().scale(2, 1).to(1, 0.5);

// Custom tween
yield* tween(duration, progress => {
  node().rotation(progress * 360);
});
```

### Common Properties
- **Transform**: `position`, `scale`, `rotation`, `skew`
- **Appearance**: `fill`, `stroke`, `opacity`, `lineWidth`
- **Layout**: `width`, `height`, `margin`, `padding`
- **Text**: `fontSize`, `fontFamily`, `fontWeight`, `textAlign`
- **Effects**: `shadowBlur`, `shadowColor`, `filters`

This cheatsheet covers the essential aspects of Motion Canvas development. Refer to the official documentation at [motioncanvas.io](https://motioncanvas.io) for detailed API references and advanced features.