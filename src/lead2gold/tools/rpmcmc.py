import ntpath
import re

from lead2gold.util import pwm2consensus
from lead2gold.tools.tool import Tool
from lead2gold.motif import Motif

class RPMCMC(Tool):
	"""Class implementing a RPMCMC search tool motif convertor.
	"""

	toolName = "RPMCMC"

	def __init__(self):
		"""Initialize all class attributes with their default values.
		"""
		super(self.__class__, self).__init__(self.toolName)


	def parse(self, motif_file, type=None):
		"""Loads the searcher parameters specified in the configuration file.

		Args:
			motif_file: file containing one or more RPMCMC motifs.

		Returns:
			[Motif()]
		"""

		basename=ntpath.basename(motif_file.name)

		def get_section(line, section, order):
			if "motif" in line.lower():
				return "header", 1
			if "A C G T" in line.upper():
				return "matrix", 2
			return section, order

		def get_template():
			return {
				"start": [],
				"header": [],
				"matrix": []
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
		identifier = ""
		alphabet = []
		matrix = []
		if t_motif["header"]:
			identifier = t_motif["header"][0]
		if t_motif["matrix"]:
			alphabet = t_motif["matrix"][0].split()
			t_motif["matrix"].pop(0)
			for row in t_motif["matrix"]:
				row_values = [float(value) for value in row.split()]
				if len(row_values) == len(alphabet):
					matrix.append(row_values)
				else:
					break

		consensus = pwm2consensus(matrix)


		motif = Motif(identifier=identifier, ppm=matrix)
		motif.set_alphabet(alphabet)
		motif.set_source(basename)
		motif.set_alternate_name(consensus)

		return motif
