# In this example a two-class support vector machine classifier is trained on a
# toy data set and the trained classifier is then used to predict labels of test
# examples. As training algorithm Gradient Projection Decomposition Technique
# (GPDT) is used with SVM regularization parameter C=1 and a Gaussian
# kernel of width 2.1. The solver returns an epsilon-precise (epsilon=1e-5) solution. 
# 
# For more details on GPDT solver see http://dm.unife.it/gpdt . 
# 

def gpbtsvm ():
	print 'GPBTSVM'

	from shogun.Features import RealFeatures, Labels
	from shogun.Kernel import GaussianKernel
	from shogun.Classifier import GPBTSVM

	feats_train=RealFeatures(fm_train_real)
	feats_test=RealFeatures(fm_test_real)
	width=2.1
	kernel=GaussianKernel(feats_train, feats_train, width)

	C=1
	epsilon=1e-5
	labels=Labels(label_train_twoclass)

	svm=GPBTSVM(C, kernel, labels)
	svm.set_epsilon(epsilon)
	svm.train()

	kernel.init(feats_train, feats_test)
	svm.classify().get_labels()


if __name__=='__main__':
	from tools.load import LoadMatrix
	lm=LoadMatrix()
	fm_train_real=lm.load_numbers('../data/fm_train_real.dat')
	fm_test_real=lm.load_numbers('../data/fm_test_real.dat')
	label_train_twoclass=lm.load_labels('../data/label_train_twoclass.dat')
	gpbtsvm()
