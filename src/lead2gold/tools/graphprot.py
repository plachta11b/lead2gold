import ntpath

from lead2gold.tools.tool import Tool
from lead2gold.util import sequence2pwm
from lead2gold.motif import Motif

class GraphProt(Tool):
	"""Class implementing a GraphProt search tool motif convertor.
	"""

	toolName = "GraphProt"

	def __init__(self):
		"""Initialize all class attributes with their default values.
		"""
		super(self.__class__, self).__init__(self.toolName)


	def parse(self, motif_file, type=None):
		"""Loads the searcher parameters specified in the configuration file.

		Args:
			motif_file: file of the GraphProt motif.

		Returns:
			[Motif()]
		"""

		lines = motif_file.read().splitlines()
		counters, _ = sequence2pwm(lines)

		basename=ntpath.basename(motif_file.name)

		motif = Motif(identifier=basename, counters=counters)
		motif.set_source(basename)
		motif.set_number_of_sites(len(lines))

		return [motif]



