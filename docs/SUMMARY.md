# FLENwheel Project Summary

**Last Updated**: 2025-11-16

## What We've Established

### ✅ Confirmed Technical Capabilities
- **FLUX inference**: Proven working on RTX 4090
- **FLUX LoRA training**: Proven working with ai-toolkit
- **System specs**: RTX 4090, 24GB VRAM, Python 3.13.3

### ❓ To Validate (Next Steps)
- **Qwen-Image-Edit-2509 inference**: Download and test (5-7 hours)
- **dx8152 LoRA quality**: Test angle editing capabilities
- **Character consistency**: Can base model preserve identity well enough?
- **Custom LoRA training**: Learn PEFT approach from dx8152

## Correct Model Stack

### Image Editing (Flywheel 1, Step 1.2)
- **Base**: Qwen/Qwen-Image-Edit-2509 (~14GB)
  - Official Qwen image editing model
  - Designed for image-to-image editing
- **Reference LoRA**: dx8152/Qwen-Edit-2509-Multiple-angles
  - Community fine-tune for angle changes
  - Proof that character-specific training works
  - Quality: "great inspiration, but not good enough yet"

### Image Generation (Flywheel 1, Steps 1.4-1.5)
- **Base**: FLUX.1-dev
- **Custom**: Character LoRAs (trained via ai-toolkit)

## Dual-Flywheel Architecture

### Flywheel 1: Character LoRA (Proven Path)
```
Source Images (10-20)
  ↓
Qwen-Image-Edit Enrichment (50-100 images)
  ↓
FLUX LoRA v1 Training
  ↓
Synthetic Generation (50-200 images)
  ↓
AI Filtering + Human Review
  ↓
Pristine Dataset (10-20 best)
  ↓
FLUX LoRA v2 Training (improved)
  ↓
Repeat until Model Card achieved
```

### Flywheel 2: Qwen Editor LoRA (Learning Required)
```
Correction Dataset (from Flywheel 1 review)
  ↓
Study dx8152 approach
  ↓
Train Custom Character LoRA
  ↓
Integrate into Flywheel 1
  ↓
Better enrichment quality
```

## Model Card Requirements

### Goal: 23 Benchmark Images

**Portraits** (20 images):
- 5 angles: Front, Half-left, Profile-left, Half-right, Profile-right
- 4 expressions: Neutral, Smiling, Angry, Sad
- Clean background, studio lighting, shoulders visible

**Body Poses** (3 images):
- T-pose: Arms extended, front view
- Standing: Neutral pose, arms at sides
- Sitting: On chair, side view

**Success Metric**: 80%+ first-try generation success rate

## Critical Decisions Needed

### 1. Base Model Quality Assessment (Week 1)
**Question**: Is Qwen-Image-Edit-2509 good enough, or do we need custom LoRA immediately?

**Test Plan**:
- Enrich 5-10 test images
- Measure character consistency (target: 70%+)
- Compare base vs dx8152 LoRA
- Identify failure modes

**Decision Impact**: 
- Good enough → Focus on Flywheel 1
- Not good enough → Start Flywheel 2 in parallel

### 2. LoRA Training Strategy (Week 2-3)
**Options**:
- A) Use base model, only train LoRA if insufficient
- B) Use dx8152 LoRA as baseline
- C) Train custom LoRA from start (following dx8152 approach)

### 3. POC Scope (Week 1)
**Recommendation**: Minimal viable loop
- 10 source images
- 30 enriched images (base model only)
- FLUX LoRA v1
- 20 synthetic images
- FLUX LoRA v2
- Measure improvement

## File Organization

