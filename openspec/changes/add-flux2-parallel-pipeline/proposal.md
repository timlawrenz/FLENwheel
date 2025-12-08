# Add FLUX2 Parallel Pipeline - Proposal

**Change ID**: `add-flux2-parallel-pipeline`  
**Type**: New Capability  
**Status**: ❌ **BLOCKED - Hardware Incompatible**  
**Created**: 2025-11-26  
**Owner**: Tim Lawrenz  
**Resolution**: FLUX2-dev requires ~23GB VRAM (exceeds RTX 4090 capacity)

## Summary

Implement a FLUX2-dev based training material generation pipeline parallel to the existing Qwen-Image-Edit workflow, enabling independent validation and potential advantages from FLUX2's native multi-reference capabilities while maintaining ComfyUI workflow independence.

## Why

We have a working 4-bit quantized FLUX2-dev model (Q4_1.gguf) running in ComfyUI that demonstrates local execution feasibility. However, we need:

1. **Independence from ComfyUI**: Our application progress should not depend on ComfyUI workflows
2. **Training Material Generation**: Even if we train LoRAs for FLUX1, FLUX2 can generate enriched training datasets
3. **Parallel Validation**: Run FLUX2 alongside Qwen to compare quality, consistency, and workflow efficiency
4. **Future-Proofing**: FLUX2's multi-reference support (up to 10 photos) may offer advantages over single-image editing

**Current Gap**: We have no Python-based FLUX2 inference infrastructure independent of ComfyUI.

## What Changes

- **NEW**: Python-based FLUX2-dev inference pipeline using gguf-quantized model
- **NEW**: Multi-reference image handling (1-10 reference photos)
- **NEW**: Training material generation workflow parallel to Qwen
- **NEW**: Character consistency evaluation framework for FLUX2
- **NEW**: Comparison metrics between FLUX2 and Qwen enrichment paths

This is **non-breaking** - it adds a parallel capability without modifying existing Qwen infrastructure.

## Impact

### Affected Specs
- None (new capability - no existing specs)

### Affected Code
- **New scripts**: `scripts/flux2_*.py` (inference, enrichment, evaluation)
- **New docs**: FLUX2 setup, usage, and comparison guides
- **Configuration**: Model paths, quantization settings, reference handling
- **Data organization**: Separate FLUX2 output directories parallel to Qwen

### Dependencies
- **Model**: `prithivMLmods/Flux.2.Dev-NF4` (4-bit quantized via bitsandbytes) OR official `black-forest-labs/FLUX.2-dev`
- **Libraries**: 
  - `diffusers` (official FLUX2Pipeline support)
  - `transformers` (text encoder)
  - `bitsandbytes` (NF4 quantization)
  - `torch` (CUDA-enabled)
- **Hardware**: RTX 4090 (24GB VRAM) with CPU offloading
- **Note**: Our GGUF model at `/mnt/essdee/ComfyUI/models/diffusion_models/flux2-dev-Q4_1.gguf` is ComfyUI-specific and not needed for Python implementation

## Goals

### Primary Goals
1. **Python Inference**: Load and run FLUX2-dev Q4_1.gguf without ComfyUI dependency
2. **Multi-Reference Support**: Handle 1-10 reference images for character consistency
3. **Training Material Generation**: Generate enriched datasets (new angles, poses, backgrounds)
4. **Parallel Workflow**: Run independently alongside Qwen validation (qwen-ecosystem-validation)
5. **Comparison Framework**: Metrics to compare FLUX2 vs Qwen enrichment quality

### Secondary Goals
- Automated character consistency scoring
- VRAM profiling and optimization
- Batch processing for efficiency
- Integration with existing face recognition filtering

## Out of Scope

- **FLUX2 LoRA training**: Focus is inference and enrichment only (training is separate concern)
- **FLUX1 replacement**: This is parallel, not replacing existing FLUX1 workflows
- **ComfyUI integration**: Explicitly avoiding ComfyUI dependency
- **Qwen modification**: No changes to existing Qwen-Edit validation work

## Success Criteria

### Must Have
- ✅ FLUX2-dev Q4_1.gguf loads and runs in Python (without ComfyUI)
- ✅ Multi-reference inference working (1, 3, 5, 10 photo tests)
- ✅ Generate 20+ enriched training images from 5 source photos
- ✅ Character identity preservation ≥70% (visual inspection)
- ✅ VRAM usage ≤20GB peak on RTX 4090
- ✅ Comparison metrics vs Qwen enrichment documented

