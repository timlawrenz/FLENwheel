# Technical Feasibility Analysis

**System**: NVIDIA GeForce RTX 4090 (24GB VRAM)  
**Date**: 2025-11-16

## 1. Inference Feasibility

### 1.1 FLUX Inference ✅ PROVEN
- **Status**: Already validated using ai-toolkit
- **VRAM**: ~10-15GB typical for FLUX.1-dev
- **Performance**: Capable on 4090
- **Tooling**: ai-toolkit proven

### 1.2 Qwen Image Editing Inference ❓ TO VALIDATE
- **Model Family**: Qwen-Image (specialized for image editing)
- **Base Model**: Qwen/Qwen-Image-Edit-2509 (official editing model)
- **Fine-tuned Variant**: dx8152/Qwen-Edit-2509-Multiple-angles (community LoRA for angles)
- **Model Size**: ~7B parameters (estimated ~14GB in fp16, ~8GB in 4-bit)
- **Purpose**: Actual image-to-image editing (NOT just vision understanding)
- **Quantization**: Can use 4-bit/8-bit quantization if needed
- **Libraries**: transformers, diffusers, bitsandbytes
- **Test needed**: 
  1. Download Qwen-Image-Edit-2509
  2. Load with 4-bit quantization
  3. Test basic image editing prompts (background, lighting, angle changes)
  4. Test with dx8152 LoRA for angle changes
  5. Measure VRAM usage
  6. Evaluate quality vs expectations

### 1.3 Concurrent Inference
- **Challenge**: Running both models simultaneously would exceed VRAM
- **Solution**: Sequential pipeline - load/unload as needed
- **Memory management**: Use `torch.cuda.empty_cache()` between model switches

## 2. Training Feasibility

### 2.1 FLUX LoRA Training ✅ PROVEN
- **Status**: Already validated
- **Method**: LoRA (Low-Rank Adaptation)
- **VRAM**: Manageable with gradient checkpointing
- **Tooling**: ai-toolkit proven
- **Typical settings**:
  - LoRA rank: 8-16
  - Batch size: 1-2
  - Gradient checkpointing: enabled
  - Mixed precision: fp16 or bf16

### 2.2 Qwen Image Edit LoRA Training ❓ TO VALIDATE
- **Status**: No experience yet, but dx8152 proves it's possible
- **Base Model**: Qwen-Image-Edit-2509
- **Proven Example**: dx8152/Qwen-Edit-2509-Multiple-angles LoRA
- **Method**: PEFT (Parameter-Efficient Fine-Tuning) with LoRA
- **Estimated VRAM**: 18-22GB with QLoRA
- **Libraries needed**:
  - `peft` (Hugging Face PEFT library)
  - `diffusers` (for image editing models)
  - `bitsandbytes` (4-bit quantization)
