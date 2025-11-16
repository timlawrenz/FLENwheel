# Quick Start: First Steps

This document outlines the immediate next steps to validate technical feasibility.

## Goal
Prove that Qwen-VL can enrich a dataset on this system, then build toward a full POC.

---

## Phase 1: Qwen-VL Basic Validation (TODAY)

### Estimated time: 4-6 hours

### Step 1: Install Dependencies (30 min)

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install core dependencies
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip install transformers accelerate bitsandbytes
pip install pillow opencv-python
pip install qwen-vl-utils  # Qwen-specific utilities
```

### Step 2: Download Qwen Image Edit Models (1-2 hours)

**Models to download**:
- **Qwen/Qwen-Image-Edit-2509** (base editing model, ~14GB)
- **dx8152/Qwen-Edit-2509-Multiple-angles** (LoRA for angle edits, ~100-500MB)

```bash
# Download base editing model
huggingface-cli download Qwen/Qwen-Image-Edit-2509

# Download community LoRA (to study and test)
huggingface-cli download dx8152/Qwen-Edit-2509-Multiple-angles
```

**Storage check**:
```bash
df -h ~/.cache/huggingface  # Make sure you have 20GB+ free
```

### Step 3: Create Basic Inference Test (1 hour)

Create `scripts/test_qwen_edit_basic.py`:

```python
#!/usr/bin/env python3
"""Test Qwen-Image-Edit basic inference"""

import torch
from diffusers import DiffusionPipeline
from PIL import Image

def test_qwen_edit_inference():
    model_name = "Qwen/Qwen-Image-Edit-2509"
    
    print(f"Loading model: {model_name}")
    
    # Load image editing pipeline
    pipe = DiffusionPipeline.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto",
    )
    
    # Optional: Load with 4-bit quantization if VRAM tight
    # pipe = DiffusionPipeline.from_pretrained(
    #     model_name,
    #     torch_dtype=torch.float16,
    #     device_map="auto",
    #     load_in_4bit=True
    # )
    
    print("Model loaded successfully!")
    print(f"VRAM usage: {torch.cuda.memory_allocated() / 1e9:.2f} GB")
    
    # Test with a simple image edit
    test_image_path = "test_data/sample.jpg"
    source_image = Image.open(test_image_path)
    
    # Simple editing test
    prompt = "Change the background to a forest, keep the person identical"
    
    print(f"Editing with prompt: {prompt}")
    
    edited_image = pipe(
        prompt=prompt,
        image=source_image,
        num_inference_steps=50,
    ).images[0]
    
    # Save result
    edited_image.save("test_data/edited_basic.jpg")
    print("Saved edited image to test_data/edited_basic.jpg")
    
    return pipe

if __name__ == "__main__":
    pipe = test_qwen_edit_inference()
```

**Run it**:
```bash
# First, create test directory and add a sample image
mkdir -p test_data
# Copy a test portrait image to test_data/sample.jpg

python scripts/test_qwen_edit_basic.py
```

**Success criteria**:
- ✅ Model loads without errors
- ✅ VRAM usage < 20GB
- ✅ Generates edited image
- ✅ Character identity preserved in output

### Step 4: Test with dx8152 LoRA (1 hour)

Create `scripts/test_qwen_edit_lora.py`:

```python
#!/usr/bin/env python3
"""Test Qwen-Image-Edit with dx8152 angle LoRA"""

import torch
from diffusers import DiffusionPipeline
from PIL import Image

