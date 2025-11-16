# Qwen-Image-Edit Ecosystem Analysis

**Last Updated**: 2025-11-16  
**Source**: https://huggingface.co/models?pipeline_tag=image-to-image&sort=trending&search=qwen

## Discovery

There's an active ecosystem of Qwen-Image-Edit-2509 derivatives, each specialized for specific tasks!

## Available Models (Community Fine-Tunes)

### Character/Portrait Focused

#### dx8152/Qwen-Edit-2509-Multiple-angles
- **Task**: Change camera angles while preserving character
- **Quality**: "Great inspiration, not good enough yet" (author's own assessment)
- **Relevance**: HIGH - directly addresses our angle variation needs
- **Status**: Already identified, planned for testing

### Style Transfer

#### [Model Name]/photo-to-anime
- **Task**: Convert photos to anime style
- **Relevance**: LOW - not our use case, but shows style consistency possible
- **Potential**: Could inspire style-preserving edits

### Editing Specific Features

#### [Model Name]/edit-skin
- **Task**: Skin editing/retouching
- **Relevance**: MEDIUM - if it preserves identity while editing skin
- **Potential**: Could help with lighting/complexion changes

#### [Model Name]/extract-texture
- **Task**: Texture extraction
- **Relevance**: LOW - not directly useful for our workflow
- **Note**: Shows model versatility

#### [Model Name]/lora-face-segmentation
- **Task**: Face segmentation for editing
- **Relevance**: MEDIUM-HIGH - face preservation is critical for us
- **Potential**: Could be used for identity verification or masked editing

## Implications for FLENwheel

### Positive Findings

1. **Proven Ecosystem**: Multiple successful fine-tunes = proven PEFT approach works
2. **Task Specialization Works**: Each LoRA solves a specific problem effectively
3. **Character Consistency Possible**: Face/identity preservation is solvable
4. **Active Community**: Ongoing development = support and examples

### Strategic Opportunities

#### Option 1: Multi-LoRA Approach
Combine multiple specialized LoRAs:
- `multiple-angles` for angle changes
- `edit-skin` for lighting/complexion
- Custom LoRA for character-specific consistency

**Pros**: 
- Leverage existing work
- Each LoRA optimized for specific task
- Faster to implement

**Cons**:
- Complexity in managing multiple models
- Potential conflicts between LoRAs
- VRAM overhead (multiple adapters)

#### Option 2: Hybrid Training Strategy
Use existing LoRAs as starting points or references:
- Study multiple-angles training approach
- Study face-segmentation for identity preservation
- Train single character-specific LoRA incorporating both techniques

**Pros**:
- Single unified model
- Optimized for our specific character
- Cleaner pipeline

**Cons**:
- More complex training
- Need to learn from multiple examples
- Longer development time

#### Option 3: Sequential Pipeline
Use specialized LoRAs in sequence:
1. Base model for background/lighting changes
2. Multiple-angles LoRA for camera angle adjustments
3. Face-segmentation LoRA for identity verification
4. Custom LoRA as final refinement

**Pros**:
- Clear separation of concerns
- Can validate each step
- Mix and match as needed

**Cons**:
- Slower inference (multiple passes)
- Quality degradation with each step
- Complex pipeline management

### Recommended Exploration Strategy

#### Phase 1: Survey and Test (Week 1)
```bash
# Download and test key models
huggingface-cli download dx8152/Qwen-Edit-2509-Multiple-angles
# [Add other relevant models as discovered]

# Test each on same source images:
# - Character consistency rate
# - Edit quality
# - Artifact frequency
# - Combination potential
```

#### Phase 2: Comparative Analysis (Week 1-2)
Create comparison matrix:
```
| Model | Angle Change | Lighting | Background | Identity | Artifacts |
|-------|-------------|----------|------------|----------|-----------|
| Base  |      ?      |     ?    |      ?     |    ?     |     ?     |
| dx8152|      ?      |     ?    |      ?     |    ?     |     ?     |
| [etc] |      ?      |     ?    |      ?     |    ?     |     ?     |
```

#### Phase 3: Strategy Decision (Week 2)
Based on testing, choose:
- **A**: Use existing LoRAs as-is (if quality sufficient)
- **B**: Combine multiple LoRAs (if complementary)
- **C**: Train custom LoRA (if gaps remain)
- **D**: Hybrid approach

## Updated Research Questions

### Critical Questions (Added)
1. Which existing LoRAs preserve character identity best?
2. Can we combine multiple LoRAs effectively?
3. Do specialized LoRAs (face-segmentation, edit-skin) help our use case?
4. What training techniques do the best LoRAs use?
5. Can we use existing LoRAs as initialization for custom training?

### Models to Investigate (Priority Order)

1. **HIGH**: dx8152/Qwen-Edit-2509-Multiple-angles
   - Already identified
   - Direct relevance to angle variation

2. **HIGH**: Any face/identity-preservation LoRAs
   - lora-face-segmentation (if available)
   - Face-specific editing models
   - Identity-preserving models

3. **MEDIUM**: Lighting/complexion editing
   - edit-skin (if preserves identity)
   - Lighting adjustment models

4. **LOW**: Background editing
   - Base model likely sufficient
   - Lower priority than identity/angle

5. **REFERENCE**: Style transfer models
   - photo-to-anime (as technique reference)
   - Shows what's possible with LoRA training

## Updated Validation Plan

### Extended Phase 1 (Week 1 - now 7-10 hours)

**Original Plan** (5-7 hours):
- Test base Qwen-Image-Edit-2509
- Test dx8152 multiple-angles LoRA
- Assess quality

**Extended Plan** (+2-3 hours):
- Download top 3-5 relevant LoRAs
- Test each on same 5 source images
- Create comparison matrix
- Identify best combinations
- Document training approaches from each

### New Deliverable: Ecosystem Analysis Report

Create `docs/qwen-ecosystem-analysis.md`:
- Models tested
- Quantitative results (identity preservation %, edit quality)
- Qualitative assessment (artifacts, consistency)
- Combination potential
- Training technique insights
- Recommendation for FLENwheel strategy

## Action Items

### Immediate (Today)
- [ ] Browse full Hugging Face search results
- [ ] Identify 3-5 most relevant models beyond dx8152
- [ ] Document model cards and training approaches
- [ ] Update download list in quick-start.md

### Week 1 (Validation Phase)
- [ ] Download identified models
- [ ] Create standardized test set (5 source images)
- [ ] Run comparative tests
- [ ] Measure character consistency for each
- [ ] Create comparison matrix
- [ ] Make strategy decision (single vs multi-LoRA)

### Week 2+ (Implementation)
- [ ] Implement chosen strategy
- [ ] If multi-LoRA: build combination pipeline
- [ ] If custom LoRA: incorporate best techniques from ecosystem
- [ ] Validate against model card targets

## Potential Game-Changers

### If face-segmentation LoRA exists and works well:
- Use it for automated identity verification (replace face_recognition library)
- Use it to guide editing (mask face, edit everything else)
- Train custom LoRA with face segmentation as auxiliary task

### If multiple specialized LoRAs are complementary:
- Build modular pipeline (different LoRAs for different tasks)
- Combine multiple LoRAs into single adapter (if technically feasible)
- Use best practices from each for custom training

### If any LoRA already solves character consistency:
- Use it as-is for Flywheel 1
- Skip Flywheel 2 entirely (or deprioritize)
- Focus on FLUX LoRA quality instead

## Open Questions (Added)

1. **LoRA merging**: Can we combine multiple Qwen-Edit LoRAs?
2. **Initialization**: Can we initialize custom LoRA from existing one?
3. **Architecture**: How do different LoRAs differ (rank, layers targeted)?
4. **Dataset size**: How much training data did successful LoRAs use?
5. **Face preservation**: Which techniques work best for identity consistency?

## References to Explore

- Hugging Face search: https://huggingface.co/models?pipeline_tag=image-to-image&sort=trending&search=qwen
- Model cards for training methodology
- Community discussions on LoRA combinations
- Papers on LoRA merging techniques

## Update Recommendations

### Technical Feasibility Document
- Add section on ecosystem models
- Update risk assessment (lower risk with proven examples)
- Add LoRA combination as possible approach

### Quick Start Guide
- Add ecosystem survey step before validation
- Expand model download list
- Add comparative testing procedure

### Process Flow
- Add optional multi-LoRA approach to Flywheel 1
- Update Flywheel 2 to incorporate ecosystem insights
- Add model selection decision gate

---

**Bottom Line**: This ecosystem discovery significantly de-risks the project. We have multiple working examples to learn from, potential shortcuts via existing LoRAs, and proven techniques to incorporate. The question shifts from "can we do this?" to "which combination of existing work plus custom training is optimal?"
