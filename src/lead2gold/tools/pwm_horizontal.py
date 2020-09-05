import ntpath
import re

from lead2gold.util import pwm2consensus
from lead2gold.tools.tool import Tool
from lead2gold.motif import Motif

from iteround import saferound

# from Bio.motifs.matrix import PositionWeightMatrix
import math

class PWM_horizontal(Tool):
	"""Class implementing a PWM_horizontal search tool motif convertor.
	"""

	toolName = "PWM_horizontal"

	def __init__(self):
		"""Initialize all class attributes with their default values.
		"""
		super(self.__class__, self).__init__(self.toolName)


	def parse(self, motif_file, type=None):
		"""Loads the searcher parameters specified in the configuration file.

		Args:
			motif_file: file containing one or more PWM_horizontal motifs.

		Returns:
			[Motif()]
		"""

		basename=ntpath.basename(motif_file.name)

		motifs = []

		alphabet = ["A", "C", "G", "T"]
		matrix = []
		for line in motif_file:
			clean_line = line.strip()
			matrix.append([(2**(float(e)))*0.25 for e in clean_line.split()])

		matrix = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

		normalized_matrix = []
		for row in matrix:
			normalized_matrix.append(saferound([e / sum(row) for e in row], places=6))
			#normalized_matrix.append(saferound(row, places=6))

		return [Motif(identifier=basename, ppm=normalized_matrix)]
