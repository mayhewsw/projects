# In this example, we demonstrate how to obtain string features
# by using a sliding window in a memory-efficient way. Instead of copying
# the string for each position of the sliding window, we only store a reference
# with respect to the complete string. This is particularly useful, when working
# with genomic data, where storing all explicitly copied strings in memory
# quickly becomes infeasible. In addition to a sliding window (of a particular
# length) over all position, we also support defining a custom position
# list.

from shogun.Features import StringCharFeatures, DNA
from shogun.Library import DynamicIntArray

# create string features with a single string
s=10*'A' + 10*'C' + 10*'G' + 10*'T'
f=StringCharFeatures([s], DNA)

# slide a window of length 5 over features
# (memory efficient, does not copy strings)
f.obtain_by_sliding_window(5,1)
print f.get_num_vectors()
print f.get_vector_length(0)
print f.get_vector_length(1)
print f.get_features()

# slide a window of length 4 over features
# (memory efficient, does not copy strings)
f.obtain_by_sliding_window(4,1)
print f.get_num_vectors()
print f.get_vector_length(0)
print f.get_vector_length(1)
print f.get_features()

# extract string-windows at position 0,6,16,25 of window size 4
# (memory efficient, does not copy strings)
f.set_features([s])
positions=DynamicIntArray()
positions.append_element(0)
positions.append_element(6)
positions.append_element(16)
positions.append_element(25)

f.obtain_by_position_list(4,positions)
print f.get_features()

# now extract windows of size 8 from same positon list
f.obtain_by_position_list(8,positions)
print f.get_features()
