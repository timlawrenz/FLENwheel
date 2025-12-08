## Context

This change represents a strategic pivot from "find the perfect model" to "generate volume and curate empirically." The key architectural decisions are driven by:

1. **Hardware capabilities**: AMD 7995X (128GB VRAM) enables parallel execution
2. **Shared storage**: NAS eliminates data duplication and enables seamless dual-server workflow
3. **Proven curation**: ELO voting system from turbo-carnival demonstrates effective human-in-the-loop
4. **Category coverage**: LoRA training needs diverse data (portraits + body + hands), not just mass

## Goals

### Primary Goals
- Enable parallel mass generation (500-1000 images in 12-24 hours)
- Provide structured coverage across image categories (not random mass)
- Implement proven ELO-based human curation
- Leverage dual-server + NAS architecture efficiently
- Get empirical data on which models work best (for future learning layer)

### Non-Goals
- ❌ ML-based model selection (deferred until we have data from 3+ characters)
- ❌ Automated quality scoring (start with human ELO voting first)
- ❌ Real-time generation (batch processing is acceptable)
- ❌ Perfect first iteration (expect to iterate on templates and workflow)

## Decisions

### Decision 1: Prompt Template System (YAML)

**Decision**: Use YAML files with structured templates and variable expansion.

**Alternatives considered**:
- **JSON templates**: More rigid, less human-readable
- **Python code**: Flexible but harder to edit for non-programmers
- **Hardcoded prompts**: No flexibility, hard to maintain

**Rationale**: YAML strikes the balance between human readability and structure. Templates can be edited without code changes.

**Example**:
```yaml
category: portraits
templates:
  headshots:
    prompt: "ohwx_char, headshot, {angle}, {expression}, studio lighting"
    variations:
      angle: [front, half-left, profile-left]
      expression: [neutral, smiling]
    count: 24  # 3 × 2 × 4 models
```

### Decision 2: Category-Based Generation (Not Random Mass)

**Decision**: Generate images across four categories: portraits, body-poses, context, hands.

**Alternatives considered**:
- **Pure volume**: Generate 1000 random variations
- **Model card only**: Generate only the 23 benchmark images
- **Aspect-based**: Organize by aspect (lighting, angle, etc.) instead of category

**Rationale**: LoRA training needs diverse data. 1000 portrait headshots won't teach full-body poses. Categories ensure coverage while still using volume approach.

**Category targets**:
- Portraits: 200 images (angles, expressions, lighting)
- Body poses: 200 images (standing, sitting, action, t-pose)
- Context: 200 images (environments, clothing, props)
- Hands: 100 images (poses, actions, close-ups - critical for quality)

### Decision 3: Dual-Server Architecture

**Decision**: AMD server generates, RTX 4090 curates and trains.

**Server roles**:
- **AMD 7995X (128GB VRAM)**: Parallel mass generation (4-6 models simultaneously)
- **RTX 4090 (24GB VRAM)**: ELO voting UI, LoRA training, model card generation

**Alternatives considered**:
- **RTX 4090 only**: Would require sequential generation, 3-5x slower
- **AMD only**: APU may not have optimal CUDA support for ai-toolkit training
- **Cloud servers**: Adds cost and complexity, against project constraints

**Rationale**: Leverage strengths of each server. AMD's massive VRAM enables parallelism, RTX 4090's CUDA optimization is ideal for training.

### Decision 4: NAS-Centric Storage

**Decision**: All data lives on `/mnt/nas-ai-models/training-data/flenwheel/`, accessed by both servers.

**Directory structure**:
```
/mnt/nas-ai-models/training-data/flenwheel/
├── sources/           # Sparse input images (10-20 per character)
│   └── character-001/
├── generated/         # Volume output from orchestrator
│   └── character-001/
│       ├── portraits/
│       ├── body-poses/
│       ├── context/
│       └── hands/
├── curated/          # ELO winners selected for training
│   └── character-001/
├── loras/            # Trained character LoRAs
│   └── character-001-v1.safetensors
└── templates/        # Prompt template library
    ├── portraits.yaml
    ├── body-poses.yaml
    ├── context.yaml
    └── hands.yaml
```

**Alternatives considered**:
- **Local storage per server**: Requires rsync/copying, wastes space
- **Database for metadata only**: Images still need shared filesystem
- **S3/object storage**: Adds complexity and latency

**Rationale**: NAS provides 32TB shared storage (11TB free), eliminating data duplication. Both servers can read/write directly.

### Decision 5: ELO Voting (Adapted from turbo-carnival)

**Decision**: Port ELO calculation and voting UI from turbo-carnival project.

**Key components to reuse**:
- `RecordVote` command with ELO calculation logic
- A/B comparison UI pattern
- Vote tracking database schema

**Adaptations needed**:
- Replace "pipeline runs" with "generation batches"
- Add category filtering (vote within portraits, body-poses, etc.)
- Add batch operations (accept/reject all from model)

**Alternatives considered**:
- **5-star rating**: Less effective than pairwise comparisons
- **Binary keep/reject**: Loses relative quality information
- **ML-based scoring**: No ground truth yet, need human baseline first

**Rationale**: ELO voting is proven in turbo-carnival. Pairwise comparisons are cognitively easier than absolute ratings. ELO scores enable data-driven model selection later.

