import ntpath
import re
import string
from iteround import saferound

from lead2gold.motif import Motif
from lead2gold.tools.tool import Tool

from math import gcd
from functools import reduce

class TRANSFAC(Tool):
	"""Class implementing a TRANSFAC motif convertor.
	"""

	toolName = "TRANSFAC"

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
			if "ID" in line[0:2]:
				return "name", 1
			if "BF" in line[0:2]:
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
		consensus = []
		for row in t_motif["matrix"]:
			if first:
				first = False
				alphabet = row.split()
				# P0\tA\tC\tG\tT remove P0
				alphabet.pop(0)
			elif len(row.split()) > len(alphabet):
				# print(row)
				row_values=row.split()
				if row_values[-1].isalpha():
					consensus.append(row_values.pop(-1))
				matrix.append([float(value) for value in row_values[1:]])

		motif = Motif(identifier=m_name, pfm=matrix)
		if not consensus:
			consensus = pwm2consensus(matrix)
		motif.set_alternate_name("".join(consensus))

		return motif

	def print(self, motifs, file):

		### https://biopython.org/docs/dev/api/Bio.motifs.transfac.html
		### http://meme-suite.org/doc/transfac-format.html
		### example from meme motif suite
		# ID any_old_name_for_motif_2
		# BF species_name_for_motif_2
		# P0      A      C      G      T
		# 01      2      1      2      0      R
		# 02      1      2      2      0      S
		# 03      0      5      0      0      C
		# 04      3      0      1      1      A
		# 05      0      0      4      1      G
		# 06      5      0      0      0      A
		# 07      0      1      4      0      G
		# 08      0      0      5      0      G
		# 09      0      0      0      5      T
		# 10      0      2      0      3      Y
		# 11      0      1      2      2      K
		# 12      1      0      3      1      G
		# XX

		for motif in motifs:

			identifier = motif.get_identifier()
			name = motif.get_alternate_name()
			alphabet = motif.get_alphabet()
			if not motif.get_length():
				continue

			# header
			if name:
				file.write("ID {}_{}\n".format(identifier,name))
			else:
				file.write("ID {}\n".format(identifier))
			file.write("BF unknown_species\n")

			# alphabet
			file.write("P0\t{}\n".format('\t'.join(alphabet)))

			# matrix
			matrix = motif.get_PPM()
			m_max = max(map(max, matrix))
			m_min = min(map(min, matrix))
			large_matrix = [[round(j * 10**6) for j in i] for i in matrix]
			m_gcd = reduce(gcd, [reduce(gcd, row) for row in large_matrix])
			denormalized_matrix = [[(j // m_gcd) for j in i] for i in large_matrix]

			for i, row in enumerate(denormalized_matrix):
				index = str(i).zfill(2)
				values = '\t'.join([str(e) for e in row])
				letter_max = str(alphabet[row.index(max(row))])
				file.write("{}\t{}\t{}\n".format(index,values,letter_max))

			# end
			file.write("XX\n\n")
