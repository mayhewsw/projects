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

        #print vstack((out.T, label_test_multiclass.T)).T
	#testerr = mean(sign(out)!=testlab)
        #if testerr != 0:
        #   print testerr


def load_numbers(filename):
    matrix=fromfile(filename, sep=' ')
    # whole matrix is 1-dim now, so reshape
    #matrix=matrix.reshape(3, len(matrix)/3)
    matrix=matrix.reshape(len(matrix)/3, 3).T
    
    return matrix

def load_labels(filename):
    return fromfile(filename, dtype=double, sep=' ')


if __name__=='__main__':
	fm_train_real=load_numbers('threeclasstraindata.dat')
	fm_test_real=load_numbers('threeclasstestdata.dat')
	label_train_multiclass=load_labels('threeclasstrainlabs.dat')
        print label_train_multiclass.shape
	label_test_multiclass=load_labels('threeclasstestlabs.dat')
	libsvm_multiclass()
