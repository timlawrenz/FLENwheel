# Qwen Ecosystem Validation - Proposal

**Change ID**: `qwen-ecosystem-validation`  
**Type**: New Capability  
**Status**: Proposed  
**Created**: 2025-11-16  
**Owner**: Tim Lawrenz

## Summary

Establish a systematic process for surveying, testing, and evaluating the Qwen-Image-Edit ecosystem of specialized LoRA models to determine the optimal image editing strategy for FLENwheel's character consistency requirements.

## Problem Statement

We have discovered an active ecosystem of specialized Qwen-Image-Edit-2509 LoRAs (angle changes, face preservation, lighting, etc.) but lack:
1. A systematic methodology to survey and catalog available models
2. Standardized testing procedures to evaluate each model's quality
3. Comparative metrics to decide between single LoRA, multi-LoRA, custom, or hybrid approaches
4. Documentation of findings to guide implementation strategy

Without this validation process, we risk:
- Choosing suboptimal models based on incomplete information
- Missing better specialized LoRAs that could solve our problems
- Wasting time on approaches that won't meet our character consistency requirements
- Making uninformed strategic decisions about custom training needs

## Goals

### Primary Goals
1. **Survey Ecosystem**: Identify and document 5-10 most relevant Qwen-Edit LoRAs for character work
2. **Validate Base Model**: Test Qwen-Image-Edit-2509 base model quality and limitations
3. **Test Specialized LoRAs**: Evaluate each identified LoRA on character consistency metrics
4. **Create Comparison Matrix**: Quantitative and qualitative comparison across all tested models
5. **Make Strategic Decision**: Choose approach (existing/multi/custom/hybrid) based on data

### Secondary Goals
- Document training methodologies from successful LoRAs
- Identify gaps that require custom training
- Establish baseline metrics for future iterations
- Create reusable testing infrastructure

## Proposed Solution

### Phase 1: Ecosystem Survey (1-2 hours)

**Approach**: Systematic catalog of Hugging Face models

**Deliverables**:
- List of 5-10 relevant models with metadata
- Documentation of training approaches from model cards
- Initial quality assessments from model descriptions

### Phase 2: Environment Setup (2-3 hours)

**Approach**: Prepare testing infrastructure

**Deliverables**:
- Python virtual environment with dependencies
- Downloaded models (base + specialized LoRAs)
- Test directory structure
- Standardized test image set (5 source images)

### Phase 3: Comparative Testing (3-5 hours)

**Approach**: Systematic testing of all models on same images

**Deliverables**:
- Test results for each model
- Character consistency measurements
- Edit quality assessments
- VRAM usage data
- Artifact frequency counts

### Phase 4: Analysis & Decision (1 hour)

**Approach**: Data-driven strategy selection

**Deliverables**:
- Comparison matrix (all models)
- Strategic recommendation with rationale
- Implementation roadmap
- `docs/qwen-ecosystem-results.md` report

## Success Criteria

### Must Have
- ✅ At least 5 specialized LoRAs identified and tested
- ✅ Base model (Qwen-Image-Edit-2509) validated
- ✅ Character consistency rate measured for each model (target: 70%+)
- ✅ Comparison matrix completed with quantitative data
- ✅ Strategic decision documented with clear rationale

### Should Have
- ✅ 10 specialized LoRAs surveyed
- ✅ Multi-LoRA combinations tested
- ✅ Training approaches documented from model cards
- ✅ Reusable test scripts created

### Nice to Have
- Face-segmentation LoRA tested for identity verification
- LoRA merging techniques explored
- Automated testing pipeline created

## Risks and Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Models take too long to download | Medium | Medium | Start downloads early, work on survey while waiting |
| Base model quality insufficient | High | Medium | Have multi-LoRA and custom training as fallbacks |
| No single LoRA meets requirements | Medium | Medium | Expected - test combinations and plan custom training |
| VRAM constraints prevent testing all models | Low | Low | Test sequentially, unload between tests |
| Inconsistent test results | Medium | Low | Use same source images, document all parameters |

## Dependencies

### Technical Dependencies
- Python 3.13.3 environment
- CUDA-compatible PyTorch
- Hugging Face libraries (transformers, diffusers, bitsandbytes)
- 50GB+ free disk space
- 24GB VRAM (RTX 4090)

### Documentation Dependencies
- docs/qwen-ecosystem-analysis.md (already exists - analysis framework)
- docs/technical-feasibility.md (validation plan)
- docs/quick-start.md (test scripts)

### Process Dependencies
- None - this is the first validation phase
- Blocks: Flywheel 1 implementation (needs model selection)

## Out of Scope

- **PEFT training**: Not part of validation phase (Flywheel 2)
- **FLUX LoRA training**: Separate from Qwen ecosystem validation
- **Production pipeline**: Only creating test infrastructure
- **Face recognition implementation**: Only documenting if needed
- **Custom LoRA training**: Only deciding if needed, not implementing

## Open Questions

1. **Model selection criteria**: What's the minimum quality threshold to consider a LoRA viable?
2. **Test image selection**: What character images best represent our use case?
3. **Combination testing scope**: How many multi-LoRA combinations to test?
4. **Quality metrics**: Beyond character consistency, what else to measure?
5. **Decision framework**: What weights to assign different quality factors?

## Approval

**Approver**: Tim Lawrenz  
**Date**: [Pending]  
**Status**: Proposed

---

## Notes

- This validation phase is critical - wrong model choice wastes weeks
- Ecosystem discovery already de-risked project significantly
- Data-driven decision will save time vs. guessing
- Reusable test infrastructure benefits future iterations
- Week 1 timeline is aggressive but achievable
