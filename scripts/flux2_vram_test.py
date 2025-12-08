#!/usr/bin/env python3
"""
FLUX2 VRAM Test Script

Tests FLUX2-dev model with NF4 quantization on RTX 4090 to verify VRAM requirements.
Measures VRAM usage with different reference image counts (1, 3, 5).

Usage:
    python scripts/flux2_vram_test.py [--model-id MODEL_ID] [--use-nf4]
"""

import argparse
import gc
import time
from pathlib import Path

import torch
from PIL import Image
from diffusers import Flux2Pipeline, Flux2Transformer2DModel, BitsAndBytesConfig
from diffusers.utils import load_image


def get_vram_usage():
    """Get current VRAM usage in GB."""
    if torch.cuda.is_available():
        return torch.cuda.memory_allocated() / 1024**3
    return 0


def get_peak_vram():
    """Get peak VRAM usage in GB."""
    if torch.cuda.is_available():
        return torch.cuda.max_memory_allocated() / 1024**3
    return 0


def reset_peak_vram():
    """Reset peak VRAM tracking."""
    if torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats()


def clear_memory():
    """Clear GPU memory."""
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


def load_pipeline_nf4(model_id: str):
    """Load FLUX2 pipeline with NF4 quantization."""
    print(f"\n🔧 Loading FLUX2 with NF4 quantization from {model_id}...")
    
    # NF4 quantization config
    nf4_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16
    )
    
    # Load quantized transformer
    transformer = Flux2Transformer2DModel.from_pretrained(
        model_id,
        subfolder="transformer" if "NF4" not in model_id else None,
        quantization_config=nf4_config,
        torch_dtype=torch.bfloat16
    )
    
    # Load pipeline with quantized transformer
    pipe = Flux2Pipeline.from_pretrained(
        "black-forest-labs/FLUX.2-dev" if "NF4" in model_id else model_id,
        transformer=transformer,
        torch_dtype=torch.bfloat16
    )
    
    pipe.enable_model_cpu_offload()
    
    print(f"✅ Pipeline loaded. VRAM after loading: {get_vram_usage():.2f}GB")
    return pipe


def load_pipeline_standard(model_id: str):
    """Load FLUX2 pipeline without quantization (bfloat16)."""
    print(f"\n🔧 Loading FLUX2 (standard bfloat16) from {model_id}...")
    
    pipe = Flux2Pipeline.from_pretrained(
        model_id,
        torch_dtype=torch.bfloat16
    )
    pipe.enable_model_cpu_offload()
    
    print(f"✅ Pipeline loaded. VRAM after loading: {get_vram_usage():.2f}GB")
    return pipe


