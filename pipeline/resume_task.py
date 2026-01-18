
from pathlib import Path
import subprocess
from video.youtube import download_and_crop_youtube
from config import PROJECT_ROOT, REEL_WIDTH, REEL_HEIGHT, HALF_HEIGHT

def get_video_duration(video_path: Path) -> float:
    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(video_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Failed to get video duration: {result.stderr}")
    return float(result.stdout.strip())

def resume_pipeline():
    output_name = "infinite_sum_reel"
    youtube_url = "https://www.youtube.com/watch?v=J90L73YOR3k"
    youtube_start = 30
    youtube_volume = 0.2
    
    # Paths
    animation_path = PROJECT_ROOT / "output" / output_name / "animation.mp4"
    final_dir = PROJECT_ROOT / "final_reels" / output_name
    final_dir.mkdir(parents=True, exist_ok=True)
    final_path = final_dir / "final.mp4"

    if not animation_path.exists():
        print(f"Error: Animation file not found at {animation_path}")
        return

    print(f"Resuming pipeline for: {output_name}")
    
    # Get duration
    duration = get_video_duration(animation_path)
    print(f"Animation duration: {duration:.2f}s")
    
    # Download YouTube
    print(f"Downloading YouTube background ({duration:.2f}s)...")
    youtube_cropped = download_and_crop_youtube(
        url=youtube_url,
        start_time=youtube_start,
        duration=duration,
        output_name=output_name
    )
    
    # Combine
    print("Combining videos...")
    filter_complex = (
        f"[0:v]scale={REEL_WIDTH}:{HALF_HEIGHT}[top];"
        f"[1:v]trim=duration={duration},setpts=PTS-STARTPTS,scale={REEL_WIDTH}:{HALF_HEIGHT}[bottom];"
        f"[top][bottom]vstack=inputs=2[v];"
        f"[1:a]atrim=duration={duration},asetpts=PTS-STARTPTS,volume={youtube_volume}[a]"
    )
    
    stack_cmd = [
        "ffmpeg",
        "-i", str(animation_path),
        "-i", str(youtube_cropped),
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-map", "[a]",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        "-y",
        str(final_path)
    ]
    
    subprocess.run(stack_cmd, check=True)
    print(f"✓ DONE! Final reel saved to: {final_path}")

if __name__ == "__main__":
    resume_pipeline()
