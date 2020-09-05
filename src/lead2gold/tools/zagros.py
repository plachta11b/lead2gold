import ntpath
import re

from lead2gold.util import pwm2consensus
from lead2gold.tools.tool import Tool
from lead2gold.motif import Motif

class Zagros(Tool):
	"""Class implementing a Zagros search tool motif convertor.
	"""

	toolName = "Zagros"

	def __init__(self):
		"""Initialize all class attributes with their default values.
		"""
		super(self.__class__, self).__init__(self.toolName)


	def parse(self, motif_file, type=None):
		"""Loads the searcher parameters specified in the configuration file.

		Args:
			motif_file: file containing one or more Zagros motifs.

		Returns:
			[Motif()]
		"""

		basename=ntpath.basename(motif_file.name)

		def get_section(line, section, order):
			if "AC" in line[0:2]:
				return "name", 1
			if "TY" in line[0:2]:
				return "type", 2
			if "P0" in line[0:2]:
				return "matrix", 3
			if "BS" in line[0:2]:
				return "sites", 4
			return section, order

		def get_template():
			return {
				"start": [],
				"name": [],
				"type": [],
				"matrix": [],
				"sites": []
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
	
		return motifs

	def _parse_motif(self, t_motif):
		m_name=t_motif["name"][0].split()[1]
		m_type=t_motif["type"][0].split()[1]

		first = True
		alphabet = []
		matrix = []
		for row in t_motif["matrix"]:
			if first:
				first = False
				alphabet = row.split()
				# P0\tA\tC\tG\tT remove P0
				alphabet.pop(0)
			elif len(row.split()) > len(alphabet):
				matrix.append([float(value) for value in row.split()[1:]])

		motif = Motif(identifier=m_name, pfm=matrix)
		consensus = pwm2consensus(matrix)
		motif.set_alternate_name(consensus)

		return motif

