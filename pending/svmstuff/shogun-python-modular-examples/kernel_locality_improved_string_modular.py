#  The LocalityImprovedString kernel is inspired by the polynomial kernel.
# Comparing neighboring characters it puts emphasize on local features.
# 
# It can be defined as
# K({\bf x},{\bf x'})=\left(\sum_{i=0}^{T-1}\left(\sum_{j=-l}^{+l}w_jI_{i+j}({\bf x},{\bf x'})\right)^{d_1}\right)^{d_2},
# where
# I_i({\bf x},{\bf x'})=1 
# if $x_i=x'_i and 0 otherwise.
# 

def locality_improved_string ():
	print 'LocalityImprovedString'
	from shogun.Features import StringCharFeatures, DNA
	from shogun.Kernel import LocalityImprovedStringKernel

	feats_train=StringCharFeatures(fm_train_dna, DNA)
	feats_test=StringCharFeatures(fm_test_dna, DNA)
	length=5
	inner_degree=5
	outer_degree=7

	kernel=LocalityImprovedStringKernel(
		feats_train, feats_train, length, inner_degree, outer_degree)

	km_train=kernel.get_kernel_matrix()
	kernel.init(feats_train, feats_test)
	km_test=kernel.get_kernel_matrix()


if __name__=='__main__':
	from tools.load import LoadMatrix
	lm=LoadMatrix()
	fm_train_dna=lm.load_dna('../data/fm_train_dna.dat')
	fm_test_dna=lm.load_dna('../data/fm_test_dna.dat')
	locality_improved_string()
