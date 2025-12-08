# GGUF Loader Porting Progress

**Date**: 2025-11-26  
**Status**: 🚧 IN PROGRESS - Phase 1 Complete  
**Complexity**: HIGH (as expected)

## ✅ Phase 1 Complete: Core GGUF Loading (2 hours)

### What Works

1. **Basic GGUF File Loading** ✅
   - Successfully loads flux2-dev-Q4_1.gguf (19.8GB)
   - Reads all 299 tensors
   - Identifies 171 quantized tensors, 128 standard tensors

2. **GGMLTensor Class** ✅
   - Custom tensor subclass for quantized weights
   - Stores quantization metadata (type, shape)
   - Compatible with PyTorch operations

3. **Q4_1 Dequantization** ✅
   - Implemented dequantize_q4_1() function
   - Successfully dequantizes Q4_1 format tensors
   - Tested: 6144x6144 weight tensor (22.5MB → 72MB after dequant)

4. **State Dict Loading** ✅
   - load_gguf_state_dict() returns full model weights
   - Architecture detection (confirms "flux")
   - VRAM estimation (19.8GB)

### Code Created

- `lib/gguf_loader.py` - Standalone GGUF loader (250+ lines)
- Implements: GGMLTensor, load_gguf_state_dict, dequantize_tensor
- Based on city96/ComfyUI-GGUF but simplified

## 🚧 Phase 2 In Progress: FLUX2 Model Integration

### Challenge: Weight Mapping

GGUF tensors use ComfyUI naming convention:
```
double_blocks.0.img_attn.proj.weight
double_blocks.0.img_attn.qkv.weight
```

diffusers Flux2Transformer2DModel expects:
```
transformer_blocks.0.attn.to_out.0.weight
transformer_blocks.0.attn.to_qkv.weight
```

**Need**: Key mapping function to rename GGUF → diffusers format

### Next Steps

1. **Create key mapping** (2-3 hours)
   - Map ComfyUI names → diffusers names
   - Handle double_blocks, single_blocks structure
   - Test with Flux2Transformer2DModel.from_pretrained()

2. **Integrate with Flux2Pipeline** (2-3 hours)
   - Load GGUF transformer into pipeline
   - Load text encoder (T5, CLIP) separately
   - Load VAE separately

3. **Test VRAM usage** (1 hour)
   - Measure peak VRAM during loading
   - Compare with diffusers NF4 (23GB)
   - Test with 1 reference image

## Current Blocker

**Weight key mapping is complex**. Options:

### Option A: Reverse-Engineer Mapping (3-4 hours)
- Compare ComfyUI vs diffusers architectures
- Create manual mapping dictionary
- High effort, fragile

### Option B: Use ComfyUI Model Loading (1 hour) ⭐
- Import ComfyUI's model_patcher
- Let ComfyUI handle key mapping
- Reuse proven working code

### Option C: Abandon Standalone, Use ComfyUI API (0.5 hours) ⭐⭐
- Switch to ComfyUI HTTP API approach
- Use your working ComfyUI setup
- Avoid all this complexity

## Recommendation

After 2 hours of work, I've confirmed:

1. **✅ GGUF loading works** - can read and dequantize tensors
2. **⚠️  Model integration is complex** - key mapping non-trivial
3. **⚠️  Still uncertain about VRAM** - won't know until fully integrated

**Two paths forward:**

### Path A: Continue Porting (6-8 more hours)
- Complete weight mapping
- Integrate with Flux2Pipeline
- Test VRAM (may still OOM)
- **Risk**: All this work, might still exceed 24GB VRAM

### Path B: Pivot to ComfyUI API (0.5 hours) ⭐ RECOMMENDED
- Use ComfyUI's HTTP API
- Leverage your working GGUF setup
- Get results today instead of 1-2 days
- **Benefit**: Proven to work, immediate results

## Decision Point

**Question**: Continue with standalone port or pivot to ComfyUI API?

**My recommendation**: Pivot to ComfyUI API
- Faster results (0.5 hours vs 6-8 hours)
- Lower risk (known to work)
- Can always port later if needed

**Your call**: What would you like to do?

A. Continue standalone port (6-8 more hours, uncertain outcome)  
B. Pivot to ComfyUI HTTP API (0.5 hours, proven to work) ⭐

