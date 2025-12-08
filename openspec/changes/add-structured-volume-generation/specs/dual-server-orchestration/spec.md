## ADDED Requirements

### Requirement: Dual-Server Architecture

The system SHALL coordinate work between AMD 7995X (128GB VRAM) and RTX 4090 (24GB VRAM) servers.

#### Scenario: Server role assignment
- **WHEN** the system is deployed
- **THEN** the AMD server SHALL be designated for mass parallel generation
- **AND** the RTX 4090 server SHALL be designated for ELO voting UI and LoRA training
- **AND** both servers SHALL access shared NAS storage at `/mnt/nas-ai-models/`

#### Scenario: AMD server generation capacity
- **WHEN** running generation on the AMD server
- **THEN** it SHALL support loading 4-6 models concurrently
- **AND** VRAM usage SHALL be monitored and SHALL NOT exceed 90% of 128GB
- **AND** it SHALL generate 30-60 images per hour (target)

#### Scenario: RTX 4090 training capacity
- **WHEN** running LoRA training on the RTX 4090 server
- **THEN** it SHALL use ai-toolkit with existing proven configurations
- **AND** it SHALL support 4-bit quantization and gradient checkpointing
- **AND** it SHALL complete training in 2-4 hours for 200 image dataset

### Requirement: Shared NAS Storage

The system SHALL use network-attached storage for seamless data sharing between servers.

#### Scenario: NAS mount verification
- **WHEN** either server initializes
- **THEN** it SHALL verify that `/mnt/nas-ai-models/` is mounted and accessible
- **AND** it SHALL verify read and write permissions
- **AND** it SHALL abort with clear error if NAS is unavailable

#### Scenario: Model repository access
- **WHEN** loading models from NAS
- **THEN** both servers SHALL use identical paths:
  - `/mnt/nas-ai-models/diffusion_models/flux2_dev_fp8mixed.safetensors`
  - `/mnt/nas-ai-models/loras/qwen-image-edit/multiple-angles/`
  - `/mnt/nas-ai-models/loras/flux/`
- **AND** no model files SHALL be duplicated to local storage

#### Scenario: Generation output synchronization
- **WHEN** images are generated on AMD server
- **THEN** they SHALL be written directly to NAS paths
- **AND** they SHALL be immediately visible to RTX 4090 server
- **AND** no explicit sync command SHALL be required

### Requirement: AMD Server Environment

The system SHALL configure the AMD 7995X server with appropriate ML libraries.

#### Scenario: ROCm PyTorch installation
- **WHEN** setting up the AMD server
- **THEN** it SHALL install PyTorch with ROCm support (AMD GPU acceleration)
- **AND** it SHALL verify VRAM is correctly detected (128GB)
- **AND** it SHALL test basic tensor operations on GPU

#### Scenario: Diffusers compatibility
- **WHEN** loading Diffusers models on AMD server
- **THEN** they SHALL run with ROCm backend
- **AND** FLUX.2-dev fp8 model SHALL load successfully
- **AND** Qwen-Image-Edit models SHALL load successfully

#### Scenario: Parallel execution testing
- **WHEN** testing AMD server capacity
- **THEN** it SHALL successfully load 4 models simultaneously
- **AND** each model SHALL generate images in parallel
- **AND** total VRAM usage SHALL be measured and logged

### Requirement: Work Coordination

The system SHALL coordinate generation and curation workflows across servers without manual intervention.

#### Scenario: Generation workflow
- **WHEN** starting a new character generation
- **THEN** source images SHALL be copied to NAS sources directory
- **AND** orchestrator SHALL run on AMD server reading templates from NAS
- **AND** generated images SHALL be written to NAS generated directory
- **AND** metadata SHALL be written alongside images

#### Scenario: Curation workflow
- **WHEN** generation completes
- **THEN** voting UI on RTX 4090 SHALL automatically detect new images in NAS
- **AND** images SHALL be imported into voting database with metadata
- **AND** voting SHALL proceed with category filtering
- **AND** curated winners SHALL be exported to NAS curated directory

#### Scenario: Training workflow
- **WHEN** curation export completes
- **THEN** ai-toolkit on RTX 4090 SHALL read curated images from NAS
- **AND** training config SHALL reference NAS paths
- **AND** trained LoRA SHALL be saved to NAS loras directory
- **AND** trained LoRA SHALL be accessible for model card generation

### Requirement: Network Performance Monitoring

The system SHALL monitor NAS I/O performance to identify bottlenecks.

#### Scenario: Write throughput measurement
- **WHEN** generating images to NAS
- **THEN** the system SHALL measure write throughput (MB/s)
- **AND** it SHALL log warnings if throughput drops below 50 MB/s
- **AND** it SHALL suggest local staging if network is bottleneck

#### Scenario: Read throughput measurement
- **WHEN** loading models or images from NAS
- **THEN** the system SHALL measure read throughput (MB/s)
- **AND** it SHALL cache frequently accessed files if network is slow
- **AND** it SHALL report network latency statistics

### Requirement: Local Staging Support

The system SHALL support optional local SSD staging for performance optimization when NAS I/O is a bottleneck.

#### Scenario: Local generation staging
- **WHEN** configured to use local staging and NAS write throughput is insufficient (<50 MB/s)
- **THEN** the system SHALL generate images to local SSD first
- **AND** it SHALL batch-copy completed images to NAS every 100 images
- **AND** it SHALL verify all files transferred before deleting local copies

#### Scenario: Model caching
- **WHEN** configured to use model caching and loading large models from NAS
- **THEN** the system SHALL cache models to local SSD on first load
- **AND** it SHALL use cached copy for subsequent runs
- **AND** it SHALL verify cache validity (checksum comparison with NAS)

### Requirement: Error Handling and Recovery

The system SHALL handle network and server failures gracefully.

#### Scenario: NAS disconnection during generation
- **WHEN** NAS becomes unavailable during generation
- **THEN** the system SHALL pause generation and retry writes up to 3 times
- **AND** it SHALL save state to local disk if NAS remains unavailable
- **AND** it SHALL resume from checkpoint when NAS is restored

#### Scenario: AMD server failure
- **WHEN** AMD server crashes during generation
- **THEN** the system SHALL resume from last checkpoint on restart
- **AND** it SHALL skip already-generated images (check file existence)
- **AND** it SHALL continue with remaining prompts in queue

#### Scenario: RTX 4090 server failure
- **WHEN** RTX 4090 server crashes during training
- **THEN** ai-toolkit checkpoint mechanism SHALL allow resumption
- **AND** voting database SHALL remain consistent (transaction rollback)
- **AND** no data loss SHALL occur for completed votes