- **Recommended approach**: QLoRA (Quantized LoRA)
  - 4-bit base model (Qwen-Image-Edit-2509)
  - LoRA adapters on top (following dx8152's approach)
  - Gradient checkpointing
  - Small batch size (1)
- **Data format**: (image_before, edit_prompt, image_after) triplets
- **Test needed**:
  1. Study dx8152's training approach/dataset structure
  2. Set up PEFT environment
  3. Create minimal training script based on dx8152's method
  4. Test with 5-10 image triplets
  5. Validate memory usage
  6. Verify output quality improves on character consistency

### 2.3 Training Pipeline Constraints
- **Can only train ONE model at a time** (VRAM limitation)
- **Recommendation**: Complete Flywheel 1 iterations before starting Flywheel 2
- **Training time**: Expect several hours per LoRA (depends on dataset size)

## 3. Qwen-VL Model Selection & Download

### 3.1 Recommended Model
**Qwen/Qwen-Image-Edit-2509** (Base editing model)
- Official Qwen image editing model (not vision understanding)
- Designed specifically for image-to-image editing
- ~7B parameters
- Fits in 24GB with quantization
- Active development and community support

### 3.2 Community Fine-Tunes to Study
- **dx8152/Qwen-Edit-2509-Multiple-angles**: LoRA for angle changes
  - Proof that fine-tuning for specific editing tasks works
  - Study this approach for our character consistency training
  - May not be good enough for our needs, but validates the concept

### 3.3 Alternative Options (if Qwen-Image-Edit insufficient)
- **InstructPix2Pix**: Alternative editing model
- **IP-Adapter + ControlNet**: More complex but powerful
- **Commercial API**: Qwen-VL-Max via API (cloud-based, no local training)

### 3.4 Download & Setup Steps
```bash
# Install dependencies
pip install transformers diffusers accelerate bitsandbytes pillow torch torchvision

# Download base editing model (will cache to ~/.cache/huggingface)
huggingface-cli download Qwen/Qwen-Image-Edit-2509

# Download community angle LoRA (to study)
huggingface-cli download dx8152/Qwen-Edit-2509-Multiple-angles

# Or download via Python
python -c "from diffusers import DiffusionPipeline; DiffusionPipeline.from_pretrained('Qwen/Qwen-Image-Edit-2509')"
```

### 3.5 Storage Requirements
- Qwen-Image-Edit-2509 weights: ~14GB
- dx8152 LoRA adapter: ~100-500MB
- Cache space: ~20GB recommended
- Dataset storage: Plan for 50-100GB (images + checkpoints)

## 4. PEFT/QLoRA Learning Path

### 4.1 No Current Experience
- Need to learn PEFT library
- Need to understand QLoRA workflow
- Need vision-language model fine-tuning specifics

### 4.2 Resources Needed
- Hugging Face PEFT documentation
- Hugging Face Diffusers documentation (for image editing models)
- QLoRA paper/examples
- **dx8152/Qwen-Edit-2509-Multiple-angles** - study this implementation!
  - Model card and training approach
  - Dataset structure
  - Training hyperparameters
- Qwen-Image-Edit-2509 documentation and examples

### 4.3 Recommended Learning Steps
1. Study dx8152/Qwen-Edit-2509-Multiple-angles model card and approach
2. Read PEFT basics (LoRA, QLoRA concepts)
3. Review Diffusers library for image editing pipelines
4. Test Qwen-Image-Edit-2509 base model inference
5. Experiment with dx8152 LoRA to understand quality level
6. Adapt approach for character consistency (our use case)
7. Create minimal training script for FLENwheel

## 5. Proposed Validation Steps

### Phase 1: Basic Qwen Image Edit Validation (Week 1)
- [ ] Install dependencies (transformers, diffusers, bitsandbytes, etc.)
- [ ] Download Qwen-Image-Edit-2509
- [ ] Download dx8152/Qwen-Edit-2509-Multiple-angles LoRA
- [ ] Load base model with 4-bit quantization
- [ ] Test basic inference with sample images
- [ ] Measure VRAM usage
- [ ] Test basic editing prompts:
  - Background changes
  - Lighting adjustments
  - Style transfers
- [ ] Test dx8152 LoRA for angle changes
- [ ] Evaluate quality vs requirements (is it "good enough" baseline?)
- [ ] Document working configuration

### Phase 2: Dataset Enrichment POC (Week 2)
- [ ] Gather 5-10 test images (character source material)
- [ ] Create enrichment script using Qwen-Image-Edit-2509:
  - Load model (with/without dx8152 LoRA)
  - Apply 3-5 different editing prompts per image
  - Save outputs
  - Track metadata (source, prompt, output)
- [ ] Manual review of outputs
- [ ] Validate character consistency (key metric!)
- [ ] Compare base model vs dx8152 LoRA quality
- [ ] Document successful prompt patterns
- [ ] Document limitations and areas needing improvement

### Phase 3: PEFT/QLoRA Learning (Week 2-3)
- [ ] Study dx8152/Qwen-Edit-2509-Multiple-angles approach
- [ ] Study PEFT library documentation
- [ ] Review Diffusers training examples
- [ ] Create minimal Qwen-Image-Edit training script
- [ ] Test with 5 image triplets (inspired by dx8152's dataset structure)
- [ ] Validate memory usage
- [ ] Test trained adapter quality vs base model
- [ ] Compare to dx8152 LoRA quality

### Phase 4: Full Loop POC (Week 3-4)
- [ ] Run complete Flywheel 1:
  1. Start with 10 source images
  2. Enrich with Qwen-Image-Edit-2509 (50 images)
  3. Train FLUX LoRA v1
  4. Generate 20 synthetic images
  5. Manual review
  6. Retrain FLUX LoRA v2
- [ ] Compare v1 vs v2 quality
- [ ] Document working parameters
- [ ] Identify bottlenecks
- [ ] Assess if base Qwen-Image-Edit quality sufficient or if custom LoRA needed

### Phase 5: Production Pipeline (Week 5+)
- [ ] Create automated scripts for each phase
- [ ] Build dataset management system
- [ ] Implement version tracking
- [ ] Create review interface (if needed)
- [ ] Optimize VRAM usage
- [ ] Document full workflow

## 6. Technical Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Qwen-Image-Edit too large for 4090 | High | Low | Use 4-bit quantization, proven to work |
| Base model quality insufficient | High | Medium | Study dx8152 LoRA approach, train custom LoRA |
| dx8152 LoRA not good enough | Medium | Medium | Train our own character-specific LoRA |
| PEFT learning curve too steep | Medium | Low | dx8152 proves it works, follow their approach |
| Training time too long | Low | Medium | Optimize batch size, use gradient accumulation |
| Dataset quality degrades | High | Medium | Strict human review gates, identity verification |
| VRAM OOM during training | High | Low | Monitor usage, reduce batch size, use checkpointing |

## 7. Required Tooling & Libraries

### Core Dependencies
```python
# Inference
transformers>=4.40.0
diffusers>=0.27.0  # For image editing pipelines
accelerate>=0.27.0
bitsandbytes>=0.43.0
torch>=2.2.0
torchvision>=0.17.0
pillow>=10.0.0

# Training (FLUX - existing)
# ai-toolkit (already installed)

# Training (Qwen-Image-Edit - new)
peft>=0.10.0
datasets>=2.18.0

# Utilities
opencv-python>=4.9.0
face-recognition>=1.3.0  # for identity filtering
numpy>=1.26.0
pandas>=2.2.0  # for dataset tracking
```

### Development Environment
- Python 3.13.3 ✅
- CUDA-compatible PyTorch
- Jupyter notebooks (for experimentation)
- Git LFS (for large model checkpoints)

## 8. Next Immediate Actions

1. **Install base dependencies** (30 min)
2. **Download Qwen-Image-Edit-2509** (1-2 hours)
3. **Download dx8152 angle LoRA** (5 min)
4. **Create basic inference test** (1 hour)
5. **Test with dx8152 LoRA** (30 min)
6. **Validate VRAM usage** (30 min)
7. **Test 3-5 editing prompts** (1 hour)
8. **Assess quality vs requirements** (critical!)

**Estimated time to basic validation**: 5-7 hours

## 9. Success Criteria

### Qwen Image Edit Inference
- ✅ Loads with <20GB VRAM
- ✅ Generates edited images in <60 seconds
- ✅ Maintains character consistency in 70%+ of outputs (KEY METRIC)
- ✅ Accepts natural language editing prompts
- ✅ Base model OR dx8152 LoRA provides acceptable quality baseline

### Qwen Image Edit Training
- ✅ Trains on 10 triplets without OOM
- ✅ Training completes in <2 hours
- ✅ Adapter improves character consistency vs base model
- ✅ Adapter quality exceeds dx8152 LoRA for our use case
- ✅ Can save and reload adapters

### Full Pipeline POC
- ✅ Completes one full iteration in <1 week
- ✅ FLUX LoRA v2 shows measurable improvement over v1
- ✅ No manual intervention needed between automated steps
- ✅ All outputs properly versioned and tracked

## 10. Open Questions

1. **Qwen-Image-Edit base quality**: Good enough or need custom LoRA immediately?
2. **dx8152 LoRA quality**: Does angle editing meet our needs?
3. **Prompt engineering**: What prompt patterns work best for character consistency?
4. **Training data volume**: How many triplets needed for meaningful improvement over base?
5. **Identity verification**: Which face recognition library/model works best?
6. **Pipeline orchestration**: Manual scripts vs workflow tool (Airflow, Prefect)?
7. **Checkpoint strategy**: How often to save, how to version?
8. **Quality metrics**: Beyond human review, any automated quality scores?
9. **Base vs LoRA strategy**: Start with base model, or train LoRA from day 1?
