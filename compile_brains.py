from nilearn import image
import os
from matrix_brain import extract_matrix

def merge_to_4d(subject_ids, base_dir, output_path="merged_4d.nii.gz"):
    imgs = [] #create empty image list
    results = [] #create empty matrix list
    ref_img = None #no reference image yet

    for sid in subject_ids:
        path = os.path.join(base_dir, sid, "anat", f"{sid}_T1w.nii.gz")
        if not os.path.exists(path):
            print(f"Skipping: {path}"); continue
        try:
            img = image.load_img(path) #load every image
            stats = extract_matrix(img) #extract matrix from every scan
        except Exception as e:
            print(f"Skipping {sid}: {e}"); continue #passing exception (had trouble loading files)

        results.append(stats)

        if ref_img is None:
            ref_img = img #the first subject becomes the reference image
        else:
            img = image.resample_to_img(img, ref_img, force_resample=True, copy_header=True) #resample to reference
        imgs.append(img) #appends image to list

    image.concat_imgs(imgs).to_filename(output_path) #concatenate all images into one 4d file
    print(f"Saved: {output_path}") #print saved path

if __name__ == "__main__":
    base_directory = "/Users/eternaiyears/PycharmProjects/mri1/ds007694"
    subjects = [f"sub-GRACE{i}" for i in range(101,243)]
    output_file = os.path.join(base_directory, "GRACE_all_T1w_merged.nii.gz")
    merge_to_4d(subjects, base_directory, output_path=output_file)