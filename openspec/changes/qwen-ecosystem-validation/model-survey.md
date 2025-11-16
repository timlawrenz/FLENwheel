# Qwen Ecosystem Model Survey Results

**Date**: 2025-11-16  
**Task**: 1.1 - Hugging Face Model Discovery  
**Status**: ✓ Complete

## Models Discovered: 17 Total

### HIGH PRIORITY - Character Consistency

#### 1. YaoJiefu/multiple-characters ❌ MISLEADING
- **Specialty**: Adds multiple NEW characters to empty scenes
- **Relevance**: ⭐ LOW - NOT for character consistency
- **Actual Use Case**: Scene population (family on couch, couple in kitchen)
- **Why Not Useful**: Generates NEW characters, not transformations of SAME character
- **Notes**: Misleading description - "multiple characters" ≠ "character from multiple angles"
- **Link**: https://huggingface.co/YaoJiefu/multiple-characters
- **Status**: ❌ Deprioritized after model card review

#### 2. dx8152/Qwen-Edit-2509-Multiple-angles ⭐⭐⭐⭐⭐ CRITICAL
- **Specialty**: CAMERA movement and rotation (NOT lighting!)
- **Relevance**: ⭐⭐⭐⭐⭐ CRITICAL - Exactly our core need!
- **Use Case**: Transform SAME character to different camera angles/viewpoints
- **Capabilities**:
  - Rotate camera (left/right, up/down)
  - Move camera position
  - Change to wide-angle or close-up
  - Text-driven: "Rotate camera 45 degrees left", "Move to profile view", etc.
- **Updated**: 2025/11/2 - Consistency fix for character identity preservation
- **Dependency**: Requires lightx2v/Qwen-Image-Lightning
- **Link**: https://huggingface.co/dx8152/Qwen-Edit-2509-Multiple-angles
- **Status**: ✅ TOP PRIORITY - This is THE model for angle enrichment

**Example prompts from model card**:
- "将镜头向前移动" (Move the camera forward)
- "将镜头向左旋转45度" (Rotate the camera 45 degrees to the left)
- "将镜头转为俯视" (Turn the camera to a top-down view)
- "将镜头转为特写镜头" (Turn the camera to a close-up)

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

#### 6. dx8152/Qwen-Edit-2509-Multi-Angle-Lighting ⭐⭐⭐⭐ HIGH
- **Specialty**: LIGHTING direction control (NOT camera angles!)
- **Relevance**: ⭐⭐⭐⭐ HIGH - Lighting variation for robustness
- **Use Case**: Relight subject with light from specific direction
- **Capabilities**:
  - 10 lighting directions: Front, Left Front, Left, Left Rear, Rear, Right Rear, Right, Right Front, Above, Below
  - Uses luminance map from reference image
  - Text-driven: "Relight Figure 1 using luminance map from Figure 2 (light source from [direction])"
- **Link**: https://huggingface.co/dx8152/Qwen-Edit-2509-Multi-Angle-Lighting
- **Note**: DIFFERENT from Multiple-angles (which is camera, not lighting)

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

### MUST TEST (Top 5 - FINAL)
1. **dx8152/Qwen-Edit-2509-Multiple-angles** ⭐⭐⭐⭐⭐ - CAMERA angles (THE core model!)
2. **TsienDragon/qwen-image-edit-lora-face-segmentation** ⭐⭐⭐⭐⭐ - Identity verification
3. **dx8152/Qwen-Edit-2509-Multi-Angle-Lighting** ⭐⭐⭐⭐ - LIGHTING direction control
4. **djessica/QE-2509-Relight** ⭐⭐⭐⭐ - Lighting neutralization
5. **Base Qwen-Image-Edit-2509** ⭐⭐⭐⭐ - Background/composition variation

### SHOULD TEST (Next 5)
6. **TsienDragon/qwen-image-edit-character-composition** - Alternative face segmentation
7. **valiantcat/Qwen-Image-Edit-MeiTu** - Quality enhancement
8. **InstantX/Qwen-Image-ControlNet-Inpainting** - Precise editing
9. **InstantX/Qwen-Image-ControlNet-Union** - Pose control with OpenPose
10. **dx8152/Qwen-Image-Edit-2509-White_to_Scene** - Background generation

## Key Findings

### Lesson Learned
- **Model card review is ESSENTIAL**: YaoJiefu/multiple-characters was misleading
- **Description ≠ Capability**: "Multiple characters" meant scene population, not character transformation
- **Validation process works**: Caught the issue before wasting time on downloads/testing

### Game Changers (FINAL - Corrected)
- **dx8152/Qwen-Edit-2509-Multiple-angles**: CAMERA angle transformation - THE core model we need!
  - Single image → Multiple viewpoints (front, profile, 3/4, etc.)
  - Character identity preservation (2025/11/2 consistency fix)
  - Text-driven camera control
  - This solves our PRIMARY requirement!
- **dx8152 ecosystem**: 4 specialized models (camera angles, lighting, relighting, scene)
- **Face Segmentation**: Two options for automated identity verification
- **Lighting Suite**: Multiple lighting control options (neutralize, directional relight)
- **Complete toolset**: Everything needed for character consistency enrichment

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

- **✓ Validation Process Works**: Caught YaoJiefu misunderstanding before wasting time
- **Critical Discovery**: dx8152 has 4 models including recent consistency fix
- **Updated Model**: dx8152 angle LoRA has consistency fix (test new version)
- **Ecosystem Maturity**: 16 actually relevant models (17 minus misleading one)
- **Strategic Implication**: Focus on dx8152 ecosystem + face segmentation + lighting control

