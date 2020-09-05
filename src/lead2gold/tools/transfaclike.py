import ntpath
import re
import string
from iteround import saferound

from lead2gold.motif import Motif
from lead2gold.tools.tool import Tool

class TRANSFAClike(Tool):
	"""Class implementing a TRANSFAClike motif convertor.
	"""

	toolName = "TRANSFAClike"

	def __init__(self):
		"""Initialize all class attributes with their default values.
		"""
		super(self.__class__, self).__init__(self.toolName)

	def parse(self, motif_file, type=None):
		"""Loads the searcher parameters specified in the configuration file.

		Args:
			motif_file: file containing motif file in TRANSFAClike format.

		Returns:
			[Motif()]
		"""
		pass
		# This is a TRANSFAC-like format having a header starting with “DE” then the matrix ID,
		# the matrix name and the matrix class. The data itself is transposed as compared to the other formats,
		# meaning that each line correspond to a column in the matrix.
		# The column lines start with a number denoting the column index (counting from 0).
		# After that follows tab separated counts for each base in that column in the order: A,C,G and T.
		# After the lines with the counts follows a final line containing the string: “XX”.

	def print(self, motifs, file):
		print("not implemented yet")
		pass

