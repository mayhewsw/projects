# In this example a two-class support vector machine classifier is trained on a
# DNA splice-site detection data set and the trained classifier is used to predict
# labels on test set. As training algorithm SVM^light is used with SVM
# regularization parameter C=1 and the Weighted Degree kernel of the degree 20 and
# a precision parameter epsilon=1e-5. The LINADD trick is used to speed up
# training.
# 
# For more details on the SVM^light see
#  T. Joachims. Making large-scale SVM learning practical. In Advances in Kernel
#  Methods -- Support Vector Learning, pages 169-184. MIT Press, Cambridge, MA USA, 1999.
# 
# For more details on the Weighted Degree kernel and the LINADD trick see
#   Sonnenburg, s. and Rätsch, G. and Rieck, K. Large Scale Learning with String
#   Kernels. In Bottou, Leon and Chapelle, Olivier and DeCoste, Dennis and Weston,
#   Jason, editor, In Large Scale Kernel Machines, pages 73-103, MIT Press,
#   Cambridge, MA. 2007.  
# 

def do_batch_linadd ():
	print 'SVMlight batch'

	from shogun.Features import StringCharFeatures, Labels, DNA
	from shogun.Kernel import WeightedDegreeStringKernel
	try:
		from shogun.Classifier import SVMLight
	except ImportError:
		print 'No support for SVMLight available.'
		return

	feats_train=StringCharFeatures(DNA)
	feats_train.set_features(fm_train_dna)
	feats_test=StringCharFeatures(DNA)
	feats_test.set_features(fm_test_dna)
	degree=20

	kernel=WeightedDegreeStringKernel(feats_train, feats_train, degree)

	C=1
	epsilon=1e-5
	num_threads=2
	labels=Labels(label_train_dna)

	svm=SVMLight(C, kernel, labels)
	svm.set_epsilon(epsilon)
	svm.parallel.set_num_threads(num_threads)
	svm.train()

	kernel.init(feats_train, feats_test)

	#print 'SVMLight Objective: %f num_sv: %d' % \
	#	(svm.get_objective(), svm.get_num_support_vectors())
	svm.set_batch_computation_enabled(False)
	svm.set_linadd_enabled(False)
	svm.classify().get_labels()

	svm.set_batch_computation_enabled(True)
	svm.classify().get_labels()

if __name__=='__main__':
	from tools.load import LoadMatrix
	lm=LoadMatrix()
	fm_train_dna=lm.load_dna('../data/fm_train_dna.dat')
	fm_test_dna=lm.load_dna('../data/fm_test_dna.dat')
	label_train_dna=lm.load_labels('../data/label_train_dna.dat')
	do_batch_linadd()
