# This example demonstrates how to use compressed strings with shogun.
# We currently support reading and writing compressed files using 
# LZO, GZIP, BZIP2 and LZMA. Furthermore, we demonstrate how to extract
# compressed streams on-the-fly in order to fit data sets into
# memory that would be too large, otherwise.
# 

from shogun.Features import StringCharFeatures, StringFileCharFeatures, RAWBYTE
from shogun.Library import UNCOMPRESSED,LZO,GZIP,BZIP2,LZMA, MSG_DEBUG
from shogun.PreProc import DecompressCharString

f=StringFileCharFeatures('features_string_char_compressed_modular.py', RAWBYTE)

print "original strings", f.get_features()

#uncompressed
f.save_compressed("foo_uncompressed.str", UNCOMPRESSED, 1)
f2=StringCharFeatures(RAWBYTE);
f2.load_compressed("foo_uncompressed.str", True)
print "uncompressed strings", f2.get_features()
print

# load compressed data and uncompress on load

#lzo
f.save_compressed("foo_lzo.str", LZO, 9)
f2=StringCharFeatures(RAWBYTE);
f2.load_compressed("foo_lzo.str", True)
print "lzo strings", f2.get_features()
print

##gzip
f.save_compressed("foo_gzip.str", GZIP, 9)
f2=StringCharFeatures(RAWBYTE);
f2.load_compressed("foo_gzip.str", True)
print "gzip strings", f2.get_features()
print

#bzip2
f.save_compressed("foo_bzip2.str", BZIP2, 9)
f2=StringCharFeatures(RAWBYTE);
f2.load_compressed("foo_bzip2.str", True)
print "bzip2 strings", f2.get_features()
print

#lzma
f.save_compressed("foo_lzma.str", LZMA, 9)
f2=StringCharFeatures(RAWBYTE);
f2.load_compressed("foo_lzma.str", True)
print "lzma strings", f2.get_features()
print

# load compressed data and uncompress via preprocessor
f2=StringCharFeatures(RAWBYTE);
f2.load_compressed("foo_lzo.str", False)
f2.add_preproc(DecompressCharString(LZO))
f2.apply_preproc()
print "lzo strings", f2.get_features()
print

# load compressed data and uncompress on-the-fly via preprocessor
f2=StringCharFeatures(RAWBYTE);
f2.load_compressed("foo_lzo.str", False)
f2.io.set_loglevel(MSG_DEBUG)
f2.add_preproc(DecompressCharString(LZO))
f2.enable_on_the_fly_preprocessing()
print "lzo strings", f2.get_features()
print

#clean up
import os
for f in ['foo_uncompressed.str', 'foo_lzo.str', 'foo_gzip.str',
'foo_bzip2.str', 'foo_lzma.str', 'foo_lzo.str', 'foo_lzo.str']:
	if os.path.exists(f):
		os.unlink(f)

##########################################################################################
# some perfectly compressible stuff follows
##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################
