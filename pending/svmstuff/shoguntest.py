# In this example a two-class support vector machine classifier is trained on a
# 2-dimensional randomly generated data set and the trained classifier is used to
# predict labels of test examples. As training algorithm the LIBSVM solver is used
# with SVM regularization parameter C=1 and a Gaussian kernel of width 2.1.
# 
# For more details on LIBSVM solver see http://www.csie.ntu.edu.tw/~cjlin/libsvm/

from numpy import *
from numpy.random import randn
from shogun.Features import *
from shogun.Classifier import *
from shogun.Kernel import *

num=100
dist=3 # Higher dist means less overlap, and much more accurate classification. 
width=2.1
C=1

traindata_real=concatenate((randn(2,num)-dist, randn(2,num)+dist), axis=1)

trainlab=concatenate((-ones(num), ones(num)));

feats_train=RealFeatures(traindata_real);

kernel=GaussianKernel(feats_train, feats_train, width);

labels=Labels(trainlab);
svm=LibSVM(C, kernel, labels);
svm.train();

# Now for the testing

for i in range(100):
    testdata_real=concatenate((randn(2,num)-dist, randn(2,num)+dist), axis=1);
    testlab=concatenate((-ones(num), ones(num)));

    feats_test=RealFeatures(testdata_real);

    kernel.init(feats_train, feats_test);
    out = svm.classify().get_labels();
    
    testerr = mean(sign(out)!=testlab)
    if testerr != 0:
        print testerr
