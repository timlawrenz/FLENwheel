# Qwen Ecosystem Model Survey Results

**Date**: 2025-11-16  
**Task**: 1.1 - Hugging Face Model Discovery  
**Status**: ✓ Complete

## Models Discovered: 17 Total

### HIGH PRIORITY - Character Consistency

#### 1. YaoJiefu/multiple-characters
- **Specialty**: Multiple characters, any angle generation
- **Relevance**: ⭐⭐⭐⭐⭐ CRITICAL - Multi-angle character generation
- **Use Case**: Generate characters that fit scene from almost any angle
- **Notes**: Can generate MULTIPLE characters - huge for our use case
- **Link**: https://huggingface.co/YaoJiefu/multiple-characters

#### 2. dx8152/Qwen-Edit-2509-Multiple-angles
- **Specialty**: Camera angle control (up/down/left/right/rotate)
- **Relevance**: ⭐⭐⭐⭐⭐ CRITICAL - Already identified, now with update
- **Use Case**: Control camera movement and rotation, wide-angle/close-up
- **Notes**: UPDATED 2025/11/2 for consistency fix. Requires lightx2v/Qwen-Image-Lightning
- **Link**: https://huggingface.co/dx8152/Qwen-Edit-2509-Multiple-angles
- **Dependency**: https://huggingface.co/lightx2v/Qwen-Image-Lightning/tree/main

#### 3. TsienDragon/qwen-image-edit-lora-face-segmentation
- **Specialty**: Face segmentation masks
- **Relevance**: ⭐⭐⭐⭐⭐ CRITICAL - Identity verification
- **Use Case**: Transform facial images to precise segmentation masks
- **Notes**: Based on Qwen-VL, PEFT with LoRA
- **Link**: https://huggingface.co/TsienDragon/qwen-image-edit-lora-face-segmentation

#### 4. TsienDragon/qwen-image-edit-character-composition
- **Specialty**: Face segmentation (Flux-Kontext architecture)
- **Relevance**: ⭐⭐⭐⭐ HIGH - Alternative face segmentation
- **Use Case**: Precise face segmentation masks
- **Notes**: Different architecture than above, compare both
- **Link**: https://huggingface.co/TsienDragon/qwen-image-edit-character-composition

### HIGH PRIORITY - Lighting Control

#### 5. djessica/QE-2509-Relight
- **Specialty**: Removes lighting, creates neutral portraits
- **Relevance**: ⭐⭐⭐⭐⭐ CRITICAL - Lighting normalization
- **Use Case**: Make portraits neutral before enrichment
- **Notes**: Could be used as preprocessing step
- **Link**: https://huggingface.co/djessica/QE-2509-Relight

#### 6. dx8152/Qwen-Edit-2509-Multi-Angle-Lighting
- **Specialty**: Directional lighting control (8 directions + above/below)
- **Relevance**: ⭐⭐⭐⭐⭐ CRITICAL - Precise lighting control
- **Use Case**: Relight with specific source direction
- **Prompt**: "Relight Figure 1 using luminance map from Figure 2 (light source from [direction])"
- **Directions**: Front, Left Front, Left, Left Rear, Rear, Right Rear, Right, Right Front, Above, Below
- **Link**: https://huggingface.co/dx8152/Qwen-Edit-2509-Multi-Angle-Lighting

#### 7. dx8152/Qwen-Image-Edit-2509-Relight
- **Specialty**: Another lighting neutralizer
- **Relevance**: ⭐⭐⭐⭐ HIGH - Compare to djessica's version
- **Use Case**: Remove light effects from images
- **Notes**: Similar to djessica/QE-2509-Relight, test both
- **Link**: https://huggingface.co/dx8152/Qwen-Image-Edit-2509-Relight

### MEDIUM PRIORITY - Scene Composition

#### 8. dx8152/Qwen-Image-Edit-2509-White_to_Scene
- **Specialty**: Generate scene around isolated object
- **Relevance**: ⭐⭐⭐ MEDIUM - Background enrichment
- **Use Case**: Fill white space with full scene
- **Notes**: Could be useful for background diversity
- **Link**: https://huggingface.co/dx8152/Qwen-Image-Edit-2509-White_to_Scene

#### 9. valiantcat/Qwen-Image-Edit-MeiTu
- **Specialty**: General finetune for cinematic/professional photos
- **Relevance**: ⭐⭐⭐ MEDIUM - Quality enhancement
- **Use Case**: Make photos more cinematic/professional
- **Notes**: Could improve overall aesthetic
- **Link**: https://huggingface.co/valiantcat/Qwen-Image-Edit-MeiTu

#### 10. lovis93/next-scene-qwen-image-lora-2509
- **Specialty**: Cinematic image sequences, visual progression
- **Relevance**: ⭐⭐ LOW - Interesting but not core need
- **Use Case**: Generate shots that flow into each other
- **Notes**: More for video/sequence work
- **Link**: https://huggingface.co/lovis93/next-scene-qwen-image-lora-2509

### LOW PRIORITY - Specialized Tools