def test_with_lora():
    base_model = "Qwen/Qwen-Image-Edit-2509"
    lora_model = "dx8152/Qwen-Edit-2509-Multiple-angles"
    
    print(f"Loading base model: {base_model}")
    
    pipe = DiffusionPipeline.from_pretrained(
        base_model,
        torch_dtype=torch.float16,
        device_map="auto",
    )
    
    print(f"Loading LoRA: {lora_model}")
    pipe.load_lora_weights(lora_model)
    
    print("Models loaded successfully!")
    print(f"VRAM usage: {torch.cuda.memory_allocated() / 1e9:.2f} GB")
    
    # Test angle changes (what dx8152 LoRA is trained for)
    test_image_path = "test_data/sample.jpg"
    source_image = Image.open(test_image_path)
    
    angle_prompts = [
        "Change camera angle to slightly left view, keep the person identical",
        "Change camera angle to profile view, maintain character appearance",
        "Show the person from a higher angle, preserve features exactly",
    ]
    
    for i, prompt in enumerate(angle_prompts):
        print(f"\n--- Test {i+1}: {prompt} ---")
        
        edited_image = pipe(
            prompt=prompt,
            image=source_image,
            num_inference_steps=50,
        ).images[0]
        
        output_path = f"test_data/edited_lora_{i+1}.jpg"
        edited_image.save(output_path)
        print(f"Saved to {output_path}")
    
    return pipe

if __name__ == "__main__":
    pipe = test_with_lora()
```

**Run it**:
```bash
python scripts/test_qwen_edit_lora.py
```

**Success criteria**:
- ✅ LoRA loads successfully
- ✅ Generates angle-changed images
- ✅ Character identity preserved
- ✅ Quality acceptable (or identify what needs improvement)

### Step 5: Comprehensive Editing Tests (2 hours)

Create `scripts/test_comprehensive_editing.py`:

```python
#!/usr/bin/env python3
"""Comprehensive test of editing capabilities"""

import torch
from diffusers import DiffusionPipeline
from PIL import Image
import os

def comprehensive_test():
    pipe = DiffusionPipeline.from_pretrained(
        "Qwen/Qwen-Image-Edit-2509",
        torch_dtype=torch.float16,
        device_map="auto",
    )
    
    test_image = Image.open("test_data/sample.jpg")
    
    # Test various editing types
    editing_tests = [
        ("background_forest", "Change background to a forest, keep person identical"),
        ("background_beach", "Change background to a beach, keep person identical"),
        ("lighting_sunset", "Make lighting look like sunset, keep subject identical"),
        ("lighting_studio", "Add studio lighting, keep person identical"),
        ("style_painting", "Convert to oil painting style, preserve features exactly"),
        ("angle_left", "Change camera angle slightly to the left, maintain appearance"),
    ]
    
    os.makedirs("test_data/comprehensive", exist_ok=True)
    
    for name, prompt in editing_tests:
        print(f"\nTesting: {prompt}")
        
        result = pipe(
            prompt=prompt,
            image=test_image,
            num_inference_steps=50,
        ).images[0]
        
        output_path = f"test_data/comprehensive/{name}.jpg"
        result.save(output_path)
        print(f"Saved to {output_path}")
    
    print("\n✅ Comprehensive test complete!")
    print("Review images in test_data/comprehensive/")
    print("Assess:")
    print("  - Character identity preservation")
    print("  - Edit quality (did background/lighting actually change?)")
    print("  - Artifacts or distortions")
    print("  - Overall suitability for dataset enrichment")

if __name__ == "__main__":
    comprehensive_test()
```

**Manual Review**:
```bash
python scripts/test_comprehensive_editing.py

# Review all outputs
ls -lh test_data/comprehensive/
# Open each image and assess quality
```

**Critical Assessment**:
- ✅ Is character identity preserved across all edits?
- ✅ Do edits actually change what we asked (backgrounds, lighting)?
- ✅ Is quality sufficient for training data?
- ❌ What fails? Document limitations
- ❓ Do we need custom LoRA training from the start?

---

## Phase 2: Dataset Enrichment POC (AFTER Phase 1 resolved)

### Prerequisites
- ✅ Working image editing solution identified
- ✅ Can edit images while preserving character identity

### Step 1: Prepare Test Dataset

```bash
# Create directory structure
mkdir -p test_data/source
mkdir -p test_data/enriched/v1

# Add 5 test character images to test_data/source/
```

### Step 2: Create Enrichment Script

Create `scripts/enrich_poc.py`:
```python
#!/usr/bin/env python3
"""POC: Enrich 5 images with different backgrounds/lighting"""

