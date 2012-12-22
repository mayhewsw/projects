# Creates features similar to the feature space of the SNP kernel. Useful when
# working with linear methods.

from shogun.Features import *
from numpy import *

sf=StringByteFeatures(DIGIT2)
sf.load_ascii_file('x', False, DIGIT2, DIGIT2)
print sf.get_features()
snps=SNPFeatures(sf)
print snps.get_feature_matrix()
print snps.get_minor_base_string()
print snps.get_major_base_string()
