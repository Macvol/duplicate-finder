#!/usr/bin/python

import sys, os, hashlib, re, argparse

ignore_hidden = False
ignore_pattern = ''
if len(sys.argv) > 2:
  ignore_hidden = True
  ignore_pattern = sys.argv[2]

if len(sys.argv) == 1:
    print "Usage: %s <directory> <exclude regexp>" % (sys.argv[0])
    sys.exit()

file_list = list()
file_ignored = list()
file_missed = list()
file_keys = dict()
full_size = 0

sys.stderr.write("Getting file list ...")
sys.stderr.flush()

# Check all files.
for root, dir_names, file_names in os.walk(sys.argv[1]):
  for file_name in file_names:
    # Get full file name
    full_file_name = os.path.join(root, file_name)

    # Check real file
    if os.path.isfile(full_file_name):

      # Getting filesize
      try:
        file_size = os.path.getsize(full_file_name)

        # Dont process ignored files
        if ignore_hidden == True:
          if re.match(ignore_pattern, full_file_name):
            file_ignored.append(full_file_name)
          else:
            file_list.append((full_file_name, file_size))
            full_size += file_size
        else:
          file_list.append((full_file_name, file_size))
          full_size += file_size

      except:
        file_missed.append(full_file_name)

sys.stderr.write("\r                                     \r")
sys.stderr.flush()

file_count = 0
size_count = 0
for file_data in file_list:
    full_file_name = file_data[0]
    file_size = file_data[1]

    sys.stderr.write("\r%d/%d (%.0f%%)\t%d/%d (%.0f%%)" %
                     (file_count, len(file_list), 100. * float(file_count) / len(file_list),
                      size_count, full_size, 100. * float(size_count) / full_size))
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

    file_count += 1
    size_count += file_size

    sys.stderr.write("\r                                                     \r")
    sys.stderr.flush()

#if ignore_hidden == True:
#  print "Ignored:"
#  for file_name in file_ignored:
#    print "\t", file_name

if len(file_missed) > 0:
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
