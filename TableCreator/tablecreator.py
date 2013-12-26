import shutil
import os
from BrocReader import confighandler

class TableCreator(object):
	"""Creates the LateX table for a range of processes"""

	header = '''\begin{table}[!htbp]
\begin{center}
    \footnotesize
        '''

	def __init__(self, config_file):
		self.config_reader = confighandler.ConfigHandler(config_file)

		output_dir = self.config_reader.get_output_dir()

		self.table_file = os.path.join(output_dir, 'table.tex')
		self.table_file = open(self.table_file, 'w')
		self.table_file.write(self.header)

	def writetable(self, processes):
		for i in range(len(processes)):
			for name in processes[i].keys():
				print name
				print processes[i][name]
