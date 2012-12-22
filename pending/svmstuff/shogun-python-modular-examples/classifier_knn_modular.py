# This example shows usage of a k-nearest neighbor (KNN) classification rule on
# a toy data set. The number of the nearest neighbors is set to k=3 and the distances
# are measured by the Euclidean metric. Finally, the KNN rule is applied to predict
# labels of test examples. 

def knn ():
	print 'KNN'

	from shogun.Features import RealFeatures, Labels
	from shogun.Classifier import KNN
	from shogun.Distance import EuclidianDistance

	feats_train=RealFeatures(fm_train_real)
	feats_test=RealFeatures(fm_test_real)
	distance=EuclidianDistance(feats_train, feats_train)

	k=3
	labels=Labels(label_train_multiclass)

	knn=KNN(k, distance, labels)
	knn.train()
	output=knn.classify(feats_test).get_labels()

if __name__=='__main__':
	from tools.load import LoadMatrix
	lm=LoadMatrix()
	fm_train_real=lm.load_numbers('../data/fm_train_real.dat')
	fm_test_real=lm.load_numbers('../data/fm_test_real.dat')
	label_train_multiclass=lm.load_labels('../data/label_train_multiclass.dat')
	knn()
