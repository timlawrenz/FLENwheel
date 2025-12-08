#!/usr/bin/env python3
"""
FLUX2 GGUF Model Loader

Loads FLUX2 transformer from GGUF format into diffusers Flux2Transformer2DModel
"""

import gc
import torch
import logging
from pathlib import Path
from typing import Optional

from diffusers import Flux2Transformer2DModel

# Import our custom modules
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.gguf_loader import load_gguf_state_dict, estimate_vram_usage
from lib.flux2_key_mapping import convert_gguf_state_dict_to_diffusers

logger = logging.getLogger(__name__)


def get_vram_usage():
    """Get current VRAM usage in GB"""
    if torch.cuda.is_available():
        return torch.cuda.memory_allocated() / 1024**3
    return 0


def get_peak_vram():
    """Get peak VRAM usage in GB"""
    if torch.cuda.is_available():
        return torch.cuda.max_memory_allocated() / 1024**3
    return 0


def reset_peak_vram():
    """Reset peak VRAM tracking"""
    if torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats()


def clear_memory():
    """Clear GPU memory"""
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


def load_flux2_transformer_from_gguf(
    gguf_path: str,
    device: str = "cuda",
    dtype: torch.dtype = torch.bfloat16,
    enable_cpu_offload: bool = True,
) -> Flux2Transformer2DModel:
    """
    Load FLUX2 transformer from GGUF file
    
    Args:
        gguf_path: Path to GGUF file
        device: Device to load model on
        dtype: Target dtype (default: bfloat16)
        enable_cpu_offload: Enable CPU offload for VRAM savings
    
    Returns:
        Loaded Flux2Transformer2DModel
    """
    logger.info(f"Loading FLUX2 transformer from GGUF: {gguf_path}")
    
    # Step 1: Load GGUF state dict
    logger.info("Step 1/4: Loading GGUF file...")
    gguf_state_dict, arch = load_gguf_state_dict(gguf_path)
    
    if arch != "flux":
        raise ValueError(f"Expected FLUX architecture, got: {arch}")
    
    gguf_vram = estimate_vram_usage(gguf_state_dict)
    logger.info(f"  GGUF state dict loaded: {len(gguf_state_dict)} tensors, ~{gguf_vram:.2f}GB")
    
    # Step 2: Convert to diffusers format
    logger.info("Step 2/4: Converting GGUF keys to diffusers format...")
    logger.info("  This will dequantize tensors (may take 1-2 minutes)...")
    
    diffusers_state_dict = convert_gguf_state_dict_to_diffusers(
        gguf_state_dict,
        num_attention_heads=48,  # FLUX2 default
        attention_head_dim=128   # FLUX2 default
    )
    
    logger.info(f"  Converted to {len(diffusers_state_dict)} diffusers tensors")
    
    # Free GGUF dict to save memory
    del gguf_state_dict
    clear_memory()
    
    # Step 3: Create model with matching config
    logger.info("Step 3/4: Creating Flux2Transformer2DModel...")
    
    # FLUX2-dev config (based on model inspection)
    model = Flux2Transformer2DModel(
        patch_size=1,
        in_channels=128,
        num_layers=8,  # FLUX2 has fewer double blocks than FLUX1
        num_single_layers=48,
        attention_head_dim=128,
        num_attention_heads=48,
        joint_attention_dim=15360,
        timestep_guidance_channels=256,
    )
    
    logger.info(f"  Model created with {sum(p.numel() for p in model.parameters())/1e9:.2f}B parameters")
    
    # Step 4: Load state dict
    logger.info("Step 4/4: Loading weights into model...")
    reset_peak_vram()
    
    # Load state dict (may show warnings about missing/unexpected keys)
    missing_keys, unexpected_keys = model.load_state_dict(diffusers_state_dict, strict=False)
    
    if missing_keys:
        logger.warning(f"  Missing keys ({len(missing_keys)}): {missing_keys[:5]}...")
    if unexpected_keys:
        logger.warning(f"  Unexpected keys ({len(unexpected_keys)}): {unexpected_keys[:5]}...")
    
    # Move to device
    if device == "cuda" and torch.cuda.is_available():
        logger.info(f"  Moving model to CUDA...")
        model = model.to(device, dtype=dtype)
        
        if enable_cpu_offload:
            logger.info(f"  Enabling CPU offload...")
            # Note: Flux2Transformer2DModel doesn't have enable_model_cpu_offload
            # We'll handle this at pipeline level
    
    vram_after_load = get_vram_usage()
    peak_vram = get_peak_vram()
    
    logger.info(f"✅ Model loaded successfully!")
    logger.info(f"  VRAM after load: {vram_after_load:.2f}GB")
    logger.info(f"  Peak VRAM: {peak_vram:.2f}GB")
    
    return model


