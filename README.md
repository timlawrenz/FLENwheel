# FLENwheel

**FLEN**wheel: **FL**ux + qw**EN** dual-flywheel training

A human-in-the-loop AI training system for creating high-quality character LoRAs through iterative refinement.

## Overview

FLENwheel uses a dual-flywheel approach to create robust character LoRAs for FLUX image generation:

1. **Flywheel 1 - Character LoRA Training**: Qwen-VL enriches source material → FLUX LoRA training → synthetic data generation → human review → improved training data
2. **Flywheel 2 - Editor Refinement**: Human corrections feed back to fine-tune the Qwen-VL editor itself

The system runs entirely on a single machine with an NVIDIA RTX 4090, using human guidance to prevent model drift and ensure quality.

## Project Status

🚧 **Early Development** - Currently in the definition and brainstorming phase

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

- [`docs/brainstorming.md`](docs/brainstorming.md) - Detailed concept and workflow
- [`docs/basic-process.td`](docs/basic-process.td) - Mermaid diagram of the dual-flywheel process
- [`openspec/project.md`](openspec/project.md) - Project context and conventions

## Constraints

- Single machine with 24GB VRAM requires memory optimization
- Manual curation is bottleneck but critical for quality
- Initial source material needs variety in angles/expressions

## License

TBD

## Contributing

Currently a personal project in early development.
