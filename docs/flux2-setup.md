# FLUX2 Parallel Pipeline

Python-based FLUX2-dev inference pipeline for training material generation, independent of ComfyUI.

## Overview

This implementation runs FLUX2-dev with multi-reference support (up to 10 reference images) to generate enriched training datasets for character LoRA training. It operates parallel to the Qwen-Image-Edit workflow for comparison and validation.

## Quick Start

### 1. VRAM Test (Recommended First Step)

Test if your RTX 4090 can handle FLUX2 with multi-reference:

```bash
# Activate virtual environment
source venv/bin/activate

# Run VRAM test
python scripts/flux2_vram_test.py

# Options:
# --max-refs N         Test up to N reference images (default: 5)
# --no-nf4             Disable NF4 quantization (test bfloat16)
# --model-id MODEL     Use different model
```

**Expected Results**:
- Model will download on first run (~5-10GB, cached to `~/.cache/huggingface/`)
- Tests 1, 3, and 5 reference images
- Reports peak VRAM usage and safe reference count
- **Target**: <20GB peak VRAM (leaving headroom on 24GB card)

### 2. Configuration

Edit `config/flux2_config.yaml` to customize:
- Model selection (NF4 vs official)
- Generation parameters (steps, guidance scale, dimensions)
- Multi-reference settings (max references, prompt format)
- Enrichment prompt templates (angles, expressions, poses)
- VRAM safety thresholds

### 3. Basic Inference (Coming Soon)

```bash
python scripts/flux2_inference.py \
    --prompt "portrait of a character" \
    --references path/to/ref1.jpg path/to/ref2.jpg \
    --output output.png
```

### 4. Training Material Generation (Coming Soon)

```bash
python scripts/flux2_enrich.py \
    --character my_character \
    --source-dir data/my_character/source \
    --variations angles,expressions
```

## Implementation Status

### ✅ Phase 1: Research & Setup (Complete)

- [x] Research FLUX2 Python implementation
- [x] Verify dependencies (diffusers, bitsandbytes, transformers)
- [x] Create VRAM test script
- [x] Create configuration file
- [x] Verify CUDA and RTX 4090 availability

### 🚧 Phase 2: Core Inference (In Progress)

- [ ] Implement basic inference script
- [ ] Test single-reference generation
- [ ] Test multi-reference generation (1, 3, 5 refs)
- [ ] Verify output quality and VRAM

### 📋 Phase 3-8: Upcoming

See `openspec/changes/add-flux2-parallel-pipeline/tasks.md` for full task list.

## Key Features

### Multi-Reference Support

FLUX2-dev natively supports **up to 10 reference images** for character consistency:

```python
from diffusers import Flux2Pipeline
from diffusers.utils import load_image

pipe = Flux2Pipeline.from_pretrained("black-forest-labs/FLUX.2-dev")
pipe.enable_model_cpu_offload()

# Load reference images
refs = [load_image(f"ref{i}.jpg") for i in range(1, 4)]

# Generate with multi-reference
image = pipe(
    prompt="the character from image 1, image 2, and image 3 in a new pose",
    image=refs,  # List of reference images
    num_inference_steps=28,
    guidance_scale=2.5,
).images[0]
```

### NF4 Quantization

Uses 4-bit NormalFloat quantization for memory efficiency:

- **Model**: `prithivMLmods/Flux.2.Dev-NF4` (community quantized)
- **VRAM Savings**: ~4x reduction vs bfloat16
- **Quality**: Minimal degradation for 4-bit
- **RTX 4090 Fit**: Designed to work within 24GB VRAM

### Character Consistency Evaluation

Automated face recognition scoring:

- **Library**: InsightFace or DeepFace
- **Threshold**: ≥70% similarity = passing
- **GPU-Accelerated**: Embedding computation on CUDA
- **Batch Reports**: Distribution, pass rate, flagged images

## Architecture

