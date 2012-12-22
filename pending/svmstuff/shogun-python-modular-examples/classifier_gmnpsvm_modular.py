# In this example a multi-class support vector machine is trained on a toy data
# set and the trained classifier is then used to predict labels of test
# examples. The training algorithm is based on BSVM formulation (L2-soft margin
# and the bias added to the objective function) which is solved by the Improved
# Mitchell-Demyanov-Malozemov algorithm. The training algorithm uses the Gaussian
# kernel of width 2.1 and the regularization constant C=1. The solver stops if the
# relative duality gap falls below 1e-5. 
# 
# For more details on the used SVM solver see 
#  V.Franc: Optimization Algorithms for Kernel Methods. Research report.
#  CTU-CMP-2005-22. CTU FEL Prague. 2005.
#  ftp://cmp.felk.cvut.cz/pub/cmp/articles/franc/Franc-PhD.pdf .
# 

def gmnpsvm ():
	print 'GMNPSVM'

	from shogun.Features import RealFeatures, Labels
	from shogun.Kernel import GaussianKernel
	from shogun.Classifier import GMNPSVM

	feats_train=RealFeatures(fm_train_real)
	feats_test=RealFeatures(fm_test_real)
	width=2.1
	kernel=GaussianKernel(feats_train, feats_train, width)

	C=1
	epsilon=1e-5
	labels=Labels(label_train_multiclass)

	svm=GMNPSVM(C, kernel, labels)
	svm.set_epsilon(epsilon)
	svm.train(feats_train)
	#kernel.init(feats_train, feats_test)
	out=svm.classify(feats_test).get_labels()

if __name__=='__main__':
	from tools.load import LoadMatrix
	lm=LoadMatrix()
	fm_train_real=lm.load_numbers('../data/fm_train_real.dat')
	fm_test_real=lm.load_numbers('../data/fm_test_real.dat')
	label_train_multiclass=lm.load_labels('../data/label_train_multiclass.dat')
	gmnpsvm()
