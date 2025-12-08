## ADDED Requirements

### Requirement: ELO Rating System

The system SHALL implement ELO-based ranking for generated images using pairwise comparisons.

#### Scenario: Initial ELO score assignment
- **WHEN** a generated image is imported for voting
- **THEN** it SHALL be assigned an initial ELO score of 1000
- **AND** it SHALL be associated with its category, model, and metadata

#### Scenario: Pairwise voting
- **WHEN** a user is presented with two images for comparison
- **THEN** the user SHALL select the image that better preserves character identity
- **AND** the system SHALL record a vote with winner_id and loser_id

#### Scenario: ELO score update
- **WHEN** a vote is recorded
- **THEN** the system SHALL calculate ELO changes using the formula:
  - Expected score = 1 / (1 + 10^((opponent_elo - own_elo) / 400))
  - New ELO = old_elo + K * (actual_score - expected_score)
  - K = 32 (standard chess K-factor)
- **AND** both winner and loser ELO scores SHALL be updated atomically

#### Scenario: Preventing duplicate votes
- **WHEN** a vote is recorded between image A and image B
- **THEN** the system SHALL prevent voting on the same pair again (A vs B or B vs A)
- **AND** the system SHALL only present pairs that have not been voted on

### Requirement: Category-Filtered Voting

The system SHALL allow voting within specific categories to ensure fair comparisons.

#### Scenario: Category selection for voting
- **WHEN** a user starts a voting session
- **THEN** the system SHALL allow filtering by category (portraits, body-poses, context, hands)
- **AND** only images from the selected category SHALL be presented for voting

#### Scenario: Cross-category voting prevention
- **WHEN** presenting images for voting
- **THEN** the system SHALL NOT present images from different categories in the same comparison
- **AND** each category SHALL have independent ELO rankings

### Requirement: Web-Based Voting UI

The system SHALL provide a web interface for efficient A/B image voting.

#### Scenario: Image pair presentation
- **WHEN** the voting UI loads
- **THEN** it SHALL display two images side-by-side
- **AND** images SHALL be loaded from NAS paths
- **AND** each image SHALL show its metadata (model, prompt) on hover

#### Scenario: Keyboard-based voting
- **WHEN** viewing an image pair
- **THEN** the user SHALL vote using keyboard shortcuts:
  - Left arrow key: left image wins
  - Right arrow key: right image wins
  - 'k' key: reject both (kill branch)
- **AND** the next pair SHALL load immediately after voting

#### Scenario: Progress tracking
- **WHEN** voting within a category
- **THEN** the UI SHALL display "X of Y pairs voted" progress
- **AND** it SHALL estimate remaining time based on avg votes/minute

### Requirement: Batch Voting Operations

The system SHALL support batch operations to accelerate voting on obvious winners/losers.

#### Scenario: Model-based batch accept
- **WHEN** a user identifies that all images from a specific model are high quality
- **THEN** the system SHALL provide "Accept all from [model_name]" button
- **AND** all unvoted images from that model SHALL receive a high default ELO (1200)

#### Scenario: Model-based batch reject
- **WHEN** a user identifies that all images from a specific model are low quality
- **THEN** the system SHALL provide "Reject all from [model_name]" button
- **AND** all unvoted images from that model SHALL receive a low default ELO (800)

#### Scenario: Top-N auto-selection
- **WHEN** voting is complete for a category
- **THEN** the system SHALL provide "Select top 30%" or "Select top 50" button
- **AND** images SHALL be sorted by ELO and the top N SHALL be marked for curation

### Requirement: Curation Export

The system SHALL export curated images (ELO winners) for LoRA training.

#### Scenario: ELO-based selection
- **WHEN** exporting curated images for a category
- **THEN** the system SHALL select images with ELO score > threshold (default: 1100)
- **OR** it SHALL select top N images by ELO ranking (default: top 50 per category)

#### Scenario: Copy to curated directory
- **WHEN** images are selected for curation
- **THEN** they SHALL be copied to `/mnt/nas-ai-models/training-data/flenwheel/curated/{character-id}/`
- **AND** directory structure SHALL preserve categories for analysis

#### Scenario: Training manifest generation
- **WHEN** curation export completes
- **THEN** the system SHALL generate a manifest file listing all curated images
- **AND** manifest SHALL include captions with instance token (e.g., "ohwx_char person")
- **AND** manifest SHALL be compatible with ai-toolkit training format

### Requirement: Analytics Dashboard

The system SHALL provide analytics on model performance based on ELO scores.

#### Scenario: Model performance comparison
- **WHEN** viewing the analytics dashboard
- **THEN** it SHALL display average ELO score per model per category
- **AND** it SHALL show total images generated per model
- **AND** it SHALL rank models by effectiveness

#### Scenario: Category coverage visualization
- **WHEN** viewing analytics
- **THEN** it SHALL show image count distribution across categories
- **AND** it SHALL highlight categories with low coverage (<50 images)
- **AND** it SHALL suggest additional template prompts for low-coverage categories

#### Scenario: ELO distribution analysis
- **WHEN** viewing analytics
- **THEN** it SHALL display ELO score distribution histogram per category
- **AND** it SHALL show median, mean, and standard deviation
- **AND** it SHALL identify outliers (very high or very low ELO images) for review

### Requirement: Vote Database Schema

The system SHALL persist votes and ELO scores in a database.

#### Scenario: TrainingImage table
- **WHEN** storing generated image metadata
- **THEN** the database SHALL include fields:
  - id, file_path, category, model_name, lora_name, prompt, seed
  - elo_score (default: 1000), vote_count (default: 0)
  - metadata_json (full metadata from generation)
  - created_at, updated_at

#### Scenario: Vote table
- **WHEN** recording a vote
- **THEN** the database SHALL include fields:
  - id, winner_id (FK to TrainingImage), loser_id (FK to TrainingImage)
  - elo_change_winner, elo_change_loser
  - created_at

#### Scenario: Database integrity
- **WHEN** a vote is recorded
- **THEN** winner_id and loser_id SHALL reference valid TrainingImage records
- **AND** winner_id SHALL NOT equal loser_id
- **AND** ELO updates SHALL occur in a transaction (atomic)
