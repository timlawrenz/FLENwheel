# FLENwheel Process Flow Documentation

## Overview

This document details the complete FLENwheel process with all loops, steps, and requirements.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      FLYWHEEL 1: Character LoRA                  │
│                                                                  │
│  Source Material → Qwen Enrichment → FLUX Training →            │
│  Synthetic Generation → Human Review → Pristine Dataset ──┐     │
│                                                            │     │
└────────────────────────────────────────────────────────────┼─────┘
                                                             │
                                                             │ feeds
                                                             │ back
┌────────────────────────────────────────────────────────────┼─────┐
│                    FLYWHEEL 2: Qwen Editor LoRA            │     │
│                                                            │     │
│  ┌─────────────────────────────────────────────────────────┘     │
│  │                                                               │
│  └─→ Correction Dataset → Qwen Training → Improved Editor       │
│                                                  │               │
└──────────────────────────────────────────────────┼───────────────┘
                                                   │
                                                   │ improves
                                                   │ Flywheel 1
                                                   └───────────────┐
                                                                   │
                                                                   ▼
                                            (Next iteration better)
```

## Flywheel 1: Character LoRA Training Loop

### Step 1.1: Source Material Curation
**Input**: Raw character images (photos, sketches, renders)  
**Output**: Curated source dataset with captions

**Requirements**:
- 10-20 initial images minimum
- Variety in angles (front, side, 3/4 view)
- Variety in expressions (if available)
- High quality (sharp, well-lit)
- Consistent character appearance

**Process**:
1. Gather source images
2. Quality check (remove blurry, poorly lit)
3. Caption with instance token (e.g., "photo of ohwx_char person")
4. Organize in `data/source/v1/` directory
5. Create metadata.json:
   ```json
   {
     "dataset_version": "v1",
     "images": [
       {
         "filename": "source_001.jpg",
         "caption": "photo of ohwx_char person, neutral expression, front view",
         "angle": "front",
         "expression": "neutral",
         "quality": "high"
       }
     ]
   }
   ```

**Success Criteria**:
- ✅ At least 10 usable images
- ✅ At least 2 different angles
- ✅ All images properly captioned
- ✅ Metadata file complete

**Tools/Scripts**:
- `scripts/curate_source.py` (to create)
- Manual review process

---

### Step 1.2: Dataset Enrichment (Qwen-Image-Edit)
**Input**: Curated source dataset  
**Output**: Enriched dataset (50-100 images)

**Requirements**:
- Qwen-Image-Edit-2509 model loaded and running
- Optional: dx8152 angle LoRA (if angle changes needed)
- Source images from Step 1.1
- Enrichment prompt templates
- VRAM available (~16GB for base model)

**Process**:
1. Load Qwen-Image-Edit-2509 pipeline
2. Optional: Load dx8152 LoRA for angle editing
3. For each source image:
   - Apply 3-5 different editing prompts:
     - "Change background to [forest/studio/beach/urban], keep person identical"
     - "Change lighting to [daylight/sunset/nighttime/studio], keep person identical"
     - "Keep the person identical, but make it look like [oil painting/watercolor/sketch]"
     - "Change camera angle to [slightly left/slightly right/lower/higher], maintain appearance"
   - Generate edited image
   - Save with metadata linking to source
4. Organize outputs in `data/enriched/v1/`
5. Create enrichment_metadata.json

**Success Criteria**:
- ✅ 5x source images = 50+ enriched images minimum
- ✅ Character identity preserved in 70%+ of outputs
- ✅ Diverse backgrounds, lighting, angles
- ✅ All outputs linked to source in metadata

**Tools/Scripts**:
- `scripts/enrich_dataset.py` (to create)
- Qwen-Image-Edit-2509 inference wrapper
- Optional: dx8152 LoRA integration

**Quality Gates**:
- Automated identity check (face_recognition library)
- Manual review of samples (every 10th image minimum)
- Reject and re-generate if character drifts

---

### Step 1.3: Human Review (Enriched Dataset)
**Input**: Enriched dataset from Step 1.2  
**Output**: Reviewed dataset with quality labels

**Requirements**:
- Human reviewer (you)
- Review interface or organized folders
- Clear quality criteria

**Process**:
1. Review each enriched image:
   - Does it look like the character? (Identity)
   - Is the edit appropriate? (Background/lighting changed, character unchanged)
   - Any artifacts or distortions? (Quality)
2. Label each image:
   - `good`: Use for training
   - `needs_correction`: Save for Qwen training dataset (Flywheel 2)
   - `reject`: Don't use
3. Move images to appropriate folders:
   - `data/enriched/v1/good/`
   - `data/enriched/v1/corrections/` (for Flywheel 2)
   - `data/enriched/v1/rejected/`

**Success Criteria**:
- ✅ All images reviewed
- ✅ At least 30 "good" images for training
- ✅ Rejection reasons documented

**Tools/Scripts**:
- `scripts/review_interface.py` (optional - to create)
- Manual folder organization

---

### Step 1.4: FLUX Character LoRA Training
**Input**: Good enriched images from Step 1.3  
**Output**: FLUX character LoRA checkpoint (char_lora_v1.safetensors)

**Requirements**:
- ai-toolkit installed and configured
- Training dataset ready (30+ images)
- Captions for all images
- VRAM available (~18-22GB for training)
- Training time (2-8 hours estimated)

**Process**:
1. Prepare training config:
   ```yaml
   # config/flux_char_lora_v1.yaml
   model: "black-forest-labs/FLUX.1-dev"
   lora_rank: 16
   learning_rate: 1e-4
   batch_size: 1
   gradient_checkpointing: true
   mixed_precision: "bf16"
   max_train_steps: 1000
   save_every: 250
   dataset_path: "data/enriched/v1/good/"
   output_path: "models/flux_lora/char_v1/"
   ```
2. Run training script
3. Monitor training loss
4. Save checkpoint

**Success Criteria**:
- ✅ Training completes without OOM
- ✅ Loss decreases steadily
- ✅ Checkpoint saved successfully
- ✅ Can load checkpoint for inference

**Tools/Scripts**:
- ai-toolkit (existing)
- `configs/flux_char_lora_v1.yaml` (to create)

---

### Step 1.5: Synthetic Data Generation (FLUX + LoRA)
**Input**: FLUX + char_lora_v1  
**Output**: Synthetic images (50-200 images)

**Requirements**:
- FLUX model + trained LoRA loaded
- Generation prompts (novel scenarios)
- VRAM available (~12-15GB for inference)

**Process**:
1. Load FLUX + char_lora_v1
2. Generate images with diverse prompts:
   - New angles: "profile view of ohwx_char person"
   - New expressions: "ohwx_char person smiling"
   - New scenarios: "ohwx_char person in a spaceship"
   - New poses: "ohwx_char person sitting on a chair"
3. Generate multiple variants per prompt (4-8 images)
4. Save to `data/synthetic/v1/`
5. Track generation prompts in metadata

**Success Criteria**:
- ✅ 50+ synthetic images generated
- ✅ Diverse prompts covering model card targets
- ✅ Metadata tracks prompt and seed

**Tools/Scripts**:
- `scripts/generate_synthetic.py` (to create)
- FLUX inference wrapper with LoRA

---

### Step 1.6: AI-Assisted Filtering
**Input**: Synthetic images from Step 1.5  
**Output**: Filtered candidates for review

**Requirements**:
- face_recognition library installed
- Reference images of character
- Similarity threshold defined

**Process**:
1. Extract face encoding from reference images
2. For each synthetic image:
   - Extract face encoding
   - Compare to reference
   - Calculate similarity score
3. Filter images above threshold (e.g., 0.6)
4. Move to `data/synthetic/v1/filtered/`

**Success Criteria**:
- ✅ Obvious bad images removed (no face, wrong character)
- ✅ Candidates reduced by 50-70%
- ✅ Few false negatives (good images not filtered out)

**Tools/Scripts**:
- `scripts/filter_identity.py` (to create)
- face_recognition library

---

### Step 1.7: Human Review (Synthetic Dataset)
**Input**: Filtered synthetic images  
**Output**: Pristine dataset for next training iteration

**Requirements**:
- Human reviewer
- Quality criteria (stricter than Step 1.3)

**Process**:
1. Review each filtered image:
   - Perfect character match?
   - Anatomically correct?
   - High quality (no artifacts)?
   - Useful for training (fills a gap)?
2. Select best 10-20 images
3. Move to `data/pristine/v1/`
4. Add to training dataset for v2

**Success Criteria**:
- ✅ 10+ pristine images selected
- ✅ Cover new angles/expressions/poses not in original dataset
- ✅ All meet strict quality bar

**Tools/Scripts**:
- Manual review process

---

### Step 1.8: Iteration (Train char_lora_v2)
**Input**: Original enriched dataset + pristine synthetic dataset  
**Output**: char_lora_v2.safetensors

**Process**:
1. Combine datasets:
   - `data/enriched/v1/good/`
   - `data/pristine/v1/`
2. Retrain FLUX LoRA (char_lora_v2)
3. Compare v1 vs v2 quality on benchmark prompts

**Success Criteria**:
- ✅ v2 shows improvement on benchmark images
- ✅ v2 handles new angles/expressions better

**Loop**: Repeat Steps 1.5-1.8 until model card targets achieved

---

## Flywheel 2: Qwen Editor LoRA Training Loop

### Step 2.1: Correction Dataset Curation
**Input**: Images marked "needs_correction" from Step 1.3  
**Output**: (source, prompt, corrected) triplet dataset

**Requirements**:
- Images that need correction
- Manual editing tools (Photoshop/GIMP) OR improved prompts
- Study of dx8152 dataset structure

**Process**:
1. For each "needs_correction" image:
   - Identify what's wrong (identity drift, artifacts, insufficient angle change)
   - Create corrected version manually OR
   - Find improved prompt that fixes the issue
2. Create training triplet (following dx8152's approach):
   ```json
   {
     "source_image": "data/source/v1/source_001.jpg",
     "edit_prompt": "Change background to forest, keep face identical",
     "target_image": "data/corrections/v1/corrected_001.jpg",
     "issue": "Original edit changed nose shape",
     "improvement": "Manual correction preserved facial structure"
   }
   ```
3. Save to `data/qwen_training/v1/`

**Success Criteria**:
- ✅ 10+ correction triplets
- ✅ Clear difference between before/after
- ✅ Corrections demonstrate desired behavior

**Tools/Scripts**:
- `scripts/create_correction_triplets.py` (to create)
- Manual editing tools

---

### Step 2.2: Qwen-Image-Edit LoRA Training
**Input**: Correction triplet dataset  
**Output**: qwen_char_lora_v1.safetensors

**Requirements**:
- PEFT library installed
- Qwen-Image-Edit-2509 base model
- Training dataset (10+ triplets)
- VRAM available (~18-22GB)
- Study of dx8152 training approach

**Process**:
1. Study dx8152/Qwen-Edit-2509-Multiple-angles:
   - Training methodology
   - Dataset structure
   - Hyperparameters used
2. Prepare training config (adapted from dx8152):
   ```python
   # QLoRA configuration for Qwen-Image-Edit
   from peft import LoraConfig
   
   lora_config = LoraConfig(
       r=8,  # LoRA rank (adjust based on dx8152)
       lora_alpha=32,
       target_modules=["q_proj", "v_proj"],  # Model-specific
       lora_dropout=0.1,
       bias="none",
   )
   ```
3. Load Qwen-Image-Edit-2509 in 4-bit
4. Add LoRA adapter
5. Train on character consistency triplets
6. Save adapter

**Success Criteria**:
- ✅ Training completes without OOM
- ✅ Adapter improves character consistency vs base model
- ✅ Adapter quality exceeds dx8152 for our specific character
- ✅ Can save/load adapter

**Tools/Scripts**:
- `scripts/train_qwen_lora.py` (to create, based on dx8152 approach)
- PEFT library

**Note**: dx8152 proves this works; our goal is character-specific improvement

---

### Step 2.3: Integration (Use qwen_char_lora_v1 in Flywheel 1)
**Input**: Trained Qwen character LoRA adapter  
**Output**: Improved enrichment in next Flywheel 1 iteration

**Process**:
1. Update enrichment script to load Qwen-Image-Edit-2509 + qwen_char_lora_v1
2. Run Step 1.2 with improved character-specific editor
3. Compare quality vs base model and dx8152 LoRA

**Success Criteria**:
- ✅ Fewer "needs_correction" images
- ✅ Better character consistency than base model
- ✅ Better character consistency than dx8152 LoRA
- ✅ Fewer manual rejections

**Loop**: Continue collecting corrections, retrain Qwen LoRA v2, v3...

---

## Model Card Requirements

### Purpose
Define concrete targets for "done" - when character LoRA is production-ready

### Required Images

#### Portrait Set (Head & Expressions)
- **Angles**: Front, Half-left, Profile-left, Half-right, Profile-right
- **Expressions**: Neutral, Smiling, Angry, Sad
- **Total**: 5 angles × 4 expressions = 20 images
- **Requirements**:
  - Clean background (solid color or simple)
  - Consistent lighting (studio-quality)
  - Sharp focus on face
  - Shoulders visible (not just floating head)

#### Body Pose Set
- **T-pose**: Front view, arms extended horizontally
- **Standing**: Front view, neutral pose, arms at sides
- **Sitting**: Side view, on chair, natural posture
- **Total**: 3 images
- **Requirements**:
  - Full body visible
  - Anatomically correct
  - Clean background
  - Consistent character appearance

#### Total Model Card Images: 23

### Quality Criteria
Each model card image must be:
- ✅ Generated from FLUX + character LoRA (no manual editing)
- ✅ Character identity verified (face recognition match)
- ✅ Anatomically correct (especially poses)
- ✅ High resolution (1024x1024 minimum)
- ✅ Artifact-free
- ✅ Meets aesthetic quality bar

### Benchmark Testing
- Generate each model card image with standardized prompt
- Track success rate (what % generate correctly on first try)
- Target: 80%+ success rate for v1.0 release

### Prompt Templates
```
# Portrait examples
"portrait of ohwx_char person, neutral expression, front view, clean background, studio lighting"
"portrait of ohwx_char person, smiling, profile-left view, clean background, studio lighting"

