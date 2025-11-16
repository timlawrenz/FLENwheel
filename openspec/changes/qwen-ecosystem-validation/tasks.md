# Qwen Ecosystem Validation - Tasks

**Change ID**: `qwen-ecosystem-validation`  
**Status**: Proposed

## Task Breakdown

### Phase 1: Ecosystem Survey

#### Task 1.1: Hugging Face Model Discovery
**Estimated**: 30 minutes  
**Owner**: Tim Lawrenz  
**Status**: ✓ COMPLETE

- [✓] Browse https://huggingface.co/models?pipeline_tag=image-to-image&sort=trending&search=qwen
- [✓] Filter for Qwen-Image-Edit-2509 derivatives
- [✓] Review first 50 results for relevance
- [✓] Create initial list of candidates

**Deliverable**: ✓ 17 models identified in model-survey.md

**Key Findings**:
- YaoJiefu/multiple-characters - GAME CHANGER (multi-character, any angle)
- 2x Face segmentation models (identity verification)
- 3x Lighting control models (neutralize + directional)
- Updated dx8152 with consistency fix (2025/11/2)
- 4 models from dx8152 (active developer)

---

#### Task 1.2: Model Card Review
**Estimated**: 1 hour  
**Owner**: Tim Lawrenz  
**Status**: ✓ PARTIALLY COMPLETE (3 of 10 models reviewed)

For each candidate model:
- [✓] YaoJiefu/multiple-characters - MISLEADING (scene population, not angle changes)
- [✓] dx8152/Qwen-Edit-2509-Multiple-angles - ✅ VALIDATED! THE core model
- [✓] InstantX/Qwen-Image-ControlNet-Union - WRONG MODEL FAMILY (Qwen-Image vs Qwen-Image-Edit)
- [ ] TsienDragon/qwen-image-edit-lora-face-segmentation
- [ ] djessica/QE-2509-Relight
- [ ] dx8152/Qwen-Edit-2509-Multi-Angle-Lighting
- [ ] dx8152/Qwen-Image-Edit-2509-Relight
- [ ] TsienDragon/qwen-image-edit-character-composition
- [ ] valiantcat/Qwen-Image-Edit-MeiTu
- [ ] Base Qwen-Image-Edit-2509

**Deliverable**: ✓ Model card analysis documented in model-survey.md

**CRITICAL FINDINGS**:
- ✅ dx8152/Multiple-angles CONFIRMED via car example
  - Takes front view → generates profile view
  - PRESERVES identity (same car, scene, lighting)
  - Changes ONLY camera viewpoint
  - Text-driven: "move camera to the right" → 45° profile
  - This solves our PRIMARY requirement!
  
- ❌ YaoJiefu/multiple-characters misleading
  - Scene population, not character transformation
  
- ❌ InstantX ControlNets incompatible
  - For Qwen-Image (generation), not Qwen-Image-Edit
  - Wrong model family entirely

**STRATEGIC VALIDATION**:
- Proof of concept exists (car example)
- Identity preservation works
- Simple text prompts
- 1 source → 8+ angle variations possible
- Ready for testing phase

---

#### Task 1.3: Relevance Scoring
**Estimated**: 30 minutes  
**Owner**: Tim Lawrenz  
**Status**: ✓ COMPLETE (updated based on model card reviews)

Score each model (1-5) on:
- [✓] Relevance to character consistency (identity preservation)
- [✓] Relevance to angle changes
- [✓] Relevance to lighting/complexion
- [✓] Quality indicators (examples, stars, downloads)
- [✓] Select top 5-10 models for testing

**Deliverable**: ✓ Prioritized list in model-survey.md

**FINAL TOP 5 (Revised after model card review)**:
1. dx8152/Qwen-Edit-2509-Multiple-angles ⭐⭐⭐⭐⭐ - CAMERA angles (VALIDATED!)
2. TsienDragon/qwen-image-edit-lora-face-segmentation ⭐⭐⭐⭐⭐ - Identity verification
3. dx8152/Qwen-Edit-2509-Multi-Angle-Lighting ⭐⭐⭐⭐ - LIGHTING direction
4. djessica/QE-2509-Relight ⭐⭐⭐⭐ - Lighting neutralization
5. Base Qwen-Image-Edit-2509 ⭐⭐⭐⭐ - Background/composition

**Deprioritized**:
- YaoJiefu/multiple-characters (scene population, not editing)
- InstantX ControlNets (wrong model family - Qwen-Image vs Qwen-Image-Edit)

**STRATEGIC DECISION**: Focus on 4 core models for multi-dimensional enrichment pipeline

---

### Phase 2: Environment Setup

#### Task 2.1: Python Environment
**Estimated**: 15 minutes  
**Owner**: Tim Lawrenz

```bash
cd /home/tim/source/activity/FLENwheel
python3 -m venv venv
source venv/bin/activate
```

- [ ] Create virtual environment
- [ ] Activate environment
- [ ] Verify Python version (3.13.3)

