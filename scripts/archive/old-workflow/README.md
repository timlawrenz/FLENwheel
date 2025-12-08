# Old Workflow Scripts (Archived)

**Date Archived**: 2025-12-08  
**Reason**: Superseded by volume generation orchestrator

## Context

These scripts were created during the initial exploration phase (Nov 2025) when the approach was:
- Manual enrichment with Qwen-Image-Edit
- Individual generation scripts per category
- One-off testing and iteration

**Replaced by**: `scripts/generate_structured_volume.py` (template-based orchestrator)

## Scripts in This Directory

### Enrichment (Old Approach)
- `enrich_0I1_complete.sh` - Full enrichment pipeline
- `enrich_0I1_portraits.py` - Portrait-specific enrichment
- `enrich_0I1_poses.py` - Pose generation

### Generation (Old Approach)
- `generate_coverage.py` - Coverage testing
- `generate_expressions.py` - Expression variations
- `generate_micro.py` - Micro-batch testing
- `generate_scenes.py` - Scene variations  
- `generate_test_portraits.py` - Portrait testing

### Utilities
- `assess_source_images.py` - Source image analysis
- `organize_samples.py` - Output organization

## Why Archived?

**Old approach problems**:
- ❌ Manual, one-off scripts for each category
- ❌ No systematic coverage
- ❌ Hard to track which model generated what
- ❌ No metadata or curation workflow

**New volume strategy**:
- ✅ Template-driven systematic generation
- ✅ Parallel execution (4-6 models)
- ✅ Metadata tracking
- ✅ ELO-based curation
- ✅ Category coverage guaranteed

## Useful References

Some concepts from these scripts influenced the new orchestrator:
- Source image assessment logic
- Caption generation patterns
- Organization by category

**See**: `scripts/generate_structured_volume.py` for current implementation
