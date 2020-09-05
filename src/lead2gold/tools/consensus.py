import ntpath
import re

from lead2gold.util import pwm2consensus
from lead2gold.tools.tool import Tool
from lead2gold.motif import Motif

class Consensus(Tool):
	"""Class implementing a Consensus sequence convertor.
	"""

	toolName = "Consensus"

	def __init__(self):
		"""Initialize all class attributes with their default values.
		"""
		super(self.__class__, self).__init__(self.toolName)

	def parse(self, motif_file, type=None):
		"""Loads the searcher parameters specified in the configuration file.

		Args:
			motif_file: file of the Consensus motif.

		Returns:
			[Motif()]
		"""


	def print(self, motifs, file):

		if not motifs:
			return

		for motif in motifs:

			pwm = motif.get_PPM()

			consensus = pwm2consensus(pwm)

			if consensus:
				file.write("{}\n".format(consensus))
