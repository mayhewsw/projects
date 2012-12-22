# This example shows how to use the polynomial kernel with sparse features.

def sparse_poly ():
	print 'SparsePoly'

	from shogun.Features import SparseRealFeatures
	from shogun.Kernel import SparsePolyKernel

	feats_train=SparseRealFeatures(fm_train_real)
	feats_test=SparseRealFeatures(fm_test_real)

	size_cache=10
	degree=3
	inhomogene=True

	kernel=SparsePolyKernel(feats_train, feats_train, size_cache, degree,
		inhomogene)
	km_train=kernel.get_kernel_matrix()

	kernel.init(feats_train, feats_test)
	km_test=kernel.get_kernel_matrix()

if __name__=='__main__':
	from tools.load import LoadMatrix
	lm=LoadMatrix()
	fm_train_real=lm.load_numbers('../data/fm_train_real.dat')
	fm_test_real=lm.load_numbers('../data/fm_test_real.dat')
	sparse_poly()
