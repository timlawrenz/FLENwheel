## ADDED Requirements

### Requirement: FLUX2-dev GGUF Inference

The system SHALL provide Python-based inference capabilities for the FLUX2-dev model in Q4_1.gguf quantized format, independent of ComfyUI or external workflow tools.

#### Scenario: Load quantized model successfully
- **WHEN** the FLUX2 inference script is initialized with the model path `/mnt/essdee/ComfyUI/models/diffusion_models/flux2-dev-Q4_1.gguf`
- **THEN** the model loads into VRAM without errors
- **AND** peak VRAM usage does not exceed 20GB on RTX 4090
- **AND** the model is ready for inference

#### Scenario: Single-reference image generation
- **WHEN** provided with 1 reference image and a text prompt
- **THEN** the system generates an output image matching the prompt description
- **AND** the generated character maintains visual similarity to the reference
- **AND** generation completes within a reasonable timeframe (≤60 seconds per image)

#### Scenario: Model unloading and cleanup
- **WHEN** inference is complete or on error
- **THEN** the model is properly unloaded from VRAM
- **AND** GPU memory is released for other processes

---

### Requirement: Multi-Reference Character Consistency

The system SHALL support multi-reference image input (1 to 10 reference photos) to maintain character identity across generated variations, leveraging FLUX2-dev's native multi-reference capabilities.

#### Scenario: Multi-reference generation with 3 images
- **WHEN** provided with 3 reference images of the same character and a transformation prompt (e.g., "change angle to 3/4 profile view")
- **THEN** the system generates an output image applying the transformation
- **AND** the character's identity remains consistent with all 3 references
- **AND** character consistency score is ≥70% (measured via face recognition)

#### Scenario: Scaling to 10 references
- **WHEN** provided with 10 reference images
- **THEN** the system successfully generates output without VRAM overflow
- **AND** character consistency improves or remains stable compared to fewer references
- **AND** VRAM usage is profiled and documented

#### Scenario: Invalid reference count
- **WHEN** provided with 0 references or more than 10 references
- **THEN** the system raises a clear validation error
- **AND** provides guidance on valid reference count range

---

### Requirement: Training Material Enrichment

The system SHALL generate enriched training datasets from source character images by creating variations across angles, expressions, poses, and backgrounds while preserving character identity.

#### Scenario: Generate angle variations
- **WHEN** provided with 5 source images and angle transformation prompts (front, 3/4 left, 3/4 right, profile, back)
- **THEN** the system generates at least 20 angle-varied images (4 variations per source)
- **AND** each generated image maintains character identity (≥70% consistency score)
- **AND** outputs are organized in `data/[character]/flux2/enriched/angles/`

#### Scenario: Generate expression variations
- **WHEN** provided with 5 source images and expression prompts (neutral, smiling, sad, angry, surprised)
- **THEN** the system generates at least 20 expression-varied images
- **AND** character identity is preserved across all expressions
- **AND** facial expression changes are clearly visible and accurate

#### Scenario: Batch processing with progress tracking
- **WHEN** running batch enrichment on 50+ generation tasks
- **THEN** the system displays progress information (current task, percentage complete, ETA)
- **AND** errors in individual tasks do not halt the entire batch
- **AND** failed generations are logged with error details

---

### Requirement: Character Consistency Evaluation

The system SHALL provide automated evaluation of character identity preservation using face recognition technology to filter and score generated images.

#### Scenario: Face recognition scoring
- **WHEN** comparing a generated image to reference images
- **THEN** the system calculates a similarity score (0-100%)
- **AND** scores ≥70% are marked as "passing" for identity preservation
- **AND** scores <70% are flagged for manual review or rejection

#### Scenario: Batch evaluation reporting
- **WHEN** evaluating a directory of 100 generated images
- **THEN** the system produces a report showing total images evaluated
- **AND** passing rate (percentage ≥70% threshold)
- **AND** distribution of scores (histogram or percentiles)
- **AND** list of flagged images with scores

#### Scenario: Integration with face recognition library
- **WHEN** the evaluation script initializes
- **THEN** a face recognition library (InsightFace or deepface) is loaded successfully
- **AND** reference embeddings are computed once and cached
- **AND** comparison operations are GPU-accelerated where possible

---

### Requirement: FLUX2 vs Qwen Comparison Framework

The system SHALL provide metrics and tools to compare the quality, consistency, and efficiency of FLUX2-based enrichment versus Qwen-Image-Edit-based enrichment.

#### Scenario: Parallel workflow execution
- **WHEN** running both FLUX2 and Qwen enrichment on the same 5 source images with equivalent transformation prompts
- **THEN** outputs are generated to separate directories for fair comparison
- **AND** identical random seeds are used where applicable
- **AND** both workflows complete without interference

