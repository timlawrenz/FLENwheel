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

### Step 2: Download Qwen2-VL Model (1-2 hours)

**Decision Point**: Which model?
- **Option A**: Qwen2-VL-2B-Instruct (~4GB, faster, lower quality)
- **Option B**: Qwen2-VL-7B-Instruct (~15GB, slower, higher quality)

**Recommendation**: Start with 2B for quick validation, upgrade to 7B if quality insufficient

```bash
# Download 2B model
huggingface-cli download Qwen/Qwen2-VL-2B-Instruct

# Or download 7B model
huggingface-cli download Qwen/Qwen2-VL-7B-Instruct
```

**Storage check**:
```bash
df -h ~/.cache/huggingface  # Make sure you have 20GB+ free
```

### Step 3: Create Basic Inference Test (1 hour)

Create `scripts/test_qwen_basic.py`:

```python
#!/usr/bin/env python3
"""Test Qwen-VL basic inference"""

import torch
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
from PIL import Image

def test_qwen_inference():
    # Model selection
    model_name = "Qwen/Qwen2-VL-2B-Instruct"  # or 7B
    
    print(f"Loading model: {model_name}")
    
    # Load with 4-bit quantization
    model = Qwen2VLForConditionalGeneration.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto",
        load_in_4bit=True
    )
    
    processor = AutoProcessor.from_pretrained(model_name)
    
    print("Model loaded successfully!")
    print(f"VRAM usage: {torch.cuda.memory_allocated() / 1e9:.2f} GB")
    
    # Test with a simple image
    test_image_path = "test_data/sample.jpg"  # You'll need to provide this
    
    # Simple description test
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": test_image_path},
                {"type": "text", "text": "Describe this image."}
            ]
        }
    ]
    
    text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = processor(text=[text], images=[Image.open(test_image_path)], return_tensors="pt")
    inputs = inputs.to("cuda")
    
    print("Generating response...")
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=128)
    
    response = processor.batch_decode(outputs, skip_special_tokens=True)[0]
    print(f"\nResponse: {response}")
    
    return model, processor

if __name__ == "__main__":
    model, processor = test_qwen_inference()
```

**Run it**:
```bash
python scripts/test_qwen_basic.py
```

**Success criteria**:
- ✅ Model loads without errors
- ✅ VRAM usage < 20GB
- ✅ Generates coherent description

### Step 4: Test Image Editing (1 hour)

Create `scripts/test_qwen_editing.py`:

```python
#!/usr/bin/env python3
"""Test Qwen-VL image editing capabilities"""

import torch
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
from PIL import Image

def test_editing_prompts(model, processor, test_image_path):
    """Test various editing prompts"""
    
    editing_prompts = [
        "Change the background to a forest, keep everything else the same.",
        "Make the lighting look like sunset, keep the subject identical.",
        "Convert this to an oil painting style, preserve the person's features exactly.",
        "Change camera angle to slightly left view, maintain character appearance.",
    ]
    
    for i, prompt in enumerate(editing_prompts):
        print(f"\n--- Test {i+1}: {prompt[:50]}... ---")
        
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": test_image_path},
                    {"type": "text", "text": prompt}
                ]
            }
        ]
        
        text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = processor(text=[text], images=[Image.open(test_image_path)], return_tensors="pt")
        inputs = inputs.to("cuda")
        
        # Note: Qwen2-VL primarily does vision understanding, not image generation
        # For actual image editing, we may need to use a different approach
        # This is a critical discovery step!
        
        with torch.no_grad():
            outputs = model.generate(**inputs, max_new_tokens=256)
        
        response = processor.batch_decode(outputs, skip_special_tokens=True)[0]
        print(f"Response: {response}")

if __name__ == "__main__":
    from test_qwen_basic import test_qwen_inference
    
    model, processor = test_qwen_inference()
    test_editing_prompts(model, processor, "test_data/sample.jpg")
```

**CRITICAL DISCOVERY POINT**: 
Qwen2-VL is primarily a **vision-language understanding** model, not an image **generation** model!

For actual image editing, we may need:
- **Option A**: Use Qwen2-VL to generate detailed descriptions, then feed to FLUX
- **Option B**: Use InstructPix2Pix or similar editing model
- **Option C**: Use Qwen-VL-Chat API which may have editing capabilities
- **Option D**: Rethink architecture: use Qwen2-VL for validation/captioning instead of editing

**This is a blocker that needs resolution!**

### Step 5: Research & Decision (2 hours)

Research actual image editing approaches:

1. **Check Qwen2-VL documentation**: Does it support image editing at all?
2. **Check Qwen-VL-Max API**: Is that the editing-capable version?
3. **Alternative models**:
   - InstructPix2Pix
   - SDXL-Turbo with ControlNet
   - DALL-E 3 API (external)
   - Stable Diffusion Inpainting

**Decision needed**: What editing approach to use?

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

### 1. Image Editing Approach
**Question**: How do we actually edit images while preserving character identity?

**Options**:
- A) Qwen2-VL + FLUX (generate descriptions, then new images)
- B) Different editing model (InstructPix2Pix, etc.)
- C) API-based solution (Qwen-VL-Max, DALL-E, etc.)
- D) Hybrid approach

**Impact**: High - affects entire architecture

**Decision by**: End of Phase 1

### 2. Model Sizes
**Question**: Qwen 2B vs 7B? FLUX schnell vs dev?

**Impact**: Medium - affects speed vs quality

**Decision by**: After initial testing

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
1. ⚠️ **CRITICAL**: Qwen2-VL may not do image editing directly
   - **Mitigation**: Research alternatives TODAY

2. ⚠️ Model download time (1-2 hours)
   - **Mitigation**: Start download early, work on other tasks

3. ⚠️ Disk space (need 50GB+ free)
   - **Mitigation**: Check now, clean up if needed

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
2. **Start Qwen2-VL-2B download** (background)
3. **Create test_qwen_basic.py** (1 hour)
4. **Research Qwen2-VL editing capabilities** (critical!)
5. **Make architecture decision** based on findings

**Start with**: Dependencies installation and model download!