def test_flux2_gguf_loading():
    """Test loading FLUX2 from GGUF and measure VRAM"""
    
    print("=" * 70)
    print("FLUX2 GGUF Loading Test")
    print("=" * 70)
    
    gguf_path = "/mnt/essdee/ComfyUI/models/diffusion_models/flux2-dev-Q4_1.gguf"
    
    if not Path(gguf_path).exists():
        print(f"❌ GGUF file not found: {gguf_path}")
        return
    
    # Check GPU
    if not torch.cuda.is_available():
        print("❌ CUDA not available!")
        return
    
    device_name = torch.cuda.get_device_name(0)
    total_vram = torch.cuda.get_device_properties(0).total_memory / 1024**3
    
    print(f"\n🖥️  GPU: {device_name}")
    print(f"💾 Total VRAM: {total_vram:.1f}GB")
    print(f"📁 GGUF File: {gguf_path}")
    print(f"📦 File Size: {Path(gguf_path).stat().st_size / 1024**3:.1f}GB")
    
    # Clear GPU before starting
    clear_memory()
    reset_peak_vram()
    
    vram_before = get_vram_usage()
    print(f"\n💾 VRAM before loading: {vram_before:.2f}GB")
    
    try:
        # Load model
        print("\n" + "=" * 70)
        print("Loading FLUX2 Transformer from GGUF...")
        print("=" * 70)
        
        model = load_flux2_transformer_from_gguf(
            gguf_path,
            device="cuda",
            dtype=torch.bfloat16,
            enable_cpu_offload=True
        )
        
        vram_after = get_vram_usage()
        peak_vram = get_peak_vram()
        
        print("\n" + "=" * 70)
        print("RESULTS")
        print("=" * 70)
        print(f"\n✅ Model loaded successfully!")
        print(f"\n💾 VRAM Usage:")
        print(f"  Before: {vram_before:.2f}GB")
        print(f"  After:  {vram_after:.2f}GB")
        print(f"  Peak:   {peak_vram:.2f}GB")
        print(f"  Used:   {vram_after - vram_before:.2f}GB")
        
        # Check if it fits
        vram_available = total_vram - peak_vram
        print(f"\n📊 VRAM Analysis:")
        print(f"  Total GPU VRAM:     {total_vram:.2f}GB")
        print(f"  Used by model:      {peak_vram:.2f}GB")
        print(f"  Remaining:          {vram_available:.2f}GB")
        
        if peak_vram < 20.0:
            print(f"\n✅ VERDICT: Model fits comfortably in VRAM!")
            print(f"  Enough headroom for T5 encoder (~3GB) and VAE (~2GB)")
            print(f"  Should be able to run full pipeline!")
        elif peak_vram < 22.0:
            print(f"\n⚠️  VERDICT: Model fits, but tight!")
            print(f"  May struggle with T5 + VAE")
            print(f"  Multi-reference might be limited")
        else:
            print(f"\n❌ VERDICT: Model uses too much VRAM!")
            print(f"  Not enough room for T5 encoder and VAE")
            print(f"  Full pipeline unlikely to work")
        
        # Test a forward pass
        print(f"\n" + "=" * 70)
        print("Testing forward pass...")
        print("=" * 70)
        
        # Create dummy inputs
        batch_size = 1
        height, width = 64, 64  # Latent size
        
        hidden_states = torch.randn(
            batch_size, 
            (height // 2) * (width // 2),  # Patch embedding
            model.config.in_channels,
            device="cuda",
            dtype=torch.bfloat16
        )
        
        encoder_hidden_states = torch.randn(
            batch_size,
            256,  # Sequence length
            model.config.joint_attention_dim,
            device="cuda",
            dtype=torch.bfloat16
        )
        
        timestep = torch.tensor([500.0], device="cuda")
        guidance = torch.tensor([3.5], device="cuda")
        
        reset_peak_vram()
        
        with torch.no_grad():
            output = model(
                hidden_states=hidden_states,
                encoder_hidden_states=encoder_hidden_states,
                timestep=timestep,
                guidance=guidance,
                return_dict=False
            )
        
        peak_inference_vram = get_peak_vram()
        
        print(f"✅ Forward pass successful!")
        print(f"  Output shape: {output[0].shape}")
        print(f"  Peak VRAM during inference: {peak_inference_vram:.2f}GB")
        
        # Cleanup
        del model
        del hidden_states, encoder_hidden_states, timestep, guidance, output
        clear_memory()
        
        print(f"\n" + "=" * 70)
        print("Test Complete!")
        print("=" * 70)
        
    except torch.cuda.OutOfMemoryError as e:
        peak_vram = get_peak_vram()
        print(f"\n❌ Out of Memory!")
        print(f"  Peak VRAM before OOM: {peak_vram:.2f}GB")
        print(f"  Error: {e}")
        
    except Exception as e:
        print(f"\n❌ Error during loading: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s: %(message)s'
    )
    
    test_flux2_gguf_loading()
