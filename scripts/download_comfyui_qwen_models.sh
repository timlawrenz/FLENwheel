#!/bin/bash
# Download Qwen models for ComfyUI

set -e

MODELS_DIR="/mnt/essdee/ComfyUI/models"

echo "Downloading Qwen models for ComfyUI..."
echo "Target: $MODELS_DIR"
echo ""

# Create directories
mkdir -p "$MODELS_DIR"/{vae,text_encoders,diffusion_models,loras}

# 1. VAE (~160MB)
echo "1/4 Downloading VAE..."
wget -nc -P "$MODELS_DIR/vae/" \
  https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/vae/qwen_image_vae.safetensors

# 2. Text Encoder (~5GB FP8)
echo "2/4 Downloading Text Encoder (5GB)..."
wget -nc -P "$MODELS_DIR/text_encoders/" \
  https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors

# 3. Diffusion Model (~12GB FP8)
echo "3/4 Downloading Diffusion Model (12GB)..."
wget -nc -P "$MODELS_DIR/diffusion_models/" \
  https://huggingface.co/Comfy-Org/Qwen-Image-Edit_ComfyUI/resolve/main/split_files/diffusion_models/qwen_image_edit_2509_fp8_e4m3fn.safetensors

# 4. Lightning LoRA (~13GB)
echo "4/4 Downloading Lightning LoRA (13GB)..."
wget -nc -P "$MODELS_DIR/loras/" \
  https://huggingface.co/lightx2v/Qwen-Image-Lightning/resolve/main/Qwen-Image-Edit-2509/Qwen-Image-Edit-2509-Lightning-4steps-V1.0-bf16.safetensors

echo ""
echo "✓ All models downloaded!"
echo ""
echo "Models installed in:"
ls -lh "$MODELS_DIR/vae/"qwen*.safetensors
ls -lh "$MODELS_DIR/text_encoders/"qwen*.safetensors
ls -lh "$MODELS_DIR/diffusion_models/"qwen*.safetensors
ls -lh "$MODELS_DIR/loras/"Qwen*.safetensors
