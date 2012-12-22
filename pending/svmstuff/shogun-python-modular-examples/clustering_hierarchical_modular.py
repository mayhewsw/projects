# In this example an agglomerative hierarchical single linkage clustering method
# is used to cluster a given toy data set. Starting with each object being
# assigned to its own cluster clusters are iteratively merged. Here the clusters
# are merged that have the closest (minimum distance, here set via the Euclidean
# distance object) two elements.


def hierarchical ():
	print 'Hierarchical'

	from shogun.Distance import EuclidianDistance
	from shogun.Features import RealFeatures
	from shogun.Clustering import Hierarchical

	merges=3
	feats_train=RealFeatures(fm_train)
	distance=EuclidianDistance(feats_train, feats_train)

	hierarchical=Hierarchical(merges, distance)
	hierarchical.train()

	hierarchical.get_merge_distances()
	hierarchical.get_cluster_pairs()

if __name__=='__main__':
	from tools.load import LoadMatrix
	lm=LoadMatrix()
	fm_train=lm.load_numbers('../data/fm_train_real.dat')

	hierarchical()