**Deliverable**: Active venv

---

#### Task 2.2: Install Dependencies
**Estimated**: 30 minutes  
**Owner**: Tim Lawrenz

```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip install diffusers transformers accelerate bitsandbytes
pip install pillow opencv-python numpy pandas
pip install huggingface_hub
```

- [ ] Install PyTorch with CUDA support
- [ ] Install Diffusers and Transformers
- [ ] Install image processing libraries
- [ ] Install Hugging Face hub
- [ ] Verify installations with `pip list`

**Deliverable**: Working Python environment with all dependencies

---

#### Task 2.3: Download Base Model
**Estimated**: 1-2 hours (mostly waiting)  
**Owner**: Tim Lawrenz

```bash
huggingface-cli login  # If needed
huggingface-cli download Qwen/Qwen-Image-Edit-2509
```

- [ ] Login to Hugging Face (if required)
- [ ] Download Qwen-Image-Edit-2509 (~14GB)
- [ ] Verify download complete
- [ ] Note storage location (~/.cache/huggingface/)

**Deliverable**: Downloaded base model

---

#### Task 2.4: Download Specialized LoRAs
**Estimated**: 30 minutes (mostly waiting)  
**Owner**: Tim Lawrenz

For each selected LoRA:
```bash
huggingface-cli download <model-name>
```

- [ ] Download dx8152/Qwen-Edit-2509-Multiple-angles
- [ ] Download face/identity preservation LoRAs (2-3 models)
- [ ] Download lighting/complexion LoRAs (1-2 models)
- [ ] Download reference models (1-2 models)
- [ ] Verify all downloads complete
- [ ] Document total disk usage

**Deliverable**: All test models downloaded

---

#### Task 2.5: Create Directory Structure
**Estimated**: 5 minutes  
**Owner**: Tim Lawrenz

```bash
mkdir -p test_data/{source,results/{base,loras}}
mkdir -p scripts
```

- [ ] Create test_data/source for input images
- [ ] Create test_data/results for outputs
- [ ] Create scripts directory
- [ ] Create .gitignore for test_data (large files)

**Deliverable**: Test directory structure

---

#### Task 2.6: Prepare Test Images
**Estimated**: 30 minutes  
**Owner**: Tim Lawrenz

- [ ] Select or create 5 character source images
- [ ] Ensure variety (angles, expressions, lighting)
- [ ] Verify image quality (sharp, well-lit)
- [ ] Copy to test_data/source/
- [ ] Name consistently (test_01.jpg - test_05.jpg)
- [ ] Document image characteristics

**Deliverable**: 5 standardized test images

---

### Phase 3: Comparative Testing

#### Task 3.1: Create Base Test Script
**Estimated**: 1 hour  
**Owner**: Tim Lawrenz

- [ ] Create scripts/test_base_model.py
- [ ] Implement model loading with 4-bit quantization
- [ ] Implement editing prompt variations
- [ ] Add VRAM monitoring
- [ ] Add error handling
- [ ] Test script runs successfully

**Deliverable**: scripts/test_base_model.py

**Script requirements**:
- Load Qwen-Image-Edit-2509 base model
- Process all 5 test images
- Apply 3-5 editing prompts per image:
  - Background change (forest, beach, studio)
  - Lighting change (sunset, daylight, studio)
  - Angle change (slightly left, slightly right)
- Save results with descriptive names
- Log VRAM usage
- Save metadata (prompt, inference time, parameters)

---

#### Task 3.2: Create LoRA Test Script
**Estimated**: 1 hour  
**Owner**: Tim Lawrenz

- [ ] Create scripts/test_lora_model.py
- [ ] Implement LoRA loading on top of base model
- [ ] Reuse editing prompts from base test
- [ ] Add LoRA-specific prompts (based on model specialty)
- [ ] Test script runs successfully

**Deliverable**: scripts/test_lora_model.py

**Script requirements**:
- Load base model + specific LoRA
- Process all 5 test images
- Apply same prompts as base model (for comparison)
- Apply LoRA-specific prompts (e.g., angle changes for dx8152)
- Save results with LoRA identifier
- Log VRAM usage with LoRA
- Save metadata

---

#### Task 3.3: Run Base Model Tests
**Estimated**: 30 minutes  
**Owner**: Tim Lawrenz

```bash
python scripts/test_base_model.py
```

- [ ] Run test script on all 5 images
- [ ] Verify outputs generated correctly
- [ ] Check VRAM usage stayed within limits
- [ ] Review sample outputs for obvious issues
- [ ] Document any errors or warnings

**Deliverable**: Base model test results in test_data/results/base/

---

#### Task 3.4: Run LoRA Model Tests
**Estimated**: 2-3 hours (sequential testing)  
**Owner**: Tim Lawrenz

For each downloaded LoRA:
```bash
python scripts/test_lora_model.py --lora <model-name>
```

