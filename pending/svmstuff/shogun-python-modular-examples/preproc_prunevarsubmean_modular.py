# In this example a kernel matrix is computed for a given real-valued data set.
# The kernel used is the Chi2 kernel which operates on real-valued vectors. It
# computes the chi-squared distance between sets of histograms. It is a very
# useful distance in image recognition (used to detect objects). The preprocessor
# PruneVarSubMean substracts the mean from each feature and removes features that
# have zero variance.

def prune_var_sub_mean ():
	print 'PruneVarSubMean'

	from shogun.Kernel import Chi2Kernel
	from shogun.Features import RealFeatures
	from shogun.PreProc import PruneVarSubMean

	feats_train=RealFeatures(fm_train_real)
	feats_test=RealFeatures(fm_test_real)

	preproc=PruneVarSubMean()
	preproc.init(feats_train)
	feats_train.add_preproc(preproc)
	feats_train.apply_preproc()
	feats_test.add_preproc(preproc)
	feats_test.apply_preproc()

	width=1.4
	size_cache=10
	
	kernel=Chi2Kernel(feats_train, feats_train, width, size_cache)

	km_train=kernel.get_kernel_matrix()
	kernel.init(feats_train, feats_test)
	km_test=kernel.get_kernel_matrix()

if __name__=='__main__':
	from tools.load import LoadMatrix
	lm=LoadMatrix()
	fm_train_real=lm.load_numbers('../data/fm_train_real.dat')
	fm_test_real=lm.load_numbers('../data/fm_test_real.dat')
	prune_var_sub_mean()

