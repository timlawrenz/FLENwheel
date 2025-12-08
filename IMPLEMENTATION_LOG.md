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
