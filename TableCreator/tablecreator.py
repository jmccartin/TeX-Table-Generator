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

                # Arrange the keys of the dictionary into the order defined in 'datasets' specified in the config
                channels = {}
                i = 0
                for dataset in self.datasets:
                        for element in process_dict.keys():
                                # Regexp the name of the dataset given the base name that appears in the config
                                name = re.search('('+str(dataset)+'\w+)', element)
                                if name:
                                        channels[name.groups()[0]] = i
                                        i += 1

                # Create an ordered dictionary with associated values to the keys that were ordered in the previous step
                sorted_processes = collections.OrderedDict()
                for key in sorted(process_dict, key=channels.get):
                        # Look up the latex translation for the given dataset name from the config
                        name = self.config_reader.get_latex_dataset_name(str(key))
                        sorted_processes[name] = process_dict[key]

                # Create an ordered dictionary with associated uncertainty values to the keys that were ordered in the previous step
                sorted_uncerts = collections.OrderedDict()
                for key in sorted(process_unc_dict, key=channels.get):
                        # Look up the latex translation for the given dataset name from the config
                        name = self.config_reader.get_latex_dataset_name(str(key))
                        sorted_uncerts[name] = process_unc_dict[key]

                # Map the values to a list so a total can be appended to it later
                events = map(list, sorted_processes.values())
                event_uncerts = map(list, sorted_uncerts.values())

                # Calculate the total events passed and associated uncertainties for each row
                total_mc = []
                total_mc_uncert = []
                for j in range(len(events[0])):
                        events_passed_total = 0
                        uncertainty_total = 0
                        for i in range(len(events)):
                                events_passed_total += events[i][j]
                                uncertainty_total += event_uncerts[i][j]
                        total_mc.append(events_passed_total)
                        total_mc_uncert.append(uncertainty_total)
                # Append the totals back to the mapped list
                events.append(total_mc)
                event_uncerts.append(total_mc_uncert)

                # Write the names of the process + channel to each column
                self.table_file.write(' & '.join(str(x) for x in sorted_processes.keys()) + ' & ')
                self.table_file.write(r'Total MC \\' + '\n')
                # Write the values + uncertainty to each column
                for i in range(len(events[0])):
                        self.table_file.write('\t' + ' & '.join(str(int(x[i])) + r' \pm ' + str(int(y[i])) for x, y in zip(events, event_uncerts)) + r' \\' + '\n')

                # Write the closing code to the table
                self.table_file.write('\t' + r'\hline' + '\n')
                self.table_file.write(r'\end{table}' + '\n')
                self.table_file.write(r'\end{center}' + '\n')
