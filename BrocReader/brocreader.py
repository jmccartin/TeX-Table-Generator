from confighandler import ConfigHandler
from physicsprocess import PhysicsProcess

class BrocReader(object):
	"""Controls the reading of the output files from the broc"""
	def __init__(self, cut_file, config_file):
		self.cut_file = open(cut_file, 'r')
		self.config_reader = ConfigHandler(config_file)
		
		
	def readfile(self):
		file_content = []
		processes = []
		accepted = {}
		overall = {}
		line = self.cut_file.readline()
                # Read over all non-empty lines in the input txt file
		while line != '':
			if '=-----------IMPOSED-CUTS-----------=' in line:
				line = self.cut_file.readline()
				values = {}
				while not '=----------------------------------=' in line:
					if 'identifier:' in line:
						process,channel,cutset = line.strip('identifier: ').split('|')
						values['process'] = process+'_'+channel
						values['cutset'] = cutset.strip('\n')
					elif 'cuts_passed' in line:
						values['cuts_passed'] = line.strip('cuts_passed: ').strip('\n')
					elif 'cuts_overall' in line:
						values['cuts_overall'] = line.strip('cuts_overall: ').strip('\n')
					line = self.cut_file.readline()
				accepted[values['process']] = []
				overall[values['process']] = []
				file_content.append(values)
			line = self.cut_file.readline()

                # Append the read-in values for cuts passed and overall to a dictionary with the process as the key
		for i in range(0,len(file_content)):
			accepted[file_content[i]['process']].append(float(file_content[i]['cuts_passed']))
			overall[file_content[i]['process']].append(float(file_content[i]['cuts_overall']))

		scaled_processes = {}
                scaled_processes_unc = {}
                sel_effs = {}

                # Loop over all processes and calculate the number of events at each cutstep for a given luminosity
		for process in accepted.keys():

			scaled_processes[process] = []
			scaled_processes_unc[process] = []
			
			try:
				preselection = self.config_reader.get_preselection(process)
			except: 
				# If no defined preselection in config, assume there is none (efficiency = 1)
				preselection = 1.0
			
			lumi = self.config_reader.get_lumi()
			
			# Set the cross section for data so that the PhysicsProcess class knows not to scale it
			if 'Data' in process:
				cross_section = -1
			else:
				cross_section = self.config_reader.get_cross_section(process)

			proc = PhysicsProcess(process)
			proc.events_accepted(accepted[process])
			proc.events_overall(overall[process])
			proc.preselection(preselection)
			proc.cross_section(cross_section)
			scaled_events,scaled_uncertainties = proc.get_scaled_events(lumi)
			scaled_processes[process] = scaled_events
			scaled_processes_unc[process] = scaled_uncertainties
			sel_effs[process] = []
			for i in range(0,len(accepted[process])):
				sel_effs[process].append(accepted[process][i]/overall[process][i])

		return scaled_processes, scaled_processes_unc, sel_effs
                
			