def create_test_image(color: str, size: tuple = (512, 512)) -> Image.Image:
    """Create a simple test image."""
    from PIL import ImageDraw
    
    img = Image.new("RGB", size, color=color)
    draw = ImageDraw.Draw(img)
    
    # Add some features so it's not blank
    draw.rectangle([100, 100, 400, 400], outline="white", width=5)
    draw.text((size[0]//2 - 50, size[1]//2), f"Test {color}", fill="white")
    
    return img


def test_inference(pipe, num_refs: int, prompt: str = "a portrait of a person"):
    """Test inference with specified number of reference images."""
    print(f"\n🧪 Testing with {num_refs} reference image(s)...")
    
    # Create test reference images
    colors = ["red", "blue", "green", "yellow", "purple", "orange", "pink", "cyan", "magenta", "lime"]
    ref_images = [create_test_image(colors[i % len(colors)]) for i in range(num_refs)]
    
    # Add image references to prompt
    if num_refs > 1:
        prompt_with_refs = f"{prompt}, combining elements from image 1"
        for i in range(2, num_refs + 1):
            prompt_with_refs += f" and image {i}"
    else:
        prompt_with_refs = f"{prompt} from the reference image"
    
    reset_peak_vram()
    vram_before = get_vram_usage()
    
    start_time = time.time()
    
    # Run inference
    image = pipe(
        prompt=prompt_with_refs,
        image=ref_images,
        num_inference_steps=28,  # Recommended trade-off
        guidance_scale=2.5,
        width=512,  # Smaller for testing
        height=512,
        generator=torch.Generator(device="cuda").manual_seed(42)
    ).images[0]
    
    duration = time.time() - start_time
    vram_peak = get_peak_vram()
    vram_after = get_vram_usage()
    
    print(f"  ✅ Generation complete")
    print(f"  ⏱️  Duration: {duration:.2f}s")
    print(f"  💾 VRAM before: {vram_before:.2f}GB")
    print(f"  📈 VRAM peak: {vram_peak:.2f}GB")
    print(f"  💾 VRAM after: {vram_after:.2f}GB")
    
    clear_memory()
    
    return {
        "num_refs": num_refs,
        "duration": duration,
        "vram_before": vram_before,
        "vram_peak": vram_peak,
        "vram_after": vram_after
    }


def main():
    parser = argparse.ArgumentParser(description="Test FLUX2 VRAM usage on RTX 4090")
    parser.add_argument(
        "--model-id",
        default="diffusers/FLUX.2-dev-bnb-4bit",
        help="HuggingFace model ID (default: diffusers/FLUX.2-dev-bnb-4bit)"
    )
    parser.add_argument(
        "--use-nf4",
        action="store_true",
        default=True,
        help="Use NF4 quantization (default: True)"
    )
    parser.add_argument(
        "--no-nf4",
        dest="use_nf4",
        action="store_false",
        help="Disable NF4 quantization (use bfloat16)"
    )
    parser.add_argument(
        "--max-refs",
        type=int,
        default=5,
        help="Maximum number of reference images to test (default: 5)"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("FLUX2 VRAM Test on RTX 4090")
    print("=" * 60)
    
    if not torch.cuda.is_available():
        print("❌ CUDA not available! Cannot run test.")
        return
    
    device_name = torch.cuda.get_device_name(0)
    total_vram = torch.cuda.get_device_properties(0).total_memory / 1024**3
    
    print(f"🖥️  GPU: {device_name}")
    print(f"💾 Total VRAM: {total_vram:.1f}GB")
    print(f"🔧 Model: {args.model_id}")
    print(f"⚙️  Quantization: {'NF4' if args.use_nf4 else 'bfloat16'}")
    print(f"📊 Testing with 1-{args.max_refs} reference images")
    
    # Load pipeline
    try:
        if args.use_nf4:
            pipe = load_pipeline_nf4(args.model_id)
        else:
            pipe = load_pipeline_standard(args.model_id)
    except Exception as e:
        print(f"\n❌ Failed to load pipeline: {e}")
        print("\nNote: If model not found, it may need to be downloaded first.")
        print("The model will be cached to ~/.cache/huggingface/hub/")
        return
    
    # Test with different reference counts
    results = []
    for num_refs in [1, 3, args.max_refs]:
        if num_refs > args.max_refs:
            continue
        
        try:
            result = test_inference(pipe, num_refs)
            results.append(result)
        except torch.cuda.OutOfMemoryError:
            print(f"\n❌ Out of memory with {num_refs} references!")
            print(f"   Maximum safe reference count: {results[-1]['num_refs'] if results else 0}")
            break
        except Exception as e:
            print(f"\n❌ Error with {num_refs} references: {e}")
            break
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if results:
        print(f"\n{'Refs':<10}{'Duration':<15}{'Peak VRAM':<15}{'Status':<20}")
        print("-" * 60)
        
        for r in results:
            status = "✅ OK" if r["vram_peak"] < 24.0 else "⚠️  Near limit"
            print(f"{r['num_refs']:<10}{r['duration']:.2f}s{'':<10}{r['vram_peak']:.2f}GB{'':<8}{status}")
        
        max_safe_refs = max([r["num_refs"] for r in results if r["vram_peak"] < 20.0], default=0)
        
        print(f"\n📊 Results:")
        print(f"   - Maximum safe reference count: {max_safe_refs} (keeping <20GB for safety)")
        print(f"   - Peak VRAM: {max([r['vram_peak'] for r in results]):.2f}GB")
        print(f"   - Average generation time: {sum([r['duration'] for r in results]) / len(results):.2f}s")
        
        if max_safe_refs >= 5:
            print("\n✅ VERDICT: RTX 4090 can handle FLUX2 with multi-reference!")
        elif max_safe_refs >= 3:
            print("\n⚠️  VERDICT: RTX 4090 works but limited to 3-5 references")
        else:
            print("\n❌ VERDICT: VRAM insufficient for multi-reference workflow")
    else:
        print("\n❌ No successful tests - VRAM requirements too high")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
