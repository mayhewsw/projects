# This example demonstrates how to read and write data in the SVMLight Format
# from Shogun.
# 

import os
from shogun.Features import SparseRealFeatures

f=SparseRealFeatures()
lab=f.load_svmlight_file('../data/train_sparsereal.light')
f.write_svmlight_file('testwrite.light', lab)
os.unlink('testwrite.light')
