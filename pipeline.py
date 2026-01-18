import os
import sys
import argparse
import subprocess
import google.generativeai as genai
from dotenv import load_dotenv
from system_prompt import MANIM_SYSTEM_PROMPT

# Load environment variables from .env file
load_dotenv()

def generate_manim_code(concept, description, length, model_name="gemini-1.5-pro-latest"):
    """
    Prompts the LLM to generate Manim code.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        sys.exit(1)

    genai.configure(api_key=api_key)
    
    # Configure the model
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name=model_name,
        generation_config=generation_config,
        system_instruction=MANIM_SYSTEM_PROMPT,
    )

    user_message = f"""
    Generate a Manim animation for the following request:
    
    **Concept**: {concept}
    **Description**: {description}
    **Target Length**: {length}
    """

    print(f"Generating code using {model_name}...")
    try:
        response = model.generate_content(user_message)
        return response.text
    except Exception as e:
        print(f"Error generating content: {e}")
        sys.exit(1)

def clean_code(code_text):
    """
    Strips markdown formatting from the generated code.
    """
    code_text = code_text.strip()
    if code_text.startswith("```python"):
        code_text = code_text[9:]
    elif code_text.startswith("```"):
        code_text = code_text[3:]
    
    if code_text.endswith("```"):
        code_text = code_text[:-3]
    
    return code_text.strip()

def render_scene(filename, scene_name="GenScene", quality="l", preview=False):
    """
    Renders the Manim scene.
    Quality options: -ql (low), -qm (medium), -qh (high), -qk (4k)
    """
    cmd = ["manim", f"-q{quality}", filename, scene_name]
    if preview:
        cmd.append("-p")
    
    print(f"Executing: {' '.join(cmd)}")
    subprocess.run(cmd, check=False) # check=False so script doesn't crash on render error, just logs it

def main():
    parser = argparse.ArgumentParser(description="Generate and render Manim animations using Gemini.")
    parser.add_argument("concept", help="Name of the math concept")
    parser.add_argument("description", help="Description of the animation")
    parser.add_argument("length", help="Desired length (e.g., '30 seconds')")
    parser.add_argument("--model", default="gemini-1.5-pro-latest", help="Gemini model to use")
    parser.add_argument("--output", default="generated_scene.py", help="Output python filename")
    parser.add_argument("--quality", default="l", choices=["l", "m", "h", "k"], help="Render quality (l=low, m=medium, h=high, k=4k)")
    parser.add_argument("--preview", action="store_true", help="Automatically open the video after rendering")

    args = parser.parse_args()

    # 1. Generate Code
    raw_code = generate_manim_code(args.concept, args.description, args.length, args.model)
    
    # 2. Clean Code
    final_code = clean_code(raw_code)
    
    # 3. Save Code
    with open(args.output, "w") as f:
        f.write(final_code)
    print(f"Code saved to {args.output}")

    # 4. Render
    render_scene(args.output, quality=args.quality, preview=args.preview)

if __name__ == "__main__":
    main()
