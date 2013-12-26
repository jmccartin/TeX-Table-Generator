#!/usr/bin/env python

import sys,os,glob

from optparse import OptionParser
from BrocReader import brocreader
from BrocReader import confighandler
from TableCreator import tablecreator

parser = OptionParser()
parser.add_option("-x", "--eXecute", dest="execute", help="define config to run")
	
(options, args) = parser.parse_args()
	
if not options.execute:
	exit

config_name = os.path.join(options.execute)
config_reader = confighandler.ConfigHandler(config_name)

input_dir = config_reader.get_input_dir()
datasets = config_reader.get_datasets()

files_to_read = glob.glob(os.path.join(input_dir, '*.txt'))

scaled_datasets = []

# Find the files corresponding to the allowed names in the config
for file in files_to_read:
	name = file[:-4].split("/")[-1]
	if name in datasets:
		broc_reader = brocreader.BrocReader(file, config_name)
		scaled_events = broc_reader.readfile()
		scaled_datasets.append(scaled_events)

#for i in range(len(scaled_datasets)):
#	print scaled_datasets[i].keys()

table_creator = tablecreator.TableCreator(config_name)
table_creator.writetable(scaled_datasets)
		
