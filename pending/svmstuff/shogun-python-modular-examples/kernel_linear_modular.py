# This is an example for the initialization of a linear kernel on real valued 
# data using scaling factor 1.2. 

def linear ():
	print 'Linear'
	from shogun.Features import RealFeatures
	from shogun.Kernel import LinearKernel, AvgDiagKernelNormalizer

	feats_train=RealFeatures(fm_train_real)
	feats_test=RealFeatures(fm_test_real)
	scale=1.2

	kernel=LinearKernel()
	kernel.set_normalizer(AvgDiagKernelNormalizer(scale))
	kernel.init(feats_train, feats_train)

	km_train=kernel.get_kernel_matrix()
	kernel.init(feats_train, feats_test)
	km_test=kernel.get_kernel_matrix()

if __name__=='__main__':
	from tools.load import LoadMatrix
	lm=LoadMatrix()
	fm_train_real=lm.load_numbers('../data/fm_train_real.dat')
	fm_test_real=lm.load_numbers('../data/fm_test_real.dat')
	linear()
