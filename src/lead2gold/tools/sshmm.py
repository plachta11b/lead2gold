import ntpath
import re

from lead2gold.util import pwm2consensus
from lead2gold.tools.tool import Tool
from lead2gold.motif import Motif

class ssHMM(Tool):
	"""Class implementing a ssHMM search tool motif convertor.
	"""

	toolName = "ssHMM"

	def __init__(self):
		"""Initialize all class attributes with their default values.
		"""
		super(self.__class__, self).__init__(self.toolName)


	def parse(self, motif_file, type=None):
		"""Loads the searcher parameters specified in the configuration file.

		Args:
			motif_file: file containing one or more ssHMM motifs.

		Returns:
			[Motif()]
		"""

		basename=ntpath.basename(motif_file.name)

		first_line = True
		alphabet = []
		matrix = []
		for line in motif_file:
			clean_line = line.strip()
			if first_line:
				first_line = False
				alphabet = [value for value in clean_line.split()]
			else:
				matrix.append([float(value) for value in clean_line.split()])

		consensus = pwm2consensus(matrix)

		motif = Motif(identifier=consensus, ppm=matrix)
		motif.set_alphabet(alphabet)
		motif.set_source(basename)

		return [motif]
