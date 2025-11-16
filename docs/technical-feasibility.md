# Technical Feasibility Analysis

**System**: NVIDIA GeForce RTX 4090 (24GB VRAM)  
**Date**: 2025-11-16

## 1. Inference Feasibility

### 1.1 FLUX Inference ✅ PROVEN
- **Status**: Already validated using ai-toolkit
- **VRAM**: ~10-15GB typical for FLUX.1-dev
- **Performance**: Capable on 4090
- **Tooling**: ai-toolkit proven

### 1.2 Qwen-VL Inference ❓ TO VALIDATE
- **Model**: Qwen2-VL (latest version)
- **Variants to consider**:
  - Qwen2-VL-2B-Instruct (~8GB VRAM estimated)
  - Qwen2-VL-7B-Instruct (~16GB VRAM estimated)
  - Qwen2-VL-72B-Instruct (❌ Too large for single 4090)
- **Recommended**: Qwen2-VL-7B-Instruct (balance of quality/VRAM)
- **Quantization**: Can use 4-bit/8-bit quantization if needed
- **Libraries**: transformers, bitsandbytes for quantization
- **Test needed**: 
  1. Download model
  2. Load with 4-bit quantization
  3. Test basic image editing prompts
  4. Measure VRAM usage

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

### 2.2 Qwen-VL LoRA Training ❓ TO VALIDATE
- **Status**: No experience yet
- **Method**: PEFT (Parameter-Efficient Fine-Tuning)
- **Estimated VRAM**: 18-22GB with QLoRA
- **Libraries needed**:
  - `peft` (Hugging Face PEFT library)
  - `trl` (Transformer Reinforcement Learning - optional)
  - `bitsandbytes` (4-bit quantization)
- **Recommended approach**: QLoRA (Quantized LoRA)
  - 4-bit base model
  - LoRA adapters on top
  - Gradient checkpointing
  - Small batch size (1)
- **Data format**: (image_before, edit_prompt, image_after) triplets
- **Test needed**:
  1. Set up PEFT environment
  2. Create minimal training script
  3. Test with 5-10 image triplets
  4. Validate memory usage
  5. Verify output quality

### 2.3 Training Pipeline Constraints
- **Can only train ONE model at a time** (VRAM limitation)
- **Recommendation**: Complete Flywheel 1 iterations before starting Flywheel 2
- **Training time**: Expect several hours per LoRA (depends on dataset size)

## 3. Qwen-VL Model Selection & Download

### 3.1 Recommended Model
**Qwen2-VL-7B-Instruct**
- Good balance of quality and VRAM usage
- Strong editing capabilities
- Fits in 24GB with quantization
- Active community support

### 3.2 Alternative Options
- **Qwen2-VL-2B**: Faster, less VRAM, lower quality
- **Qwen-VL (v1)**: Older, still capable
- **Commercial API**: Qwen-VL-Max via API (no local inference)

### 3.3 Download & Setup Steps
```bash
# Install dependencies
pip install transformers accelerate bitsandbytes pillow torch torchvision

# Download model (will cache to ~/.cache/huggingface)
python -c "from transformers import AutoModel; AutoModel.from_pretrained('Qwen/Qwen2-VL-7B-Instruct')"

# Or use huggingface-cli
huggingface-cli download Qwen/Qwen2-VL-7B-Instruct
```

### 3.4 Storage Requirements
- Model weights: ~15GB
- Cache space: ~20GB recommended
- Dataset storage: Plan for 50-100GB (images + checkpoints)

## 4. PEFT/QLoRA Learning Path

### 4.1 No Current Experience
- Need to learn PEFT library
- Need to understand QLoRA workflow
- Need vision-language model fine-tuning specifics

### 4.2 Resources Needed
- Hugging Face PEFT documentation
- QLoRA paper/examples
- Vision-language model fine-tuning tutorials
- Qwen2-VL specific examples

### 4.3 Recommended Learning Steps
1. Read PEFT basics (LoRA, QLoRA concepts)
2. Run simple text-only LoRA example
3. Find vision-language LoRA example
4. Adapt for Qwen2-VL
5. Create minimal training script for FLENwheel

## 5. Proposed Validation Steps

