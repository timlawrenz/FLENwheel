# FLUX2 VRAM Test - Issue Found

## Problem

The FLUX2-dev 4-bit quantized model (diffusers/FLUX.2-dev-bnb-4bit) **ran out of VRAM during loading** on the RTX 4090 (23.5GB).

### Error Details

```
CUDA out of memory. Tried to allocate 80.00 MiB. 
GPU 0 has a total capacity of 23.49 GiB of which 56.50 MiB is free. 
Including non-PyTorch memory, this process has 20.36 GiB memory in use.
Process 1281049 has 2.63 GiB memory in use.
```

### Root Causes

1. **Other process using GPU**: Process 1281049 (training/compare_phase_ii2_validation.py) is using 2.7GB VRAM
2. **Model loading peak**: FLUX2 tried to use 20.36 GB during loading phase
3. **Total exceeded**: 20.36GB (FLUX2) + 2.7GB (other) > 23.5GB (available)

## Solutions

### Immediate (Before Re-Running Test)

1. **Stop competing processes:**
   ```bash
   # Check what's using GPU
   nvidia-smi
   
   # Kill the training process if safe to do so
   # (Process 1281049: training/compare_phase_ii2_validation.py)
   ```

2. **Clear GPU memory:**
   ```bash
   # If you can safely stop process 1281049:
   kill 1281049
   
   # Or use fuser to clear GPU
   sudo fuser -v /dev/nvidia*
   ```

3. **Re-run test with clear GPU:**
   ```bash
   source venv/bin/activate
   python scripts/flux2_vram_test.py --max-refs 3
   ```

### Long-term (Script Improvements Needed)

The test script needs updates:

1. **Check GPU availability before loading**
2. **Implement sequential CPU offload** (more aggressive than model_cpu_offload)
3. **Load model components one at a time** to reduce peak memory
4. **Add VRAM monitoring** during load phase

## Key Finding

**FLUX2-dev 4-bit requires ~20GB VRAM just to load**, leaving only ~3.5GB for:
- Reference images
- Generation process
- System overhead

This suggests:
- ✅ Model can fit on RTX 4090 (barely)
- ⚠️  Very tight VRAM budget
- 📉 May not support many reference images (maybe 1-3 max)
- 🔧 Needs aggressive memory optimization

## Recommendation

**Before concluding FLUX2 is unworkable:**

1. Clear GPU (kill process 1281049)
2. Re-run test with clean GPU
3. Test with smaller dimensions (512x512 instead of 1024x1024)
4. Try with just 1 reference image first

**If still OOM after cleanup:**
- Consider that FLUX2 may not be viable for RTX 4090
- Qwen-Image-Edit uses ~12-16GB (more headroom)
- FLUX2 advantage (multi-ref) may be offset by VRAM limits

## Next Steps

1. **You decide**: Stop the training process (1281049) if safe
2. **Re-run test** with clear GPU
3. **Report results** - we'll know definitively if FLUX2 fits

