# FLUX.2-dev Evaluation & Strategic Assessment

**Date**: 2025-11-26  
**Status**: 🚨 Urgent evaluation required  
**Decision Deadline**: End of Week 1 (with Qwen-Edit comparison)

---

## Executive Summary

FLUX.2-dev was released with **native multi-reference support** (up to 10 photos), potentially disrupting our planned Qwen-Edit enrichment workflow. This document evaluates whether to pivot to FLUX.2, use a hybrid approach, or continue with FLUX.1 + Qwen-Edit.

---

## FLUX.2-dev Overview

### Official Information

- **Repository**: https://huggingface.co/black-forest-labs/FLUX.2-dev
- **Announcement**: https://huggingface.co/blog/flux-2
- **Key Feature**: Multi-reference image support (up to 10 reference photos)
- **License**: Non-commercial (same as FLUX.1-dev)
- **Model Size**: Similar to FLUX.1-dev (~12B parameters)

### Current Local Setup

- **Format**: 4-bit quantized GGUF
- **Platform**: ComfyUI
- **Performance**: TBD (needs testing)
- **VRAM Usage**: Significantly lower than fp16 (exact TBD)

---

## Strategic Options

### Option A: Pivot to FLUX.2 🆕

**Workflow**: 
```
Source Photos (10-20) 
  → FLUX.2 multi-ref generation (new angles/poses/scenes)
  → Human review + filtering
  → Train FLUX.2 LoRA on curated dataset
  → Iterate
```

**Advantages**:
- ✅ Single model for both enrichment and generation
- ✅ Native character consistency (designed for multi-reference)
- ✅ Simpler pipeline (no separate editor model)
- ✅ Already running locally (4-bit GGUF)
- ✅ Official Black Forest Labs release

**Disadvantages**:
- ❌ Unknown: Can we train LoRAs on FLUX.2-dev?
- ❌ Unknown: Quality of 4-bit GGUF vs fp16
- ❌ Unknown: Actual character consistency with 10 refs
- ❌ ComfyUI workflow vs Python scripting
- ❌ Less control over specific edits vs Qwen-Edit

**Risk**: Medium - unproven for LoRA training

---

### Option B: Hybrid FLUX.2 + Qwen-Edit 🔀

**Workflow**:
```
Source Photos (10-20)
  → Qwen-Edit enrichment (angles, backgrounds)
  → FLUX.2 multi-ref generation (using enriched set)
  → Human review + filtering
  → Train FLUX.2 LoRA
  → Iterate
```

**Advantages**:
- ✅ Best of both worlds: precision editing + multi-ref consistency
- ✅ Qwen-Edit for controlled transformations
- ✅ FLUX.2 for character-consistent generation
- ✅ Fallback if one model underperforms

**Disadvantages**:
- ❌ Most complex pipeline
- ❌ Two models to manage
- ❌ Highest VRAM orchestration complexity
- ❌ Longest processing time

**Risk**: High - complexity overhead

---

### Option C: Continue FLUX.1 + Qwen-Edit ✅

**Workflow**:
```
Source Photos (10-20)
  → Qwen-Edit enrichment
  → FLUX.1 LoRA training (proven)
  → Synthetic generation
  → Human review
  → Iterate
```

**Advantages**:
- ✅ Proven: FLUX.1 LoRA training works
- ✅ Already invested time in Qwen-Edit setup
- ✅ Qwen-Edit ecosystem (dx8152 LoRA, etc.)
- ✅ Clear separation: editor vs generator
- ✅ Known VRAM requirements

**Disadvantages**:
- ❌ Doesn't leverage FLUX.2 multi-ref capability
- ❌ Two-model pipeline
- ❌ Potential character drift between editor/generator

**Risk**: Low - established approach

---

### Option D: Parallel Testing 🧪

**Approach**: Run both pipelines in parallel, choose based on results

**Week 1 Tests**:
1. **FLUX.2 Track**:
   - Test multi-ref with 1, 3, 5, 10 photos
   - Measure character consistency
   - Evaluate generation quality
   - Test LoRA training (if possible)

2. **Qwen-Edit Track**:
   - Complete dx8152 LoRA testing
   - Test base model vs LoRA
   - Evaluate enrichment quality

3. **Comparison**:
   - Character consistency score
   - Edit control precision
   - Workflow complexity
   - Processing time
   - VRAM requirements

**Advantages**:
- ✅ Data-driven decision
- ✅ Comprehensive evaluation
- ✅ No premature commitment

