import numpy as np


def analyze_brain(img):
    data = img.get_fdata()
    print(f"Image shape: {data.shape}")
    print(f"Affine matrix:\n{img.affine}")
    print(f"Voxel intensity stats — mean: {np.mean(data):.2f}, max: {np.max(data):.2f}, min: {np.min(data):.2f}")

    # if functional (4D), print basic time series info for voxel at center
    if data.ndim == 4:
        center = tuple(s // 2 for s in data.shape[:3])
        ts = data[center[0], center[1], center[2], :]
        print(f"Center voxel time series length: {len(ts)}")
        print(f"First 5 timepoints: {ts[:5]}")
