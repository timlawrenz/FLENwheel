# Volume Strategy Implementation - Progress Report

**Date**: 2025-12-08  
**Branch**: `volume`  
**Status**: Phase 1 Complete ✅

## What Was Implemented

### 1. OpenSpec Proposal: `add-structured-volume-generation`

Complete strategic proposal created and validated:

- **proposal.md**: Rationale for pivot from "perfect model" to "volume + ELO curation"
- **tasks.md**: 180+ implementation tasks across 10 phases
- **design.md**: Architecture decisions, risks, success criteria
- **3 capability specs**: 65 scenarios across volume-generation, elo-curation, dual-server-orchestration

**Validation**: ✅ `openspec validate --strict` passes

### 2. NAS Directory Structure

Created on `/mnt/nas-ai-models/training-data/flenwheel/`:

```
flenwheel/
├── sources/        # Sparse input images (10-20 per character)
├── generated/      # Volume output from orchestrator
├── curated/        # ELO winners for training
├── loras/          # Trained character LoRAs
└── templates/      # Prompt templates (YAML)
```

### 3. Prompt Template Library

Four category templates created:

#### `portraits.yaml`
- **Target**: 200 images
- **Templates**: headshots, bust_shots, close_ups, environmental
- **Coverage**: 6 angles × 4 expressions + lighting variations
- **Expected**: 184 images (adjust seeds to 200)

#### `body-poses.yaml`
- **Target**: 200 images  
- **Templates**: standing, model_card (t-pose, a-pose), sitting, action, angle_coverage
- **Coverage**: Full body from 8 angles, sitting variations, dynamic poses
- **Expected**: 130 images (generate more seeds)

#### `hands.yaml`
- **Target**: 100 images
- **Templates**: hands_visible, hand_actions, hand_closeups, specific_positions
- **Coverage**: Critical for LoRA quality - hand poses, actions, close-ups
- **Uses**: Detailed_Hands-000001.safetensors LoRA from NAS

#### `context.yaml`
- **Target**: 200 images
- **Templates**: environments, clothing, lighting_scenarios, props_interaction
- **Coverage**: 8 environments × 4 lighting + clothing + props
- **Expected**: 210 images

### 4. Generation Orchestrator

**File**: `scripts/generate_structured_volume.py`

**Features**:
- ✅ Loads YAML templates from NAS
- ✅ Expands variable combinations (angles × expressions × etc.)
- ✅ Parallel execution with ThreadPoolExecutor
- ✅ VRAM monitoring (115GB max for 128GB AMD server)
- ✅ Progress tracking and ETA
- ✅ Metadata JSON for every generated image
- ✅ Checkpoint support (skip existing files)
- ✅ Category-based output organization

**Test Results**:
- Character: `test-001` (5 source images)
- Category: `portraits` only
- Generated: **184 tasks** (46 prompts × 4 models)
- Output: 184 images + 184 metadata files
- Rate: **~19 images/second** (with placeholder generation)

**Usage**:
```bash
python scripts/generate_structured_volume.py \
  --character test-001 \
  --categories portraits,body-poses,context,hands \
  --parallel 4 \
  --seeds 1
```

### 5. Metadata Tracking

Each generated image has JSON metadata:

```json
{
  "category": "portraits",
  "template_name": "headshots",
  "prompt": "ohwx_char, professional headshot, front view, neutral expression...",
  "model_name": "qwen-base",
  "lora_name": null,
  "source_images": ["/mnt/nas-ai-models/.../test_01.png", ...],
  "seed": 1000000,
  "generated_at": "2025-12-08T17:42:21.083613",
  "output_path": "/mnt/nas-ai-models/.../portraits_headshots_qwen_base_01000000.png"
}
```

This enables:
- ELO voting system to track which model generated each image
- Analytics dashboard to show model performance
- Future learning layer to predict best models

## What's NOT Yet Implemented

### Actual Model Inference (TODO)
The orchestrator currently:
- ✅ Loads templates
- ✅ Expands prompts
- ✅ Manages parallelism
- ✅ Tracks metadata
- ❌ **Generates placeholder files instead of real images**

**Next step**: Replace placeholder with actual Diffusers pipeline calls.

### ELO Voting System (TODO)
- Database schema (TrainingImage, Vote tables)
- Web UI for A/B comparisons
- ELO calculation (port from turbo-carnival)
- Category filtering
- Batch operations
- Curation export

### AMD Server Setup (TODO)
- ROCm PyTorch installation
- Test model compatibility (Qwen-Image-Edit, FLUX.2)
- Benchmark parallel capacity (4 vs 6 models)
- Network I/O testing

## Expected Volume with All Templates

| Category | Templates | Prompts | Models | Total Tasks |
|----------|-----------|---------|--------|-------------|
| Portraits | 4 | 46 | 4 | 184 |
| Body Poses | 6 | ~65 | 2 | 130 |
| Hands | 6 | ~34 | 2 | 68 |
| Context | 4 | ~70 | 3 | 210 |
| **TOTAL** | **20** | **215** | **varied** | **~592 tasks** |

With `--seeds 2`: **~1,184 images**  
After ELO curation (top 30-40%): **~350-470 training images**

