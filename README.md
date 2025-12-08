# FLENwheel

**FLEN**wheel: **FL**ux + qw**EN** dual-flywheel training

A human-in-the-loop AI training system for creating high-quality character LoRAs through **volume generation and ELO-based curation**.

## Overview

FLENwheel uses a volume-first approach to create robust character LoRAs:

**Core Strategy**: Generate 500-1000 images using multiple models in parallel → ELO voting to curate best 200-400 → Train LoRA on curated dataset

Key principles:
- **Volume over precision**: Statistical robustness from diverse data
- **Category coverage**: Portraits, body poses, context, hands (not random mass)
- **ELO curation**: Human-in-the-loop quality control via pairwise voting
- **Parallel execution**: 4-6 models running simultaneously on AMD server (128GB VRAM)
- **Adaptive to ecosystem**: Use all available models, let results determine best performers

## Current Status

🚧 **Active Development** - Volume generation system implemented

**Latest**: 2025-12-08
- ✅ Infrastructure complete (OpenSpec proposal, NAS setup, templates)
- ✅ Generation orchestrator with real Diffusers integration
- ✅ Validated on RTX 4090 (needs AMD server for parallel execution)
- ⏭️ **Next**: AMD server setup for production volume generation

See [SESSION_SUMMARY.md](SESSION_SUMMARY.md) for detailed progress.

## Architecture

### Dual-Server Setup

**AMD 7995X (128GB VRAM)**: Parallel mass generation
- Run 4-6 models simultaneously
- Generate 500-1000 images in 12-24 hours
- Template-driven prompt expansion

**RTX 4090 (24GB VRAM)**: Curation and training
- ELO voting UI for image selection
- LoRA training with ai-toolkit
- Model card generation

### Shared NAS Storage

**Location**: `/mnt/nas-ai-models/training-data/flenwheel/`
- 32TB capacity, 11TB free
- Accessible from both servers
- Model repository, training data, templates

### Prompt Template System

YAML-based templates ensure coverage:
- **portraits.yaml**: 184 images (angles × expressions × lighting)
- **body-poses.yaml**: 130 images (full body, t-pose, sitting, action)
- **hands.yaml**: 68 images (critical for LoRA quality)
- **context.yaml**: 210 images (environments × clothing)

Total: ~592 baseline tasks → 1,184 images with 2 seeds

## Goals

- Achieve robust character consistency across multiple angles, expressions, and body poses
- Generate a comprehensive "model card" benchmark set:
  - **Portraits**: Neutral, smiling, angry, sad expressions from multiple angles
  - **Body Poses**: T-pose, standing, sitting positions
- Bootstrap from minimal source material (10-20 images) to hundreds of high-quality training examples

## Tech Stack

- **Hardware**:
  - AMD 7995X APU (128GB VRAM) - Parallel generation
  - NVIDIA RTX 4090 (24GB VRAM) - Training and curation
  - Shared NAS storage (32TB)
- **Image Generation**: 
  - Qwen-Image-Edit-2509 (multiple models/LoRAs)
  - FLUX.2-dev (multi-reference support)
  - FLUX.1-dev (character LoRAs)
- **Training**: ai-toolkit (FLUX LoRA training), PEFT
- **Language**: Python
- **Framework**: Diffusers, PyTorch
- **Framework**: Diffusers, PyTorch

## Workflow

```
1. GENERATION (AMD Server, 12-24 hours)
   ├─ Load YAML templates from NAS
   ├─ Run 4-6 models in parallel
   ├─ Generate 500-1000 categorized images
   └─ Save to NAS with metadata

2. CURATION (RTX 4090, 2-4 hours)
   ├─ ELO voting: pairwise A/B comparisons
   ├─ Category-filtered (portraits, body, hands, context)
   ├─ Select top 200-400 images by ELO score
   └─ Export to curated directory

3. TRAINING (RTX 4090, 2-4 hours)
   ├─ Train FLUX LoRA on curated dataset
   ├─ Generate model card (23 benchmark images)
   └─ Evaluate success rate

4. ITERATE
   └─ Refine templates based on results
```

## Documentation

### Phase 1: Source Material Curation
- Gather 10-20 initial images (photos, sketches, renderings)
- Caption with instance tokens (e.g., "ohwx_char person")

### Phase 2: Dataset Enrichment
- Use Qwen-VL to create variations (backgrounds, lighting, angles)
- Human review to ensure character consistency
- Build enriched dataset (50-100 images)

### Phase 3: LoRA Training
- Phased approach: head/expressions first, then full body
- Train on 4090 with memory-efficient techniques

### Phase 4: Synthetic Data Generation
- Generate novel scenarios with FLUX + character LoRA
- AI-assisted filtering with face recognition
- Human review for quality control

### Phase 5: Meta-Learning
- Curate corrections to fine-tune Qwen-VL editor
- Improve future enrichment quality

## Key Features

- **Human-in-the-Loop**: Manual review gates ensure quality at every stage
- **Iterative Refinement**: Each version improves the next
- **Benchmark-Driven**: Model card targets provide measurable progress
- **Local-First**: All processing on a single machine

## Documentation

- **Start here**: [docs/SUMMARY.md](docs/SUMMARY.md) - Quick overview and current status
- **Ecosystem**: [docs/qwen-ecosystem-analysis.md](docs/qwen-ecosystem-analysis.md) - Specialized LoRA options
- **Technical**: [docs/technical-feasibility.md](docs/technical-feasibility.md) - Detailed feasibility analysis
- **Process**: [docs/process-flow.md](docs/process-flow.md) - Complete dual-flywheel workflow
- **Quick Start**: [docs/quick-start.md](docs/quick-start.md) - Hands-on validation guide
- **Concept**: [docs/brainstorming.md](docs/brainstorming.md) - Original vision and design
- **Diagram**: [docs/basic-process.td](docs/basic-process.td) - Visual flowchart

## Constraints

- Single machine with 24GB VRAM requires memory optimization
- Manual curation is bottleneck but critical for quality
- Initial source material needs variety in angles/expressions
- Multiple LoRA management adds complexity but provides flexibility

## License

TBD

## Contributing

Currently a personal project in early development.
