# In this example the k-means clustering method is used to cluster a given toy
# data set. In k-means clustering one tries to partition n observations into k
# clusters in which each observation belongs to the cluster with the nearest mean.
# The algorithm class constructor takes the number of clusters and a distance to
# be used as input. The distance used in this example is Euclidean distance.
# After training one can fetch the result of clustering by obtaining the cluster
# centers and their radiuses.

#!/usr/bin/env python
"""
Explicit examples on how to use clustering
"""

def kmeans ():
	print 'KMeans'

	from shogun.Distance import EuclidianDistance
	from shogun.Features import RealFeatures
	from shogun.Clustering import KMeans

	k=3
	feats_train=RealFeatures(fm_train)
	distance=EuclidianDistance(feats_train, feats_train)

	kmeans=KMeans(k, distance)
	kmeans.train()

	kmeans.get_cluster_centers()
	kmeans.get_radiuses()

if __name__=='__main__':
	from tools.load import LoadMatrix
	lm=LoadMatrix()
	fm_train=lm.load_numbers('../data/fm_train_real.dat')
	kmeans()