**Disadvantages**:
- ❌ Double the testing effort
- ❌ Delays decision by 1 week
- ❌ Resource intensive

**Risk**: Low - but time-consuming

---

## Technical Questions to Answer

### FLUX.2 Multi-Reference

1. **Character Consistency**: 
   - Can FLUX.2 maintain identity across 10+ reference photos?
   - Consistency rate vs FLUX.1 + LoRA?
   - Does more references = better consistency? (1 vs 3 vs 5 vs 10)

2. **LoRA Training**:
   - Can we train LoRAs on FLUX.2-dev like FLUX.1-dev?
   - Same tools (ai-toolkit) or new workflow?
   - Multi-reference during training vs inference only?

3. **Quality**:
   - 4-bit GGUF quality vs fp16 full precision?
   - Acceptable for production or need higher precision?
   - Speed vs quality trade-offs?

4. **Workflow Integration**:
   - ComfyUI only or Python API available?
   - Batch processing capabilities?
   - Integration with existing scripts?

### Qwen-Edit Comparison

5. **Edit Precision**:
   - Can FLUX.2 match Qwen-Edit's controlled transformations?
   - Background changes, angle adjustments, lighting?

6. **Ecosystem**:
   - Will FLUX.2 develop specialized LoRAs like Qwen-Edit?
   - Community adoption rate?

---

## Testing Plan

### Phase 1: FLUX.2 Capability Assessment (2-3 hours)

**Setup**:
- [ ] Verify 4-bit GGUF running in ComfyUI
- [ ] Create test character set (5 photos)
- [ ] Design test prompts (angles, scenes, expressions)

**Tests**:
- [ ] Generate with 1 reference photo (baseline)
- [ ] Generate with 3 reference photos
- [ ] Generate with 5 reference photos
- [ ] Generate with 10 reference photos
- [ ] Measure VRAM usage at each level
- [ ] Assess character consistency (visual inspection)

**Metrics**:
- Character identity preservation (subjective 1-10 scale)
- Image quality (artifacts, clarity)
- Generation speed (seconds per image)
- VRAM peak usage

---

### Phase 2: LoRA Training Feasibility (3-4 hours)

**Research**:
- [ ] Check if ai-toolkit supports FLUX.2-dev
- [ ] Search for FLUX.2 LoRA training examples
- [ ] Check Black Forest Labs documentation

**Test** (if possible):
- [ ] Attempt minimal LoRA training (5-10 images)
- [ ] Compare to FLUX.1 LoRA training
- [ ] Verify workflow compatibility

**Outcome**:
- ✅ LoRA training works → FLUX.2 viable
- ❌ LoRA training blocked → FLUX.2 inference only

---

### Phase 3: Direct Comparison (2-3 hours)

**Test Set**: Same 5 source images

**FLUX.2 Path**:
- Input: 5 source photos as multi-reference
- Generate: 10 variations (different angles/scenes)
- Measure: Character consistency across variations

**Qwen-Edit Path**:
- Input: 5 source photos
- Process: Enrich each with 2-3 variations (dx8152 LoRA)
- Measure: Character consistency in enriched images

**Comparison**:
- Identity preservation rate
- Edit quality (backgrounds, angles, lighting)
- Workflow simplicity (subjective)
- Total processing time
- VRAM requirements

---

### Phase 4: Strategic Decision (1 hour)

**Decision Matrix**:

| Criteria | Weight | FLUX.2 | Hybrid | FLUX.1+Qwen |
|----------|--------|--------|--------|-------------|
| Character Consistency | 40% | ? | ? | ? |
| LoRA Training Support | 30% | ? | ? | ✅ |
| Workflow Simplicity | 15% | ? | ? | ? |
| Processing Speed | 10% | ? | ? | ? |
| Community Support | 5% | ? | ? | ✅ |
| **TOTAL** | 100% | **?** | **?** | **?** |

**Decision Rules**:
- If FLUX.2 scores ≥80% → **Pivot to FLUX.2** (Option A)
- If Hybrid scores ≥75% → **Use Hybrid** (Option B)
- If FLUX.1+Qwen scores ≥70% → **Continue** (Option C)
- If unclear → **Parallel testing** (Option D) for another week

---

## Success Criteria

### Minimum Viable FLUX.2 (to pivot)

- [ ] Character consistency ≥70% across 10 references
- [ ] LoRA training confirmed working (or clear path)
- [ ] 4-bit GGUF quality acceptable for production
- [ ] Python API or ComfyUI automation possible
- [ ] VRAM fits on 4090 (≤20GB peak)

