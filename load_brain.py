from nilearn import image, plotting
import numpy as np
import os

def load_brain(file_path, plot_type="anat", title=None):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    print(f"Loading: {file_path}")
    img = image.load_img(file_path)

    if plot_type == "func":
        img = image.mean_img(img)

    data = img.get_fdata()
    brightest_idx = np.unravel_index(np.argmax(data), data.shape)
    max_val = data[brightest_idx]
    print(f"Brightest voxel at: {brightest_idx} with value {max_val:.2f}")

    # Clamp all coords safely within bounds (10 voxels margin)
    x, y, z = brightest_idx
    x_safe = x if 10 < x < data.shape[0] - 10 else data.shape[0] // 2
    y_safe = y if 10 < y < data.shape[1] - 10 else data.shape[1] // 2
    z_safe = z if 10 < z < data.shape[2] - 10 else data.shape[2] // 2

    cut_coords = [int(x_safe), int(y_safe), int(z_safe)]

    # Create overlay mask (3x3x3 block)
    overlay_data = np.zeros_like(data)
    block = 1
    overlay_data[
        x - block:x + block + 1,
        y - block:y + block + 1,
        z - block:z + block + 1
    ] = max_val

    overlay_img = image.new_img_like(img, overlay_data)

    # Plot with color overlay
    plotting.plot_stat_map(
        stat_map_img=overlay_img,
        bg_img=img,
        threshold=0.1,
        display_mode='ortho',
        cut_coords=cut_coords,
        cmap='hot',
        title=title or f"Brightest Voxel Block: {brightest_idx}"
    )
    plotting.show()

    return img

if __name__ == "__main__":
    test_path = r"C:\Users\etern\OneDrive\Desktop\mridata\sub-01\ses-01\anat\sub-01_ses-01_T1w.nii.gz"
    load_brain(test_path, plot_type="anat")