# Implementation depends on Phase 1 decision
# Pseudocode:

# for each source image:
#   for each editing_prompt in [background_prompts, lighting_prompts]:
#     edited_image = apply_editing(source_image, editing_prompt)
#     save_image(edited_image, metadata)
```

### Step 3: Run and Review

```bash
python scripts/enrich_poc.py

# Manual review
ls -lh test_data/enriched/v1/
# Open images, verify character consistency
```

**Success criteria**:
- ✅ 5 source → 25 enriched images
- ✅ Character recognizable in 70%+ of outputs
- ✅ Backgrounds/lighting actually changed

---

## Critical Decisions Needed

### 1. Image Editing Quality
**Question**: Is Qwen-Image-Edit-2509 base model good enough, or do we need custom LoRA immediately?

**Assessment criteria**:
- Character identity preservation rate
- Edit effectiveness (backgrounds, lighting, angles)
- Artifact frequency
- Comparison to dx8152 LoRA quality

**Impact**: High - determines whether Flywheel 2 starts immediately or after Flywheel 1

**Decision by**: End of Phase 1 comprehensive testing

### 2. LoRA Strategy
**Question**: Use base model first, or train custom LoRA from start?

**Options**:
- A) Start with base model, train LoRA only if insufficient
- B) Study dx8152 approach, train LoRA immediately for character consistency
- C) Use dx8152 LoRA as-is if quality sufficient

**Impact**: Medium - affects timeline and complexity

**Decision by**: After comprehensive testing

### 3. POC Scope
**Question**: How minimal for POC? Just Flywheel 1, or both?

**Recommendation**: Flywheel 1 only initially

**Impact**: Medium - affects timeline

---

## Expected Timeline

### Week 1: Discovery & Validation
- Day 1-2: Phase 1 (Qwen-VL validation)
- Day 3: Research image editing alternatives
- Day 4-5: Phase 2 POC (enrichment)

### Week 2: FLUX Integration
- Day 1-2: Prepare training dataset
- Day 3-4: Train first FLUX LoRA
- Day 5: Generate synthetic images

### Week 3: Full Loop
- Day 1-2: AI filtering + human review
- Day 3-4: Retrain FLUX LoRA v2
- Day 5: Compare v1 vs v2, document findings

### Week 4: PEFT Learning (Flywheel 2)
- Day 1-3: Learn PEFT/QLoRA
- Day 4-5: Attempt Qwen-VL LoRA training

---

## Blockers & Risks

### Immediate Blockers
1. ✅ **RESOLVED**: Using Qwen-Image-Edit-2509 for actual image editing
   - Now need to validate quality for our use case

2. ⚠️ Model download time (1-2 hours)
   - **Mitigation**: Start download early, work on other tasks

3. ⚠️ Disk space (need 50GB+ free)
   - **Mitigation**: Check now, clean up if needed

4. ⚠️ **NEW**: dx8152 LoRA may not be "good enough" yet
   - **Mitigation**: Test thoroughly, prepare to train custom LoRA

### Medium-term Risks
1. Editing quality insufficient → Need to try multiple approaches
2. VRAM constraints → May need smaller models or more aggressive quantization
3. Training time too long → May need to optimize or accept slower iterations

---

## Success Metrics

### Phase 1 Success
- ✅ Image editing workflow functional (some approach)
- ✅ Can process 5 images in <10 minutes
- ✅ Character identity preserved in majority

### POC Success  
- ✅ One complete Flywheel 1 iteration (source → enriched → trained → synthetic → retrained)
- ✅ FLUX LoRA v2 measurably better than v1
- ✅ All steps documented and reproducible

---

## Next Actions (Right Now)

1. **Install dependencies** (30 min)
2. **Start Qwen-Image-Edit-2509 download** (background, 1-2 hours)
3. **Download dx8152 LoRA** (5 min)
4. **Create test scripts** (1 hour)
5. **Run comprehensive editing tests** (2 hours)
6. **Critical quality assessment** - is it good enough?
7. **Make LoRA training decision** based on findings

**Start with**: Dependencies installation and model downloads!
