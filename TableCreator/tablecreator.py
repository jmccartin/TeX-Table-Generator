import shutil
import os
import re
import collections
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
                self.datasets = self.config_reader.get_datasets()

		self.table_file = os.path.join(output_dir, 'table.tex')
		self.table_file = open(self.table_file, 'w')
		self.table_file.write(self.header)

                

        def writetable(self, processes):

                a = {}
                for dictionary in processes:
                        for key,value in dictionary.items():
                                a[key] = value

                print self.datasets
                print a.keys()

                channels = {}
                i = 0
                for dataset in self.datasets:
                        for element in a.keys():
                                name = re.search('('+str(dataset)+'\w+)', element)
                                if name:
                                        channels[name.groups()[0]] = i
                                        i += 1

                #for keys in a.keys():
                #print keys.split('_mu')[0]
                b = collections.OrderedDict()

                for key in sorted(a, key=channels.get):
                        print key, a[key]
                        b[key] = a[key]

                print b.values()

                c = map(list, zip(*b.values()))
                d = map(list, zip(b.values()))
                print c
                print d
                print ', '.join(str(x[0][1]) for x in d)

                #for i in range(3):
                #        print ', '.join(str(b.values()[x][i]) for x in b.values())

                #print ', '.join(str(x[0]) + ' & ' for x, y in b.values())
                

                #print ', '.join(str(y[0]) + ' & ' for x, y in b.values())

                l = [{'TTbar_mu_background': [27788.89963334056, 13115.937348527106, 3347.493030905431], 'TTbar_muon': [172984.55107924066, 74237.27154686248, 12724.78661393308]}, {'WJetsToLNu_TuneZ2Star_mu_background': [383179.1468881293, 261484.51429064505, 1587.9517304703465]}]

                #l = {'TTbar_mu_background': [27788.89963334056, 13115.937348527106, 3347.49303090543], 'TTbar_muon': [172984.55107924066, 74237.27154686248, 12724.78661393308]}

                #print ', '.join(str(x.values()) for x in l)

                #print ', '.join(str(x) + ' && ' for x, y in l.items())
                #print ', '.join(str(y[0]) + ' && ' for x, y in l.items())

