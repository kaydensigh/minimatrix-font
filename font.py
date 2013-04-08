# A set of utilities for converting a font between C representation and a string
# representation that can be easily edited.
#
# Edit the font in newfontmap.py, run process(), look at newfont.txt.
#
# Definitions:
#  Array: a list of bytes, one per column, similar to C representation.
#      See fontarray.py.
#  Map: a list of strings, one per row. Easy to edit by a human.
#      See newfontmap.py.

import re
import io

import fontarray
import newfontmap

def char_map_to_array(charmap):
  """Convert a character from a map to an array."""
  columns = len(charmap[0])
  char = [0] * columns
  for r in range(len(charmap)):
    row = charmap[r]
    for c in range(columns):
      char[c] = char[c] | ((1 if (row[c] == '#' or row[c] == '1') else 0) << r)
  return char

def char_array_to_map(char):
  """Convert a character from an array to a map."""
  charmap = []
  for r in range(8):
    row = []
    for col in char:
      row.append(col & (1 << r) and '1' or '0')
    charmap.append(''.join(row))
  return charmap

def font_array_to_map(fontarray):
  """Convert a list of character arrays to a list of maps."""
  s = []
  for char in fontarray:
    s.append(char_array_to_map(char))
  return s

def font_map_to_array(fontmap):
  """Convert a list of character maps to a list of arrays."""
  newarray = []
  for charmap in fontmap:
    newarray.append(char_map_to_array(charmap))
  return newarray

def test(fontarray):
  return fontarray == font_map_to_array(font_array_to_map(fontarray))

def font_array_to_hex(array):
  """Generate a repr of the array with literals in hex."""
  s = repr(array)
  s = re.split('(\d+)', s)
  o = []
  for i in s:
    if re.search('\d+', i):
      o.append(hex(int(i)))
    else:
      o.append(i)
  return ''.join(o)

def check_lengths(fontmap):
  """Check that all rows have the same length in each character."""
  for charmap in fontmap:
    columns = len(charmap[0])
    for row in charmap:
      if columns != len(row):
        print charmap
        break

def total_length(array):
  total = 0
  for char in array:
    total = total + len(char)
  return total

def offsets(array, step):
  """Generate the table of offsets.

  |step| is the average width of all characters. A character's start and end
  points in the flattened array are then (c * step + offset[c]) and
  ((c+1) * step + offset[c+1])
  """
  off = []
  total = 0;
  # An extra entry at the end makes finding the last character easier.
  for i in xrange(len(array) + 1):
    off.append(total - i * step)
    if (i < len(array)):
      total = total + len(array[i])
  return off

def process():
  """Output the new font as a C file."""
  check_lengths(newfontmap.font)
  newarray = font_map_to_array(newfontmap.font)
  newarrayh = font_array_to_hex(newarray)
  off = offsets(newarray, 5)

  a = total_length(newarray)
  o = len(off)
  print "Total size is %d + %d = %d." % (a, o, a + o)

  f = io.open('newfont.txt', 'w')
  f.write('\nunsigned char font[] = ' + unicode(newarrayh).replace('[[', '{\n').replace('[', '').replace('], ', ',\n').replace(']]', ',\n};'))
  f.write('\n\nchar offset[] = ' + unicode(off).replace('[', '{\n').replace(']', '\n};'))
  f.close()
