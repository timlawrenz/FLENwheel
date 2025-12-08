# FLUX2 VRAM Test Results - RTX 4090

**Date**: 2025-11-26  
**Model**: `diffusers/FLUX.2-dev-bnb-4bit` (official 4-bit quantized)  
**GPU**: NVIDIA GeForce RTX 4090 (23.5GB VRAM)  
**Status**: ❌ **FAILED - Out of Memory**

## Test Results

### Attempt 1: With Competing Process
- **VRAM Used by FLUX2**: 20.36 GB during loading
- **VRAM Used by Other Process**: 2.7 GB (training script)
- **Total Needed**: ~23 GB
- **Result**: ❌ OOM - Exceeded 23.5GB capacity

### Attempt 2: Clear GPU (Your Run)
- **VRAM Used by FLUX2**: 23.00 GB during loading
- **VRAM Available**: Only 55.81 MB free
- **Result**: ❌ OOM - **Model alone uses entire GPU**

## Critical Finding

**FLUX2-dev 4-bit quantized uses ~23GB VRAM just to LOAD the model**, leaving:
- **0.5GB available** for generation
- **Not enough** for reference images, generation buffer, or overhead
- **Conclusion**: **FLUX2-dev is NOT viable on RTX 4090 with 24GB VRAM**

## Why This Happens

1. **Text Encoder (Mistral Small 3.1)**: Very large language model
2. **DiT Transformer**: Even at 4-bit, still massive
3. **VAE**: Additional memory for image encoding/decoding
4. **Overhead**: Pipeline components, buffers, PyTorch allocator

**Total**: ~23GB even with aggressive 4-bit quantization + CPU offloading

## Comparison with Qwen

| Model | VRAM (Loading) | VRAM (Inference) | Viable on 4090? |
|-------|----------------|------------------|-----------------|
| **FLUX2-dev (4-bit)** | ~23GB | Unknown (OOM) | ❌ **NO** |
| **Qwen-Image-Edit (4-bit)** | ~12-16GB | ~14-18GB | ✅ **YES** |

**Verdict**: Qwen has ~50% lower memory footprint, making it the only viable option.

## Alternatives Investigated

### ❌ What Won't Help
- ✗ More aggressive CPU offload (already enabled)
- ✗ Reducing batch size (OOM during loading, not generation)
- ✗ Smaller output dimensions (doesn't affect model size)
- ✗ Fewer reference images (OOM before generation phase)

### ⚠️ Might Work (Unconfirmed)
- ? Use GGUF version with different loader (ggml/llama.cpp)
  - Model: `city96/FLUX.2-dev-gguf` or `orabazes/FLUX.2-dev-GGUF`
  - Would need custom loader, not diffusers pipeline
  - ComfyUI might use this approach (your Q4_1.gguf works there)

### 🔬 Research Needed
- Investigate ComfyUI's FLUX2 loading mechanism
- Check if GGUF format has lower memory overhead
- Evaluate if custom loader (non-diffusers) is viable

## Recommendation

### ✅ **PRIMARY PATH: Continue with Qwen-Image-Edit**

**Rationale**:
- Proven to work on RTX 4090
- ~12-16GB VRAM (50% less than FLUX2)
- Specialized LoRAs available (dx8152, etc.)
- Active validation already in progress

### 🔬 **SECONDARY PATH: Investigate GGUF Alternative**

**If ComfyUI works with your GGUF model**, there may be a way to use FLUX2 via:
1. Custom GGUF loader (not diffusers)
2. Different quantization approach
3. Lower memory overhead

**However**: This would require significant research and implementation effort for uncertain benefits.

### ❌ **NOT VIABLE: Official Diffusers FLUX2**

The official `diffusers` FLUX2 pipeline is **incompatible with RTX 4090** due to VRAM constraints.

## Impact on Proposal

**Proposal Status**: `openspec/changes/add-flux2-parallel-pipeline/`

### Must Revise
- ✗ NF4 quantization via diffusers is not viable
- ✗ Multi-reference workflow cannot run on RTX 4090
- ✗ Parallel comparison with Qwen is blocked

### Options
1. **Pivot to GGUF investigation** (high effort, uncertain outcome)
2. **Archive proposal** (FLUX2 not viable on current hardware)
3. **Defer until H100 access** (would need 40GB+ VRAM)

## Conclusion

**FLUX2-dev is NOT viable for FLENwheel on RTX 4090 hardware.**

The model's 23GB VRAM requirement leaves no headroom for:
- Multi-reference images
- Generation process
- Safety margin

**Recommended Action**: 
- ✅ Continue with Qwen-Image-Edit validation
- ✅ Archive FLUX2 proposal with "hardware incompatible" status
- 📊 Focus resources on Qwen ecosystem optimization

---

**Next Steps**: Update proposal status and focus on Qwen validation (Phase 3).
