# FLENwheel Documentation

## Start Here

**New to the project?** Read in this order:

1. **[SUMMARY.md](SUMMARY.md)** - Quick overview, current status, immediate next steps
2. **[brainstorming.md](brainstorming.md)** - Original concept and detailed workflow explanation
3. **[technical-feasibility.md](technical-feasibility.md)** - Detailed technical analysis
4. **[quick-start.md](quick-start.md)** - Step-by-step validation guide
5. **[process-flow.md](process-flow.md)** - Complete dual-flywheel process documentation

## Document Purposes

### SUMMARY.md
**What**: High-level project overview  
**When to read**: First time, or when returning after time away  
**Contains**: Current status, decisions needed, file organization, next steps

### brainstorming.md
**What**: Original concept exploration and detailed design  
**When to read**: To understand the "why" behind the architecture  
**Contains**: Dual-flywheel concept, HITL philosophy, model card goals

### basic-process.td
**What**: Visual diagram of the dual-flywheel process  
**When to read**: To visualize the workflow  
**Format**: Mermaid diagram (view in GitHub or compatible editor)

### technical-feasibility.md
**What**: Detailed technical analysis and risk assessment  
**When to read**: Before starting implementation, when troubleshooting  
**Contains**: 
- VRAM estimates and model sizes
- Training feasibility analysis
- Dependencies and libraries needed
- Validation phases and success criteria
- Risk mitigation strategies

### quick-start.md
**What**: Hands-on getting started guide  
**When to read**: When ready to start coding  
**Contains**:
- Installation commands
- Test scripts with code examples
- Expected timeline (day-by-day)
- Immediate blockers and mitigations

### process-flow.md
**What**: Authoritative reference for each step in both flywheels  
**When to read**: During implementation, when documenting procedures  
**Contains**:
- Step-by-step procedures for all 8 flywheel steps
- Input/output requirements
- Success criteria for each step
- Model card specifications
- Dependencies between steps

## Quick Reference

### Current Status
- ✅ Documentation complete
- ✅ Architecture defined
- ✅ Correct models identified
- ❓ Qwen-Image-Edit-2509 not yet validated
- ❓ Base model quality unknown
- 📅 Week 1: Validation phase (5-7 hours)

### Models to Download
- `Qwen/Qwen-Image-Edit-2509` (~14GB)
- `dx8152/Qwen-Edit-2509-Multiple-angles` (~100-500MB)
- FLUX.1-dev (already have via ai-toolkit)

### Critical Questions
1. Is base Qwen-Image-Edit-2509 good enough?
2. Does dx8152 LoRA improve quality sufficiently?
3. Do we need custom LoRA from day 1?

### Next Physical Steps
```bash
# 1. Set up environment
python3 -m venv venv
source venv/bin/activate
pip install torch torchvision diffusers transformers accelerate bitsandbytes pillow opencv-python

# 2. Download models
huggingface-cli download Qwen/Qwen-Image-Edit-2509
huggingface-cli download dx8152/Qwen-Edit-2509-Multiple-angles

# 3. Create test scripts (see quick-start.md)
# 4. Run validation tests
# 5. Assess quality and make decisions
```

## Document History

- **2025-11-16**: Initial documentation created
  - Established dual-flywheel architecture
  - Identified correct Qwen-Image-Edit models (vs Qwen2-VL)
  - Defined model card requirements (23 images)
  - Created comprehensive validation plan

## Contributing

When updating documentation:
1. Keep SUMMARY.md current with latest status
2. Update technical-feasibility.md with new findings
3. Adjust quick-start.md if procedures change
4. Keep process-flow.md as authoritative reference
5. Document decisions and rationale
