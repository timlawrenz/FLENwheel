# ComfyUI Workflow Integration

This directory contains saved ComfyUI workflows in API format for volume generation.

## How to Save a Workflow from ComfyUI

1. **Load your workflow** in ComfyUI UI
2. **Click the gear icon** (⚙️) or Settings menu
3. **Select "Save (API Format)"** - NOT "Save Workflow"
4. Save to this directory: `workflows/qwen_edit_api.json`

### Why API Format?

- ✅ API format is JSON with node IDs and types
- ✅ Can be programmatically modified (change prompts, seeds, etc.)
- ✅ Works with ComfyUI REST API
- ❌ Workflow format (UI format) contains positions and UI metadata

## Available Workflows

### qwen_edit_api.json
**Qwen Image Edit workflow for creating training variations**

- Input: Source image
- Process: Text-guided image editing
- Output: Variation with same identity
- Speed: ~60 seconds per image (1024×1024)
- Steps: 4 (with Lightning LoRA)

**Node Requirements:**
- LoadImage
- TextEncodeQwenImageEdit / TextEncodeQwenImageEditPlus  
- UNETLoader (qwen_image_edit_2509_fp8_e4m3fn)
- VAELoader (qwen_image_vae)
- CLIPLoader (qwen_2.5_vl_7b_fp8_scaled)
- LoraLoader (Qwen-Image-Edit-2509-Lightning-4steps)
- KSampler
- SaveImage

## Usage

```python
from pathlib import Path
from lib.comfyui_client import ComfyUIClient
from lib.comfyui_workflow import QwenComfyUIWorkflow

# Connect to ComfyUI
client = ComfyUIClient(base_url="http://127.0.0.1:8188")

# Load workflow
workflow = QwenComfyUIWorkflow(
    workflow_path=Path("workflows/qwen_edit_api.json"),
    comfyui_client=client
)

# Generate variation
result = workflow.generate(
    source_image=Path("source.jpg"),
    prompt="professional headshot, slight smile, studio lighting",
    seed=42,
    steps=4
)

if result.success:
    print(f"✓ Generated: {result.output_path}")
    print(f"  Time: {result.duration_seconds:.1f}s")
```

## Troubleshooting

### "Could not find critical nodes"
- Make sure you saved in **API format**, not Workflow format
- Check that workflow contains required nodes (LoadImage, TextEncode, etc.)

### "No output images generated"  
- Verify workflow has SaveImage or PreviewImage node
- Check ComfyUI logs for errors

### "Connection refused"
- Make sure ComfyUI is running: `http://127.0.0.1:8188`
- Check firewall settings