# Body pose examples
"full body photo of ohwx_char person in T-pose, front view, white background"
"full body photo of ohwx_char person standing, front view, neutral pose, clean background"
"full body photo of ohwx_char person sitting on a chair, side view, clean background"
```

---

## Dependencies Between Steps

### Critical Path
```
1.1 (Source) → 1.2 (Enrich) → 1.3 (Review) → 1.4 (Train FLUX) →
1.5 (Generate) → 1.6 (Filter) → 1.7 (Review) → 1.8 (Retrain)
```

### Parallel Path (Flywheel 2)
```
1.3 (Review) → 2.1 (Corrections) → 2.2 (Train Qwen) → 2.3 (Integrate)
                                                          ↓
                                                    Back to 1.2
```

### Blocking Requirements
- **Can't do 1.2** until Qwen-Image-Edit working
- **Can't do 1.4** until training data ready
- **Can't do 1.5** until FLUX LoRA trained
- **Can't do 2.2** until dx8152 approach studied and PEFT implemented
- **Step 2.2 is optional** - Flywheel 1 can run with base model or dx8152 LoRA

---

## Proof of Concept Milestones

### POC Phase 1: Basic Validation (Week 1)
- [ ] Qwen-Image-Edit-2509 inference working
- [ ] Test with dx8152 LoRA
- [ ] Can enrich 5 test images
- [ ] Manual review confirms character consistency
- [ ] Assess quality: good enough or need custom LoRA?

### POC Phase 2: Single Flywheel 1 Iteration (Week 2-3)
- [ ] Complete Steps 1.1-1.4
- [ ] Generate char_lora_v1
- [ ] Test on benchmark prompts

### POC Phase 3: Full Flywheel 1 Loop (Week 3-4)
- [ ] Complete Steps 1.5-1.8
- [ ] Generate char_lora_v2
- [ ] Measure improvement v1 → v2

### POC Phase 4: Flywheel 2 (Week 5+)
- [ ] Study dx8152 approach thoroughly
- [ ] Learn PEFT for image editing models
- [ ] Complete Steps 2.1-2.2
- [ ] Test qwen_char_lora_v1 in next iteration
- [ ] Compare: base model vs dx8152 vs custom LoRA

---

## Open Questions & Decisions Needed

1. **Base model quality**: Is Qwen-Image-Edit-2509 good enough or need custom LoRA immediately?
2. **dx8152 LoRA**: Can we use it as-is, or just as reference?
3. **Instance token naming**: "ohwx_char" or something else?
4. **Review interface**: Manual folders or build UI?
5. **Automated quality metrics**: Beyond face recognition, what else?
6. **Version control**: How to track dataset versions?
7. **Checkpoint strategy**: How often to save during training?
8. **Flywheel 2 priority**: Start after Flywheel 1 proven, or in parallel?
9. **Training data volume**: How many triplets for meaningful custom LoRA improvement?
