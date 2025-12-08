#!/usr/bin/env python3
"""
Comprehensive test of Qwen-Image-Edit-2509 editing capabilities.
Tests different editing types on all source images.
"""

import torch
from diffusers import QwenImageEditPlusPipeline
from PIL import Image
import os
import time
from pathlib import Path

def setup_pipeline(model_path):
    """Load pipeline with sequential CPU offloading for memory efficiency."""
    print("=" * 60)
    print("Loading Qwen-Image-Edit-2509 Pipeline")
    print("=" * 60)
    
    start = time.time()
    
    pipe = QwenImageEditPlusPipeline.from_pretrained(
        model_path,
        torch_dtype=torch.bfloat16  # Use bfloat16, not float16
    )
    
    # Use sequential CPU offloading (moves components on demand)
    pipe.enable_sequential_cpu_offload()
    
    load_time = time.time() - start
    print(f"✅ Pipeline loaded in {load_time:.1f}s")
    print()
    
    return pipe

def run_comprehensive_tests():
    """Run comprehensive editing tests on all source images."""
    
    # Configuration
    model_path = "/mnt/essdee/ComfyUI/models/diffusers/qwen-image-edit-2509"
    source_dir = Path("/home/tim/source/activity/FLENwheel/test_data/source")
    output_dir = Path("/home/tim/source/activity/FLENwheel/test_data/enriched/v1")
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Define test categories
    editing_tests = {
        "background": [
            "Change background to a forest with trees, keep the person identical",
            "Change background to a beach with ocean, keep the person identical",
            "Change background to a modern studio, keep the person identical",
            "Change background to an urban city street, keep the person identical",
        ],
        "lighting": [
            "Add warm sunset lighting, keep the person identical",
            "Add professional studio lighting, keep the person identical",
            "Add dramatic side lighting, keep the person identical",
            "Add soft diffused lighting, keep the person identical",
        ],
        "angle": [
            "Change camera angle slightly to the left, maintain character appearance",
            "Change to profile view from the side, preserve facial features",
            "Show from a slightly higher camera angle, keep features identical",
        ],
    }
    
    # Find all source images
    source_images = sorted(list(source_dir.glob("*.png")) + list(source_dir.glob("*.jpg")))
    
    if not source_images:
        print(f"❌ No images found in {source_dir}")
        return
    
    print(f"Found {len(source_images)} source images:")
    for img_path in source_images:
        print(f"  - {img_path.name}")
    print()
    
    # Load pipeline
    pipe = setup_pipeline(model_path)
    
    # Run tests
    total_tests = len(source_images) * sum(len(prompts) for prompts in editing_tests.values())
    test_count = 0
    
    print("=" * 60)
    print(f"Running {total_tests} editing tests")
    print("=" * 60)
    print()
    
    results = []
    
    for source_path in source_images:
        source_name = source_path.stem
        print(f"\n{'='*60}")
        print(f"Processing: {source_path.name}")
        print(f"{'='*60}\n")
        
        # Load source image
        source_image = Image.open(source_path)
        
        # Save source image to output for comparison
        source_output = output_dir / f"{source_name}_source.png"
        source_image.save(source_output)
        
        for category, prompts in editing_tests.items():
            print(f"\n--- Category: {category.upper()} ---")
            
            for idx, prompt in enumerate(prompts, 1):
                test_count += 1
                
                print(f"\n[{test_count}/{total_tests}] {category}_{idx}")
                print(f"Prompt: {prompt}")
                
                start_time = time.time()
                
                try:
                    # Generate edited image with correct parameters
                    with torch.inference_mode():
                        output = pipe(
                            image=source_image,
                            prompt=prompt,
                            negative_prompt=" ",  # Important: space, not empty
                            num_inference_steps=40,
                            true_cfg_scale=4.0,
                            guidance_scale=1.0,
                            generator=torch.manual_seed(test_count),  # Different seed per test
                        )
                    
                    result = output.images[0]
                    
                    # Save result
                    output_filename = f"{source_name}_{category}_{idx:02d}.png"
                    output_path = output_dir / output_filename
                    result.save(output_path)
                    
                    elapsed = time.time() - start_time
                    
                    print(f"✅ Saved: {output_filename}")
                    print(f"   Time: {elapsed:.1f}s")
                    
                    results.append({
                        "source": source_name,
                        "category": category,
                        "idx": idx,
                        "prompt": prompt,
                        "output": output_filename,
                        "time": elapsed,
                        "success": True,
                        "error": None
                    })
                    
                except Exception as e:
                    elapsed = time.time() - start_time
                    
                    print(f"❌ Error: {e}")
                    print(f"   Time: {elapsed:.1f}s")
                    
                    results.append({
                        "source": source_name,
                        "category": category,
                        "idx": idx,
                        "prompt": prompt,
                        "output": None,
                        "time": elapsed,
                        "success": False,
                        "error": str(e)
                    })
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    successful = sum(1 for r in results if r["success"])
    failed = sum(1 for r in results if not r["success"])
    avg_time = sum(r["time"] for r in results) / len(results) if results else 0
    
    print(f"\nTotal tests: {len(results)}")
    print(f"Successful: {successful} ({successful/len(results)*100:.1f}%)")
    print(f"Failed: {failed} ({failed/len(results)*100:.1f}%)")
    print(f"Average time per edit: {avg_time:.1f}s")
    
    print(f"\n✅ All outputs saved to: {output_dir}")
    
    # Save results log
    log_path = output_dir / "test_results.txt"
    with open(log_path, "w") as f:
        f.write("QWEN IMAGE EDIT COMPREHENSIVE TEST RESULTS\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Model: {model_path}\n")
        f.write(f"Source images: {len(source_images)}\n")
        f.write(f"Total tests: {len(results)}\n")
        f.write(f"Successful: {successful} ({successful/len(results)*100:.1f}%)\n")
        f.write(f"Failed: {failed} ({failed/len(results)*100:.1f}%)\n")
        f.write(f"Average time: {avg_time:.1f}s per edit\n\n")
        
        f.write("DETAILED RESULTS:\n")
        f.write("=" * 60 + "\n\n")
        
        for r in results:
            status = "✅" if r["success"] else "❌"
            f.write(f"{status} {r['source']}_{r['category']}_{r['idx']:02d}\n")
            f.write(f"   Prompt: {r['prompt']}\n")
            f.write(f"   Time: {r['time']:.1f}s\n")
            if r["output"]:
                f.write(f"   Output: {r['output']}\n")
            if r["error"]:
                f.write(f"   Error: {r['error']}\n")
            f.write("\n")
    
    print(f"📄 Results log saved to: {log_path}")
    
    print("\n" + "=" * 60)
    print("NEXT STEPS")
    print("=" * 60)
    print(f"\n1. Review all generated images in: {output_dir}")
    print("2. For each image, assess:")
    print("   - Character identity preservation (same person?)")
    print("   - Edit effectiveness (did background/lighting change?)")
    print("   - Image quality (artifacts, distortions?)")
    print("3. Calculate character consistency rate (target: 70%+)")
    print("4. Document findings for decision making")
    print()

if __name__ == "__main__":
    run_comprehensive_tests()
