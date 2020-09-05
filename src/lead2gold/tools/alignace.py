import ntpath
import re

from lead2gold.util import sequence2pwm
from lead2gold.util import pwm2consensus
from lead2gold.tools.tool import Tool
from lead2gold.motif import Motif

class AlignACE(Tool):
	"""Class implementing a AlignACE search tool motif convertor.
	"""

	toolName = "AlignACE"

	def __init__(self):
		"""Initialize all class attributes with their default values.
		"""
		super(self.__class__, self).__init__(self.toolName)


	def parse(self, motif_file, type=None):
		"""Loads the searcher parameters specified in the configuration file.

		Args:
			motif_file: file containing one or more AlignACE motifs.

		Returns:
			[Motif()]
		"""

		basename=ntpath.basename(motif_file.name)

		star_space_line=re.compile('^[\s\*]+$')

		def get_section(line, section, order):
			if "Motif " in line:
				return "sequences", 1
			if "MAP Score:" in line or star_space_line.match(line):
				return "summary", 2
			return section, order

		def get_template():
			return {
				"start": [],
				"sequences": [],
				"summary": []
			}

		motifs = []

		section = "start"
		order = 0
		t_motif = get_template()
		for line in motif_file:
			clean_line = line.strip()
			section, order_new = get_section(line, section, order)
			if order_new < order:
				motifs.append(self._parse_motif(t_motif, basename))
				t_motif = get_template()
			order = order_new

			t_motif[section].append(clean_line)

		motifs.append(self._parse_motif(t_motif, basename))
	
		return list(filter(None, motifs))

	def _parse_motif(self, t_motif, basename):

		if len(t_motif["sequences"]) < 2:
			return None

		# alphabet = []
		sequences = []
		name = t_motif["sequences"].pop(0)
		for line in t_motif["sequences"]:
			line_values = line.split()
			if len(line_values) == 4:
				sequences.append(line_values[0])
			else:
				break

		counters, alphabet = sequence2pwm(sequences)

		motif = Motif(identifier=name, counters=counters)
		consensus = pwm2consensus(motif.get_PPM())
		motif.set_alphabet(alphabet)
		motif.set_alternate_name(consensus)
		motif.set_source(basename)

		return motif
