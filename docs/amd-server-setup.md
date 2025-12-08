# AMD Radeon 8060S (gfx1151) Setup - Lessons Learned

**Date**: 2025-12-08  
**Hardware**: AMD Radeon 8060S Graphics (Strix Halo, gfx1151, RDNA 3.5)  
**Software**: PyTorch 2.5 + ROCm 6.1, Python 3.13  
**Status**: ❌ PyTorch Diffusers incompatible with gfx1151  
**Next Review**: Q1 2025 (ROCm 6.3/PyTorch 2.6 expected)

---

## Summary

Attempted to run FLENwheel volume generation on AMD Radeon 8060S APU with 96GB unified memory. Model loads successfully to GPU but fails during inference due to missing HIP kernels for gfx1151 architecture.

**Verdict**: Use RTX 4090 for now, revisit AMD when ROCm support matures.

---

## Hardware Specifications

```
GPU: AMD Radeon 8060S Graphics (Strix Halo)
Architecture: RDNA 3.5 (gfx1151)
Compute Capability: 11.5
VRAM: 96GB (unified memory, dynamically allocated)
CPU RAM: 32GB (remainder of 128GB total)
ROCm Version: 6.1
```

**rocm-smi output:**
```
GPU[0]: Card Series: Strix Halo [Radeon Graphics / Radeon 8050S Graphics / Radeon 8060S Graphics]
GPU[0]: GFX Version: gfx1151
GPU[0]: Card Model: 0x1586
```

---

## Setup Process

### 1. Environment Creation ✅

```bash
cd ~/activity/FLENwheel
git checkout volume
python3 -m venv venv-amd395
source venv-amd395/bin/activate.fish  # or .../activate for bash

pip install --upgrade pip
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.1
pip install diffusers transformers accelerate peft
pip install pyyaml pillow
```

**Key finding**: ROCm 5.7 has no Python 3.13 wheels. ROCm 6.1 works.

### 2. PyTorch GPU Detection ✅

```bash
python -c "import torch; print('CUDA available:', torch.cuda.is_available()); \
print('Device count:', torch.cuda.device_count()); \
print('Device name:', torch.cuda.get_device_name(0)); \
print('VRAM GB:', torch.cuda.get_device_properties(0).total_memory / 1024**3)"
```

**Output:**
```
CUDA available: True
Device count: 1
Device name: Radeon 8060S Graphics
VRAM GB: 96.0
```

✅ **PyTorch recognizes the GPU** (ROCm uses CUDA API compatibility layer)

### 3. Model Loading ✅

```bash
python scripts/generate_structured_volume.py \
  --character test-001 \
  --categories test \
  --parallel 1 \
  --seeds 1
```

**Result**: Model loads successfully to GPU
- Load time: ~11.5 minutes (loading from NAS)
- VRAM usage: 15% (~14.4GB)
- No errors during loading

### 4. Inference ❌

**Error during first generation:**
```
HIP error: invalid device function
HIP kernel errors might be asynchronously reported at some other API call
```

**Failure rate**: 5/5 images (100%)  
**Failure point**: Immediately upon calling pipeline()

---

## Root Cause Analysis

### Why Ollama Works But PyTorch Doesn't

**Ollama (llama.cpp/ggml)**:
- Uses custom HIP kernels for specific LLM operations
- Narrow, well-tested kernel set (matrix multiply, attention, etc.)
- Inference-only, quantized models
- Successfully uses 27% VRAM (~26GB) with qwen2-vl:32b

**PyTorch Diffusers**:
- Generic deep learning framework with hundreds of kernels
- Diffusion-specific operations (conv2d, timestep embedding, cross-attention)
- Some kernels not implemented for gfx1151 in ROCm 6.1
- Broader operation support = more breaking points

### Missing Kernel Investigation

The "invalid device function" error indicates:
- Kernel compilation succeeded (model loads)
- Specific runtime kernel missing for gfx1151
- Likely in attention or convolution operations

