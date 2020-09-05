import ntpath
import re

from lead2gold.tools.tool import Tool
from lead2gold.motif import Motif

class Weeder(Tool):
	"""Class implementing a Weeder search tool motif convertor.
	"""

	toolName = "Weeder"

	def __init__(self):
		"""Initialize all class attributes with their default values.
		"""
		super(self.__class__, self).__init__(self.toolName)


	def parse(self, motif_file, type=None):
		"""Loads the searcher parameters specified in the configuration file.

		Args:
			motif_file: file containing one or more Weeder motifs.

		Returns:
			[Motif()]
		"""

		basename=ntpath.basename(motif_file.name)

		def get_section(line, section, order):
			if ">" in line:
				return "header", 1
			if not ">" in line:
				return "data", 2
			return section, order

		def get_template():
			return {
				"header": [],
				"data": []
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
		if not len(t_motif["header"]):
			return None

		header_list=t_motif["header"][0].replace(">","").split()
		matrix = []
		alphabet = []
		for row in t_motif["data"]:
			row_values = row.split()
			alphabet.append(row_values[0])
			matrix.append(row_values[1:])

		matrix2 = []
		first = True
		for row in matrix:
			for c, column in enumerate(row):
				if first:
					matrix2.append([float(column)])
				else:
					matrix2[c].append(float(column))
			first = False

		motif = Motif(identifier=header_list[0], ppm=matrix2)
		motif.set_alternate_name(header_list[1])

		return motif
