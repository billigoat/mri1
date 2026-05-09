import numpy as np
import nibabel as nib

def extract_matrix (img):
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
    return {
        "shape": data.shape,
        "mean": np.mean(data),
        "max": np.max(data),
        "min": np.min(data),
        "affine": img.affine
    }

def main():
    path = input("What is the path name: ").strip().lower().strip("'")
    img = nib.load(path)
    extract_matrix(img)

if __name__ == "__main__":
    main()