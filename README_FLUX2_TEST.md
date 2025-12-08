# FLUX2 VRAM Test - Ready to Run

## Phase 1 Complete ✅

All setup tasks are complete. You're ready to test FLUX2 on your RTX 4090!

## Run the Test

```bash
# Activate environment
source venv/bin/activate

# Run VRAM test (will download model on first run)
python scripts/flux2_vram_test.py
```

## What the Test Does

1. **Downloads** NF4-quantized FLUX2 model (~5-10GB, one-time)
2. **Loads** model with CPU offloading
3. **Tests** generation with 1, 3, and 5 reference images
4. **Reports** VRAM usage, generation speed, and safe reference count

## Expected Output

```
============================================================
FLUX2 VRAM Test on RTX 4090
============================================================
🖥️  GPU: NVIDIA GeForce RTX 4090
💾 Total VRAM: 23.5GB
🔧 Model: prithivMLmods/Flux.2.Dev-NF4
⚙️  Quantization: NF4
📊 Testing with 1-5 reference images

🔧 Loading FLUX2 with NF4 quantization...
[Model download progress...]
✅ Pipeline loaded. VRAM after loading: XX.XXG

B
🧪 Testing with 1 reference image(s)...
  ✅ Generation complete
  ⏱️  Duration: XX.XXs
  💾 VRAM before: XX.XXGB
  📈 VRAM peak: XX.XXGB
  💾 VRAM after: XX.XXGB

[... more tests ...]

============================================================
SUMMARY
============================================================
Refs      Duration       Peak VRAM      Status              
------------------------------------------------------------
1         XX.XXs          XX.XXGB        ✅ OK
3         XX.XXs          XX.XXGB        ✅ OK
5         XX.XXs          XX.XXGB        ✅ OK / ⚠️  Near limit

📊 Results:
   - Maximum safe reference count: X (keeping <20GB for safety)
   - Peak VRAM: XX.XXGB
   - Average generation time: XX.XXs

✅ VERDICT: RTX 4090 can handle FLUX2 with multi-reference!
```

## After the Test

Based on results, update `config/flux2_config.yaml`:

```yaml
multi_reference:
  max_references: X  # Use the safe count from test results
```

## What's Next

If test succeeds (VRAM < 20GB):
- ✅ Phase 1 complete
- 🚀 Begin Phase 2: Implement inference script
- 📊 Run comparison with Qwen

If test shows VRAM issues:
- Try `--max-refs 3` (test fewer references)
- Enable attention slicing in config
- Consider using smaller output dimensions (512x512)

## Files Created

- ✅ `scripts/flux2_vram_test.py` - VRAM testing script
- ✅ `config/flux2_config.yaml` - Pipeline configuration
- ✅ `docs/flux2-setup.md` - Full documentation
- ✅ `openspec/changes/add-flux2-parallel-pipeline/` - Proposal & research

## Questions?

See:
- `docs/flux2-setup.md` - Full setup guide
- `openspec/changes/add-flux2-parallel-pipeline/flux2-python-research.md` - Implementation details
- `openspec/changes/add-flux2-parallel-pipeline/proposal.md` - Strategic overview
