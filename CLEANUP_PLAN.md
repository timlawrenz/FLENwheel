# Uncommitted Files Analysis & Plan

**Date**: 2025-12-08  
**Purpose**: Document and organize uncommitted files before next session

## Categories & Decisions

### 1. ✅ KEEP & COMMIT - Test/Validation Scripts

**Purpose**: Model validation from previous sessions, useful for debugging

```
scripts/test_qwen_basic.py
scripts/test_qwen_quick.py
scripts/test_qwen_comprehensive.py
scripts/test_qwen_8bit.py
scripts/test_qwen_quantized.py
scripts/test_qwen_dfloat11.py
scripts/test_dx8152_lora.py
scripts/test_angles_dfloat11.py
scripts/test_flux2_minimal.py
```

**Action**: Commit with message "chore: Add model validation test scripts"

### 2. ✅ KEEP & COMMIT - FLUX2 Exploration Docs

**Purpose**: Alternative approach documentation, strategic context

```
docs/flux2-evaluation.md
docs/flux2-setup.md
README_FLUX2_TEST.md
README_FLUX2_VRAM_ISSUE.md
scripts/flux2_gguf_inspect.py
scripts/flux2_gguf_loader.py
scripts/flux2_vram_test.py
openspec/changes/add-flux2-parallel-pipeline/
```

**Reasoning**: 
- Documents strategic pivot consideration (FLUX.2 multi-reference)
- Valuable context for future decisions
- OpenSpec proposal shows thought process

**Action**: Commit with message "docs: Add FLUX.2 evaluation and exploration"

### 3. 📁 ARCHIVE - Old Workflow Scripts

**Purpose**: Pre-volume strategy scripts, superseded by orchestrator

```
scripts/enrich_0I1_complete.sh
scripts/enrich_0I1_portraits.py
scripts/enrich_0I1_poses.py
scripts/generate_coverage.py
scripts/generate_expressions.py
scripts/generate_micro.py
scripts/generate_scenes.py
scripts/generate_test_portraits.py
scripts/assess_source_images.py
scripts/organize_samples.py
```

**Options**:
- A) Move to `scripts/archive/` directory
- B) Delete (available in git history if needed)
- C) Keep as reference examples

**Recommendation**: Move to `scripts/archive/old-workflow/`

**Action**: 
```bash
mkdir -p scripts/archive/old-workflow
git mv scripts/enrich_0I1_*.py scripts/archive/old-workflow/
git mv scripts/generate_{coverage,expressions,micro,scenes,test_portraits}.py scripts/archive/old-workflow/
git mv scripts/{assess_source_images,organize_samples}.py scripts/archive/old-workflow/
```

### 4. ✅ KEEP & COMMIT - Utility Scripts

**Purpose**: Still useful for current workflow

```
scripts/caption_training_data.py - Still needed for ai-toolkit training
scripts/generate_model_card.py - Model card generation (keep)
scripts/generate_model_card_safe.py - Safer version
scripts/browse_samples.sh - Useful for reviewing outputs
```

**Action**: Commit with message "chore: Add utility scripts for training workflow"

### 5. ❌ GITIGNORE - Data/Runtime Directories

**Purpose**: Generated data, downloads, logs - should NOT be in git

```
DFloat11__Qwen-Image-Edit-2509-DF11/  (27GB - model download)
data/  (415MB - generated images)
models/  (282MB - model files)
config/  (16KB - runtime config)
lib/  (56KB - downloaded libraries)
logs/  (8KB - runtime logs)
```

**Action**: Add to `.gitignore`

### 6. ⚠️ REVIEW - Working Notes

```
TODO.md - Task tracking from Nov 26 session
```

**Content**: Mix of completed tasks and FLUX.2 evaluation notes

**Options**:
- A) Keep as historical TODO (commit)
- B) Archive to `docs/archive/`
- C) Delete (superseded by OpenSpec tasks)

**Recommendation**: Move to `docs/archive/TODO-2025-11-26.md` with context note

## Size Analysis

```
Total uncommitted: ~28GB
├── 27GB   DFloat11 model (gitignore)
├── 415MB  data/ (gitignore)
├── 282MB  models/ (gitignore)
├── <1MB   docs/scripts to commit
└── <100KB config/lib/logs (gitignore)
```

**Impact**: Committing scripts/docs adds <1MB to repo

## Implementation Plan

### Step 1: Update .gitignore

