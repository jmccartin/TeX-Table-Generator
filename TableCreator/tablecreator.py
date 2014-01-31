import shutil
import os
import re
import collections
from BrocReader import confighandler

class TableCreator(object):
	"""Creates the LateX table for a range of processes"""

	header = r'''\begin{table}[!htbp]
\begin{center}
    \footnotesize
        '''

	def __init__(self, config_file):
		self.config_reader = confighandler.ConfigHandler(config_file)

		output_dir = self.config_reader.get_output_dir()
                self.datasets = self.config_reader.get_datasets()

                # Write the header information to the latex file
		self.table_file = os.path.join(output_dir, 'table.tex')
		self.table_file = open(self.table_file, 'w')
		self.table_file.write(self.header)

                

        def writetable(self, processes, processes_unc):

                # Resort the collection of all datasets into a single dictionary
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
                for dataset in self.datasets:
                        for element in process_dict.keys():
                                matched_name = re.search('('+str(dataset)+'\w+)', element)
                                if matched_name:
                                        translated_id = self.config_reader.get_latex_dataset_name(str(matched_name.groups()[0]))
                                        sorted_processes[translated_id] = process_dict[matched_name.groups()[0]]
                                        sorted_uncerts[translated_id] = process_unc_dict[matched_name.groups()[0]]

                sorted_processes_2 = collections.OrderedDict()
                for i in range(len(sorted_processes.keys())):
                        if (i == 0):
                                sorted_processes_2[sorted_processes.keys()[1]] = sorted_processes.values()[1]
                        elif (i == 1):
                                sorted_processes_2[sorted_processes.keys()[0]] = sorted_processes.values()[0]
                        else:
                                sorted_processes_2[sorted_processes.keys()[i]] = sorted_processes.values()[i]

                # Calculate the total events passed and associated uncertainties for each row
                total_mc = []
                total_mc_uncert = []
                for j in range(len(sorted_processes.values()[0])):
                        events_passed_total = 0
                        uncertainty_total = 0
                        for i in range(len(sorted_processes.values())):
                                events_passed_total += sorted_processes.values()[i][j]
                                uncertainty_total += sorted_uncerts.values()[i][j]
                        total_mc.append(events_passed_total)
                        total_mc_uncert.append(uncertainty_total)

                # Append the totals back to the dict
                sorted_processes['Total MC'] = total_mc
                sorted_uncerts['Total MC'] = total_mc_uncert

                # Write the names of the process + channel to each column
                self.table_file.write(' & '.join(str(x) for x in sorted_processes.keys()) + r' \\ ' + '\n')
                # Write the values + uncertainty to each column
                for i in range(len(sorted_processes.values()[0])):
                        self.table_file.write('\t' + ' & '.join(str(int(x[i])) + r' \pm ' + str(int(y[i])) for x, y in zip(sorted_processes.values(), sorted_uncerts.values())) + r' \\' + '\n')

                # Write the closing code to the table
                self.table_file.write('\t' + r'\hline' + '\n')
                self.table_file.write(r'\end{table}' + '\n')
                self.table_file.write(r'\end{center}' + '\n')
