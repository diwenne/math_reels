# Sierpinski Triangle

A mesmerizing fractal animation showing the recursive construction of the Sierpinski Triangle (Sierpinski Gasket).

## Quick Start

```bash
python -m pipeline.generate "Sierpinski Triangle" "Recursive triangle fractal formed by removing center triangles" 15
```

## Concept Overview

The **Sierpinski Triangle** is a fractal created by:

1. Starting with an equilateral triangle
2. Connecting the midpoints of each side to form 4 smaller triangles
3. Removing the center triangle
4. Repeating steps 2-3 on each remaining triangle

```
Iteration 0:        Iteration 1:        Iteration 2:
    ▲                   ▲                   ▲
   ╱ ╲                 ╱ ╲                 ╱ ╲
  ╱   ╲               ▲   ▲               ▲   ▲
 ╱     ╲             ╱ ╲ ╱ ╲             ╱ ╲ ╱ ╲
▲───────▲           ▲   ▲   ▲           ▲ ▲ ▲ ▲ ▲
                       (center           (pattern
                        removed)          repeats)
```

---

## Animation Guidelines

### Layout Zones

| Zone   | Position  | Content                 |
| ------ | --------- | ----------------------- |
| Top    | UP \* 5.0 | Title (font_size=42)    |
| Center | ±1.5      | Triangle animation      |
| Bottom | DOWN \* 5 | Equation (font_size=48) |

### Recommended Equation

```python
MathTex(r"T_n = 3^n \text{ triangles}", font_size=48)
# Or pure math version:
MathTex(r"T_n = 3^n", font_size=48)
```

### Key Considerations

| Aspect         | Recommendation                                      |
| -------------- | --------------------------------------------------- |
| Max Iterations | **6-8** (beyond 8, triangles become too small)      |
| Triangle Count | Grows as 3^n (3, 9, 27, 81, 243...)                 |
| Scaling        | Use `scale_to_fit_width(7.0)` to stay within bounds |
| Color Scheme   | Warm gradient (RED → ORANGE) or (GOLD → MAROON)     |

### Pacing

```python
# Per iteration
run_time = 0.2  # Fast morph
self.wait(0.3)  # Brief hold

# End hold
self.wait(2.0)  # Final pause
```

---

## Implementation Approach

### Method 1: Polygon Replacement

```python
def subdivide_triangle(triangle):
    """Split triangle into 3 corner triangles, removing center."""
    p1, p2, p3 = triangle.get_vertices()
    m12 = (p1 + p2) / 2
    m23 = (p2 + p3) / 2
    m31 = (p3 + p1) / 2

    return [
        Polygon(p1, m12, m31),   # Top corner
        Polygon(m12, p2, m23),   # Right corner
        Polygon(m31, m23, p3),   # Left corner
    ]
    # Center triangle (m12, m23, m31) is removed
```

### Method 2: Chaos Game (Alternative)

Randomly plot points using the chaos game algorithm:

1. Pick 3 vertices of a triangle
2. Start at a random point
3. Repeatedly move halfway toward a random vertex
4. Plot each point

This naturally forms the Sierpinski pattern.

---

## Common Errors & Fixes

| Error                | Cause                      | Fix                               |
| -------------------- | -------------------------- | --------------------------------- |
| Triangles too small  | Too many iterations        | Cap at 6-8 iterations             |
| Pattern off-screen   | No containment             | Scale to fit width 7.0            |
| Lag during animation | Too many mobjects at once  | Use `VGroup` and batch transforms |
| Center not removed   | Logic error in subdivision | Verify midpoint calculations      |

---

## Expected Output

```
output/sierpinski_triangle/
├── scene.py              # Generated Manim code
├── visual_plan.json      # LLM output
└── final_reel.mp4        # Final video (1080x1920 @ 60fps)
```

## Mathematical Properties

- **Fractal Dimension**: ~1.585 (log(3)/log(2))
- **Self-Similarity**: Contains 3 copies of itself at 1/2 scale
- **Area**: Approaches 0 as iterations → ∞
- **Perimeter**: Approaches ∞ as iterations → ∞

---

## Related Concepts

- **Koch Snowflake**: Another recursive fractal (edge-based)
- **Sierpinski Carpet**: 2D square version
- **Pascal's Triangle**: Odd entries form Sierpinski pattern
- **Chaos Game**: Probabilistic construction method