### Should Have
- Automated face recognition scoring for consistency
- Batch processing script for efficiency
- VRAM profiling per reference count (1 vs 10 refs)
- Documentation: setup, usage, troubleshooting

### Nice to Have
- Multi-LoRA support (if applicable to FLUX2)
- Prompt template library for common transformations
- Integration with existing data curation tools

## Risks and Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| ~~GGUF Python loading incompatible~~ | ~~High~~ | ~~Medium~~ | ✅ RESOLVED - Use NF4 quantization via diffusers instead |
| NF4 + CPU offload still exceeds 24GB VRAM | High | Medium | Test incrementally; use attention slicing, sequential offload if needed |
| 4-bit quality insufficient for training data | Medium | Low | Compare to Qwen output; evaluate with face recognition scores |
| Multi-reference doesn't preserve identity | Medium | Medium | Start with 3 refs, adjust; use face recognition filtering |
| VRAM scales poorly with reference count | Medium | Medium | Profile incrementally (1→3→5→10), limit to safe count |
| No clear advantage over Qwen | Low | Medium | Expected - goal is validation, not replacement |

## Open Questions

### ✅ Resolved (from HuggingFace blog research)

1. **~~GGUF Loading~~**: ✅ SOLVED - Use official `Flux2Pipeline` with NF4 quantization instead
   - Model: `prithivMLmods/Flux.2.Dev-NF4` (community 4-bit quantized)
   - Our GGUF model is ComfyUI-specific, not needed for Python implementation
   
2. **~~Multi-Reference API~~**: ✅ CONFIRMED - `image=[img1, img2, ...]` parameter
   - Supports up to 10 reference images
   - Reference by index ("image 1") or natural language ("the kangaroo")
   - Best results with combination of both
   
3. **~~LoRA Training Support~~**: ✅ CONFIRMED - Blog has dedicated LoRA fine-tuning section

### ❓ Still Open (requires testing)

4. **VRAM Feasibility**: Will NF4 + CPU offload fit in 24GB on RTX 4090?
   - Blog shows ~62GB on H100 (bfloat16 + CPU offload)
   - NF4 should reduce significantly, but needs validation
   
5. **Multi-Reference VRAM Scaling**: How does VRAM usage scale with reference count (1 vs 3 vs 5 vs 10)?

6. **Prompt Engineering**: What prompt format optimizes character consistency with multi-ref?

7. **Quality Threshold**: What face recognition score constitutes "acceptable" identity preservation?

8. **Workflow Orchestration**: Run FLUX2 in parallel with Qwen or sequentially for fair comparison?

## Timeline Estimate

**Week 1** (Research & Setup):
- Research GGUF loading options (1 day)
- Set up Python environment and dependencies (0.5 day)
- Implement basic inference script (1 day)
- Test 1-ref, 3-ref, 5-ref, 10-ref (0.5 day)

**Week 2** (Enrichment & Evaluation):
- Build training material generation workflow (1 day)
- Implement face recognition scoring (1 day)
- Run parallel comparison with Qwen results (1 day)
- Document findings and recommendations (0.5 day)

**Total**: 7-10 days (can overlap with qwen-ecosystem-validation Phase 3+)

## Dependencies

### Blocks
- None (parallel to existing work)

### Blocked By
- None (GGUF model already available locally)

### Related Changes
- `qwen-ecosystem-validation` - Running in parallel, will provide comparison baseline

## Approval

**Approver**: Tim Lawrenz  
**Date**: [Pending]  
**Status**: Proposed

---

## Notes

### Key Decisions
- **Why parallel?** Allows fair comparison without disrupting proven Qwen path
- **Why gguf?** Already validated in ComfyUI, memory-efficient (4-bit)
- **Why multi-reference?** FLUX2's unique capability vs Qwen's single-image editing

### Strategic Value
- **Data-driven decision**: Empirical comparison vs speculation
- **Risk mitigation**: Two paths reduce single-model dependency
- **Future flexibility**: If FLUX2 excels, we can pivot; if Qwen wins, we continue
- **Training material**: Even if we train FLUX1 LoRAs, FLUX2 can still enrich datasets

### Alignment with Project Goals
- Supports Flywheel 1 (training material generation)
- Maintains human-in-the-loop quality control
- Enables iterative refinement
- No disruption to existing validation work
