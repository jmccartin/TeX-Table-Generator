import math

class PhysicsProcess(object):
	"""Stores the selection efficiencies for a physics process"""

	def __init__(self, process):
		self.process = process

	def events_accepted(self, events_accepted):
		self.events_accepted = events_accepted

	def events_overall(self, events_overall):
		self.events_overall = events_overall

	def cross_section(self, cross_section):
		self.cross_section = float(cross_section)

        def preselection(self, preselection):
                self.preselection = float(preselection)

	def get_scaled_events(self, lumi):
		events_accepted_normalised = []
                event_uncertainties = []

                # Loop over each cutstep and scale the events according to their cross-sections
		for i in range(0, len(self.events_accepted)):
                        if (self.cross_section == -1):  # Data
                                events_accepted_normalised.append(self.events_accepted[i])
                                event_uncertainties.append(0)
                        else:
                                selection_efficiency = self.events_accepted[i]/self.events_overall[i]
                                normalised_events = self.preselection * selection_efficiency * self.cross_section * float(lumi) * 1000
                                if selection_efficiency != 0:
                                        raw_frac_uncertainty = (1/math.sqrt(self.events_accepted[i]))
                                else:
                                        raw_frac_uncertainty = 0
                                normalised_uncertainty = raw_frac_uncertainty*normalised_events
                                events_accepted_normalised.append(normalised_events)
                                event_uncertainties.append(normalised_uncertainty)

                # Return a list of the normalised events and their uncertainties
		return events_accepted_normalised, event_uncertainties


