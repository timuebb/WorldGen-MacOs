import sys
import torch
import numpy as np
from PIL import Image

# Try to import UniK3D (only available on Linux and Windows due to Triton dependency)
try:
    from unik3d.models import UniK3D
    from unik3d.utils.camera import Spherical
    UNIK3D_AVAILABLE = True
except ImportError:
    UNIK3D_AVAILABLE = False
    if sys.platform == 'darwin':
        print("⚠️  UniK3D is not available on macOS (requires Triton which is Linux/Windows only).")
        print("⚠️  Depth estimation features will not work. This is a known limitation.")
    else:
        print("⚠️  UniK3D is not installed. Depth estimation features will not work.")

def build_depth_model(device: torch.device = 'cuda'):
    if not UNIK3D_AVAILABLE:
        raise ImportError(
            "UniK3D is not available on this platform. "
            "Depth estimation requires Linux or Windows due to Triton dependency. "
            "macOS is not currently supported for this feature."
        )
    model = UniK3D.from_pretrained("lpiccinelli/unik3d-vitl")
    model.eval()
    model = model.to(device)
    return model

def pred_pano_depth(model, image: Image.Image):
    rgb = torch.from_numpy(np.array(image)).permute(2, 0, 1)  # C, H, W
    rgb = rgb.to(model.device)
    H, W = rgb.shape[1:]

    camera = Spherical(params=torch.tensor([1.0, 1.0, 1.0, 1.0, W, H, np.pi, np.pi/2]))
    predictions = model.infer(rgb, camera)
    h, w = predictions["depth"].shape[2:]

    rgb = torch.tensor(np.array(image.resize((w, h))), device=model.device)
    depth = predictions["depth"].squeeze(0).squeeze(0)
    distance = predictions["distance"].squeeze(0).squeeze(0)
    rays = predictions["rays"].squeeze(0).permute(1, 2, 0)

    results = {
        "rgb": rgb, # (H, W, 3)
        "depth": depth, # (H, W)
        "distance": distance, # (H, W)
        "rays": rays # (H, W, 3)
    }

    return results

def pred_depth(model, image: Image.Image):
    rgb = torch.from_numpy(np.array(image)).permute(2, 0, 1)  # C, H, W
    rgb = rgb.to(model.device)
    H, W = rgb.shape[1:]

    predictions = model.infer(rgb)
    h, w = predictions["depth"].shape[2:]

    rgb = torch.tensor(np.array(image.resize((w, h))), device=model.device)
    depth = predictions["depth"].squeeze(0).squeeze(0)
    distance = predictions["distance"].squeeze(0).squeeze(0)
    rays = predictions["rays"].squeeze(0).permute(1, 2, 0)

    results = {
        "rgb": rgb, # (H, W, 3)
        "depth": depth, # (H, W)
        "distance": distance, # (H, W)
        "rays": rays # (H, W, 3)
    }

    return results
if __name__ == "__main__":
    model = build_depth_model()
    image = Image.open("data/background/timeless_desert.png")
    predictions = pred_pano_depth(model, image)
    print(predictions)