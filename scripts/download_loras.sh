#!/bin/bash
# Download Qwen-Edit LoRAs to ComfyUI directory
# Created: 2025-11-16

set -e

LORA_DIR="/mnt/essdee/ComfyUI/models/loras/qwen-image-edit"
mkdir -p "$LORA_DIR"

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║      Downloading Qwen-Edit LoRAs to ComfyUI                   ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "Target directory: $LORA_DIR"
echo ""

# Activate venv
cd /home/tim/source/activity/FLENwheel
source venv/bin/activate

# Download dx8152/Qwen-Edit-2509-Multiple-angles (THE CRITICAL ONE!)
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1/3: dx8152/Qwen-Edit-2509-Multiple-angles (CAMERA angles)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
huggingface-cli download dx8152/Qwen-Edit-2509-Multiple-angles \
    --local-dir "$LORA_DIR/multiple-angles" \
    --local-dir-use-symlinks False

# Download dx8152/Qwen-Edit-2509-Multi-Angle-Lighting
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2/3: dx8152/Qwen-Edit-2509-Multi-Angle-Lighting (LIGHTING)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
huggingface-cli download dx8152/Qwen-Edit-2509-Multi-Angle-Lighting \
    --local-dir "$LORA_DIR/multi-angle-lighting" \
    --local-dir-use-symlinks False

# Download TsienDragon/qwen-image-edit-lora-face-segmentation
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3/3: TsienDragon/face-segmentation (IDENTITY verification)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
huggingface-cli download TsienDragon/qwen-image-edit-lora-face-segmentation \
    --local-dir "$LORA_DIR/face-segmentation" \
    --local-dir-use-symlinks False

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ ALL LORAS DOWNLOADED!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
ls -lh "$LORA_DIR"
echo ""
echo "Next step: Test dx8152/Multiple-angles with Python scripts!"