- [ ] Test dx8152 angle LoRA
- [ ] Test face/identity LoRAs (2-3 models)
- [ ] Test lighting/complexion LoRAs (1-2 models)
- [ ] Test reference models (1-2 models)
- [ ] Verify outputs for each
- [ ] Document VRAM usage
- [ ] Note any loading errors

**Deliverable**: All LoRA test results in test_data/results/loras/<lora-name>/

---

#### Task 3.5: Manual Quality Review
**Estimated**: 1-2 hours  
**Owner**: Tim Lawrenz

For each model's outputs:
- [ ] Review all generated images
- [ ] Assess character identity preservation (1-5 scale)
- [ ] Assess edit quality (did it do what we asked?) (1-5 scale)
- [ ] Count visible artifacts
- [ ] Note specific failure modes
- [ ] Document best/worst examples

**Deliverable**: Quality assessment notes for each model

---

#### Task 3.6: Quantitative Analysis
**Estimated**: 30 minutes  
**Owner**: Tim Lawrenz

- [ ] Create comparison spreadsheet/table
- [ ] Calculate average identity preservation per model
- [ ] Calculate average edit quality per model
- [ ] Calculate artifact frequency per model
- [ ] Compare VRAM usage across models
- [ ] Rank models by overall quality

**Deliverable**: Comparison matrix with quantitative data

---

### Phase 4: Analysis & Decision

#### Task 4.1: Create Results Document
**Estimated**: 30 minutes  
**Owner**: Tim Lawrenz

- [ ] Create docs/qwen-ecosystem-results.md
- [ ] Document survey findings (models identified)
- [ ] Include comparison matrix
- [ ] Add best/worst example images
- [ ] Document VRAM and performance data
- [ ] List strengths/weaknesses per model

**Deliverable**: docs/qwen-ecosystem-results.md

---

#### Task 4.2: Strategic Analysis
**Estimated**: 30 minutes  
**Owner**: Tim Lawrenz

Evaluate strategic options:
- [ ] **Option A**: Use existing LoRA(s) as-is
  - Which model(s)?
  - What quality gaps remain?
  - Estimated timeline to production
- [ ] **Option B**: Multi-LoRA combination
  - Which models to combine?
  - Technical feasibility assessment
  - Complexity vs. benefit trade-off
- [ ] **Option C**: Custom LoRA training
  - What gaps require custom training?
  - Estimated training time/effort
  - Which existing LoRA to use as reference?
- [ ] **Option D**: Hybrid approach
  - Which existing LoRAs to start with?
  - What to train custom for?
  - Phased implementation plan

**Deliverable**: Strategic options analysis with pros/cons

---

#### Task 4.3: Make Decision
**Estimated**: 15 minutes  
**Owner**: Tim Lawrenz

- [ ] Select optimal approach based on data
- [ ] Document decision rationale
- [ ] Identify next steps for chosen approach
- [ ] Update project timeline
- [ ] Update STATUS.md with decision

**Deliverable**: Strategic decision documented in results.md

---

#### Task 4.4: Update Documentation
**Estimated**: 15 minutes  
**Owner**: Tim Lawrenz

- [ ] Update docs/SUMMARY.md with results
- [ ] Update STATUS.md with validation complete
- [ ] Update docs/technical-feasibility.md with findings
- [ ] Commit all documentation changes
- [ ] Push to GitHub

**Deliverable**: All documentation synchronized

---

## Summary

**Total Estimated Time**: 7-10 hours  
**Time Spent (Phase 1)**: ~2 hours
**Critical Path**: Survey → Setup → Testing → Decision  
**Parallelizable**: Model downloads (can work on other tasks while downloading)  

**Phase 1 Progress**: ✓ COMPLETE (all 3 tasks)
- ✓ Task 1.1: Ecosystem Survey (17 models identified)
- ✓ Task 1.2: Model Card Review (3 critical reviews completed)
- ✓ Task 1.3: Relevance Scoring (Top 5 finalized)

**KEY BREAKTHROUGH**: 
dx8152/Qwen-Edit-2509-Multiple-angles VALIDATED
- Car example proves identity preservation works
- Front view → profile view with text prompt
- Preserves everything except camera angle
- This solves our PRIMARY requirement!

**READY FOR PHASE 2**: Environment Setup & Testing  

**Dependencies**:
- Task 2.4 depends on Task 1.3 (need to know which models to download)
- Task 3.x depends on Task 2.x (need environment setup)
- Task 4.x depends on Task 3.x (need test results)

**Checkpoints**:
- After Task 1.3: Confirm model selection before downloading
- After Task 2.6: Verify test images are appropriate
- After Task 3.3: Sanity check base model results before testing LoRAs
- After Task 4.2: Review strategic options before finalizing decision

---

## Task Status Tracking

Mark tasks as:
- [ ] Not started
- [→] In progress  
- [✓] Complete
- [✗] Blocked/Failed

Update this file as you work through tasks to track progress.
