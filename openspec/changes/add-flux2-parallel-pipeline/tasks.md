# Add FLUX2 Parallel Pipeline - Implementation Tasks

## 1. Research & Setup

### 1.1 Implementation Strategy Confirmation ✅
- [x] 1.1.1 Research Python libraries for FLUX2 inference
  - ✅ **Confirmed**: Official `diffusers.Flux2Pipeline` support
  - ✅ **Quantization**: NF4 via bitsandbytes (not GGUF)
  - ✅ **Multi-reference**: `image=[img1, img2, ...]` API confirmed
  - ✅ **LoRA Training**: Supported per official blog
- [x] 1.1.2 Document recommended approach with rationale
  - See: `flux2-python-research.md`
  - **Recommended**: Diffusers + NF4 quantization (`prithivMLmods/Flux.2.Dev-NF4`)
- [x] 1.1.3 Verify VRAM requirements with test script
  - ✅ Created: `scripts/flux2_vram_test.py`
  - Ready to test with 1, 3, 5 reference images
  - Will confirm <24GB VRAM with NF4 + CPU offloading

### 1.2 Environment Setup
- [x] 1.2.1 Ensure Python virtual environment has required packages
  - ✅ Virtual environment at `venv/` active
- [x] 1.2.2 Install required dependencies
  - ✅ `diffusers` 0.36.0.dev0 (latest with Flux2Pipeline)
  - ✅ `transformers` 4.57.1 (for text encoder)
  - ✅ `bitsandbytes` 0.48.2 (for NF4 quantization)
  - ✅ `accelerate` 1.11.0 (for CPU offloading)
  - ✅ PIL/Pillow (already available)
  - ✅ torch 2.9.1 (CUDA-enabled)
- [x] 1.2.3 Verify CUDA and GPU accessibility
  - ✅ CUDA available: True
  - ✅ GPU: NVIDIA GeForce RTX 4090
  - ✅ Total VRAM: 23.5GB
- [ ] 1.2.4 Download NF4 quantized model (`prithivMLmods/Flux.2.Dev-NF4`) or use official model
  - Will download on first run of test script

### 1.3 Model Configuration
- [x] 1.3.1 Create configuration file for model setup
  - ✅ Created: `config/flux2_config.yaml`
  - Model choice: `prithivMLmods/Flux.2.Dev-NF4` (NF4 quantized)
  - Output directories: `data/[character]/flux2/`
  - Quantization config: NF4 via bitsandbytes
  - CPU offloading: enabled
- [x] 1.3.2 Document model specifications (size, quantization, parameters)
  - Documented in `config/flux2_config.yaml`
- [x] 1.3.3 Create VRAM test script template
  - ✅ Created: `scripts/flux2_vram_test.py`

## 2. Core Inference Implementation

### 2.1 Basic Inference Script
- [ ] 2.1.1 Create `scripts/flux2_inference.py`
- [ ] 2.1.2 Implement model loading function
- [ ] 2.1.3 Implement single-reference inference
  - [ ] Text prompt handling
  - [ ] Reference image loading and preprocessing
  - [ ] Generation parameters (steps, guidance, seed)
- [ ] 2.1.4 Test with 1 reference image
- [ ] 2.1.5 Verify output quality and VRAM usage

### 2.2 Multi-Reference Support
- [ ] 2.2.1 Research FLUX2 multi-reference API/format
- [ ] 2.2.2 Implement multi-reference image handling
  - [ ] Load and preprocess multiple images
  - [ ] Concatenation or separate input handling
  - [ ] Embedding combination (if applicable)
- [ ] 2.2.3 Test with 3, 5, and 10 reference images
- [ ] 2.2.4 Profile VRAM usage at each reference count

### 2.3 Generation Parameters
- [ ] 2.3.1 Implement configurable parameters
  - [ ] Number of inference steps
  - [ ] Guidance scale (CFG)
  - [ ] Random seed control
  - [ ] Image dimensions
  - [ ] Batch size
- [ ] 2.3.2 Create parameter presets for different use cases
- [ ] 2.3.3 Add command-line argument parsing

## 3. Training Material Generation

### 3.1 Enrichment Workflow
- [ ] 3.1.1 Create `scripts/flux2_enrich.py`
- [ ] 3.1.2 Implement prompt template library
  - [ ] Angle variations (front, 3/4, profile, back)
  - [ ] Expression changes (neutral, smiling, sad, angry)
  - [ ] Pose variations (standing, sitting, T-pose)
  - [ ] Background/scene changes
- [ ] 3.1.3 Batch generation from reference set
- [ ] 3.1.4 Organize outputs by transformation type

### 3.2 Character Consistency Evaluation
- [ ] 3.2.1 Create `scripts/flux2_evaluate.py`
- [ ] 3.2.2 Integrate face recognition library (InsightFace or deepface)
- [ ] 3.2.3 Implement identity consistency scoring
  - [ ] Compare generated images to reference
  - [ ] Calculate similarity scores
  - [ ] Flag low-confidence outputs
- [ ] 3.2.4 Generate evaluation report with metrics

