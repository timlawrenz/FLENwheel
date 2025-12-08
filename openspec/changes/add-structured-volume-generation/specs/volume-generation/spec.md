## ADDED Requirements

### Requirement: Prompt Template System

The system SHALL provide a YAML-based prompt template system that defines structured image generation across categories.

#### Scenario: Template loading and parsing
- **WHEN** the orchestrator loads a template file from `/mnt/nas-ai-models/training-data/flenwheel/templates/`
- **THEN** it SHALL parse the YAML and extract category, models, templates, and variations
- **AND** it SHALL validate that all referenced models exist in the NAS model repository

#### Scenario: Variable expansion
- **WHEN** a template contains variables like `{angle}` and `{expression}`
- **THEN** the system SHALL expand all combinations (e.g., `[front, side]` × `[smiling, neutral]` = 4 prompts)
- **AND** each expanded prompt SHALL be associated with its source template for tracking

#### Scenario: Target count validation
- **WHEN** a template specifies `count: 100`
- **THEN** the system SHALL calculate expected images from (variations × models × seeds)
- **AND** it SHALL warn if actual count differs significantly from target

### Requirement: Category-Based Generation

The system SHALL generate images across predefined categories to ensure diverse training data coverage.

#### Scenario: Portrait category generation
- **WHEN** generating portrait category images
- **THEN** the system SHALL produce headshots, bust shots, and close-ups
- **AND** it SHALL ensure coverage of multiple angles (front, half-left, profile, half-right, profile-right)
- **AND** it SHALL ensure coverage of multiple expressions (neutral, smiling, serious, contemplative)

#### Scenario: Body pose category generation
- **WHEN** generating body-pose category images
- **THEN** the system SHALL produce standing, sitting, and action poses
- **AND** it SHALL include model card specific poses (t-pose, a-pose, neutral standing)
- **AND** full body SHALL be visible in all body-pose images

#### Scenario: Hands category generation
- **WHEN** generating hands category images
- **THEN** the system SHALL produce images with hands clearly visible and in focus
- **AND** it SHALL include various hand poses (at sides, clasped, gesturing, holding)
- **AND** it SHALL generate hand close-ups with detailed skin texture

#### Scenario: Context category generation
- **WHEN** generating context category images
- **THEN** the system SHALL vary environments (beach, urban, forest, studio, home)
- **AND** it SHALL vary lighting conditions (golden hour, overcast, dramatic, soft)
- **AND** it SHALL vary clothing and accessories

### Requirement: Parallel Model Execution

The system SHALL execute multiple models concurrently on the AMD server to maximize throughput.

#### Scenario: Concurrent model loading
- **WHEN** the orchestrator starts on the AMD server with 128GB VRAM
- **THEN** it SHALL load 4-6 models in parallel based on VRAM availability
- **AND** it SHALL monitor VRAM usage and refuse to load more models if >90% utilized

#### Scenario: Queue-based work distribution
- **WHEN** multiple models are loaded
- **THEN** each model SHALL pull work from a shared prompt queue
- **AND** generation SHALL proceed in parallel across all loaded models
- **AND** completed images SHALL be written to NAS with metadata

#### Scenario: Progress tracking and checkpointing
- **WHEN** generation is in progress
- **THEN** the system SHALL log progress every 10 images
- **AND** it SHALL checkpoint state every 50 images (per category)
- **AND** it SHALL support resumption from last checkpoint if interrupted

### Requirement: Metadata Tracking

The system SHALL track comprehensive metadata for each generated image to enable analytics and future learning.

#### Scenario: Image metadata capture
- **WHEN** an image is generated
- **THEN** the system SHALL save a JSON metadata file alongside the image
- **AND** metadata SHALL include: source_images, model_name, lora_name (if used), prompt, seed, category, timestamp

#### Scenario: Model performance tracking
- **WHEN** generation completes
- **THEN** the system SHALL aggregate metadata to calculate per-model statistics
- **AND** statistics SHALL include: total_images, categories_used, avg_generation_time
- **AND** results SHALL be exportable for future ML-based model selection

### Requirement: NAS Storage Integration

The system SHALL use shared NAS storage (`/mnt/nas-ai-models/`) for all models and training data.

#### Scenario: NAS directory structure
- **WHEN** the system initializes
- **THEN** it SHALL verify the following NAS paths exist:
  - `/mnt/nas-ai-models/training-data/flenwheel/sources/`
  - `/mnt/nas-ai-models/training-data/flenwheel/generated/`
  - `/mnt/nas-ai-models/training-data/flenwheel/curated/`
  - `/mnt/nas-ai-models/training-data/flenwheel/loras/`
  - `/mnt/nas-ai-models/training-data/flenwheel/templates/`

#### Scenario: Cross-server data access
- **WHEN** images are generated on the AMD server
- **THEN** they SHALL be immediately accessible from the RTX 4090 server via NAS
- **AND** no explicit data synchronization SHALL be required

#### Scenario: Model loading from NAS
- **WHEN** loading a model or LoRA
- **THEN** the system SHALL read from NAS paths:
  - Base models: `/mnt/nas-ai-models/diffusion_models/`
  - LoRAs: `/mnt/nas-ai-models/loras/`
- **AND** both AMD and RTX 4090 servers SHALL use identical paths
