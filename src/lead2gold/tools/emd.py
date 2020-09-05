import ntpath

from lead2gold.tools.tool import Tool
from lead2gold.util import pwm2consensus
from lead2gold.util import sequence2pwm
from lead2gold.motif import Motif

class EMD(Tool):
	"""Class implementing a EMD search tool motif convertor.
	"""

	toolName = "EMD"

	def __init__(self):
		"""Initialize all class attributes with their default values.
		"""
		super(self.__class__, self).__init__(self.toolName)

	def parse(self, motif_file, type=None):
		"""Loads the searcher parameters specified in the configuration file.

		Args:
			motif_file: file containing one or more EMD motifs.

		Returns:
			[Motif()]
		"""

		basename=ntpath.basename(motif_file.name)

		def get_section(line, section, order):
			if len(line) < 2:
				return "stop", 1
			if "Motif " in line[0:8]:
				return "name", 2
			return section, order

		def get_template():
			return {
				"start": [],
				"stop": [],
				"name": []
			}

		motifs = []

		section = "start"
		order = 0
		t_motif = get_template()
		for line in motif_file:
			clean_line = line.strip()
			section, order_new = get_section(line, section, order)
			if order_new < order:
				motifs.append(self._parse_motif(t_motif))
				t_motif = get_template()
			order = order_new

			t_motif[section].append(clean_line)

		motifs.append(self._parse_motif(t_motif))
	
		return list(filter(None, motifs))

	def _parse_motif(self, t_motif):

		name = t_motif["name"].pop(0)

		sequences = []
		for row in t_motif["name"]:
			row_values = row.split()
			if len(row_values) == 4:
				sequences.append(row_values[0])

		counters, _ = sequence2pwm(sequences)

		motif = Motif(identifier=name, counters=counters)

		consensus = pwm2consensus(motif.get_PPM())
		motif.set_number_of_sites(len(sequences))
		motif.set_alternate_name(consensus)

		return motif
