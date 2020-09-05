import ntpath
import re

from lead2gold.util import pwm2consensus
from lead2gold.tools.tool import Tool
from lead2gold.motif import Motif

class PWM_vertical(Tool):
	"""Class implementing a PWM_vertical search tool motif convertor.
	"""

	toolName = "PWM_vertical"

	def __init__(self):
		"""Initialize all class attributes with their default values.
		"""
		super(self.__class__, self).__init__(self.toolName)


	def parse(self, motif_file, type=None):
		"""Loads the searcher parameters specified in the configuration file.

		Args:
			motif_file: file containing one or more PWM_vertical motifs.

		Returns:
			[Motif()]
		"""

		basename=ntpath.basename(motif_file.name)

		motifs = []

		matrix = []
		for line in motif_file:
			clean_line = line.strip()
			values = [(2**float(e))*0.25 for e in clean_line.split()]
			matrix.append(values)


		return [Motif(identifier=basename, ppm=matrix)]
