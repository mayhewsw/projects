# In this example a one-class support vector machine classifier is trained on a
# toy data set. The training algorithm finds a hyperplane in the RKHS which
# separates the training data from the origin. The one-class classifier is
# typically used to estimate the support of a high-dimesnional distribution. 
# For more details see e.g. 
#   B. Schoelkopf et al. Estimating the support of a high-dimensional
#   distribution. Neural Computation, 13, 2001, 1443-1471. 
# 
# In the example, the one-class SVM is trained by the LIBSVM solver with the
# regularization parameter C=1 and the Gaussian kernel of width 2.1 and the
# precision parameter epsilon=1e-5.
# 
# For more details on LIBSVM solver see http://www.csie.ntu.edu.tw/~cjlin/libsvm/

def libsvm_oneclass ():
	print 'LibSVMOneClass'

	from shogun.Features import RealFeatures, Labels
	from shogun.Kernel import GaussianKernel
	from shogun.Classifier import LibSVMOneClass

	feats_train=RealFeatures(fm_train_real)
	feats_test=RealFeatures(fm_test_real)
	width=2.1
	kernel=GaussianKernel(feats_train, feats_train, width)

	C=1
	epsilon=1e-5

	svm=LibSVMOneClass(C, kernel)
	svm.set_epsilon(epsilon)
	svm.train()

	kernel.init(feats_train, feats_test)
	svm.classify().get_labels()

if __name__=='__main__':
	from tools.load import LoadMatrix
	lm=LoadMatrix()
	fm_train_real=lm.load_numbers('../data/fm_train_real.dat')
	fm_test_real=lm.load_numbers('../data/fm_test_real.dat')
	libsvm_oneclass()
