# macOS Installation Guide for WorldGen

This guide provides detailed instructions for installing and running WorldGen on macOS systems.

## Prerequisites

- macOS 10.15 (Catalina) or later
- Python 3.11 or later
- Conda or Miniconda installed
- For Apple Silicon Macs (M1/M2/M3/M4): macOS 12.3 or later for MPS support
- Sufficient disk space (at least 10GB for models and dependencies)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/ZiYang-xie/WorldGen.git
cd WorldGen
```

### 2. Create and Activate Conda Environment

```bash
# Create a new conda environment with Python 3.11
conda create -n worldgen python=3.11
conda activate worldgen
```

### 3. Install PyTorch

For macOS, install PyTorch without CUDA support:

```bash
# Important: Use 'pip' (not 'pip3') when inside a conda environment
pip install torch torchvision
```

This will automatically install the appropriate version for your system:
- **Apple Silicon (M1/M2/M3/M4)**: Includes MPS (Metal Performance Shaders) support for GPU acceleration
- **Intel-based Macs**: CPU-only version

> [!IMPORTANT]
> **Always use `pip` (not `pip3`) when inside a conda environment.** Using `pip3` may reference your system Python instead of the conda environment, causing installation errors on macOS.

### 4. Install WorldGen

```bash
pip install .
```

**Note**: The installation will automatically skip the `nunchaku` dependency on macOS, as it's not available for this platform.

## Platform-Specific Considerations

### Apple Silicon (M1/M2/M3/M4) Macs

✅ **Advantages:**
- Native MPS support for GPU acceleration
- Generally better performance than Intel Macs for ML tasks
- Lower power consumption

⚠️ **Limitations:**
- No low VRAM mode (Nunchaku is not available)
- Requires sufficient memory (16GB+ RAM recommended)
- Some operations may be slower than CUDA on NVIDIA GPUs

### Intel-based Macs

⚠️ **Limitations:**
- CPU-only processing (no GPU acceleration)
- Significantly slower than GPU-accelerated systems
- Not recommended for production use
- Requires patience for generation tasks

## Device Detection

WorldGen automatically detects the best available device:

1. **CUDA** (not available on macOS) - highest priority
2. **MPS** (Apple Silicon only) - second priority
3. **CPU** (fallback) - lowest priority

You can verify the device being used by checking the console output when initializing WorldGen.

## Known Limitations on macOS

### 1. Low VRAM Mode Not Available

The low VRAM feature (using Nunchaku) is **not available** on macOS because:
- Nunchaku only provides pre-built wheels for Linux and Windows
- The library uses platform-specific optimizations

**Impact**: You'll need more GPU memory (24GB+ recommended for Apple Silicon) or accept slower performance.

**Workaround**: Use a lower resolution setting to reduce memory requirements:
```python
worldgen = WorldGen(mode="t2s", resolution=1024)  # Instead of default 1600
```

### 2. xformers Not Available

The `xformers` library is not installed on macOS as it's primarily designed for CUDA. This may result in:
- Slightly slower attention computations
- Higher memory usage in some cases

### 3. Generation Speed

Expected generation times on different hardware:

| Hardware | Typical Generation Time |
|----------|------------------------|
| Apple M1 Max/Ultra (MPS) | 5-10 minutes |
| Apple M1/M2 (MPS) | 10-20 minutes |
| Intel Mac (CPU) | 30-60+ minutes |

## Troubleshooting

### Issue: "MPS backend out of memory"

**Solution**: Reduce the resolution or use CPU as fallback:
```python
worldgen = WorldGen(mode="t2s", device="cpu", resolution=1024)
```

### Issue: "No module named 'nunchaku'"

**Solution**: This is expected on macOS. The code automatically handles this and disables low VRAM mode. No action needed.

### Issue: Slow generation

**Solutions**:
1. Ensure you're using an Apple Silicon Mac for MPS acceleration
2. Close other applications to free up memory
3. Reduce the resolution parameter
4. Consider using a cloud service with NVIDIA GPUs for faster generation

### Issue: Installation fails with dependency errors

**Solution**: Make sure you're using Python 3.11:
```bash
python --version  # Should show Python 3.11.x
```

If using a different version, recreate the conda environment with Python 3.11.

## Example Usage on macOS

### Basic Text-to-Scene Generation

```python
import torch
from worldgen import WorldGen
from PIL import Image

# Device is automatically selected (MPS on Apple Silicon, CPU otherwise)
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
print(f"Using device: {device}")

# Initialize WorldGen
# Note: low_vram is automatically disabled on macOS
worldgen = WorldGen(mode="t2s", device=device)

# Generate a scene
splat = worldgen.generate_world("A beautiful mountain landscape with a lake")

# Save the result
splat.save("output.ply")
```

### Running the Demo

```bash
# Generate a scene and visualize it
python demo.py -p "A cozy living room with fireplace"

# The demo will automatically:
# - Detect your device (MPS or CPU)
# - Disable low_vram mode
# - Open a web viewer at http://localhost:8080
```

## Performance Optimization Tips

1. **Use lower resolution for testing**:
   ```python
   worldgen = WorldGen(mode="t2s", resolution=1024)
   ```

2. **Close unnecessary applications** to free up memory

3. **Monitor Activity Monitor** during generation to ensure you're not running out of memory

4. **For production use**, consider using cloud services with NVIDIA GPUs

## Reporting Issues

If you encounter issues specific to macOS, please report them on the GitHub repository with:
- Your macOS version
- Your Mac model (Apple Silicon or Intel)
- Python version
- Full error message and traceback
- Steps to reproduce

## Comparison with Other Platforms

| Feature | Linux (CUDA) | Windows (CUDA) | macOS (MPS) | macOS (CPU) |
|---------|-------------|----------------|-------------|-------------|
| Low VRAM Mode | ✅ | ✅ | ❌ | ❌ |
| GPU Acceleration | ✅ (CUDA) | ✅ (CUDA) | ✅ (MPS) | ❌ |
| xformers | ✅ | ✅ | ❌ | ❌ |
| Recommended for Production | ✅ | ✅ | ⚠️ | ❌ |
| Relative Speed | 100% | 95% | 40-60% | 5-10% |

## Conclusion

While macOS support is available, it comes with limitations compared to Linux/Windows with NVIDIA GPUs. For occasional use and testing, Apple Silicon Macs work reasonably well. For intensive production use, consider using a Linux system with an NVIDIA GPU or cloud-based GPU services.
