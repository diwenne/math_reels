# Manim Reel Generator

A pipeline for generating vertical (9:16) Manim animation reels optimized for social media platforms like Instagram Reels, TikTok, and YouTube Shorts.

## Quick Start

```bash
# Single reel
python -m pipeline.generate "Concept Name" "Description of the animation" 15

# Batch generation
python -m pipeline.batch_generate batches/fractals_batch.json
```

## Project Structure

```
reel_generator_2/
├── config.py                 # Configuration (API keys, paths, dimensions)
├── manim.cfg                 # Manim settings (1080x1920 vertical)
├── pipeline/
│   ├── generate.py           # Main entry point
│   ├── generator.py          # LLM interaction (Gemini)
│   ├── prompts.py            # System prompt for Manim code generation
│   └── batch_generate.py     # Batch processing multiple concepts
├── rendering/
│   └── renderer.py           # Manim execution and video output
├── batches/                  # JSON files for batch generation
└── output/                   # Generated reels (gitignored)
```

---

## LLM Instructions for Future Development

### Core Philosophy

This pipeline generates **visually stunning, fast-paced math animations**. The goal is to create content that:

1. **Wows the viewer immediately** with premium aesthetics
2. **Prioritizes visuals over explanations** - show, don't tell
3. **Uses a steady, hypnotic rhythm** - no speeding up or slowing down
4. **Fits perfectly in the 9:16 vertical format** with strict zone boundaries

---

### Layout System (CRITICAL)

The screen is divided into **3 strict zones**. Elements must NOT overlap.

```
┌─────────────────────────────────────┐
│           TOP ZONE (Title)          │  UP * 5.0
│            font_size=42             │
├─────────────────────────────────────┤
│                                     │
│         CENTER ZONE (Stage)         │  UP*1.5 to DOWN*1.5
│         Main animations here        │
│                                     │
├─────────────────────────────────────┤
│        BOTTOM ZONE (Equation)       │  DOWN * 5.0
│           font_size=48              │
└─────────────────────────────────────┘
```

**Safe Width**: 8.0 units (from x=-4 to x=+4). Never let content go off-screen horizontally.

---

### Pacing Rules

**"Snap-and-Hold" Rhythm**:

- **Morph**: `run_time = 0.3` (Fast transition)
- **Pause**: `self.wait(0.5)` (Brief hold to see the step)

**CRITICAL RULES**:

1. **NO ACCELERATION**: Use constant timing. Never do `run_time = 1.0 if i < 3 else 0.5`.
2. **LINEAR PROGRESSION**: Show every step (1, 2, 3... Final). Do not skip.
3. **ITERATE UNTIL THE END**: Use the full duration. Don't stop early.
4. **SHORT CONCLUSION**: Only 2s hold at the very end. Prioritize more iterations.

**For Fractals**: Limit to 12-14 iterations max to avoid exponential segment explosion.

---

### Aesthetics

**Default Theme**: WARM / SUNSET

```python
c1, c2 = RED, ORANGE  # or GOLD, MAROON or PINK, YELLOW
```

**Color Usage**:

- **Theme Gradient**: Title, Diagrams, Key Equations
- **Pure White**: Labels, Axis Lines, Secondary Text
- **Background**: Always BLACK

**Text Classes**:

- `MathTex(r"...", font_size=...)` for equations (PURE MATH ONLY, no English words)
- `Text("...", font_size=...)` for titles and labels

---

### Animation Rules

**Intro**:

- Title: `self.add(title)` immediately (no animation)
- Center + Equation: Animate **SIMULTANEOUSLY** using `self.play(Create(diagram), Write(equation))`
- **Use `Create()` for diagrams, `Write()` for equations**. NO shifting/sliding in.

**Banned Patterns**:

- `fix_in_frame()` - Not supported in 2D Scene
- `FadeIn` for intro (use `Create`/`Write` instead)
- Sliding/shifting as intro transition
- Words in `MathTex` (only pure mathematical notation)

---

### Horizontal Containment

For growing patterns (Recamán, Fractals):

1. **Pre-calculate bounds**: Know the max extent of the pattern
2. **Scale to fit**: Set `unit_size` or `scale()` so it fits in width 8.0
3. **Alternative**: Use camera zoom out as it grows

---

### Common Concepts & Their Considerations

| Concept           | Starting Shape              | Key Consideration                |
| ----------------- | --------------------------- | -------------------------------- |
| Levy C Curve      | `+` (Plus sign, 4 segments) | Cap at 12 iterations             |
| Koch Snowflake    | Triangle                    | Each side triples segments       |
| Sierpinski        | Triangle                    | Remove center recursively        |
| Recamán           | Number line                 | Scale to fit max value           |
| Hilbert Curve     | U-shape                     | Space-filling, cap iterations    |
| Fourier Epicycles | Circles                     | Computing/animating many circles |

---

### Batch Generation

Create a JSON file:

```json
[
  {
    "concept": "Koch Snowflake",
    "description": "Recursive triangle construction...",
    "length": 15
  },
  {
    "concept": "Dragon Curve",
    "description": "Paper folding fractal...",
    "length": 12
  }
]
```

Run:

```bash
python -m pipeline.batch_generate batches/my_batch.json
```

---

### Debugging Common Errors

| Error                    | Cause                | Fix                                       |
| ------------------------ | -------------------- | ----------------------------------------- |
| `fix_in_frame` not found | Used in 2D Scene     | Remove the call, just use `self.add()`    |
| Content off-screen       | No bounds checking   | Scale down or zoom out                    |
| Render hangs             | Too many iterations  | Cap fractal iterations at 12-14           |
| `NotFound` model error   | Invalid Gemini model | Check `config.py`, use `gemini-1.5-flash` |

---

### API & Dependencies

**LLM**: Google Gemini (via `google-generativeai`, deprecated - migrate to `google.genai`)
**Rendering**: Manim v0.19+
**Other**: `python-dotenv`, `numpy`, `ffmpeg`

**Environment Variables** (in `.env`):

```
GEMINI_API_KEY=your_key_here
```

---

### Output

Renders are saved to:

```
output/<concept_name>/
├── scene.py              # Generated Manim code
├── visual_plan.json      # LLM output
└── final_reel.mp4        # Final video (1080x1920 @ 60fps)
```

---

## Summary for LLMs

When generating Manim code for this pipeline:

1. **Layout**: 3 zones, respect boundaries, max width 8.0
2. **Pacing**: Snap-and-Hold (0.3s move, 0.5s wait), constant rhythm
3. **Theme**: Warm colors (Red/Orange/Gold), black background
4. **Intro**: Simultaneous `Create()` + `Write()`, no shifting
5. **Equations**: Pure math only, no English text in MathTex
6. **Fractals**: Cap iterations at 12-14, scale to fit
7. **Banned**: `fix_in_frame()`, adaptive timing, FadeIn for intro

Always return valid JSON with `manim_code` and `estimated_duration` keys.
