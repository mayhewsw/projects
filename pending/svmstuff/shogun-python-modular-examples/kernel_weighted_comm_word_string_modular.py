# The WeightedCommWordString kernel may be used to compute the weighted
# spectrum kernel (i.e. a spectrum kernel for 1 to K-mers, where each k-mer
# length is weighted by some coefficient \f$\beta_k\f$) from strings that have
# been mapped into unsigned 16bit integers.
# 
# These 16bit integers correspond to k-mers. To applicable in this kernel they
# need to be sorted (e.g. via the SortWordString pre-processor).
# 
# It basically uses the algorithm in the unix "comm" command (hence the name)
# to compute:
# 
# k({\bf x},({\bf x'})= \sum_{k=1}^K\beta_k\Phi_k({\bf x})\cdot \Phi_k({\bf x'})
# 
# where \f$\Phi_k\f$ maps a sequence \f${\bf x}\f$ that consists of letters in
# \f$\Sigma\f$ to a feature vector of size \f$|\Sigma|^k\f$. In this feature
# vector each entry denotes how often the k-mer appears in that \f${\bf x}\f$.
# 
# Note that this representation is especially tuned to small alphabets
# (like the 2-bit alphabet DNA), for which it enables spectrum kernels
# of order 8.
# 
# For this kernel the linadd speedups are quite efficiently implemented using
# direct maps.
# 

def weighted_comm_word_string ():
	print 'WeightedCommWordString'
	from shogun.Kernel import WeightedCommWordStringKernel
	from shogun.Features import StringWordFeatures, StringCharFeatures, DNA
	from shogun.PreProc import SortWordString

	order=3
	gap=0
	reverse=True

	charfeat=StringCharFeatures(fm_train_dna, DNA)
	feats_train=StringWordFeatures(charfeat.get_alphabet())
	feats_train.obtain_from_char(charfeat, order-1, order, gap, reverse)
	preproc=SortWordString()
	preproc.init(feats_train)
	feats_train.add_preproc(preproc)
	feats_train.apply_preproc()

	charfeat=StringCharFeatures(fm_test_dna, DNA)
	feats_test=StringWordFeatures(charfeat.get_alphabet())
	feats_test.obtain_from_char(charfeat, order-1, order, gap, reverse)
	feats_test.add_preproc(preproc)
	feats_test.apply_preproc()

	use_sign=False
	kernel=WeightedCommWordStringKernel(feats_train, feats_train, use_sign)
	km_train=kernel.get_kernel_matrix()

	kernel.init(feats_train, feats_test)
	km_test=kernel.get_kernel_matrix()


if __name__=='__main__':
	from tools.load import LoadMatrix
	lm=LoadMatrix()
	fm_train_dna=lm.load_dna('../data/fm_train_dna.dat')
	fm_test_dna=lm.load_dna('../data/fm_test_dna.dat')
	weighted_comm_word_string()
