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

	def get_scaled_events(self, lumi):
		events_accepted_normalised = []
		for i in range(0, len(self.events_accepted)):
			efficiency = float(self.events_accepted[i]/self.events_overall[i])
			normalised_events =	efficiency * self.cross_section * float(lumi) * 1000
			events_accepted_normalised.append(normalised_events)
		return events_accepted_normalised

