import shutil
import os
import re
import collections
import math
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
                process_uncert_dict = {}
                for dictionary in processes:
                        for key,value in dictionary.items():
                                process_dict[key] = value
                for dictionary in processes_unc:
                        for key,value in dictionary.items():
                                process_uncert_dict[key] = value

                # Calculate the total events passed and associated uncertainties for each row
                combine_single_top = self.config_reader.combine_single_top()
                single_top_channels = self.config_reader.single_top_channels()
                combine_wjets = self.config_reader.combine_wjets()
                wjets_channels = self.config_reader.wjets_channels()
                decay_channel = self.config_reader.get_decay_channel()
                
                total_single_top = []
                total_single_top_uncert = []
                total_wjets = []
                total_wjets_uncert = []
                total_mc = []
                total_mc_uncert = []

                # Loop over cutsets
                for i in range(len(process_dict.values()[0])):
                        single_top = 0
                        single_top_uncert = 0
                        wjets = 0
                        wjets_uncert = 0
                        events_passed_total = 0
                        uncertainty_total = 0
                        # Loop over all datasets for the cutset
                        for j in range(len(process_dict.keys())):
                                key = process_dict.keys()[j]
                                if key[:4] != 'Data':
                                        events_passed_total += process_dict.values()[j][i]
                                        uncertainty_total += math.pow(process_uncert_dict.values()[j][i],2) # Sum the errors in quadrature
                                if combine_single_top:
                                        if process_dict.keys()[j].split('_')[0] + '_' + process_dict.keys()[j].split('_')[1] in single_top_channels:
                                                single_top += process_dict.values()[j][i]
                                                single_top_uncert += process_uncert_dict.values()[j][i]
                                if combine_wjets:
                                        # Combine the first two splits of the string due to naming conventions (ie W1Jets_TuneZ2)
                                        #print process_dict.keys()[j].split('_')[0] + '_' + process_dict.keys()[j].split('_')[1]
                                        #if process_dict.keys()[j].split('_')[0] + '_' + process_dict.keys()[j].split('_')[1] in wjets_channels:
                                        if process_dict.keys()[j].split('_')[0] in wjets_channels:
                                                wjets += process_dict.values()[j][i]
                                                wjets_uncert += process_uncert_dict.values()[j][i]
                        if combine_single_top:
                                total_single_top.append(single_top)
                                total_single_top_uncert.append(single_top_uncert)
                        if combine_wjets:
                                total_wjets.append(wjets)
                                total_wjets_uncert.append(wjets_uncert)
                        total_mc.append(events_passed_total)
                        total_mc_uncert.append(math.sqrt(uncertainty_total))

                # Create an ordered dictionary with associated values to the keys that were ordered in the previous step
                sorted_processes = collections.OrderedDict()
                sorted_uncerts = collections.OrderedDict()
                print 'Processing channels:'
                for i, dataset in enumerate(self.datasets):
                        ids = []
                        regex=re.compile(".*("+dataset+").*")
                        for id in [name.group(0) for l in process_dict.keys() for name in [regex.search(l)] if name]:
                                ids.append(id)
                        for id in ids:
                                if i == 0:
                                        if decay_channel == "electron":
                                                sorted_processes[ids[1]] = process_dict[ids[1]]
                                                sorted_uncerts[ids[1]] = process_uncert_dict[ids[1]]
                                                sorted_processes[ids[0]] = process_dict[ids[0]]
                                                sorted_uncerts[ids[0]] = process_uncert_dict[ids[0]]
                                        if decay_channel == "muon":
                                                sorted_processes[ids[1]] = process_dict[ids[1]]
                                                sorted_uncerts[ids[1]] = process_uncert_dict[ids[1]]
                                                sorted_processes[ids[0]] = process_dict[ids[0]]
                                                sorted_uncerts[ids[0]] = process_uncert_dict[ids[0]]

                                                #sorted_processes[id] = process_dict[id]
                                                #sorted_uncerts[id] = process_uncert_dict[id]
                                                
                                else:
                                        # If combining wjets or single top, don't add them into the dict just yet (ordering reasons)
                                        if (combine_single_top and id.split('_')[0] + '_' + id.split('_')[1] in single_top_channels) or (combine_wjets and id.split('_')[0] in wjets_channels):
                                                pass
                                        elif id.split('_')[0] == 'Data':
                                                data_name = id
                                        else:
                                                sorted_processes[id] = process_dict[id]
                                                sorted_uncerts[id] = process_uncert_dict[id]

                        # for element in process_dict.keys():
                        #         matched_name = re.search('('+str(dataset)+'\w+)', element)
                        #         if matched_name:
                        #                 id = matched_name.groups()[0]
                        #                 if i == 1:
                        #                         print id
                        #                 # If combining wjets or single top, don't add them into the dict just yet (ordering reasons)
                        #                 if (combine_single_top and id.split('_')[0] in single_top_channels) or (combine_wjets and id.split('_')[0] in wjets_channels):
                        #                         pass
                        #                 elif id.split('_')[0] == 'Data':
                        #                         data_name = id
                        #                 else:
                        #                         sorted_processes[id] = process_dict[id]
                        #                         sorted_uncerts[id] = process_uncert_dict[id]

                # Append Data and the totals calculated earlier back to the dict
                if combine_single_top:
                        sorted_processes['Single_Top'] = total_single_top
                        sorted_uncerts['Single_Top'] = total_single_top_uncert
                if combine_wjets:
                        sorted_processes['WJets'] = total_wjets
                        sorted_uncerts['WJets'] = total_wjets_uncert

                sorted_processes['Total_MC'] = total_mc
                sorted_uncerts['Total_MC'] = total_mc_uncert

                if self.config_reader.get_process_data_bool():
                        sorted_processes['Data'] = process_dict.get(data_name)
                        sorted_uncerts['Data'] = process_uncert_dict.get(data_name)

                # Calculate the efficiency and purity of the signal process
                eff = []
                pur = []
                eff_pur = []

                for i in range(0,len(sorted_processes[sorted_processes.keys()[0]])):
                        if self.config_reader.get_process_data_bool():
                                purity = sorted_processes[sorted_processes.keys()[0]][i]/sorted_processes[sorted_processes.keys()[-2]][i]
                        else:
                                purity = sorted_processes[sorted_processes.keys()[0]][i]/sorted_processes[sorted_processes.keys()[-1]][i]
                        efficiency = sorted_processes[sorted_processes.keys()[0]][i]/sorted_processes[sorted_processes.keys()[0]][0]
                        pur.append(purity)
                        eff.append(efficiency)
                        eff_pur.append(efficiency*purity)

                sorted_processes['Eff'] = eff
                sorted_processes['Pur'] = pur
                sorted_processes['EffPur'] = eff_pur

                row_label = self.config_reader.get_cutset_definitions()

                # Construct the header of the table based on the amount of datasets
                self.table_file.write(r'\documentclass[landscape, 12pt]{article}' +'\n' + r'\usepackage{lscape}' + '\n' + r'\usepackage[showframe=false]{geometry}' + '\n')
                self.table_file.write(r'\usepackage{changepage}' + '\n' + r'\begin{document}' + '\n\n')

                self.table_file.write(r'\begin{table}[!htbp]' +'\n')
                self.table_file.write(r'\begin{adjustwidth}{-3cm}{}' + '\n')

                self.table_file.write(r'\footnotesize'+'\n')
                self.table_file.write(r'\begin{tabular}{' + '|'.join('c' for x in range(len(sorted_processes.keys())+1)) + r'}' +'\n')

                # Write the names of the process + channel to each column
                self.table_file.write('\t & $ '+'$ & $'.join(str(self.config_reader.get_latex_dataset_name(x)) for x in sorted_processes.keys()) + r'$ \\ ' + '\n' + '\t' + r'\hline' + '\n')
                # Write the values + uncertainty to each column
                for i in range(len(sorted_processes.values()[0])):
                        self.table_file.write('\t' + str(row_label[i]) + '& $ ' + '$ & $'.join(str(int(x[i])) + r' \pm ' + str(int(y[i])) for x, y in zip(sorted_processes.values(), sorted_uncerts.values())) )
                        self.table_file.write('$ & $ {0:.{1}f}'.format(sorted_processes['Eff'][i], 3) + '$ & $ {0:.{1}f}'.format(sorted_processes['Pur'][i], 3) + '$ & $ {0:.{1}f}'.format(sorted_processes['EffPur'][i], 3))  
                        self.table_file.write(r'$ \\' + '\n')

                # Write the closing code to the table
                self.table_file.write('\t' + r'\hline' + '\n')
                self.table_file.write(r'\end{tabular}' + '\n')
                self.table_file.write(r'\end{adjustwidth}' + '\n')
                self.table_file.write(r'\end{table}' + '\n\n')
                self.table_file.write(r'\end{document}')

                print '\nCreated table: '+str(os.path.join(self.output_dir, 'table.tex'))
