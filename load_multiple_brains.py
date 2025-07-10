from nilearn import image
import os
import numpy as np

def merge_to_4d(subject_ids, base_dir, session="01", output_path="merged_4d.nii.gz"):
    imgs = []
    ref_img = None
    for subject_id in subject_ids:
        ses_folder = f"ses-{session}\\anat"
        file_name = f"{subject_id}_ses-{session}_T1w.nii.gz"
        file_path = os.path.join(base_dir, subject_id, ses_folder, file_name)
        if os.path.exists(file_path):
            print(f"Loading {file_path}")
            img = image.load_img(file_path)
            if ref_img is None:
                ref_img = img
            else:
                # Resample to reference affine & shape
                img = image.resample_to_img(img, ref_img)
            imgs.append(img)
        else:
            print(f"File not found: {file_path}, skipping.")

    if not imgs:
        print("No images loaded, aborting.")
        return

    merged_img = image.concat_imgs(imgs)
    merged_img.to_filename(output_path)
    print(f"Saved merged 4D NIfTI file to: {output_path}")

if __name__ == "__main__":
    base_directory = r"C:\Users\etern\OneDrive\Desktop\mridata"
    subjects = [f"sub-{i:02d}" for i in range(1,12)]
    output_file = os.path.join(base_directory, "sub01_to_sub11_ses01_merged.nii.gz")

    merge_to_4d(subjects, base_directory, session="01", output_path=output_file)
img = image.resample_to_img(img, ref_img, force_resample=True, copy_header=True)
