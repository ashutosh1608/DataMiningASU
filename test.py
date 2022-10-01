import os

import brainExtraction

curr_dir = os.getcwd()
test_dir = os.path.join(curr_dir, r'testPatient')
l = brainExtraction.reader(test_dir)
slices_dir = os.path.join(curr_dir, r'Slices')
os.makedirs(slices_dir)
bound_dir = os.path.join(curr_dir, r'Boundaries')
os.makedirs(bound_dir)
for i in l:
    slice_dir_i = os.path.join(slices_dir, i.split('_')[0] + '_' + i.split('_')[1])
    bound_dir_i = os.path.join(bound_dir, i.split('_')[0] + '_' + i.split('_')[1])
    os.makedirs(slice_dir_i)
    os.makedirs(bound_dir_i)
    brainExtraction.extraction(curr_dir, test_dir, slice_dir_i, bound_dir_i, i)