#### 11. InstantX/Qwen-Image-ControlNet-Inpainting
- **Specialty**: Mask-based inpainting/outpainting
- **Relevance**: ⭐⭐⭐ MEDIUM - Precise editing
- **Use Case**: Mask-based image editing
- **Notes**: ControlNet, not LoRA - different usage pattern
- **Link**: https://huggingface.co/InstantX/Qwen-Image-ControlNet-Inpainting

#### 12. InstantX/Qwen-Image-ControlNet-Union
- **Specialty**: ControlNet including OpenPose
- **Relevance**: ⭐⭐⭐ MEDIUM - Pose control
- **Use Case**: Control pose with OpenPose
- **Notes**: ControlNet for body pose control
- **Link**: https://huggingface.co/InstantX/Qwen-Image-ControlNet-Union

#### 13. starsfriday/Qwen-Image-Edit-Remover-General-LoRA
- **Specialty**: Object removal, maintains consistency
- **Relevance**: ⭐⭐ LOW - Not core need
- **Use Case**: Remove objects from images
- **Notes**: For ComfyUI, maintains original image consistency
- **Link**: https://huggingface.co/starsfriday/Qwen-Image-Edit-Remover-General-LoRA

#### 14. tarn59/extract_texture_qwen_image_edit_2509
- **Specialty**: Extract textures from objects
- **Relevance**: ⭐ VERY LOW - Not relevant
- **Use Case**: Extract texture patterns
- **Link**: https://huggingface.co/tarn59/extract_texture_qwen_image_edit_2509

#### 15. tarn59/apply_texture_qwen_image_edit_2509
- **Specialty**: Apply textures to objects
- **Relevance**: ⭐ VERY LOW - Not relevant
- **Use Case**: Force similar style via textures
- **Link**: https://huggingface.co/tarn59/apply_texture_qwen_image_edit_2509

#### 16. chestnutlzj/Edit-R1-Qwen-Image-Edit-2509
- **Specialty**: Unknown - needs investigation
- **Relevance**: ❓ UNKNOWN
- **Use Case**: TBD
- **Notes**: Unclear from description
- **Link**: https://huggingface.co/chestnutlzj/Edit-R1-Qwen-Image-Edit-2509

## Summary Statistics

- **Total Models Found**: 17
- **HIGH Priority (⭐⭐⭐⭐⭐)**: 7 models
- **MEDIUM Priority (⭐⭐⭐-⭐⭐⭐⭐)**: 5 models  
- **LOW Priority (⭐-⭐⭐)**: 4 models
- **Unknown**: 1 model

## Priority Categories for Testing

### MUST TEST (Top 5)
1. **YaoJiefu/multiple-characters** - Multi-character, multi-angle (game changer!)
2. **dx8152/Qwen-Edit-2509-Multiple-angles** - Updated version with consistency fix
3. **TsienDragon/qwen-image-edit-lora-face-segmentation** - Face segmentation for identity
4. **djessica/QE-2509-Relight** - Lighting neutralization
5. **dx8152/Qwen-Edit-2509-Multi-Angle-Lighting** - Directional lighting control

### SHOULD TEST (Next 5)
6. **dx8152/Qwen-Image-Edit-2509-Relight** - Alternative lighting neutralizer
7. **TsienDragon/qwen-image-edit-character-composition** - Alternative face segmentation
8. **valiantcat/Qwen-Image-Edit-MeiTu** - Quality enhancement
9. **InstantX/Qwen-Image-ControlNet-Inpainting** - Precise editing
10. **InstantX/Qwen-Image-ControlNet-Union** - Pose control

## Key Findings

### Game Changers
- **YaoJiefu/multiple-characters**: Can generate MULTIPLE characters from any angle - this is HUGE if it works well
- **Face Segmentation Models**: Two options for automated identity verification
- **Lighting Suite**: Multiple lighting control options (neutralize, directional relight)
- **Updated dx8152**: Consistency fix in latest version (2025/11/2)

### Ecosystem Patterns
- Many models from **dx8152** (4 models) - active developer
- Multiple approaches to same problem (2x relight, 2x face-seg) - can compare
- Mix of LoRAs and ControlNets - different usage patterns
- Some models have dependencies (dx8152 angles needs lightx2v/Qwen-Image-Lightning)

### Dependencies Discovered
- **dx8152/Qwen-Edit-2509-Multiple-angles** requires:
  - lightx2v/Qwen-Image-Lightning (https://huggingface.co/lightx2v/Qwen-Image-Lightning/tree/main)

## Next Steps (Task 1.2)

Detailed model card review for top 10 models:
- Extract training methodology
- Document dataset sizes
- Review example images
- Assess quality claims
- Note any reported issues
- Check download sizes

## Notes

- **Critical Discovery**: YaoJiefu/multiple-characters could be game-changing for character consistency
- **Updated Model**: dx8152 angle LoRA has consistency fix (test new version)
- **Ecosystem Maturity**: 17 specialized models shows very active community
- **Strategic Implication**: May not need custom training at all with this many options!