```
FLENwheel/
├── docs/
│   ├── brainstorming.md          # Original concept
│   ├── basic-process.td          # Mermaid diagram
│   ├── technical-feasibility.md  # Detailed analysis
│   ├── process-flow.md           # Step-by-step procedures
│   ├── quick-start.md            # Immediate next actions
│   └── SUMMARY.md                # This file
├── openspec/
│   └── project.md                # Project context for AI agents
├── scripts/                       # To create
│   ├── test_qwen_edit_basic.py
│   ├── test_qwen_edit_lora.py
│   ├── test_comprehensive_editing.py
│   ├── enrich_dataset.py
│   ├── filter_identity.py
│   ├── generate_synthetic.py
│   └── train_qwen_lora.py
├── data/                          # To create
│   ├── source/v1/
│   ├── enriched/v1/
│   ├── synthetic/v1/
│   ├── pristine/v1/
│   └── qwen_training/v1/
└── models/                        # To create
    ├── flux_lora/char_v1/
    └── qwen_lora/char_v1/
```

## Immediate Next Steps (Today/This Week)

### Phase 1: Environment Setup (2-3 hours)
```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install torch torchvision diffusers transformers accelerate bitsandbytes pillow opencv-python

# 3. Download models (background - 1-2 hours)
huggingface-cli download Qwen/Qwen-Image-Edit-2509
huggingface-cli download dx8152/Qwen-Edit-2509-Multiple-angles

# 4. Create directory structure
mkdir -p {scripts,test_data,data/{source,enriched,synthetic,pristine,qwen_training}/v1,models/{flux_lora,qwen_lora}}
```

### Phase 2: Basic Validation (3-4 hours)
1. Create and run `test_qwen_edit_basic.py`
2. Create and run `test_qwen_edit_lora.py` (with dx8152)
3. Create and run `test_comprehensive_editing.py`
4. Manual review of all outputs
5. Document quality assessment

### Phase 3: Decision Point (End of Week 1)
Based on Phase 2 results:
- ✅ Quality good enough → Proceed with Flywheel 1 POC
- ❌ Quality insufficient → Plan Flywheel 2 parallel development
- 📊 Document findings in new `docs/validation-results.md`

## Success Criteria by Phase

### Week 1: Validation Complete
- [ ] Qwen-Image-Edit-2509 running
- [ ] dx8152 LoRA tested
- [ ] 5 test images enriched
- [ ] Character consistency rate measured
- [ ] Decision made: base model vs custom LoRA

### Week 2-3: First Loop Complete
- [ ] 10 source images prepared
- [ ] 30+ enriched images generated
- [ ] FLUX LoRA v1 trained
- [ ] 20+ synthetic images generated
- [ ] FLUX LoRA v2 trained
- [ ] Quality improvement documented

### Week 4-5: PEFT Learning
- [ ] dx8152 approach understood
- [ ] PEFT library working
- [ ] Test Qwen LoRA trained (5 triplets)
- [ ] Quality improvement vs base measured

## Key Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Base model quality insufficient | Have custom LoRA path ready via dx8152 study |
| VRAM constraints | 4-bit quantization proven to work |
| Training time too long | Start with small datasets, optimize later |
| Character identity drift | Strict human review gates + face recognition |
| PEFT learning curve | dx8152 provides working example |

## Reference Links

- **Base Model**: https://huggingface.co/Qwen/Qwen-Image-Edit-2509
- **Reference LoRA**: https://huggingface.co/dx8152/Qwen-Edit-2509-Multiple-angles
- **Qwen Image Collection**: https://huggingface.co/collections/Qwen/qwen-image
- **FLUX**: black-forest-labs/FLUX.1-dev
- **ai-toolkit**: (your existing installation)

## Open Questions

1. What's the actual character consistency rate of base Qwen-Image-Edit-2509?
2. Does dx8152 LoRA improve angle editing sufficiently?
3. How many correction triplets needed for meaningful custom LoRA improvement?
4. Should we train custom LoRA immediately or only if base insufficient?
5. What face recognition model/threshold works best for filtering?
6. Manual review UI needed, or folder-based workflow sufficient?
7. How to version datasets and model checkpoints effectively?

## Notes for Future Reference

- dx8152 acknowledges their LoRA is "not good enough yet" - validates our need for improvement
- Qwen-Image collection shows active development - may see better base models soon
- PEFT/QLoRA proven to work on 4090 via dx8152 example
- Character consistency is THE critical metric - everything else is secondary
- Human review is bottleneck but essential - don't skip or automate prematurely