```bash
cat >> .gitignore << 'EOF'

# Model downloads and generated data
DFloat11__Qwen-Image-Edit-2509-DF11/
models/
data/
lib/
config/
logs/

# Python cache
__pycache__/
*.pyc
*.pyo
*.egg-info/

# Virtual environments
venv/
.venv/

# IDE
.vscode/
.idea/
*.swp
EOF
```

### Step 2: Archive Old Workflow Scripts

```bash
mkdir -p scripts/archive/old-workflow
git mv scripts/enrich_0I1_complete.sh scripts/archive/old-workflow/
git mv scripts/enrich_0I1_portraits.py scripts/archive/old-workflow/
git mv scripts/enrich_0I1_poses.py scripts/archive/old-workflow/
git mv scripts/generate_coverage.py scripts/archive/old-workflow/
git mv scripts/generate_expressions.py scripts/archive/old-workflow/
git mv scripts/generate_micro.py scripts/archive/old-workflow/
git mv scripts/generate_scenes.py scripts/archive/old-workflow/
git mv scripts/generate_test_portraits.py scripts/archive/old-workflow/
git mv scripts/assess_source_images.py scripts/archive/old-workflow/
git mv scripts/organize_samples.py scripts/archive/old-workflow/
```

### Step 3: Archive Historical TODO

```bash
mkdir -p docs/archive
cat > docs/archive/TODO-2025-11-26.md << 'HEADER'
# Historical TODO from 2025-11-26

**Context**: This TODO is from the pre-volume strategy phase when FLUX.2 was just released.
Most tasks superseded by OpenSpec proposal: `add-structured-volume-generation`

Original content:
---

HEADER
cat TODO.md >> docs/archive/TODO-2025-11-26.md
git add docs/archive/TODO-2025-11-26.md
rm TODO.md
```

### Step 4: Commit Test Scripts

```bash
git add scripts/test_*.py
git commit -m "chore: Add model validation test scripts

Test scripts for Qwen-Image-Edit and FLUX.2:
- test_qwen_basic.py - Basic model loading
- test_qwen_quick.py - Single image generation
- test_qwen_comprehensive.py - Full test suite
- test_qwen_8bit/quantized.py - Memory optimization tests
- test_dx8152_lora.py - Multiple angles LoRA
- test_angles_dfloat11.py - DFloat11 LoRA testing
- test_flux2_minimal.py - FLUX.2 validation

Purpose: Debugging and model validation"
```

### Step 5: Commit FLUX2 Documentation

```bash
git add docs/flux2-*.md README_FLUX2_*.md scripts/flux2_*.py
git add openspec/changes/add-flux2-parallel-pipeline/
git commit -m "docs: Add FLUX.2 evaluation and exploration

FLUX.2-dev multi-reference investigation:
- Strategic assessment (flux2-evaluation.md)
- Setup documentation (flux2-setup.md)
- VRAM testing results (README_FLUX2_VRAM_ISSUE.md)
- Test results (README_FLUX2_TEST.md)
- Inspection/loading scripts (flux2_gguf_*.py)
- OpenSpec proposal (alternative to Qwen-Edit approach)

Context: FLUX.2-dev released with 10-photo multi-reference support,
evaluated as potential alternative to volume generation strategy.
Kept for future reference if multi-reference proves superior."
```

### Step 6: Commit Utility Scripts

```bash
git add scripts/caption_training_data.py
git add scripts/generate_model_card*.py
git add scripts/browse_samples.sh
git commit -m "chore: Add utility scripts for training workflow

- caption_training_data.py: Generate captions for ai-toolkit
- generate_model_card.py/safe.py: Benchmark image generation
- browse_samples.sh: Quick image review tool

These complement the volume generation orchestrator"
```

### Step 7: Final Review and Push

```bash
git status
git log --oneline -10
git push origin volume
```

## Summary

**Commits to add**: 4
1. Test scripts (model validation)
2. FLUX2 docs (strategic exploration)
3. Utility scripts (training support)
4. Archive old workflow + cleanup

**Gitignored**: ~28GB of data/models/logs

**Result**: Clean repo with useful reference material, no bloat

## Verification Checklist

- [ ] .gitignore updated
- [ ] Old workflow scripts archived
- [ ] Test scripts committed
- [ ] FLUX2 docs committed
- [ ] Utility scripts committed
- [ ] Historical TODO archived
- [ ] No large files in git
- [ ] `git status` clean
- [ ] Pushed to GitHub