## Next Steps

### Immediate (This Week)
1. **Implement actual image generation**:
   - Add Diffusers pipeline loading in `ModelManager`
   - Implement Qwen-Image-Edit generation in `execute_task()`
   - Test with 1 model × 10 prompts first
   
2. **Test on AMD server**:
   - SSH to AMD server
   - Install dependencies (PyYAML, PyTorch+ROCm)
   - Run small test (10 images)
   - Benchmark VRAM and throughput

3. **ELO voting system foundation**:
   - Create database schema (SQLite initially)
   - Port RecordVote logic from turbo-carnival
   - Build minimal CLI voting interface (before web UI)

### Week 2-3
4. Web UI for ELO voting
5. Analytics dashboard
6. First production run with real character

## Files Modified/Created

**New files** (staged):
```
openspec/changes/add-structured-volume-generation/
├── proposal.md
├── tasks.md
├── design.md
└── specs/
    ├── volume-generation/spec.md
    ├── elo-curation/spec.md
    └── dual-server-orchestration/spec.md

scripts/generate_structured_volume.py
```

**NAS files** (not in git):
```
/mnt/nas-ai-models/training-data/flenwheel/
├── sources/test-001/          # 5 test images
├── generated/test-001/
│   └── portraits/              # 184 images + metadata
└── templates/
    ├── portraits.yaml
    ├── body-poses.yaml
    ├── hands.yaml
    └── context.yaml
```

## Success Criteria (Phase 1)

- [x] OpenSpec proposal validated
- [x] NAS directory structure created
- [x] Template system working (YAML parsing + variable expansion)
- [x] Orchestrator runs without errors
- [x] Metadata tracking functional
- [x] Parallel execution working (ThreadPoolExecutor)
- [ ] ~~Actual image generation~~ (next phase)

**Conclusion**: Infrastructure is ready. Next focus: integrate actual model inference.

---

## Phase 2: Option A - Integrate Actual Generation (In Progress)

**Date**: 2025-12-08 (continued)

### Completed
- ✅ Added Diffusers imports to orchestrator
- ✅ Implemented `ModelManager.load_model()` with actual `QwenImageEditPlusPipeline`
- ✅ Implemented `execute_task()` with real image generation
- ✅ Model loading working (loads in ~1-2 seconds)
- ✅ Source image selection (random from available)
- ✅ Metadata enhanced with actual generation parameters

### Issues Encountered

**VRAM Management on RTX 4090**:
- Qwen-Image-Edit-2509 with bfloat16 + CPU offload consumes ~22GB VRAM
- First generation attempt runs but hits OOM during inference
- Device placement errors after OOM (`cuda:0` vs `cpu` tensor mismatch)
- 24GB RTX 4090 is at capacity with single model

**Root Cause**:
- ComfyUI was using 18.72GB when first tested (now stopped)
- Even with clean GPU, Qwen model fills nearly all 24GB
- `enable_model_cpu_offload()` helps but not enough for 24GB GPU

### Solutions to Implement

**Option 1: Use 8-bit quantization** (fastest fix for RTX 4090)
```python
pipeline = QwenImageEditPlusPipeline.from_pretrained(
    model_path,
    torch_dtype=torch.float16,  # or bfloat16
    load_in_8bit=True  # Reduce VRAM by ~40%
)
```

**Option 2: Move to AMD server** (recommended for production)
- 128GB VRAM can easily handle 4-6 models in parallel
- This was the original plan
- RTX 4090 better suited for LoRA training, not parallel generation

**Option 3: Reduce inference steps** (quality vs speed trade-off)
```python
num_inference_steps=20  # vs current 40
# Halves generation time and reduces peak VRAM
```

### Next Steps

**Immediate** (choose one):
1. **Quantization**: Add 8-bit support to ModelManager (test on RTX 4090)
2. **AMD Server**: Set up AMD environment and move generation there
3. **Hybrid**: Keep RTX 4090 for single-model testing, AMD for production volume

**Recommendation**: Go with **AMD Server** (Option 2) since:
- Original architecture design
- Enables 4-6 parallel models (core value proposition)
- RTX 4090 freed up for training and ELO voting UI

### Code Changes Made

**Updated files**:
- `scripts/generate_structured_volume.py`:
  - Added ML imports (torch, diffusers, PIL)
  - `ModelManager.load_model()`: Real Diffusers loading
  - `ModelManager.get_pipeline()`: Accessor for loaded pipelines
  - `execute_task()`: Actual generation with Qwen pipeline
  - Metadata tracking: Added actual source image used, generation params

**New test template**:
- `/mnt/nas-ai-models/training-data/flenwheel/templates/test.yaml`
- 5 prompts for quick validation

### Lessons Learned

1. **RTX 4090 (24GB) is tight for Qwen-Image-Edit**: Need quantization or AMD server
2. **Model loading works great**: ~1-2 seconds with CPU offload
3. **Device placement is sensitive**: OOM leads to cuda/cpu tensor mismatches
4. **Architecture is validated**: Template expansion, task generation, metadata all working

**Status**: Infrastructure proven, memory optimization needed for RTX 4090 testing.