### Phase 1: Basic Qwen-VL Validation (Week 1)
- [ ] Install dependencies (transformers, bitsandbytes, etc.)
- [ ] Download Qwen2-VL-7B-Instruct
- [ ] Load model with 4-bit quantization
- [ ] Test basic inference with sample images
- [ ] Measure VRAM usage
- [ ] Test basic editing prompts:
  - Background changes
  - Lighting adjustments
  - Style transfers
- [ ] Document working configuration

### Phase 2: Dataset Enrichment POC (Week 2)
- [ ] Gather 5-10 test images (character source material)
- [ ] Create enrichment script:
  - Load Qwen-VL
  - Apply 3-5 different editing prompts per image
  - Save outputs
  - Track metadata (source, prompt, output)
- [ ] Manual review of outputs
- [ ] Validate character consistency
- [ ] Document successful prompt patterns

### Phase 3: PEFT/QLoRA Learning (Week 2-3)
- [ ] Study PEFT library documentation
- [ ] Run basic text LoRA tutorial
- [ ] Find vision-language fine-tuning example
- [ ] Create minimal Qwen-VL training script
- [ ] Test with 5 image triplets
- [ ] Validate memory usage
- [ ] Test trained adapter quality

### Phase 4: Full Loop POC (Week 3-4)
- [ ] Run complete Flywheel 1:
  1. Start with 10 source images
  2. Enrich with Qwen-VL (50 images)
  3. Train FLUX LoRA v1
  4. Generate 20 synthetic images
  5. Manual review
  6. Retrain FLUX LoRA v2
- [ ] Compare v1 vs v2 quality
- [ ] Document working parameters
- [ ] Identify bottlenecks

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
| Qwen-VL too large for 4090 | High | Medium | Use 4-bit quantization, smaller variant (2B) |
| Qwen-VL quality insufficient | Medium | Low | Test multiple prompt patterns, consider API fallback |
| PEFT learning curve too steep | Medium | Medium | Start simple, use examples, community support |
| Training time too long | Low | Medium | Optimize batch size, use gradient accumulation |
| Dataset quality degrades | High | Medium | Strict human review gates, identity verification |
| VRAM OOM during training | High | Low | Monitor usage, reduce batch size, use checkpointing |

## 7. Required Tooling & Libraries

### Core Dependencies
```python
# Inference
transformers>=4.40.0
accelerate>=0.27.0
bitsandbytes>=0.43.0
torch>=2.2.0
torchvision>=0.17.0
pillow>=10.0.0

# Training (FLUX - existing)
# ai-toolkit (already installed)

# Training (Qwen-VL - new)
peft>=0.10.0
trl>=0.8.0  # optional, for advanced training
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
2. **Download Qwen2-VL-7B-Instruct** (1-2 hours)
3. **Create basic inference test** (1 hour)
4. **Validate VRAM usage** (30 min)
5. **Test 3-5 editing prompts** (1 hour)

**Estimated time to basic validation**: 4-6 hours

## 9. Success Criteria

### Qwen-VL Inference
- ✅ Loads with <20GB VRAM
- ✅ Generates edited images in <60 seconds
- ✅ Maintains character consistency in 70%+ of outputs
- ✅ Accepts natural language editing prompts

### Qwen-VL Training
- ✅ Trains on 10 triplets without OOM
- ✅ Training completes in <2 hours
- ✅ Adapter improves quality on test prompts
- ✅ Can save and reload adapters

### Full Pipeline POC
- ✅ Completes one full iteration in <1 week
- ✅ FLUX LoRA v2 shows measurable improvement over v1
- ✅ No manual intervention needed between automated steps
- ✅ All outputs properly versioned and tracked

## 10. Open Questions

1. **Qwen-VL variant**: 2B vs 7B - which provides best quality/VRAM tradeoff?
2. **Prompt engineering**: What prompt patterns work best for character consistency?
3. **Training data volume**: How many triplets needed for meaningful Qwen-VL improvement?
4. **Identity verification**: Which face recognition library/model works best?
5. **Pipeline orchestration**: Manual scripts vs workflow tool (Airflow, Prefect)?
6. **Checkpoint strategy**: How often to save, how to version?
7. **Quality metrics**: Beyond human review, any automated quality scores?
