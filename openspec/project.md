# Project Context

## Purpose
FLENwheel is a human-in-the-loop (HITL) AI training system that creates high-quality character LoRAs for FLUX image generation through an iterative dual-flywheel approach:

1. **Flywheel 1**: Uses Qwen-VL to enrich source material → trains FLUX character LoRAs → generates synthetic data with human review
2. **Flywheel 2**: Fine-tunes the Qwen-VL editor itself using curated corrections from human review

The goal is to achieve robust character consistency across multiple angles, expressions, and body poses, ultimately producing a comprehensive "model card" set of benchmark images.

## Tech Stack
- **GPU**: NVIDIA RTX 4090 (24GB VRAM) - single local machine
- **Image Generation**: FLUX foundation model with character LoRAs
- **Image Editing**: Qwen-Image-Edit-2509 + specialized ecosystem LoRAs
  - Base model: Qwen/Qwen-Image-Edit-2509 (official)
  - Community ecosystem: Multiple specialized fine-tunes available
    - Angle changes (dx8152/Qwen-Edit-2509-Multiple-angles)
    - Face/identity preservation models
    - Lighting/complexion adjustments
    - Style transfer (reference)
  - Strategy: Single LoRA, multi-LoRA, custom, or hybrid approach
- **Training**: LoRA/PEFT techniques (QLoRA, 4-bit quantization, gradient checkpointing)
- **AI Curation**: Face recognition libraries for identity filtering
- **Language**: Python (primary - for ML/AI workflows)
- **Frameworks**: 
  - ai-toolkit (FLUX LoRA training - proven)
  - Diffusers (Qwen-Image-Edit inference and training)
  - PEFT (LoRA training for image editing models)

## Project Conventions

### Code Style
- Python: TBD (will follow standard ML/AI conventions)
- Clear variable names that reflect the dual-flywheel concept (e.g., `char_lora_v1`, `qwen_lora_v2`)
- Document prompts and hyperparameters for reproducibility

### Architecture Patterns
- **Phased Training**: Head/expressions first, then full body
- **Human-in-the-loop**: Manual review gates between generation and training phases
- **Iterative Refinement**: Each flywheel version improves the next
- **Dataset Organization**: Separate enriched, synthetic, and pristine datasets

### Testing Strategy
- **Benchmark-driven**: Use model card targets (neutral/smiling/angry/sad portraits from different angles, T-pose, standing, sitting)
- **Version comparison**: Test each LoRA version against benchmark prompts
- **Identity verification**: Automated face recognition filtering before human review

### Git Workflow
- TBD (currently in brainstorming/planning phase)

## Domain Context
- **Character LoRA Training**: Training lightweight adapters that teach foundation models to generate specific characters
- **HITL Data Generation**: Using human judgment to prevent model drift and maintain quality
- **Instance vs Class Tokens**: Training uses instance prompts (e.g., "ohwx_char person") and class prompts (e.g., "a person")
- **Multi-stage Pipeline**: Data enrichment → training → generation → curation → fine-tuning

## Important Constraints
- **Local-only deployment**: All processing runs on a single machine with one 4090
- **24GB VRAM limit**: Requires memory-saving techniques (4-bit quantization, low LoRA rank, gradient checkpointing)
- **Manual curation bottleneck**: Human review is critical for quality but limits throughput
- **Bootstrap problem**: Initial source material (10-20 images) must have variety in angles/expressions
- **Multi-LoRA complexity**: Managing multiple specialized LoRAs adds operational overhead but provides flexibility

## External Dependencies
- Qwen-Image-Edit-2509 model (official Qwen image editing model)
- **Qwen-Edit ecosystem** (community specialized LoRAs):
  - dx8152/Qwen-Edit-2509-Multiple-angles (angle changes)
  - Face/identity preservation LoRAs (to be identified)
  - Lighting/skin editing LoRAs (to be identified)
  - Reference: https://huggingface.co/models?pipeline_tag=image-to-image&sort=trending&search=qwen
- FLUX foundation model (for image generation)
- Face recognition libraries (for automated identity filtering)
- Diffusers and PEFT libraries (for training and inference)
