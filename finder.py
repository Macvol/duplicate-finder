#!/usr/bin/python

import sys, os, hashlib, re

ignore_hidden = False
ignore_pattern = ''
if len(sys.argv) > 2:
  ignore_hidden = True
  ignore_pattern = sys.argv[2]


file_list = list()
file_ignored = list()
file_missed = list()
file_keys = dict()

sys.stderr.write("Getting file list ...")
sys.stderr.flush()

for root, dir_names, file_names in os.walk(sys.argv[1]):
  for file_name in file_names:
    full_file_name = os.path.join(root, file_name)
    if ignore_hidden == True:
      if re.match(ignore_pattern, full_file_name):
        file_ignored.append(full_file_name)
      else:
        file_list.append(full_file_name)
    else:
      file_list.append(full_file_name)

sys.stderr.write("\r                                     \r")
sys.stderr.flush()

file_count = 0
for full_file_name in file_list:
    file_count += 1
    sys.stderr.write("\r%d/%d (%.0f%%)" % (file_count, len(file_list), 100 * float(file_count) / len(file_list)))
    sys.stderr.flush()

    #print full_file_name
    try:
      with open(full_file_name, 'rb') as input_file:
        file_key = hashlib.sha1(input_file.read()).hexdigest()
        if file_key in file_keys.keys():
          file_keys[file_key].update({full_file_name})
        else:
          file_keys.update({file_key : set({full_file_name})})
    except:
      file_missed.append(full_file_name)

sys.stderr.write("\r                                    \r")
sys.stderr.flush()

#if ignore_hidden == True:
#  print "Ignored:"
#  for file_name in file_ignored:
#    print "\t", file_name

print "Missed:"
for file_name in file_missed:
  print "\t", file_name

group_id = 1
for file_key in file_keys:
  if len(file_keys[file_key]) > 1:
    print "Duplicated [", group_id, "]:"
    for file_name in file_keys[file_key]:
      print "\t", file_name
    group_id += 1
