# This example shows how to read and write plain ascii files, binary files and
# hdf5 datasets.
# 
# For ascii files it shows how to obtain shogun's RealFeatures
# (a simple feature matrix of doubles with 1 column == 1 example, nr_columns ==
#  number of examples) and also sparse features in SVM light format.
# 
# Binary files use some custom native format and datasets can be read/written
# from/to hdf5 files with arbitrary group / path.

def io ():
	print 'Features IO'
	import numpy
	from shogun.Features import SparseRealFeatures, RealFeatures, Labels
	from shogun.Kernel import GaussianKernel
	from shogun.Library import AsciiFile, BinaryFile, HDF5File

	feats=SparseRealFeatures(fm_train_real)
	feats2=SparseRealFeatures()

	f=BinaryFile("fm_train_sparsereal.bin","w")
	feats.save(f)

	f=AsciiFile("fm_train_sparsereal.ascii","w")
	feats.save(f)

	f=BinaryFile("fm_train_sparsereal.bin")
	feats2.load(f)

	f=AsciiFile("fm_train_sparsereal.ascii")
	feats2.load(f)

	feats=RealFeatures(fm_train_real)
	feats2=RealFeatures()

	f=BinaryFile("fm_train_real.bin","w")
	feats.save(f)

	f=HDF5File("fm_train_real.h5","w", "/data/doubles")
	feats.save(f)

	f=AsciiFile("fm_train_real.ascii","w")
	feats.save(f)

	f=BinaryFile("fm_train_real.bin")
	feats2.load(f)
	print "diff binary", numpy.max(numpy.abs(feats2.get_feature_matrix().flatten()-fm_train_real.flatten()))

	f=AsciiFile("fm_train_real.ascii")
	feats2.load(f)
	print "diff ascii", numpy.max(numpy.abs(feats2.get_feature_matrix().flatten()-fm_train_real.flatten()))

	lab=Labels(numpy.array([1.0,2.0,3.0]))
	lab2=Labels()
	f=AsciiFile("label_train_twoclass.ascii","w")
	lab.save(f)

	f=BinaryFile("label_train_twoclass.bin","w")
	lab.save(f)

	f=HDF5File("fm_train_real.h5","a", "/data/labels")
	lab.save(f)

	f=AsciiFile("label_train_twoclass.ascii")
	lab2.load(f)

	f=BinaryFile("label_train_twoclass.bin")
	lab2.load(f)

	f=HDF5File("fm_train_real.h5","r", "/data/doubles")
	feats2.load(f)
	print feats2.get_feature_matrix()
	f=HDF5File("fm_train_real.h5","r", "/data/labels")
	lab2.load(f)
	print lab2.get_labels()

	#clean up
	import os
	for f in ['fm_train_sparsereal.bin','fm_train_sparsereal.ascii',
			'fm_train_real.bin','fm_train_real.h5','fm_train_real.ascii',
			'label_train_twoclass.ascii','label_train_twoclass.bin']:
		os.unlink(f)

if __name__=='__main__':
	from tools.load import LoadMatrix
	lm=LoadMatrix()
	fm_train_real=lm.load_numbers('../data/fm_train_real.dat')
	label_train_twoclass=lm.load_numbers('../data/label_train_twoclass.dat')
	io()
