"""Content generator using GPT or Gemini - outputs Manim scene code only."""

import json
import textwrap
from pathlib import Path
from dataclasses import dataclass

import sys
# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import OPENAI_API_KEY, GEMINI_API_KEY, LLM_MODEL, OUTPUT_DIR
from pipeline.prompts import COMBINED_GENERATION_PROMPT


@dataclass
class ContentOutput:
    """Output from content generation."""
    manim_code: str
    estimated_duration: int
    output_dir: Path


def generate_content(
    concept: str,
    description: str,
    length: int,
    output_name: str = None,
    template_code: str = None
) -> ContentOutput:
    """Generate Manim scene code for an animation."""
    
    user_prompt = f"""Concept: {concept}
Description: {description}
Target length: {length} seconds MINIMUM. Use the FULL time to explain thoroughly. Don't rush.

"""

    if template_code:
        user_prompt += f"""
IMPORTANT: STYLE TRANSFER MODE
The user has provided a TEMPLATE scene below. You must:
1. COPY the exact visual style (colors, fonts, sizes, grid style, background).
2. COPY the exact code structure (setup, intro, main loop, outro).
3. ONLY change the mathematical content/objects to explain '{concept}'.
4. Keep the same animation pacing and transitions.

TEMPLATE CODE:
```python
{template_code}
```
"""

    user_prompt += "Generate the complete Manim scene code."

    
    # Select prompt (Always use 2D vertical prompt for now)
    system_prompt = COMBINED_GENERATION_PROMPT
    
    # Check if using Gemini or OpenAI
    if LLM_MODEL.startswith("gemini"):
        content = _generate_with_gemini(user_prompt, system_prompt)
    else:
        content = _generate_with_openai(user_prompt, system_prompt)
    
    # Clean the code (simple strip)
    content = content.strip()
    # If the model returned markdown json block, strip it
    if content.startswith("```json"):
        content = content[7:]
    if content.endswith("```"):
        content = content[:-3]
    
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        # Fallback if valid JSON wasn't returned, sometimes raw text comes
        print("Warning: LLM did not return valid JSON. Attempting to parse raw.")
        data = {"manim_code": content, "estimated_duration": length}
    
    # Create output directory
    if output_name is None:
        output_name = concept.lower().replace(" ", "_")
    
    reel_output_dir = OUTPUT_DIR / output_name
    reel_output_dir.mkdir(exist_ok=True)
    
    # Remove any extra newlines or BOM marks
    manim_code = data.get("manim_code", "").strip()

    # Save visual_plan.json (for reference/debugging)
    (reel_output_dir / "visual_plan.json").write_text(json.dumps({
        "manim_code": manim_code,
        "estimated_duration": data.get("estimated_duration", length)
    }, indent=2))
    
    # Generate scene.py logic
    # Detect if LLM gave a full file or just construct body
    is_full_file = ('class ' in manim_code and 'Scene' in manim_code and 'def construct' in manim_code)
    
    if is_full_file:
        scene_content = f'''"""Generated Manim scene for: {concept}"""
from manim import *
import random
import numpy as np

{manim_code}
'''
    else:
        # Wrap the code
        import re
        # Strip standalone def construct line
        manim_code = re.sub(r'^\s*def\s+construct\s*\(\s*self\s*\)\s*:\s*$', '', manim_code, flags=re.MULTILINE)
        manim_code = re.sub(r'^\s*def\s+construct\s*\(\s*self\s*\)\s*->\s*None\s*:\s*$', '', manim_code, flags=re.MULTILINE)
        
        manim_code = textwrap.dedent(manim_code).strip()
        
        lines = []
        for line in manim_code.split('\n'):
            if line.strip():
                lines.append("        " + line)
            else:
                lines.append("")
        
        scene_content = f'''"""Generated Manim scene for: {concept}"""
from manim import *
import random
import numpy as np

class GeneratedScene(Scene):
    def construct(self):
{chr(10).join(lines)}
'''
    
    (reel_output_dir / "scene.py").write_text(scene_content)
    
    return ContentOutput(
        manim_code=manim_code,
        estimated_duration=data.get("estimated_duration", length),
        output_dir=reel_output_dir
    )


def _generate_with_openai(user_prompt: str, system_prompt: str) -> str:
    """Generate content using OpenAI API."""
    from openai import OpenAI
    
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY not set. Check your .env file.")
    
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"}
    )
    
    return response.choices[0].message.content


def _generate_with_gemini(user_prompt: str, system_prompt: str) -> str:
    """Generate content using Google Gemini API."""
    import google.generativeai as genai
    
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not set. Check your .env file.")
    
    genai.configure(api_key=GEMINI_API_KEY)
    
    model = genai.GenerativeModel(
        model_name=LLM_MODEL,
        system_instruction=system_prompt,
        generation_config={
            "response_mime_type": "application/json"
        }
    )
    
    response = model.generate_content(user_prompt)
    return response.text
