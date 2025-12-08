# Change: Add Structured Volume Generation System

## Why

The current FLENwheel approach focuses on finding the "perfect" single model and careful enrichment strategy. This is premature optimization before validating whether the approach works at all.

**Key insights from discussion:**
1. **Volume + diversity beats precision**: Neural nets learn from statistical patterns, not perfect data
2. **Category coverage is critical**: 1000 portrait headshots won't teach full-body consistency
3. **AMD server (128GB VRAM) enables parallelism**: Can run 4-6 models simultaneously
4. **Shared NAS storage**: Both servers access `/mnt/nas-ai-models/` - seamless data flow
5. **ELO voting is proven**: turbo-carnival demonstrates effective human curation
6. **Fast iteration beats perfect planning**: Get empirical data, then optimize

**Current problem**: The project is stuck in analysis paralysis, comparing individual models instead of generating training data.

**Proposed solution**: Build a structured volume generation system that:
- Generates 500-1000 images across multiple categories using all available models
- Uses prompt templates to ensure coverage (portraits, body poses, context, hands)
- Employs ELO voting (turbo-carnival style) for human curation
- Leverages dual-server + NAS architecture for parallel execution
- Defers "learning which models work best" until we have empirical data

## What Changes

### New Capabilities
- **Prompt template system**: YAML-based templates for structured generation across categories
- **Dual-server orchestration**: AMD server generates in parallel, RTX 4090 curates and trains
- **Category-based generation**: Portraits, body-poses, context, hands (not random mass)
- **ELO-based curation**: Adapted from turbo-carnival voting system
- **NAS-centric workflow**: All data stored in `/mnt/nas-ai-models/training-data/flenwheel/`

### Changed Approach
- **Before**: Find optimal single model → enrich carefully → train
- **After**: Use all models in parallel → generate volume → ELO curate → train
- **Volume over precision**: 500-1000 generated images, curate down to 200-400 best
- **Empirical over theoretical**: Measure which models produce best results, don't predict
- **Deferred learning**: Skip ML-based model selection initially, use ELO rankings instead

### Architecture Changes
- **Dual-server setup**: 
  - AMD 7995X (128GB VRAM): Parallel mass generation
  - RTX 4090 (24GB VRAM): ELO voting UI, LoRA training, model card generation
- **Shared NAS**: `/mnt/nas-ai-models/` (32TB, 11TB free)
  - Models: `/diffusion_models/`, `/loras/`
  - Training data: `/training-data/flenwheel/`
  - No data duplication between servers

### Implementation Components
1. **Prompt template library** (`/mnt/nas-ai-models/training-data/flenwheel/templates/`)
   - `portraits.yaml`: Headshots, bust shots, close-ups (target: 200 images)
   - `body-poses.yaml`: Standing, sitting, action poses (target: 200 images)
   - `context.yaml`: Environments, lighting, clothing (target: 200 images)
   - `hands.yaml`: Hand poses, actions, close-ups (target: 100 images)

2. **Generation orchestrator** (`scripts/generate_structured_volume.py`)
   - Loads templates from NAS
   - Runs 4-6 models in parallel on AMD server
   - Expands prompts with variable substitution
   - Saves to NAS with metadata (model, prompt, seed, category)

3. **ELO voting system** (adapted from turbo-carnival)
   - Web UI presents A/B image comparisons per category
   - Updates ELO rankings based on votes
   - Tracks which models produce highest-rated outputs
   - Selects top N images per category for training

4. **Metadata tracking**
   - Which model generated each image
   - Prompt used, seed, category
   - ELO score evolution
   - Model performance statistics (for future learning layer)

## Impact

### Affected Components
- **New**: Prompt template system
- **New**: Generation orchestrator for AMD server
- **New**: ELO voting UI (port from turbo-carnival)
- **New**: NAS directory structure
- **Modified**: Documentation (pivot from single-model to volume approach)
- **Modified**: `openspec/project.md` (add AMD server, NAS storage)

### Breaking Changes
- None (greenfield project, no existing implementation to break)

### Migration Path
- Existing test scripts (`test_qwen_*.py`) remain valid for model validation
- Can still run individual model tests for debugging
- Shift from "test models one-by-one" to "run all models in batch"

### Timeline
- **Week 1**: Infrastructure setup, prompt templates, NAS directory structure
- **Week 2**: Generation orchestrator implementation and testing
- **Week 3**: ELO voting system adaptation
- **Week 4**: First complete run (generate → vote → train → benchmark)
- **Week 5+**: Iterate, add learning layer if patterns emerge

### Success Metrics
- Generate 500-1000 images in <24 hours (AMD server parallelism)
- ELO voting session completes in 2-4 hours (human review)
- Curated dataset has coverage: 50+ portraits, 50+ body poses, 30+ hands
- Trained LoRA achieves >60% success rate on model card benchmarks (first iteration)
- System tracks which models perform best (data for future learning layer)

### Risks
- **AMD server setup complexity**: Mitigated by using same Python environment as RTX 4090
- **NAS I/O bottleneck**: Network storage may slow generation - monitor and optimize
- **ELO voting fatigue**: 500 images = ~250 votes - may need shortcuts (batch accept/reject)
- **Model compatibility**: Some models may not run on AMD APU - fallback to RTX 4090

### Future Enhancements (Deferred)
- **ML-based model selection**: After 3+ characters, train recommender system
- **Automated quality scoring**: Reduce human voting burden with AI pre-filtering
- **Progressive refinement**: Use v1 LoRA to generate v2 training data
- **Multi-character learning**: "Characters like X work best with models Y"

## Dependencies
- AMD 7995X server access and configuration
- NAS mount verified on both servers (`/mnt/nas-ai-models/`)
- Python environment with Diffusers, PEFT, PyYAML
- Web framework for voting UI (Flask/FastAPI - TBD)
- Face recognition library for identity filtering (InsightFace or similar)

## Open Questions
1. Should voting UI be standalone web app or integrated into turbo-carnival?
2. What's the optimal number of parallel models on AMD server? (4, 6, 8?)
3. Should we implement batch voting shortcuts (top 10%, bottom 10% auto-decide)?
4. Do we need automated pre-filtering before ELO voting? (face similarity threshold)
5. Should templates be YAML or JSON? (YAML more human-readable)
