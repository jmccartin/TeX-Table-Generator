#!/usr/bin/env python

import sys,os,glob

from optparse import OptionParser
from BrocReader import brocreader
from BrocReader import confighandler
from TableCreator import tablecreator

# Parse config and input files to the program
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


# Declare arrays
datasets_read = []
scaled_datasets = []
scaled_datasets_unc = []
overall_wevents_dict = {}

# Find the files corresponding to the allowed names in the config
for file in files_to_read:
        print 'Reading ' + str(file) + '...'
	name = file[:-4].split("/")[-1]
        broc_reader = brocreader.BrocReader(file, config_name)
        scaled_events, scaled_uncertainties, overall_wevents = broc_reader.readfile()
        scaled_datasets.append(scaled_events)
        scaled_datasets_unc.append(scaled_uncertainties)
        for key,value in overall_wevents.items():
                overall_wevents_dict[key] = value

        datasets_read.append(name)

if 'Data' in datasets_read:
        config_reader.set_process_data_bool(True)

print '\nCreating table...\n'
# Initalise and write the table
table_creator = tablecreator.TableCreator(config_name)
table_creator.writetable(scaled_datasets, scaled_datasets_unc, overall_wevents_dict)
		
