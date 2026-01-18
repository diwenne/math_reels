"""Batch generation script for creating multiple reels sequentially."""

import sys
import json
import time
from pathlib import Path
from pipeline.generate import create_reel

def run_batch(batch_file: str):
    path = Path(batch_file)
    if not path.exists():
        print(f"Error: Batch file not found at {path}")
        sys.exit(1)
        
    try:
        tasks = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        sys.exit(1)
        
    if not isinstance(tasks, list):
        print("Error: Batch file must contain a JSON list of objects.")
        sys.exit(1)
        
    print(f"\nStarting Batch Generation: {len(tasks)} reels queued.")
    
    for i, task in enumerate(tasks):
        concept = task.get("concept")
        description = task.get("description")
        length = task.get("length", 30)
        output_name = task.get("output_name")
        
        if not concept or not description:
            print(f"Skipping task {i+1}: Missing 'concept' or 'description'")
            continue
            
        print(f"\n>>> PROCESSING TASK {i+1}/{len(tasks)}: {concept}")
        
        try:
            create_reel(concept, description, length, output_name)
        except Exception as e:
            print(f"FAILED task {concept}: {e}")
            import traceback
            traceback.print_exc()
            
        # Small cooldown between tasks to be safe with APIs/resources
        if i < len(tasks) - 1:
            print("Cooling down for 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m pipeline.batch_generate <path_to_json_file>")
        print("Example: python -m pipeline.batch_generate batches/example.json")
        sys.exit(1)
        
    run_batch(sys.argv[1])