### Decision Confidence Threshold

- **High confidence** (≥80%): Proceed immediately
- **Medium confidence** (60-79%): Extended testing (1 more week)
- **Low confidence** (<60%): Fall back to FLUX.1 + Qwen-Edit

---

## Timeline

**Day 1-2** (Now - 2025-11-27):
- Complete FLUX.2 multi-reference testing
- Measure character consistency

**Day 3-4** (2025-11-28 - 2025-11-29):
- Research LoRA training for FLUX.2
- Attempt minimal training if possible

**Day 5-6** (2025-11-30 - 2025-12-01):
- Direct comparison with Qwen-Edit results
- Complete comparison matrix

**Day 7** (2025-12-02):
- Strategic decision
- Update project plan
- Document findings

---

## Open Questions

### Critical (Must Answer This Week)

1. Can FLUX.2 maintain character identity with 10 reference photos?
2. Is LoRA training supported/possible on FLUX.2-dev?
3. Is 4-bit GGUF quality sufficient for production?

### Important (Nice to Know)

4. Python API available or ComfyUI only?
5. Processing speed vs FLUX.1?
6. Community adoption trajectory?

### Future (Can Wait)

7. Will FLUX.2 ecosystem develop like Qwen-Edit?
8. Licensing implications for production?
9. Future model iterations (FLUX.3)?

---

## Recommendation Framework

### If FLUX.2 Multi-Ref Works Well (≥70% consistency)

**AND** LoRA training possible:
- ✅ **PIVOT TO FLUX.2** (Option A)
- Simplest pipeline
- Native multi-ref support
- Single model to optimize

**BUT** LoRA training not possible:
- 🔀 **HYBRID APPROACH** (Option B)
- Use FLUX.2 for enrichment
- Train LoRA on FLUX.1 (proven)
- Best quality, more complexity

### If FLUX.2 Multi-Ref Underwhelms (<70% consistency)

**OR** LoRA training blocked:
- ✅ **CONTINUE WITH FLUX.1 + QWEN-EDIT** (Option C)
- Proven approach
- Don't fix what isn't broken
- Revisit FLUX.2 when ecosystem matures

---

## Documentation Updates Required

**If pivoting to FLUX.2**:
- [ ] Update README.md tech stack
- [ ] Revise docs/process-flow.md workflow
- [ ] Update docs/technical-feasibility.md model info
- [ ] Create docs/flux2-multi-reference-guide.md
- [ ] Update TODO.md priorities

**If hybrid approach**:
- [ ] Document dual-model orchestration
- [ ] Update VRAM management strategy
- [ ] Revise workflow diagrams

**If continuing FLUX.1**:
- [ ] Document FLUX.2 evaluation results
- [ ] Note for future reconsideration
- [ ] Continue with Qwen-Edit path

---

## Risk Assessment

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| FLUX.2 LoRA training not supported | Medium | High | Fall back to FLUX.1 |
| 4-bit quality insufficient | Low | Medium | Test fp16 version |
| Multi-ref doesn't improve consistency | Low | High | Use Qwen-Edit instead |
| ComfyUI limits automation | Medium | Medium | Find Python API or fork |

### Strategic Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Premature pivot wastes Qwen-Edit investment | Medium | Medium | Thorough testing first |
| FLUX.2 ecosystem slow to develop | Medium | Low | Already have working solution |
| FLUX.3 released next month | Low | Medium | Flexible architecture |

---

## Next Actions

**Immediate** (Today):
1. [ ] Set up FLUX.2 multi-reference test in ComfyUI
2. [ ] Create test character set (5 photos)
3. [ ] Run 1-ref, 3-ref, 5-ref, 10-ref tests
4. [ ] Document initial observations

**This Week**:
1. [ ] Research FLUX.2 LoRA training
2. [ ] Compare to Qwen-Edit results
3. [ ] Complete decision matrix
4. [ ] Make strategic decision
5. [ ] Update all project documentation

---

## Conclusion

FLUX.2's multi-reference capability is potentially transformative for FLENwheel. However, we need **empirical data** before pivoting. This week's testing will determine:

1. **Can FLUX.2 replace Qwen-Edit?** (character consistency test)
2. **Can we train LoRAs?** (feasibility research)
3. **Is it production-ready?** (quality/performance assessment)

**Decision by**: 2025-12-02 (end of Week 1)

---

*This document will be updated as testing progresses.*
