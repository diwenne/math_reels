"""Simplified pipeline: Generate Manim animation ONLY."""

import sys
from pathlib import Path
from config import PROJECT_ROOT, OUTPUT_DIR
from pipeline.generator import generate_content
from rendering.renderer import render_from_plan

def create_reel(
    concept: str,
    description: str,
    length: int = 30,
    output_name: str = None,
    template_path: str = None
) -> Path:
    """
    Create a Manim reel from concept and description.
    """
    if output_name is None:
        output_name = concept.lower().replace(" ", "_")
    
    print(f"\n{'='*60}")
    print(f"CREATING MANIM REEL: {concept}")
    print(f"{'='*60}\n")
    
    # Step 1: Generate Manim content
    print("Step 1/2: Generating Manim content...")
    
    template_code = None
    if template_path:
        template_file = Path(template_path)
        if template_file.exists():
             print(f"  [TEMPLATE MODE] Using style from: {template_file.name}")
             template_code = template_file.read_text()

    content_result = generate_content(
        concept=concept,
        description=description,
        length=length,
        output_name=output_name,
        template_code=template_code
    )
    
    # Step 2: Render
    print("\nStep 2/2: Rendering Manim animation...")
    visual_plan_path = content_result.output_dir / "visual_plan.json"
    animation_path = content_result.output_dir / "final_reel.mp4"
    
    render_from_plan(visual_plan_path, animation_path)
    
    print(f"\n{'='*60}")
    print(f"✓ REEL COMPLETE: {animation_path}")
    print(f"{'='*60}\n")
    
    return animation_path

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python -m pipeline.generate '<concept>' '<description>' [length] [output_name]")
        sys.exit(1)
    
    concept = sys.argv[1]
    description = sys.argv[2]
    length = int(sys.argv[3]) if len(sys.argv) > 3 else 30
    output_name = sys.argv[4] if len(sys.argv) > 4 else None
    
    create_reel(concept, description, length, output_name)
