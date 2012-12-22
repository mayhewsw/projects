# The Weighted Degree Position String kernel (Weighted Degree kernel with shifts).
# 
# The WD-shift kernel of order d compares two sequences X and
# Y of length L by summing all contributions of k-mer matches of
# lengths k in 1...d, weighted by coefficients beta_k
# allowing for a positional tolerance of up to shift s.
# 

def weighted_degree_position_string ():
	print 'WeightedDegreePositionString'
	from shogun.Features import StringCharFeatures, DNA
	from shogun.Kernel import WeightedDegreePositionStringKernel

	feats_train=StringCharFeatures(fm_train_dna, DNA)
	feats_test=StringCharFeatures(fm_test_dna, DNA)
	degree=20

	kernel=WeightedDegreePositionStringKernel(feats_train, feats_train, degree)

	#kernel.set_shifts(zeros(len(data['train'][0]), dtype=int))

	km_train=kernel.get_kernel_matrix()
	kernel.init(feats_train, feats_test)
	km_test=kernel.get_kernel_matrix()


if __name__=='__main__':
	from tools.load import LoadMatrix
	lm=LoadMatrix()
	fm_train_dna=lm.load_dna('../data/fm_train_dna.dat')
	fm_test_dna=lm.load_dna('../data/fm_test_dna.dat')
	weighted_degree_position_string()
