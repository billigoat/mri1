import os
from nilearn import image


def merge_to_4d(subject_ids, base_dir, output_path="merged_4d.nii.gz"):
    imgs = []
    ref_img = None

    for sid in subject_ids:
        path = os.path.join(base_dir, sid, "anat", f"{sid}_T1w.nii.gz")
        if not os.path.exists(path):
            print(f"Skipping (Missing): {path}")
            continue

        try:
            img = image.load_img(path)
            data = img.get_fdata()

            brain_voxels = data[data > 0]
            if brain_voxels.size == 0:
                continue

            normalized = (data - brain_voxels.mean()) / brain_voxels.std()
            norm_img = image.new_img_like(img, normalized)

            if ref_img is None:
                ref_img = norm_img
                imgs.append(norm_img)
            else:
                resampled = image.resample_to_img(norm_img, ref_img, force_resample=True, copy_header=True)
                imgs.append(resampled)

        except Exception as e:
            print(f"Error processing {sid}: {e}")

    if imgs:
        image.concat_imgs(imgs).to_filename(output_path)
        print(f"Saved: {output_path}")
    else:
        print("No valid images found to merge.")


if __name__ == "__main__":
    base_directory = "/Users/eternaiyears/PycharmProjects/mri1/ds007694"
    subjects = [f"sub-GRACE{i}" for i in range(101, 243)]
    output_file = os.path.join(base_directory, "GRACE_all_T1w_merged.nii.gz")

    merge_to_4d(subjects, base_directory, output_path=output_file)
