""" Abstract class module for unified
"""

from abc import abstractmethod 
from lead2gold.motif.motif import Motif

class Tool():
	"""Base abstract class for known tools and required functions
	"""

	def __init__(self, toolName):
		"""Initialize all class attributes with their default values.
		"""
		self.toolName = toolName

	@abstractmethod
	def parse(self, file_path, type=None):
		"""Parse the motif from given motif file.
		Tool should recognize input type but for speedup this can be skipped by adding $type param.
		Function should raise as soon as posible if motif does not seems to be in valid format.

		Args:
			path: path of the motif file.
			type: type of tool output (stdout, .meme, .w2, etc.)

		Returns:
			Returns [Motif()].
		"""
		return [Motif()]

	@abstractmethod
	def print(self, motif, file_path):
		"""Performs motif search.

		Args:
			motif: object Motif for
			file_path: file where motif would be saved.

		Returns:
			Returns None
		"""
		return None
