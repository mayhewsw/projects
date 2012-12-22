# In this example a multi-class support vector machine classifier is trained on a
# toy data set and the trained classifier is used to predict labels of test
# examples. As training algorithm the LIBSVM solver is used with SVM
# regularization parameter C=1 and a Gaussian kernel of width 2.1 and the
# precision parameter epsilon=1e-5. 
# 
# For more details on LIBSVM solver see http://www.csie.ntu.edu.tw/~cjlin/libsvm/
from numpy import *
from numpy.random import randn
from shogun.Features import *
from shogun.Classifier import *
from shogun.Kernel import *


def libsvm_multiclass ():
	print 'LibSVMMultiClass'

	from shogun.Features import RealFeatures, Labels
	from shogun.Kernel import GaussianKernel
	from shogun.Classifier import LibSVMMultiClass

	feats_train=RealFeatures(fm_train_real)
	feats_test=RealFeatures(fm_test_real)
	width=2.1
	kernel=GaussianKernel(feats_train, feats_train, width)

	C=1
	epsilon=1e-5
	labels=Labels(label_train_multiclass)

	svm=LibSVMMultiClass(C, kernel, labels)
	svm.set_epsilon(epsilon)
	svm.train()

	kernel.init(feats_train, feats_test)
	out = svm.classify().get_labels()
    
	testerr = mean(sign(out)!=testlab)
        if testerr != 0:
           print testerr


if __name__=='__main__':
	from tools.load import LoadMatrix
	lm=LoadMatrix()
	fm_train_real=lm.load_numbers('../shogun-data-0.1/toy/fm_train_real.dat')
	fm_test_real=lm.load_numbers('../shogun-data-0.1/toy/fm_test_real.dat')
	label_train_multiclass=lm.load_labels('../shogun-data-0.1/toy/label_train_multiclass.dat')
	libsvm_multiclass()
