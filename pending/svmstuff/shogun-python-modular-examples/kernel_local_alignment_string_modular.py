# This is an example for the initialization of the local alignment kernel on 
# DNA sequences, where each column of the matrices of type char corresponds to 
# one training/test example. 

def local_alignment_string():
	print 'LocalAlignmentString'
	from shogun.Features import StringCharFeatures, DNA
	from shogun.Kernel import LocalAlignmentStringKernel

	feats_train=StringCharFeatures(fm_train_dna, DNA)
	feats_test=StringCharFeatures(fm_test_dna, DNA)

	kernel=LocalAlignmentStringKernel(feats_train, feats_train)
	km_train=kernel.get_kernel_matrix()

	kernel.init(feats_train, feats_test)
	km_test=kernel.get_kernel_matrix()


if __name__=='__main__':
	from tools.load import LoadMatrix
	lm=LoadMatrix()
	fm_train_dna=lm.load_dna('../data/fm_train_dna.dat')
	fm_test_dna=lm.load_dna('../data/fm_test_dna.dat')
	local_alignment_string()