**Tested configurations** (all failed):
- torch.bfloat16 ❌
- torch.float16 ❌  
- torch.float32 (CPU mode - OOM killed, 32GB insufficient) ❌

---

## Attempted Workarounds

### 1. CPU Mode
**Config**: `torch.float32`, `pipeline.to("cpu")`  
**Result**: ❌ Kernel OOM killed (32GB CPU RAM insufficient)  
**VRAM allocation**: 96GB to GPU, only 32GB to CPU

### 2. Float16 GPU Mode
**Config**: `torch.float16`, `device_map="cuda"`  
**Result**: ❌ Same HIP kernel error  
**Finding**: fp16 has same kernel gaps as bfloat16

### 3. Explicit Device Placement
**Config**: `device_map="cuda:0"` → `device_map="cuda"`  
**Result**: ✅ Model loads, ❌ inference fails  
**Finding**: Diffusers requires `"cuda"` string, not `"cuda:0"`

### 4. Environment Variables
**Config**: `AMD_SERIALIZE_KERNEL=3`, `PYTORCH_HIP_ALLOC_CONF=...`  
**Result**: ❌ No effect on kernel availability

---

## Why This Happens

### Timeline Issue

**gfx1151 release**: Late 2024 (Strix Halo APU)  
**PyTorch ROCm 6.1**: Released before gfx1151 silicon availability  
**Result**: Kernel library predates hardware

### Architecture Gap

RDNA 3.5 (gfx1151) is:
- Consumer/prosumer APU (not datacenter)
- Very new architecture variant
- Low priority for AMD ROCm team (focus on MI300, MI250)

### Kernel Development

PyTorch ROCm kernels require:
1. Architecture-specific compilation
2. ISA (instruction set) implementation
3. Performance tuning
4. Validation across operation types

**Estimated timeline**: Q1-Q2 2025 for full support

---

## What Works on gfx1151

✅ **Ollama** - Custom kernels, LLM inference  
✅ **rocm-smi** - GPU monitoring  
✅ **PyTorch basics** - Tensor ops, simple operations  
❌ **PyTorch Diffusers** - Complex inference pipelines  
❌ **Training** - Even more kernel requirements  

---

## Comparison: RTX 4090 vs AMD 8060S

| Feature | RTX 4090 (24GB) | AMD 8060S (96GB) |
|---------|-----------------|------------------|
| **VRAM** | 24GB GDDR6X | 96GB unified |
| **PyTorch Support** | ✅ Perfect | ❌ Incomplete (gfx1151) |
| **Diffusers** | ✅ Works | ❌ Kernel errors |
| **Load Time** | ~2 seconds | ~11 minutes (NAS) |
| **Inference** | ✅ Fast | ❌ Fails |
| **Parallel Execution** | ⚠️ 1 model (VRAM limit) | 🔮 4-6 models (if it worked) |
| **Cost** | Already owned | Already owned |
| **Best Use** | **Generation NOW** | Ollama, future experiments |

**Winner for FLENwheel**: RTX 4090 (until ROCm catches up)

---

## Recommendations

### Immediate (December 2025)

1. ✅ **Use RTX 4090 for volume generation**
   - Works perfectly
   - 24GB sufficient for sequential generation
   - Proven stable

2. ✅ **Use AMD 8060S for Ollama**
   - 96GB enables huge models
   - Already working well
   - Good for LLM experiments

3. ✅ **Document findings** (this file)
   - Save time when revisiting
   - Help others with gfx1151

### Future (Q1-Q2 2025)

4. ⏰ **Test PyTorch ROCm 6.3+**
   - Expected: Better gfx1151 support
   - Check: https://pytorch.org/get-started/locally/
   - Test: Same `generate_structured_volume.py` script

5. ⏰ **Monitor PyTorch/ROCm releases**
   - GitHub: https://github.com/pytorch/pytorch
   - ROCm: https://github.com/ROCm/ROCm
   - Look for gfx1151/RDNA 3.5 mentions

6. 💡 **File PyTorch issue** (optional, 1-2 hours)
   - Document gfx1151 incompatibility
   - Help prioritize support
   - Template below

