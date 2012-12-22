# In this example a support vector regression algorithm is trained on a
# real-valued toy data set. The underlying library used for the SVR training is
# LIBSVM. The SVR is trained with regularization parameter C=1 and a gaussian
# kernel with width=2.1. The labels of both the train and the test data are
# fetched via svr.classify().get_labels().
# 
# For more details on LIBSVM solver see http://www.csie.ntu.edu.tw/~cjlin/libsvm/ .

def libsvr ():
	print 'LibSVR'
	from shogun.Features import Labels, RealFeatures
	from shogun.Kernel import GaussianKernel
	from shogun.Regression import LibSVR

	feats_train=RealFeatures(fm_train)
	feats_test=RealFeatures(fm_test)
	width=2.1
	kernel=GaussianKernel(feats_train, feats_train, width)

	C=1
	epsilon=1e-5
	tube_epsilon=1e-2
	labels=Labels(label_train)

	svr=LibSVR(C, epsilon, kernel, labels)
	svr.set_tube_epsilon(tube_epsilon)
	svr.train()

	kernel.init(feats_train, feats_test)
	out1=svr.classify().get_labels()
	out2=svr.classify(feats_test).get_labels()

if __name__=='__main__':
	from numpy import array
	from numpy.random import seed, rand
	from tools.load import LoadMatrix
	lm=LoadMatrix()
	fm_train=lm.load_numbers('../data/fm_train_real.dat')
	fm_test=lm.load_numbers('../data/fm_test_real.dat')
	label_train=lm.load_labels('../data/label_train_twoclass.dat')
	libsvr()
