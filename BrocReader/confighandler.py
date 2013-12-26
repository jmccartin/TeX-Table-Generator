import ConfigParser
import os

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
		
	def get_cross_section(self, process):
		return self.get('cross_sections', process)		
	
	def get_lumi(self):
		return self.get('default', 'lumi')
