# In this example a two-class linear support vector machine classifier is trained
# on a toy data set and the trained classifier is used to predict labels of test
# examples. As training algorithm the steepest descent subgradient algorithm is
# used. The SVM regularization parameter is set to C=0.9 and the bias in the
# classification rule is switched off. The solver iterates until it finds an
# epsilon-precise solution (epsilon=1e-3) or the maximal training time
# max_train_time=1 (seconds) is exceeded. The unbiased linear rule is trained.
# 
# Note that this solver often does not converges because the steepest descent
# subgradient algorithm is oversensitive to rounding errors. Note also that this
# is an unpublished work which was predecessor of the OCAS solver (see
# classifier_svmocas).

def subgradient_svm ():
	print 'SubGradientSVM'

	from shogun.Features import RealFeatures, SparseRealFeatures, Labels
	from shogun.Classifier import SubGradientSVM

	realfeat=RealFeatures(fm_train_real)
	feats_train=SparseRealFeatures()
	feats_train.obtain_from_simple(realfeat)
	realfeat=RealFeatures(fm_test_real)
	feats_test=SparseRealFeatures()
	feats_test.obtain_from_simple(realfeat)

	C=0.9
	epsilon=1e-3
	num_threads=1
	max_train_time=1.
	labels=Labels(label_train_twoclass)

	svm=SubGradientSVM(C, feats_train, labels)
	svm.set_epsilon(epsilon)
	svm.parallel.set_num_threads(num_threads)
	svm.set_bias_enabled(False)
	svm.set_max_train_time(max_train_time)
	svm.train()

	svm.set_features(feats_test)
	svm.classify().get_labels()

if __name__=='__main__':
	from tools.load import LoadMatrix
	lm=LoadMatrix()
	fm_train_real=lm.load_numbers('../data/fm_train_real.dat')
	fm_test_real=lm.load_numbers('../data/fm_test_real.dat')
	label_train_twoclass=lm.load_labels('../data/label_train_twoclass.dat')
	subgradient_svm()
