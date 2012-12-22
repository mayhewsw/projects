# This is an example for the initialization of the PolyMatchString kernel on string data. 
# The PolyMatchString kernel sums over the matches of two stings of the same length and 
# takes the sum to the power of 'degree'. The strings consist of the characters 'ACGT' corresponding 
# to the DNA-alphabet. Each column of the matrices of type char corresponds to 
# one training/test example.

def poly_match_word_string ():
	print 'PolyMatchWordString'
	from shogun.Kernel import PolyMatchWordStringKernel
	from shogun.Features import StringWordFeatures, StringCharFeatures, DNA

	degree=2
	inhomogene=True
	order=3
	gap=0
	reverse=False

	charfeat=StringCharFeatures(fm_train_dna, DNA)
	feats_train=StringWordFeatures(DNA)
	feats_train.obtain_from_char(charfeat, order-1, order, gap, reverse)

	charfeat=StringCharFeatures(fm_test_dna, DNA)
	feats_test=StringWordFeatures(DNA)
	feats_test.obtain_from_char(charfeat, order-1, order, gap, reverse)

	kernel=PolyMatchWordStringKernel(feats_train, feats_train, degree, inhomogene)

	km_train=kernel.get_kernel_matrix()
	kernel.init(feats_train, feats_test)
	km_test=kernel.get_kernel_matrix()


if __name__=='__main__':
	from tools.load import LoadMatrix
	lm=LoadMatrix()
	fm_train_dna=lm.load_dna('../data/fm_train_dna.dat')
	fm_test_dna=lm.load_dna('../data/fm_test_dna.dat')
	poly_match_word_string()
