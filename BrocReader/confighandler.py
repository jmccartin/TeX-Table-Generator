import ConfigParser
import os

run_on_data = False

class ConfigHandler(ConfigParser.RawConfigParser):
	"""Gets and holds the config variables"""

	def __init__(self, config_name):
		ConfigParser.RawConfigParser.__init__(self)
		
		if not os.path.exists(config_name):
			raise IOError("cannot find configuation:"+config_name+", exiting...")
		
		self.read(config_name)

		
	def get_output_dir(self):
		return self.get('default', 'output_dir')

	def get_input_dir(self):
		return self.get('default', 'input_dir')

	def get_datasets(self):
		return self.get('default', 'datasets').split(":")
        
        def get_preselection(self, process):
                return self.get('preselection', process)
		
	def get_cross_section(self, process):
		return self.get('cross_sections', process)		
	
	def get_lumi(self):
		return self.get('default', 'lumi')

        def get_latex_dataset_name(self, name):
                return self.get('latex', name)

        def set_process_data_bool(self, run_on_data_bool):
                global run_on_data
                run_on_data = run_on_data_bool

        def get_process_data_bool(self):
                return run_on_data
        
        def get_cutset_definitions(self):
                return self.get('default', 'cutset_definitions').split(':')

        def combine_single_top(self):
                return self.getboolean('default', 'combine_single_top')

        def single_top_channels(self):
                return self.get('default', 'single_top_channels').split(':')

        def combine_wjets(self):
                return self.getboolean('default', 'combine_wjets')

        def wjets_channels(self):
                return self.get('default', 'wjets_channels').split(':')
