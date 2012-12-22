# This example demonstrates how to encode string
# features efficiently by creating a more compactly encoded
# bit-string from StringCharFeatures.
# For instance, when working with the DNA alphabet {A,T,G,C}
# using 1 char = 1 byte per symbol would be wasteful, as we
# can encode 4 symbols using 2 bits only.
# Here, this is done in junks of 16bit (word).

from shogun.Features import StringCharFeatures, StringWordFeatures, RAWBYTE
from numpy import array, uint16

#create string features
cf=StringCharFeatures(['hey','guys','string'], RAWBYTE)
wf=StringWordFeatures(RAWBYTE)

#start=0, order=2, gap=0, rev=False)
wf.obtain_from_char(cf, 0, 2, 0, False)

#and output several stats
print "max string length", wf.get_max_vector_length()
print "number of strings", wf.get_num_vectors()
print "length of first string", wf.get_vector_length(0)
print "string[2]", wf.get_feature_vector(2)
print "strings", wf.get_features()

#replace string 0
wf.set_feature_vector(array([1,2,3,4,5], dtype=uint16), 0)

print "strings", wf.get_features()
