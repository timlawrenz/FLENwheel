# FLUX2 GGUF Investigation Results

**Date**: 2025-11-26  
**GGUF File**: `/mnt/essdee/ComfyUI/models/diffusion_models/flux2-dev-Q4_1.gguf`  
**File Size**: 19.80 GB (vs 23GB for diffusers NF4)  
**Status**: ✅ File Valid, Contains 299 Tensors

## GGUF Inspection Results

```
Architecture: FLUX
Quantization: Q4_1 (4-bit)  
Total Tensors: 299
File Size: 19.80 GB

Sample Tensors:
1. double_blocks.0.img_attn.norm.key_norm.scale
2. double_blocks.0.img_attn.norm.query_norm.scale
3. double_blocks.0.img_attn.proj.weight [6144 x 6144]
4. double_blocks.0.img_attn.qkv.weight [6144 x 18432]
... and 295 more
```

## Key Finding

**GGUF model is 3.2GB smaller** than diffusers NF4 version:
- **GGUF Q4_1**: 19.80 GB
- **Diffusers NF4**: 23.00 GB

This suggests GGUF **might** fit in VRAM where diffusers NF4 doesn't!

## Implementation Options

### Option 1: ComfyUI as Python Library ⭐ **RECOMMENDED**

**Approach**: Import ComfyUI modules directly in Python

**Pros**:
- Reuse proven working GGUF loader
- ComfyUI-GGUF infrastructure already handles dequantization
- Your Q4_1 model already works in ComfyUI
- No need to reverse-engineer GGUF format

**Cons**:
- Dependency on ComfyUI codebase
- Need to understand ComfyUI's model management
- Less "clean" than pure diffusers

**Implementation**:
```python
import sys
sys.path.append('/mnt/essdee/ComfyUI')

from nodes import NODE_CLASS_MAPPINGS
from comfy_extras.nodes_gguf import UnetLoaderGGUF

# Load GGUF model
unet_loader = UnetLoaderGGUF()
unet = unet_loader.load_unet("flux2-dev-Q4_1.gguf")[0]

# Use in workflow...
```

**Effort**: Medium (1-2 days)

---

### Option 2: ComfyUI HTTP API

**Approach**: Use ComfyUI's server API to queue workflows

**Pros**:
- Complete separation from ComfyUI code
- ComfyUI handles all model loading
- Can run ComfyUI as separate service
- Works with existing setup

**Cons**:
- Requires ComfyUI server running
- HTTP overhead
- Workflow in JSON format
- Less flexible than Python API

**Implementation**:
```python
import requests

# Queue workflow
workflow = {
    "prompt": {...},  # ComfyUI workflow JSON
}
response = requests.post("http://localhost:8188/prompt", json=workflow)

# Poll for results
result_id = response.json()["prompt_id"]
# ... polling logic ...
```

**Effort**: Low (0.5-1 day)

---

### Option 3: Port ComfyUI-GGUF to Standalone

**Approach**: Extract and adapt ComfyUI-GGUF code for standalone use

**Pros**:
- Pure Python, no ComfyUI dependency
- Full control over implementation
- Can integrate with diffusers

**Cons**:
- High complexity (GGUF dequantization layer)
- Need to understand city96's custom ops
- Maintenance burden
- May still exceed VRAM (unknown)

**What Needs Porting**:
1. `ops.py` - GGUF tensor class and dequantization
2. `gguf_loader.py` - Model loading logic
3. `dequant.py` - Quantization format handling
4. Integration with FLUX2 transformer architecture

**Effort**: High (5-7 days)

---

### Option 4: Continue with Qwen ✅ **SAFEST**

**Approach**: Stick with Qwen-Image-Edit validation

**Pros**:
- Proven to work on RTX 4090
- 50% less VRAM than FLUX2
- Already has ecosystem (dx8152 LoRA, etc.)
- Validation in progress

**Cons**:
- No multi-reference capability
- Single-image editing only

**Effort**: 0 (already in progress)

## Recommendation Matrix

| Option | VRAM Risk | Complexity | Time | Viability |
|--------|-----------|------------|------|-----------|
| **1. ComfyUI as Library** | Medium | Medium | 1-2 days | ⭐⭐⭐⭐ |
| **2. ComfyUI HTTP API** | Low | Low | 0.5-1 day | ⭐⭐⭐ |
| **3. Port GGUF Loader** | Medium | High | 5-7 days | ⭐⭐ |
| **4. Continue Qwen** | None | Low | 0 days | ⭐⭐⭐⭐⭐ |

## VRAM Analysis

**Question**: Will GGUF Q4_1 (19.8GB) fit where diffusers NF4 (23GB) doesn't?

**Answer**: **Possibly**, but risky:
- GGUF saves **3.2GB** vs diffusers NF4
- diffusers NF4 used **23GB** during loading
- GGUF **might** fit in **~20-21GB** (more testing needed)
- Still leaves only **2-3GB** for generation (very tight)

**Risk**: Even if it loads, may OOM during generation with multi-reference.

## Strategic Decision Tree

```
Do you need FLUX2 specifically for multi-reference?
│
├─ YES → Try Option 1 (ComfyUI as library)
│         ├─ Success → Great! Use FLUX2
│         └─ OOM → Fall back to Qwen
│
└─ NO → Use Option 4 (Qwen)
          └─ Lower risk, proven path
```

## Next Steps

### If Proceeding with FLUX2 GGUF:

1. **Test Option 1** (ComfyUI as library):
   ```bash
   # Create test script
   python scripts/flux2_comfyui_loader.py
   ```

2. **Measure VRAM**:
   - Track peak usage during load
   - Test with 1 reference image
   - Compare to diffusers NF4 results

3. **If Success**:
   - Implement full inference pipeline
   - Test multi-reference (3, 5 refs)
   - Compare with Qwen results

4. **If OOM**:
   - Document findings
   - Archive FLUX2 proposal
   - Continue with Qwen

### If Sticking with Qwen:

1. Continue `qwen-ecosystem-validation`
2. Complete Phase 3 testing
3. Optimize Qwen workflow
4. No FLUX2 work needed

## Your Call

**What would you like to do?**

A. Try Option 1 (ComfyUI as library) - 1-2 day effort, medium risk  
B. Try Option 2 (ComfyUI HTTP API) - 0.5-1 day effort, low risk  
C. Continue with Qwen only - 0 days, no risk  

Let me know and I'll implement your choice!

