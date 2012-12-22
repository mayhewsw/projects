# This example shows how to compute the Manhatten Distance.

def manhattan_metric ():
	print 'ManhattanMetric'

	from shogun.Features import RealFeatures
	from shogun.Distance import ManhattanMetric

	feats_train=RealFeatures(fm_train_real)
	feats_test=RealFeatures(fm_test_real)

	distance=ManhattanMetric(feats_train, feats_train)

	dm_train=distance.get_distance_matrix()
	distance.init(feats_train, feats_test)
	dm_test=distance.get_distance_matrix()

if __name__=='__main__':
	from tools.load import LoadMatrix
	lm=LoadMatrix()
	fm_train_real=lm.load_numbers('../data/fm_train_real.dat')
	fm_test_real=lm.load_numbers('../data/fm_test_real.dat')
	manhattan_metric()
