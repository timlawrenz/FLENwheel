# FLUX2 Python Implementation Research

**Date**: 2025-11-26  
**Sources**: 
- https://huggingface.co/blog/flux-2
- https://huggingface.co/black-forest-labs/FLUX.2-dev

## Official Python Implementation

### ✅ Confirmed: Diffusers Library Support

FLUX2-dev is officially supported via HuggingFace Diffusers library using `Flux2Pipeline`.

### Basic Text-to-Image Example

```python
from diffusers import Flux2Pipeline
import torch

repo_id = "black-forest-labs/FLUX.2-dev"
pipe = Flux2Pipeline.from_pretrained(repo_id, torch_dtype=torch.bfloat16)
pipe.enable_model_cpu_offload()

image = pipe(
    prompt="dog dancing near the sun",
    num_inference_steps=50,  # 28 is a good trade-off
    guidance_scale=4,
    height=1024,
    width=1024
).images[0]
```

### Key Findings

1. **Library**: Uses `diffusers.Flux2Pipeline` (not FluxPipeline)
2. **Data Type**: `torch.bfloat16` recommended
3. **Memory**: ~62GB without CPU offloading on H100 (!)
4. **CPU Offloading**: Required for consumer GPUs (`pipe.enable_model_cpu_offload()`)
5. **Flash Attention 3**: Available for Hopper GPUs (H100+) - not applicable to RTX 4090

### VRAM Concerns 🚨

**Critical Issue**: Official example requires ~62GB VRAM on H100 even with CPU offloading!

**RTX 4090 Implications** (24GB VRAM):
- CPU offloading is **mandatory**
- May need additional optimizations:
  - Lower precision (bfloat16 already used)
  - Smaller batch sizes
  - Model quantization (our Q4_1.gguf approach)
  - Sequential attention slicing

### Multi-Reference Image Support ✅

**Status**: CONFIRMED - Official API documented in blog post.

**Official API**:
```python
from diffusers import Flux2Pipeline
from diffusers.utils import load_image

# Load reference images
image_one = load_image("path/to/reference1.png")
image_two = load_image("path/to/reference2.png")
# ... up to 10 images

# Generate with multi-reference
image = pipe(
    prompt="the kangaroo from image 1 and the turtle from image 2 fighting at a beach",
    image=[image_one, image_two],  # List of PIL images
    num_inference_steps=50,
    guidance_scale=2.5,
    width=1024,
    height=768,
).images[0]
```

**Key Features**:
- Supports **up to 10 reference images**
- Reference via index (e.g., "image 1", "image 2") or natural language (e.g., "the kangaroo")
- Best results with **combination of both** reference methods
- **Warning**: Each additional image increases VRAM usage

### Quantization Support ✅ (Partial)

**NF4 Quantization Confirmed**: Diffusers blog shows NF4-quantized models work natively!

```python
from diffusers import BitsAndBytesConfig, Flux2Pipeline, Flux2Transformer2DModel

# NF4 quantization config
nf4_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

# Load quantized model components
transformer = Flux2Transformer2DModel.from_pretrained(
    "prithivMLmods/Flux.2.Dev-NF4",
    subfolder="transformer",
    quantization_config=nf4_config,
    torch_dtype=torch.bfloat16
)

pipe = Flux2Pipeline.from_pretrained(
    "black-forest-labs/FLUX.2-dev",
    transformer=transformer,
    torch_dtype=torch.bfloat16
)
```

**GGUF Compatibility**: ❓ **Still Unknown**

**Our GGUF Model**: `/mnt/essdee/ComfyUI/models/diffusion_models/flux2-dev-Q4_1.gguf`

**Questions**:
1. Can `Flux2Pipeline` load GGUF files? (Likely NO - GGUF is llama.cpp format)
2. Do we need to convert GGUF → NF4/bitsandbytes format?
3. Does ComfyUI use custom GGUF loader? (Likely YES)
4. Can we use the NF4 approach instead of GGUF?

### Next Research Steps

1. **Multi-reference API**: Read full blog post for reference image examples
2. **GGUF Loading**: Check if diffusers supports GGUF or needs adapter
3. **Memory Optimization**: Test on RTX 4090 with CPU offloading + quantization
4. **ComfyUI Backend**: Reverse-engineer how ComfyUI loads our Q4_1.gguf

### Implementation Strategy Options

**Option A: Official Diffusers + NF4 Quantization** ⭐ **RECOMMENDED**
- Pros: Official support, clean API, multi-reference confirmed, 4-bit quantization built-in
- Cons: Need to test VRAM on RTX 4090 (should fit with CPU offload + NF4)
- Model: `prithivMLmods/Flux.2.Dev-NF4` (community NF4 version)

**Option B: Official Diffusers (Full Precision bfloat16)**
- Pros: Official support, clean API
- Cons: ~62GB VRAM (unworkable on 4090)

**Option C: ComfyUI Backend Extraction**
- Pros: Already works with our Q4_1.gguf
- Cons: Reverse-engineering, non-standard, maintenance burden, no clear Python API

**Option D: GGUF → NF4 Conversion** (if Option A insufficient)
- Pros: Reuse existing GGUF model
- Cons: Conversion tooling may not exist, complexity

### Recommendation 🎯

1. **Immediate**: Test **Option A (Diffusers + NF4)** on RTX 4090
   - Use `prithivMLmods/Flux.2.Dev-NF4` quantized model
   - Enable CPU offloading
   - Measure actual VRAM with 1, 3, 5 reference images
   
2. **If VRAM fits (<24GB)**: 
   - Proceed with official Diffusers pipeline
   - Implement multi-reference workflow
   - Our GGUF model becomes secondary/backup
   
3. **If VRAM exceeds 24GB**: 
   - Investigate additional optimizations (attention slicing, sequential offload)
   - Consider ComfyUI extraction as fallback
   
4. **Update proposal** with test results and final library choice

### LoRA Training Confirmation ✅

Blog mentions "LoRA fine-tuning" section - confirms FLUX2 supports LoRA training!

This resolves one of the major open questions in the proposal.

---

**Status**: Research Complete - Ready for implementation testing

- [x] Multi-reference API details (confirmed: `image=[img1, img2, ...]`)
- [x] Quantization support (NF4 via bitsandbytes, not GGUF)
- [x] LoRA training support (confirmed in blog)
- [ ] Actual VRAM usage on RTX 4090 (needs testing)
- [ ] Reference image preprocessing requirements
- [ ] NF4 model download and setup

**Next Action**: Create test script to validate VRAM on RTX 4090 with NF4 quantization
