# Gray matter volume differences between HS vs low schizotypy
from nilearn import image
from nilearn import plotting
import nibabel as nib
import numpy as np

def difference_map (merged_img):
    data = merged_img.get_fdata()  # the 4D file
    hs_group = data[:,:,:,:69]     # first 69 = high schizotypy
    ls_group = data[:,:,:,69:]     # last 72 = low schizotypy
    mean_hs = np.mean(hs_group, axis=3)
    mean_ls = np.mean(ls_group, axis=3)
    diff_map = mean_hs - mean_ls  # where do brains differ
    return diff_map

def main():
    merged_img = image.load_img("/Users/eternaiyears/PycharmProjects/mri1/ds007694/GRACE_all_T1w_merged.nii")
    diff_map = difference_map(merged_img) # captures result
    diff_img = nib.Nifti1Image(diff_map, merged_img.affine)
    plotting.plot_stat_map(
        diff_img, title = "High Schizotypical vs Low Schizotypical Brain Difference", colorbar= True, draw_cross = False, threshold = 10
    )
    plotting.show()

if __name__ == "__main__":
    main()