#### Scenario: Quantitative comparison metrics
- **WHEN** generating a comparison report
- **THEN** the report includes character identity preservation rate (% ≥70%)
- **AND** generation speed (images per minute)
- **AND** peak VRAM usage (GB)
- **AND** image quality scores (manual or automated)
- **AND** transformation accuracy (how well prompts were followed)

#### Scenario: Side-by-side visualization
- **WHEN** comparing outputs from both pipelines
- **THEN** the system generates side-by-side comparison images (FLUX2 | Qwen)
- **AND** displays prompts, scores, and metadata for each
- **AND** exports to a visual report format (HTML, PDF, or image grid)

---

### Requirement: Configuration and Parameter Management

The system SHALL provide configurable parameters for model paths, generation settings, and output organization to support flexible experimentation and deployment.

#### Scenario: Configuration file loading
- **WHEN** the FLUX2 pipeline initializes
- **THEN** it loads configuration from a YAML or JSON file specifying model path (GGUF file location)
- **AND** output directories
- **AND** default generation parameters (steps, CFG, dimensions)
- **AND** face recognition thresholds

#### Scenario: Command-line parameter override
- **WHEN** running a script with CLI arguments (e.g., `--guidance-scale 7.5 --steps 30`)
- **THEN** CLI arguments override configuration file defaults
- **AND** the system logs which parameters are being used
- **AND** invalid parameter values raise clear validation errors

#### Scenario: Prompt template library
- **WHEN** using predefined transformation types (e.g., "angle:profile" or "expression:smiling")
- **THEN** the system expands these to full FLUX2 prompts using a template library
- **AND** templates are editable in a configuration file
- **AND** custom templates can be added without code changes

---

### Requirement: Data Organization and Metadata Tracking

The system SHALL organize generated images, reference data, and metadata in a structured directory hierarchy parallel to existing Qwen workflows.

#### Scenario: Directory structure creation
- **WHEN** initializing a new character for FLUX2 enrichment
- **THEN** the system creates `data/[character]/flux2/reference/` for source images
- **AND** `data/[character]/flux2/enriched/` for generated variations
- **AND** `data/[character]/flux2/filtered/` for consistency-passing images
- **AND** `data/[character]/flux2/metadata/` for scores and generation logs

#### Scenario: Metadata tracking
- **WHEN** an image is generated
- **THEN** a JSON metadata file is saved alongside it containing original prompt text
- **AND** generation parameters (steps, CFG, seed, reference count)
- **AND** character consistency score (if evaluated)
- **AND** generation timestamp
- **AND** reference image filenames

#### Scenario: Filtered dataset curation
- **WHEN** running the evaluation and filtering step
- **THEN** images with scores ≥70% are copied to the `filtered/` directory
- **AND** metadata includes the filtering threshold used
- **AND** a summary report lists total generated, passing, and rejected counts

---

### Requirement: Error Handling and Robustness

The system SHALL handle errors gracefully, including VRAM limitations, corrupted images, and invalid inputs, providing clear diagnostics to the user.

#### Scenario: VRAM overflow handling
- **WHEN** generation would exceed available VRAM (e.g., 10 refs on 4090 with 24GB)
- **THEN** the system detects the condition before attempting generation
- **AND** suggests reducing reference count or batch size
- **AND** does not crash the entire pipeline

#### Scenario: Invalid image file handling
- **WHEN** a reference image file is corrupted or unreadable
- **THEN** the system logs a clear error identifying the file
- **AND** skips the file and continues processing remaining images
- **AND** includes the error in the final report

#### Scenario: Model loading failure
- **WHEN** the GGUF model file is missing or incompatible
- **THEN** the system provides a diagnostic message with expected file path
- **AND** possible causes (file not found, unsupported format, library version mismatch)
- **AND** suggested remediation steps

---

### Requirement: Performance Profiling and Optimization

The system SHALL provide profiling tools to measure VRAM usage, generation speed, and bottlenecks across different configurations (reference counts, batch sizes, parameters).

#### Scenario: VRAM profiling across reference counts
- **WHEN** running profiling mode with 1, 3, 5, and 10 references
- **THEN** the system logs peak VRAM usage for each configuration
- **AND** identifies the maximum safe reference count for RTX 4090 (24GB)
- **AND** generates a VRAM usage chart or table

#### Scenario: Batch processing optimization
- **WHEN** generating 100 images in batch mode
- **THEN** the system maximizes throughput by reusing loaded models across generations
- **AND** batching where VRAM permits
- **AND** minimizing redundant preprocessing (reference embedding caching)

#### Scenario: Performance report generation
- **WHEN** profiling is complete
- **THEN** the system generates a report including average generation time per image
- **AND** images per minute throughput
- **AND** VRAM usage statistics (min, max, avg)
- **AND** bottleneck identification (model loading, preprocessing, generation, postprocessing)