---

## Testing Checklist for Future

When PyTorch/ROCm updates:

```bash
# 1. Update PyTorch
pip install --upgrade torch torchvision torchaudio \
    --index-url https://download.pytorch.org/whl/rocm6.3  # or latest

# 2. Verify GPU detection
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"

# 3. Test model loading
python scripts/generate_structured_volume.py \
  --character test-001 \
  --categories test \
  --parallel 1 \
  --seeds 1

# 4. Check for kernel errors
# If generates successfully: ✅ ROCm support improved!
# If same HIP error: ⏳ Wait for next release

# 5. If working, scale up
python scripts/generate_structured_volume.py \
  --character test-001 \
  --categories portraits \
  --parallel 4 \
  --seeds 2
# Expected: ~200 images, 96GB VRAM allows 4-6 models in parallel
```

---

## PyTorch Issue Template (Optional)

If you want to help prioritize AMD support:

```markdown
**Title**: ROCm: gfx1151 (RDNA 3.5, Strix Halo) missing HIP kernels for diffusion models

**Environment**:
- GPU: AMD Radeon 8060S (gfx1151, RDNA 3.5)
- PyTorch: 2.5.1+rocm6.1
- ROCm: 6.1
- OS: Linux

**Issue**:
PyTorch recognizes gfx1151 GPU but inference fails with "HIP error: invalid device function" when running diffusion models (Diffusers library, QwenImageEditPlusPipeline).

**Reproducer**:
```python
import torch
from diffusers import QwenImageEditPlusPipeline

pipe = QwenImageEditPlusPipeline.from_pretrained(
    "path/to/qwen-image-edit-2509",
    torch_dtype=torch.float16,
    device_map="cuda"
)
# Loads successfully

result = pipe(
    prompt="test",
    image=image,
    num_inference_steps=40
)
# Fails: HIP error: invalid device function
```

**Expected**: Inference succeeds (works on NVIDIA CUDA)  
**Actual**: Kernel error on gfx1151

**Notes**: 
- Ollama/llama.cpp works on same GPU (custom kernels)
- Likely missing kernels for attention/conv ops
- gfx1151 is new (late 2024), may need explicit support

**Request**: Add gfx1151 to kernel compilation targets for diffusion operations
```

**Link**: https://github.com/pytorch/pytorch/issues

---

## Files Modified

**Repository**: https://github.com/timlawrenz/FLENwheel  
**Branch**: `volume`

**Commits**:
- `a36d931` - CPU mode attempt (failed - OOM)
- `df2f531` - fp16 GPU attempt (failed - kernels)
- `682611d` - device_map GPU forcing
- `9060351` - Fix device_map syntax

**Final state**: Model loads to GPU, inference fails with HIP kernel error

---

## Useful Commands

```bash
# Check GPU
rocm-smi
rocm-smi --showproductname

# Monitor VRAM during load
watch -n 2 rocm-smi

# Check PyTorch device
python -c "import torch; print(torch.cuda.get_device_capability())"
# Output: (11, 5) = gfx1151

# Check ROCm version
dpkg -l | grep rocm

# Install rocm-smi
sudo apt install rocm-smi
```

---

## Conclusion

The AMD Radeon 8060S is **excellent hardware** (96GB unified memory!) but **bleeding-edge software support** is incomplete. For production work today, stick with RTX 4090. For future-proofing and experiments, keep the AMD server ready for when ROCm/PyTorch catch up.

**Expected working date**: Q1-Q2 2025  
**Will revisit**: When PyTorch ROCm 6.3+ or PyTorch 2.6+ releases

**Success criteria for future test**:
- Model loads to GPU ✅ (already working)
- Inference completes without HIP errors ⏳ (waiting for ROCm)
- Can run 4-6 models in parallel 🎯 (unlocks volume generation)

---

**Last tested**: 2025-12-08  
**Next test**: When PyTorch ROCm 6.3+ available  
**Fallback**: RTX 4090 (working perfectly)
