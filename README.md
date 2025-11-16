# FLENwheel

**FLEN**wheel: **FL**ux + qw**EN** dual-flywheel training

A human-in-the-loop AI training system for creating high-quality character LoRAs through iterative refinement.

## Overview

FLENwheel uses a dual-flywheel approach to create robust character LoRAs for FLUX image generation:

1. **Flywheel 1 - Character LoRA Training**: Qwen-Image-Edit enriches source material → FLUX LoRA training → synthetic data generation → human review → improved training data
2. **Flywheel 2 - Editor Refinement**: Human corrections feed back to fine-tune the Qwen-Image-Edit editor itself

The system runs entirely on a single machine with an NVIDIA RTX 4090, using human guidance to prevent model drift and ensure quality.

## 🚀 Major Update: Ecosystem Discovery

**Active ecosystem of specialized Qwen-Image-Edit LoRAs discovered!**

Multiple community fine-tunes exist for:
- **Angle changes**: Camera viewpoint adjustments
- **Face preservation**: Identity-preserving edits
- **Lighting/skin**: Complexion and lighting adjustments
- **Style transfer**: Technique references

**Strategy options**:
1. Use existing specialized LoRAs (fastest)
2. Combine multiple LoRAs for different tasks
3. Train custom character-specific LoRA
4. Hybrid: existing + custom refinement

See [docs/qwen-ecosystem-analysis.md](docs/qwen-ecosystem-analysis.md) for full analysis.

## Project Status

🚧 **Early Development** - Currently in the definition and planning phase

**Next**: Ecosystem survey and validation (Week 1, 7-10 hours)

## Goals

- Achieve robust character consistency across multiple angles, expressions, and body poses
- Generate a comprehensive "model card" benchmark set:
  - **Portraits**: Neutral, smiling, angry, sad expressions from multiple angles
  - **Body Poses**: T-pose, standing, sitting positions
- Bootstrap from minimal source material (10-20 images) to hundreds of high-quality training examples

## Tech Stack

- **GPU**: NVIDIA RTX 4090 (24GB VRAM)
- **Image Generation**: FLUX foundation model with character LoRAs
- **Image Editing**: Qwen-VL-Max for dataset enrichment
- **Training**: LoRA/PEFT techniques (QLoRA, 8-bit optimizers, gradient checkpointing)
- **Language**: Python
- **Framework**: Diffusers library (planned)

## Workflow Phases

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
