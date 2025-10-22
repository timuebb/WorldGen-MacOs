# Quick Start for macOS Users

## TL;DR - Fast Installation

```bash
# 1. Install prerequisites
# Make sure you have Conda installed from https://docs.conda.io/en/latest/miniconda.html

# 2. Quick setup
git clone https://github.com/ZiYang-xie/WorldGen.git
cd WorldGen
conda create -n worldgen python=3.11 -y
conda activate worldgen
pip3 install torch torchvision
pip install .

# 3. Test it works
python -c "from worldgen import WorldGen; print('✅ Installation successful!')"

# 4. Generate your first scene (takes 10-20 minutes on Apple Silicon)
python demo.py -p "A beautiful mountain landscape"
# Open http://localhost:8080 in your browser to view the scene
```

## Important Notes for macOS Users

### ⚡ Apple Silicon (M1/M2/M3/M4) Users
- **You're in good shape!** Your Mac will use MPS for GPU acceleration
- Expect generation times of 5-20 minutes depending on your model
- Make sure you have at least 16GB RAM

### 💻 Intel Mac Users
- **Warning:** Generation will be slow (30-60+ minutes) as it runs on CPU only
- Consider using a cloud service with GPU for better performance
- Close other applications to free up resources

### ❌ What Doesn't Work on macOS
- **Low VRAM mode** - Not available (requires nunchaku library which only supports Linux/Windows)
- If you see warnings about nunchaku, **this is normal and expected** on macOS

## Usage Example

```python
from worldgen import WorldGen
import torch

# Device is automatically detected (MPS on Apple Silicon, CPU on Intel)
worldgen = WorldGen(mode="t2s")  # text-to-scene mode

# Generate a 3D scene
scene = worldgen.generate_world("A cozy cabin in the woods with snow")

# Save the scene
scene.save("my_scene.ply")
```

## Troubleshooting

**Problem:** "MPS backend out of memory"
**Solution:** Use a lower resolution:
```python
worldgen = WorldGen(mode="t2s", resolution=1024)
```

**Problem:** Generation is too slow
**Solution:** 
- Apple Silicon: Make sure MPS is being used (check console output)
- Intel Mac: Consider using a cloud GPU service
- Both: Reduce resolution to speed up generation

**Problem:** Import errors or dependency issues
**Solution:** Make sure you're using Python 3.11:
```bash
python --version  # Should show 3.11.x
```

## Next Steps

- **For detailed documentation:** See [MACOS_INSTALLATION.md](MACOS_INSTALLATION.md)
- **For complete API reference:** See the main [README.md](README.md)
- **For technical details on changes:** See [MACOS_CHANGES_SUMMARY.md](MACOS_CHANGES_SUMMARY.md)

## Need Help?

If you run into issues:
1. Check [MACOS_INSTALLATION.md](MACOS_INSTALLATION.md) for detailed troubleshooting
2. Make sure you're using Python 3.11 and latest conda/pip
3. Report issues on GitHub with your macOS version and Mac model

## Performance Expectations

| Mac Model | Expected Time | Notes |
|-----------|---------------|-------|
| M3 Max/Ultra | 5-10 min | Best performance |
| M2 Pro/Max | 8-15 min | Very good |
| M1 Pro/Max | 10-20 min | Good |
| M1/M2 Base | 15-25 min | Acceptable |
| Intel Mac | 30-60+ min | Not recommended |

**Pro Tip:** Start with a simple prompt to test the setup before trying complex scenes!
