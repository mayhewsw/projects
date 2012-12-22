# In this example a two-class support vector machine classifier is trained on a
# toy data set and the trained classifier is used to predict labels of test
# examples. As training algorithm the Minimal Primal Dual SVM is used with SVM
# regularization parameter C=1 and a Gaussian kernel of width 1.2 and the
# precision parameter 1e-5. 
# 
# For more details on the MPD solver see 
#  Kienzle, W. and B. Schölkopf: Training Support Vector Machines with Multiple
#  Equality Constraints. Machine Learning: ECML 2005, 182-193. (Eds.) Carbonell,
#  J. G., J. Siekmann, Springer, Berlin, Germany (11 2005)

def mpdsvm ():
	print 'MPDSVM'

	from shogun.Features import RealFeatures, Labels
	from shogun.Kernel import GaussianKernel
	from shogun.Classifier import MPDSVM

	feats_train=RealFeatures(fm_train_real)
	feats_test=RealFeatures(fm_test_real)
	width=2.1
	kernel=GaussianKernel(feats_train, feats_train, width)

	C=1
	epsilon=1e-5
	labels=Labels(label_train_twoclass)

	svm=MPDSVM(C, kernel, labels)
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
	mpdsvm()