### Decision 6: Defer Learning Layer

**Decision**: Do NOT implement ML-based model selection in v1. Track metadata for future use.

**What to track now**:
- Which model generated each image
- ELO scores per image
- Model performance statistics (avg ELO by model per category)

**What to defer**:
- Recommender system ("character like X → use models Y")
- Automated model selection
- Prompt optimization

**Rationale**: Need data from 3+ characters to train a meaningful recommender. Premature to build ML system before we have training data.

## Risks and Mitigations

### Risk 1: NAS I/O Bottleneck

**Risk**: Network storage may be slower than local SSD, causing generation slowdowns.

**Mitigation**:
- Monitor I/O during first test run
- Consider staging: generate to local SSD, copy to NAS in batch
- NAS is gigabit+ network, should handle image writes fine

### Risk 2: AMD Server Compatibility

**Risk**: Some models may not run on AMD APU (ROCm vs CUDA differences).

**Mitigation**:
- Test each model on AMD server before first production run
- Fallback: Run incompatible models on RTX 4090
- Most Diffusers models are ROCm-compatible via PyTorch

### Risk 3: ELO Voting Fatigue

**Risk**: 500 images = ~250 pairwise votes, may be too much.

**Mitigation**:
- Implement batch operations (top 10% auto-accept)
- Add face similarity pre-filtering (reject obvious failures)
- Split voting across multiple sessions
- Target: 2-4 hours total, ~60-100 votes/hour

### Risk 4: Template Coverage Gaps

**Risk**: Initial templates may miss important variations.

**Mitigation**:
- Start with comprehensive templates (based on model card requirements)
- Iterate: analyze which categories have low ELO scores, add templates
- Templates are YAML - easy to edit and re-run

## Migration Plan

No migration needed (greenfield implementation).

**Integration with existing work**:
- Existing `test_qwen_*.py` scripts remain valid for individual model testing
- `generate_model_card.py` will be updated to use NAS-stored LoRAs
- `caption_training_data.py` will be updated to read from NAS curated directory

## Open Questions

### Question 1: Voting UI Integration

**Question**: Should voting UI be standalone Flask app or integrated into turbo-carnival?

**Options**:
- **A) Standalone**: Separate repo, simpler to build, FLENwheel-specific
- **B) Integrated**: Add FLENwheel as a module in turbo-carnival
- **C) Shared library**: Extract voting logic to gem/package

**Recommendation**: Start with standalone (A) for speed, extract to library later if turbo-carnival needs it.

### Question 2: Parallel Model Count

**Question**: How many models should AMD server run in parallel?

**Factors**:
- 128GB VRAM total
- Qwen-Image-Edit base model: ~20GB
- FLUX.2-dev fp8: ~10GB with quantization
- Overhead: ~10GB

**Recommendation**: Start with 4 models (safe), benchmark, scale to 6 if VRAM allows.

### Question 3: Automated Pre-filtering

**Question**: Should we auto-reject images before ELO voting?

**Criteria for auto-reject**:
- Face similarity < 0.6 (wrong character)
- Obvious artifacts (blur detection, truncation)
- Aesthetic score < threshold

**Recommendation**: Add face similarity filter (reject <0.6), defer other filters until we see failure modes.

### Question 4: Template Format Details

**Question**: How to handle multiple source images for FLUX.2 multi-reference?

**Options**:
- **A) Templates specify source image selection** (e.g., "use all sources")
- **B) Orchestrator auto-selects** (random subset of sources)
- **C) Separate template type** for multi-reference vs single-image

**Recommendation**: Start with (B) - orchestrator randomly picks 1-5 source images for FLUX.2, keeps it simple.

### Question 5: Checkpoint Frequency

**Question**: How often should orchestrator checkpoint progress?

**Options**:
- **A) After each image**: Safest but most I/O
- **B) After each category**: Balance safety and performance
- **C) After each model completes**: Minimal I/O

**Recommendation**: (B) - After each category (every ~50-100 images). Balances resume capability with performance.

## Performance Targets

### Generation Phase (AMD Server)
- **Target**: 700 images in 12-24 hours
- **Throughput**: 30-60 images/hour with 4 parallel models
- **VRAM usage**: <90% of 128GB (leave headroom)

### Voting Phase (RTX 4090)
- **Target**: 200-300 votes in 2-4 hours
- **Throughput**: 60-100 votes/hour (human speed)
- **Selection rate**: Top 30-40% by ELO per category

### Training Phase (RTX 4090)
- **Target**: LoRA training in 2-4 hours (existing ai-toolkit)
- **Model card generation**: 23 images in 10-15 minutes
- **Success metric**: >60% first-try generation on model card

## Success Criteria

### Must Have (Week 4)
- ✅ Generate 500+ images across all 4 categories
- ✅ ELO voting system functional and used for curation
- ✅ Trained LoRA from curated dataset
- ✅ Model card generated with success rate measured

### Should Have (Week 6)
- ✅ Analytics dashboard showing model performance
- ✅ Template library refined based on first run learnings
- ✅ End-to-end workflow documented
- ✅ Second character completed with improved templates

### Nice to Have (Week 8+)
- ✅ Automated face similarity pre-filtering
- ✅ Batch voting shortcuts implemented
- ✅ Metadata export for future learning layer
- ✅ Performance optimizations (local staging, etc.)
