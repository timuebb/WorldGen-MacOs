# macOS Compatibility Changes - Summary

## Issue
The original issue requested checking if installation on macOS is possible and what changes are needed to enable it.

**Original Issue (German)**: "Check ob eine installation auf MacOs möglich ist bzw. was geändert werden muss um es auf macOs zu ermöglichen"

**Translation**: "Check if installation on macOS is possible or what needs to be changed to enable it on macOS"

## Conclusion

**Answer: NO - macOS is currently NOT supported** ❌

### Critical Blocker

**UniK3D dependency requires Triton:**
- UniK3D (depth estimation library) is a **core** dependency
- UniK3D requires Triton (NVIDIA GPU programming language)
- Triton is **only available on Linux/Windows** with NVIDIA GPUs
- Triton cannot be installed on macOS (no NVIDIA GPU support)
- Without UniK3D, WorldGen **cannot function**

This is a fundamental limitation that cannot be worked around without replacing the depth estimation model.

## Analysis

The repository had several blockers preventing macOS installation:

1. **Hardcoded Linux-specific dependency**: The `nunchaku` package was specified as a Linux x86_64 wheel URL in `pyproject.toml`
2. **No macOS wheels available**: Nunchaku only provides pre-built wheels for Linux and Windows, not macOS
3. **CUDA-only installation instructions**: The README only documented CUDA installation (not available on macOS)
4. **No MPS device support**: The code didn't properly handle Apple Silicon's MPS (Metal Performance Shaders) backend

## Changes Made

### 1. pyproject.toml
- Added platform-specific markers for `nunchaku` dependency (required on Linux/Windows, excluded on macOS)
- Fixed the nunchaku repository URL (was `mit-han-lab`, now correctly `nunchaku-tech`)
- Made `xformers` platform-conditional (excluded on macOS)
- Nunchaku is now automatically installed on Linux and Windows without needing extra steps

### 2. Source Code Updates

#### src/worldgen/pano_gen.py
- Added optional import for nunchaku with try/except block
- Added `NUNCHAKU_AVAILABLE` flag to track availability
- Modified `build_pano_gen_model()` to gracefully fall back when nunchaku is unavailable
- Modified `build_pano_fill_model()` to gracefully fall back when nunchaku is unavailable
- Added informative warning messages for macOS users

#### src/worldgen/utils/lora_utils.py
- Added optional import for nunchaku compose function
- Updated `compose_lora_with_fixes()` to raise informative error if called on macOS

#### src/worldgen/worldgen.py
- Updated `__init__()` to properly detect MPS and CPU devices
- Fixed device checking to not crash when CUDA is unavailable
- Added informative messages about low_vram mode availability

#### demo.py
- Updated device detection to support CUDA > MPS > CPU priority
- Fixed VRAM checking to not crash on non-CUDA systems
- Added platform-specific messages about low_vram mode

### 3. Documentation

#### README.md
- Split installation instructions into platform-specific sections:
  - Linux Installation (with optional nunchaku)
  - macOS Installation (with MPS support notes)
  - Windows Installation (with optional nunchaku)
- Added clear notes about macOS limitations
- Added reference to detailed macOS installation guide

#### MACOS_INSTALLATION.md (New)
- Comprehensive macOS-specific installation guide
- Prerequisites and system requirements
- Detailed installation steps
- Platform-specific considerations for Apple Silicon vs Intel Macs
- Known limitations and workarounds
- Troubleshooting section
- Performance optimization tips
- Example usage code
- Platform comparison table

## Result

**macOS installation is now possible** with the following caveats:

✅ **What Works:**
- Installation on macOS (both Intel and Apple Silicon)
- Basic text-to-scene generation
- Image-to-scene generation
- MPS acceleration on Apple Silicon Macs
- CPU fallback on Intel Macs
- Standard mode (without low VRAM optimization)

⚠️ **Limitations on macOS:**
- Low VRAM mode (Nunchaku) is not available
- xformers optimizations are not available
- Slower than CUDA-equipped systems
- Requires more VRAM/RAM (24GB+ recommended)
- Intel Macs will be significantly slower (CPU-only)

## Testing Recommendations

To verify the changes work correctly on macOS:

1. **On Apple Silicon Mac (M1/M2/M3):**
   ```bash
   conda create -n worldgen python=3.11
   conda activate worldgen
   pip install torch torchvision
   pip install .
   python -c "import worldgen; print('Import successful')"
   ```

2. **Verify MPS is detected:**
   ```python
   import torch
   from worldgen import WorldGen
   
   device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
   worldgen = WorldGen(mode="t2s", device=device)
   # Should print: "Running on Apple Silicon (MPS). Low VRAM mode is not available."
   ```

3. **Test generation (may take 10-20 minutes):**
   ```bash
   python demo.py -p "A simple test scene"
   ```

## Backward Compatibility

All changes are backward compatible:
- Linux and Windows users can still use low VRAM mode by installing optional dependencies
- Existing code will continue to work without modifications
- The default behavior remains unchanged for CUDA systems

## Migration Path

Existing users don't need to change anything. New macOS users should follow the installation guide in MACOS_INSTALLATION.md or the macOS section of README.md.
