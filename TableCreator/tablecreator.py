import shutil
import os
import re
import collections
from BrocReader import confighandler

class TableCreator(object):
	"""Creates the LateX table for a range of processes"""

	def __init__(self, config_file):
		self.config_reader = confighandler.ConfigHandler(config_file)

		self.output_dir = self.config_reader.get_output_dir()
                self.datasets = self.config_reader.get_datasets()

                # Write the header information to the latex file
		self.table_file = os.path.join(self.output_dir, 'table.tex')
		self.table_file = open(self.table_file, 'w')
                
        def writetable(self, processes, processes_unc):

                # Sort the collection of all datasets into a single dictionary
                process_dict = {}
                process_unc_dict = {}
                for dictionary in processes:
                        for key,value in dictionary.items():
                                process_dict[key] = value
                for dictionary in processes_unc:
                        for key,value in dictionary.items():
                                process_unc_dict[key] = value

                # Create an ordered dictionary with associated values to the keys that were ordered in the previous step
                sorted_processes = collections.OrderedDict()
                sorted_uncerts = collections.OrderedDict()
                i = 0
                print 'Processing channels:'
                for dataset in self.datasets:
                        for element in process_dict.keys():
                                matched_name = re.search('('+str(dataset)+'\w+)', element)
                                if matched_name:
                                        id = matched_name.groups()[0]
                                        sorted_processes[id] = process_dict[matched_name.groups()[0]]
                                        sorted_uncerts[id] = process_unc_dict[matched_name.groups()[0]]

                # Calculate the total events passed and associated uncertainties for each row
                total_single_top = []
                total_single_top_uncert = []
                total_mc = []
                total_mc_uncert = []
                # If last dataset is 'Data', don't sum over values in Total MC calculation
                if self.config_reader.get_process_data_bool():
                        max_range = len(sorted_processes.values())-1
                else:
                        max_range = len(sorted_processes.values())

                combine_single_top = self.config_reader.combine_single_top()
                single_top_channels = self.config_reader.single_top_channels()
                
                # Loop over cutsets
                for j in range(len(sorted_processes.values()[0])):
                        single_top = 0
                        single_top_uncert = 0
                        events_passed_total = 0
                        uncertainty_total = 0
                        # Loop over all datasets for the cutset
                        for i in range(max_range):
                                events_passed_total += sorted_processes.values()[i][j]
                                uncertainty_total += sorted_uncerts.values()[i][j]
                                if combine_single_top:
                                        if sorted_processes.keys()[i].split('_')[0] in single_top_channels:
                                                single_top += sorted_processes.values()[i][j]
                                                single_top_uncert += sorted_uncerts.values()[i][j]
                        if combine_single_top:
                                total_single_top.append(single_top)
                                total_single_top_uncert.append(single_top_uncert)
                        total_mc.append(events_passed_total)
                        total_mc_uncert.append(uncertainty_total)

                # Append the totals back to the dict
                if combine_single_top:
                        sorted_processes['Single_Top'] = total_single_top
                        sorted_uncerts['Single_Top'] = total_single_top_uncert
                sorted_processes['Total_MC'] = total_mc
                sorted_uncerts['Total_MC'] = total_mc_uncert

                # Create a new dictionary in order to swap the first two elements over (ttbar channels), and the last two (data and total MC)
                sorted_processes_2 = collections.OrderedDict()
                sorted_uncerts_2 = collections.OrderedDict()
                max_iter = len(sorted_processes.keys())-1
                for i in range(max_iter+1):
                        if (i == 0):  # TTbar -> mu
                                sorted_processes_2[sorted_processes.keys()[1]] = sorted_processes.values()[1]
                                sorted_uncerts_2[sorted_uncerts.keys()[1]] = sorted_uncerts.values()[1]
                        elif (i == 1):  # TTbar -> other
                                sorted_processes_2[sorted_processes.keys()[0]] = sorted_processes.values()[0]
                                sorted_uncerts_2[sorted_uncerts.keys()[0]] = sorted_uncerts.values()[0]
                        if self.config_reader.get_process_data_bool():
                                if combine_single_top:
                                        print sorted_processes.keys()[i]

                                        if (i == max_iter-2):  # Data
                                                sorted_processes_2[sorted_processes.keys()[max_iter-1]] = sorted_processes.values()[max_iter-1] # Replace Data with Single Top
                                                sorted_uncerts_2[sorted_uncerts.keys()[max_iter-1]] = sorted_uncerts.values()[max_iter-1]
                                        elif (i == max_iter-1): # Single Top
                                                sorted_processes_2[sorted_processes.keys()[max_iter]] = sorted_processes.values()[max_iter] # Replace Single Top with Total MC
                                                sorted_uncerts_2[sorted_uncerts.keys()[max_iter]] = sorted_uncerts.values()[max_iter]
                                        elif (i == max_iter):  # Total MC
                                                sorted_processes_2[sorted_processes.keys()[max_iter-2]] = sorted_processes.values()[max_iter-2] # Replace Total MC with Data
                                                sorted_uncerts_2[sorted_uncerts.keys()[max_iter-2]] = sorted_uncerts.values()[max_iter-2]
                                        else:
                                                if sorted_processes.keys()[i].split('_')[0] not in single_top_channels:
                                                        sorted_processes_2[sorted_processes.keys()[i]] = sorted_processes.values()[i]
                                                        sorted_uncerts_2[sorted_uncerts.keys()[i]] = sorted_uncerts.values()[i]
                                else:
                                        if (i == max_iter-1):  # Data
                                                sorted_processes_2[sorted_processes.keys()[max_iter]] = sorted_processes.values()[max_iter] # Replace Data with Total MC
                                                sorted_uncerts_2[sorted_uncerts.keys()[max_iter]] = sorted_uncerts.values()[max_iter]
                                        elif (i == max_iter):  # Total MC
                                                sorted_processes_2[sorted_processes.keys()[max_iter-1]] = sorted_processes.values()[max_iter-1] # Replace Total MC with Data
                                                sorted_uncerts_2[sorted_uncerts.keys()[max_iter-1]] = sorted_uncerts.values()[max_iter-1]
                                        else:
                                                sorted_processes_2[sorted_processes.keys()[i]] = sorted_processes.values()[i]
                                                sorted_uncerts_2[sorted_uncerts.keys()[i]] = sorted_uncerts.values()[i]

                        else:
                                if combine_single_top:
                                        if sorted_processes.keys()[i].split('_')[0] not in single_top_channels:
                                                sorted_processes_2[sorted_processes.keys()[i]] = sorted_processes.values()[i]
                                                sorted_uncerts_2[sorted_uncerts.keys()[i]] = sorted_uncerts.values()[i]
                                                
                                else:
                                        sorted_processes_2[sorted_processes.keys()[i]] = sorted_processes.values()[i]
                                        sorted_uncerts_2[sorted_uncerts.keys()[i]] = sorted_uncerts.values()[i]

                row_label = self.config_reader.get_cutset_definitions()

                # Construct the header of the table based on the amount of datasets
                self.table_file.write(r'\documentclass[landscape, 12pt]{article}' +'\n' + r'\usepackage{lscape}' + '\n' + r'\usepackage[showframe=false]{geometry}' + '\n')
                self.table_file.write(r'\usepackage{changepage}' + '\n' + r'\begin{document}' + '\n')

                self.table_file.write(r'\begin{table}[!htbp]' +'\n')
                self.table_file.write(r'\begin{adjustwidth}{-3cm}{}' + '\n')

                self.table_file.write(r'\footnotesize'+'\n')
                self.table_file.write(r'\begin{tabular}{' + '|'.join('c' for x in range(len(sorted_processes_2.keys())+1)) + r'}' +'\n')

                # Write the names of the process + channel to each column
                self.table_file.write('\t Process & $ '+'$ & $'.join(str(self.config_reader.get_latex_dataset_name(x)) for x in sorted_processes_2.keys()) + r'$ \\ ' + '\n' + '\t' + r'\hline' + '\n')
                # Write the values + uncertainty to each column
                for i in range(len(sorted_processes_2.values()[0])):
                        self.table_file.write('\t' + str(row_label[i]) + '& $ ' + '$ & $'.join(str(int(x[i])) + r' \pm ' + str(int(y[i])) for x, y in zip(sorted_processes_2.values(), sorted_uncerts_2.values())) + r'$ \\' + '\n')

                # Write the closing code to the table
                self.table_file.write('\t' + r'\hline' + '\n')
                self.table_file.write(r'\end{tabular}' + '\n')
                self.table_file.write(r'\end{adjustwidth}' + '\n\n')
                self.table_file.write(r'\end{table}' + '\n')
                self.table_file.write(r'\end{document}')

                print '\nCreated table: '+str(os.path.join(self.output_dir, 'table.tex'))
