import ntpath
import re

from lead2gold.tools.tool import Tool
from lead2gold.motif import Motif

class MDS(Tool):
	"""Class implementing a MDS search tool motif convertor.
	"""

	toolName = "MDS"

	def __init__(self):
		"""Initialize all class attributes with their default values.
		"""
		super(self.__class__, self).__init__(self.toolName)


	def parse(self, motif_file, type=None):
		"""Loads the searcher parameters specified in the configuration file.

		Args:
			motif_file: file of the MDS motif.

		Returns:
			[Motif()]
		"""

		basename=ntpath.basename(motif_file.name)

		matrix=[]
		first_line = True
		for line in motif_file:
			# removing trailing tabs too
			clean_line = line.strip()
			if first_line == True:
				first_line = False
				alphabet = clean_line.split('\t')
				alphabet.pop(0)
			else:
				row_values = clean_line.split('\t')
				row_values.pop(0)
				matrix.append([float(i) for i in row_values])

		identifier = re.sub('PPM-([a-zA-Z\[\]]*).txt', r'\1', basename)
		motif = Motif(identifier=identifier, pfm=matrix)

		return [motif]