```
FLUX2 Pipeline (Parallel to Qwen)
│
├── Inference
│   ├── Single-reference (1 image)
│   ├── Multi-reference (3-10 images)
│   └── Batch processing
│
├── Enrichment
│   ├── Angle variations (front, 3/4, profile, back)
│   ├── Expression variations (neutral, smiling, sad, angry)
│   ├── Pose variations (standing, sitting, T-pose)
│   └── Background variations (beach, forest, city)
│
├── Evaluation
│   ├── Face recognition scoring
│   ├── Consistency filtering (≥70%)
│   └── Batch reporting
│
└── Comparison
    ├── FLUX2 vs Qwen metrics
    ├── Side-by-side visualizations
    └── Strategic recommendation
```

## Data Organization

```
data/
└── {character}/
    └── flux2/
        ├── reference/      # Source images (input)
        ├── enriched/       # Generated variations (output)
        │   ├── angles/
        │   ├── expressions/
        │   ├── poses/
        │   └── backgrounds/
        ├── filtered/       # Passing consistency check (≥70%)
        └── metadata/       # JSON files with scores, params
```

## Dependencies

All dependencies are already installed in the project `venv/`:

- **diffusers** 0.36.0.dev0 - FLUX2Pipeline support
- **transformers** 4.57.1 - Text encoder (Mistral Small 3.1)
- **bitsandbytes** 0.48.2 - NF4 quantization
- **accelerate** 1.11.0 - CPU offloading
- **torch** 2.9.1 - CUDA-enabled (RTX 4090)
- **Pillow** - Image handling

## Hardware Requirements

- **GPU**: NVIDIA RTX 4090 (24GB VRAM)
- **CPU Offloading**: Required (enabled by default)
- **Disk Space**: ~10GB for cached models
- **RAM**: 32GB+ recommended

## References

- **HuggingFace Blog**: https://huggingface.co/blog/flux-2
- **Model Card**: https://huggingface.co/black-forest-labs/FLUX.2-dev
- **NF4 Model**: https://huggingface.co/prithivMLmods/Flux.2.Dev-NF4
- **OpenSpec Proposal**: `openspec/changes/add-flux2-parallel-pipeline/`

## Comparison with Qwen

| Feature | FLUX2 | Qwen-Image-Edit |
|---------|-------|-----------------|
| **Approach** | Multi-reference generation | Single-image editing |
| **Max References** | 10 images | 1 image |
| **Use Case** | Character-consistent generation | Precise image transformations |
| **VRAM** | ~15-20GB (NF4 + offload) | ~12-16GB (4-bit + offload) |
| **LoRA Training** | Yes (FLUX2 LoRAs) | Yes (Qwen LoRAs) |
| **Strength** | Native consistency across refs | Fine-grained control |

**Strategy**: Run both in parallel, compare results, choose based on empirical data.

## Troubleshooting

### Out of Memory (OOM)

If you encounter VRAM errors:

1. **Reduce reference count**: Try 3 or 1 reference images
2. **Enable attention slicing**: Set `enable_attention_slicing: true` in config
3. **Reduce output size**: Use 512x512 instead of 1024x1024
4. **Enable VAE slicing**: Set `enable_vae_slicing: true` in config

### Model Download Issues

Models are cached to `~/.cache/huggingface/hub/`. If download fails:

```bash
# Use HuggingFace CLI to pre-download
huggingface-cli login  # If needed
huggingface-cli download prithivMLmods/Flux.2.Dev-NF4
```

### Slow Generation

- **Expected**: 30-60s per image on RTX 4090 with 28 steps
- **Optimize**: Reduce `num_inference_steps` to 20 (faster, lower quality)
- **Flash Attention**: Not available on RTX 4090 (Hopper GPUs only)

## Next Steps

1. ✅ **Run VRAM test**: Confirm FLUX2 fits on RTX 4090
2. 📝 **Review results**: Check VRAM usage with 1, 3, 5 refs
3. 🔧 **Adjust config**: Update `max_references` based on test
4. 🚀 **Begin Phase 2**: Implement basic inference script
5. 📊 **Compare with Qwen**: Run parallel validation

## License

FLUX.2-dev is under non-commercial license (same as FLUX.1-dev). Check model card for details.
