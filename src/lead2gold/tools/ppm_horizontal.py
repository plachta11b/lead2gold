import ntpath
import re

from lead2gold.util import pwm2consensus
from lead2gold.tools.tool import Tool
from lead2gold.motif import Motif

from iteround import saferound

# from Bio.motifs.matrix import PositionWeightMatrix
import math

class PPM_horizontal(Tool):
	"""Class implementing a PPM_horizontal search tool motif convertor.
	"""

	toolName = "PPM_horizontal"

	def __init__(self):
		"""Initialize all class attributes with their default values.
		"""
		super(self.__class__, self).__init__(self.toolName)


	def parse(self, motif_file, type=None):
		"""Loads the searcher parameters specified in the configuration file.

		Args:
			motif_file: file containing one or more PPM_horizontal motifs.

		Returns:
			[Motif()]
		"""

		basename=ntpath.basename(motif_file.name)

		motifs = []

		match_letter = re.compile(r'[a-zA-Z]')
		# match_number = re.compile(r'[+-]?((\d+(\.\d+)?)|(\.\d+))')
		match_number = re.compile(r'[-+]?\d*\.\d+|\d+')
		
		match_matrix_brackets = re.compile(r'\[.*?\]')

		def num(s):
			try:
				return int(s)
			except ValueError:
				return float(s)

		alphabet_default = ["A", "C", "G", "T"]
		alphabet = []
		matrix = []
		for line in motif_file:
			clean_line = line.strip()
			numbers = match_number.findall(clean_line)
			matrix.append([num(e) for e in numbers])

		if not len(matrix):
			return []

		if len(alphabet) != len(matrix):
			alphabet = alphabet_default

		matrix = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

		motif = Motif(identifier=basename.replace(".","_"), pfm=matrix)
		motif.set_alphabet(alphabet)

		return [motif]