### 3.3 Data Organization
- [ ] 3.3.1 Create directory structure
  - `data/[character]/flux2/reference/` (source images)
  - `data/[character]/flux2/enriched/` (generated variations)
  - `data/[character]/flux2/filtered/` (passing consistency check)
- [ ] 3.3.2 Implement metadata tracking (prompts, parameters, scores)

## 4. Comparison Framework

### 4.1 Qwen vs FLUX2 Comparison
- [ ] 4.1.1 Create `scripts/compare_enrichment.py`
- [ ] 4.1.2 Implement comparison metrics
  - [ ] Character identity preservation rate
  - [ ] Image quality assessment
  - [ ] Transformation accuracy (angle, expression, etc.)
  - [ ] Generation speed (images/minute)
  - [ ] VRAM usage peak
- [ ] 4.1.3 Generate side-by-side comparison visualizations
- [ ] 4.1.4 Create comparison report document

### 4.2 Benchmarking
- [ ] 4.2.1 Define standard test set (same 5 source images as Qwen)
- [ ] 4.2.2 Run equivalent transformations on both pipelines
- [ ] 4.2.3 Collect quantitative metrics
- [ ] 4.2.4 Document qualitative observations

## 5. Optimization & Polish

### 5.1 Performance Optimization
- [ ] 5.1.1 Profile memory usage and identify bottlenecks
- [ ] 5.1.2 Implement batch processing optimizations
- [ ] 5.1.3 Add progress bars and status logging
- [ ] 5.1.4 Implement caching for repeated operations

### 5.2 Error Handling
- [ ] 5.2.1 Add graceful VRAM overflow handling
- [ ] 5.2.2 Implement retry logic for failed generations
- [ ] 5.2.3 Validate inputs (image formats, file existence)
- [ ] 5.2.4 Add informative error messages

### 5.3 User Experience
- [ ] 5.3.1 Add verbose/quiet modes
- [ ] 5.3.2 Implement dry-run mode (validate without generating)
- [ ] 5.3.3 Create simple CLI interface
- [ ] 5.3.4 Add configuration file support (YAML/JSON)

## 6. Documentation

### 6.1 Setup Documentation
- [ ] 6.1.1 Create `docs/flux2-setup.md`
  - [ ] Installation instructions
  - [ ] Dependency requirements
  - [ ] Model download/location
  - [ ] Environment configuration
- [ ] 6.1.2 Add troubleshooting section

### 6.2 Usage Documentation
- [ ] 6.2.1 Create `docs/flux2-usage.md`
  - [ ] Basic inference examples
  - [ ] Multi-reference usage
  - [ ] Enrichment workflow walkthrough
  - [ ] Parameter tuning guide
- [ ] 6.2.2 Add code examples and screenshots

### 6.3 Comparison Results
- [ ] 6.3.1 Create `docs/flux2-vs-qwen-comparison.md`
  - [ ] Methodology description
  - [ ] Quantitative results (tables, charts)
  - [ ] Qualitative observations
  - [ ] Recommendations based on findings

### 6.4 Update Project Documentation
- [ ] 6.4.1 Update `README.md` with FLUX2 pipeline mention
- [ ] 6.4.2 Update `docs/process-flow.md` with parallel workflow diagram
- [ ] 6.4.3 Update `openspec/project.md` tech stack (add FLUX2)

## 7. Testing & Validation

### 7.1 Unit Tests
- [ ] 7.1.1 Test model loading and unloading
- [ ] 7.1.2 Test single vs multi-reference inference
- [ ] 7.1.3 Test parameter validation
- [ ] 7.1.4 Test error handling edge cases

### 7.2 Integration Tests
- [ ] 7.2.1 End-to-end enrichment workflow test
- [ ] 7.2.2 Comparison pipeline test
- [ ] 7.2.3 VRAM limits test (maximum reference count)

### 7.3 Quality Validation
- [ ] 7.3.1 Visual inspection of generated images
- [ ] 7.3.2 Verify character consistency scores meet threshold (≥70%)
- [ ] 7.3.3 Compare to ComfyUI workflow outputs (sanity check)

## 8. Deployment & Finalization

### 8.1 Code Review
- [ ] 8.1.1 Review all scripts for code quality
- [ ] 8.1.2 Add docstrings to functions
- [ ] 8.1.3 Format code consistently (black/autopep8)
- [ ] 8.1.4 Remove debug code and temporary files

### 8.2 Final Documentation
- [ ] 8.2.1 Update all documentation with final results
- [ ] 8.2.2 Create decision summary document
- [ ] 8.2.3 Document lessons learned and next steps

### 8.3 Archive Preparation
- [ ] 8.3.1 Mark all tasks complete
- [ ] 8.3.2 Prepare for change archival (when appropriate)
- [ ] 8.3.3 Update project status documents

---

## Task Completion Tracking

**Total Tasks**: 78  
**Completed**: 0  
**In Progress**: 0  
**Blocked**: 0  

**Estimated Duration**: 7-10 days  
**Priority**: High (parallel to qwen-ecosystem-validation)
