# This example demonstrates how to load ASCII features from a file into shogun.

from shogun.Features import StringFileCharFeatures, RAWBYTE

f = StringFileCharFeatures('features_string_file_char_modular.py', RAWBYTE)

print "strings", f.get_features()
