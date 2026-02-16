
import subprocess
import json
import sys
from pathlib import Path

def render_from_plan(visual_plan_path: Path, output_file: Path):
    """
    Renders a Manim scene based on the visual plan.
    """
    plan = json.loads(visual_plan_path.read_text())
    manim_code = plan.get("manim_code", "")
    
    # Save code to scene.py in the same folder if not already there
    scene_path = visual_plan_path.parent / "scene.py"
    if not scene_path.exists():
        # Wrap in minimal scene if needed, but generator usually handles this
        scene_path.write_text(manim_code)
    
    # We assume the class name is 'GeneratedScene' based on generator.py logic
    # But it might be different if the LLM generated a full file.
    # We can try to grep the class name or just rely on 'GeneratedScene'
    
    # Quick regex to find class name
    import re
    match = re.search(r"class\s+(\w+)\s*\(", manim_code)
    scene_name = match.group(1) if match else "GeneratedScene"
    
    cmd = [
        "manim",
        "--quality", "h", # High quality rendering
        "--resolution", "1080,1920",
        "--fps", "60",
        "--media_dir", str(visual_plan_path.parent / "media"),
        "-o", str(output_file.name),
        str(scene_path),
        scene_name
    ]
    
    print(f"Executing: {' '.join(cmd)}")
    
    # Manim writes output to specific folders (media/videos/scene/quality/name.mp4)
    # We need to capture where it puts it and move it to output_file
    
    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        print("Manim render failed!")
        raise RuntimeError("Manim render failed")
    
    # Locate the output file
    # Default manim structure: media_dir/videos/scene_filename/quality/scene_name.mp4
    # But since we passed -o output_file.name, it might be in media_dir/videos/scene_filename/quality/output_file.name.mp4
    # Actually -o specifies the filename. 
    
    # Let's search for the file
    possible_files = list((visual_plan_path.parent / "media").glob("**/*.mp4"))
    if not possible_files:
        raise FileNotFoundError("Could not find rendered video file.")
        
    # Get the most recently modified mp4
    latest_video = max(possible_files, key=os.path.getmtime)
    
    # Move/Copy to final destination
    import shutil
    shutil.move(str(latest_video), str(output_file))
    print(f"Rendered video saved to: {output_file}")

import os
