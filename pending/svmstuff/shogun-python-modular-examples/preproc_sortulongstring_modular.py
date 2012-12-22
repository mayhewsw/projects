# In this example a kernel matrix is computed for a given string data set. The
# CommUlongString kernel is used to compute the spectrum kernel from strings that
# have been mapped into unsigned 64bit integers. These 64bit integers correspond
# to k-mers. To be applicable in this kernel the mapped k-mers have to be sorted.
# This is done using the SortUlongString preprocessor, which sorts the indivual
# strings in ascending order. The kernel function basically uses the algorithm in
# the unix "comm" command (hence the name). Note that this representation enables
# spectrum kernels of order 8 for 8bit alphabets (like binaries) and order 32 for
# 2-bit alphabets like DNA. For this kernel the linadd speedups are implemented
# (though there is room for improvement here when a whole set of sequences is
# ADDed) using sorted lists.

def sort_ulong_string ():
	print 'CommUlongString'

	from shogun.Kernel import CommUlongStringKernel
	from shogun.Features import StringCharFeatures, StringUlongFeatures, DNA
	from shogun.PreProc import SortUlongString

	order=3
	gap=0
	reverse=False

	charfeat=StringCharFeatures(DNA)
	charfeat.set_features(fm_train_dna)
	feats_train=StringUlongFeatures(charfeat.get_alphabet())
	feats_train.obtain_from_char(charfeat, order-1, order, gap, reverse)

	charfeat=StringCharFeatures(DNA)
	charfeat.set_features(fm_test_dna)
	feats_test=StringUlongFeatures(charfeat.get_alphabet())
	feats_test.obtain_from_char(charfeat, order-1, order, gap, reverse)

	preproc=SortUlongString()
	preproc.init(feats_train)
	feats_train.add_preproc(preproc)
	feats_train.apply_preproc()
	feats_test.add_preproc(preproc)
	feats_test.apply_preproc()

	use_sign=False

	kernel=CommUlongStringKernel(feats_train, feats_train, use_sign)

	km_train=kernel.get_kernel_matrix()
	kernel.init(feats_train, feats_test)
	km_test=kernel.get_kernel_matrix()

if __name__=='__main__':
	from tools.load import LoadMatrix
	lm=LoadMatrix()
	fm_train_dna=lm.load_dna('../data/fm_train_dna.dat')
	fm_test_dna=lm.load_dna('../data/fm_test_dna.dat')
	sort_ulong_string()
