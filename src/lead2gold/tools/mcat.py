import ntpath
import re
import string

from lead2gold.tools.tool import Tool
from lead2gold.motif import Motif

class MCAT(Tool):
	"""Class implementing a MCAT search tool motif convertor.
	"""

	toolName = "MCAT"

	def __init__(self):
		"""Initialize all class attributes with their default values.
		"""
		super(self.__class__, self).__init__(self.toolName)


	def parse(self, motif_file, type=None):
		"""Loads the searcher parameters specified in the configuration file.

		Args:
			motif_file: file of the MCAT motif.

		Returns:
			[Motif()]
		"""

		basename=ntpath.basename(motif_file.name)

		motifs=[]

		def create_motif(name,length,score,matrix,alphabet,instances):

			print(name)
			print(matrix)

			motif = Motif(name, ppm=matrix)

			motif.set_enrichment(score)
			motif.set_alphabet(alphabet)
			motif.set_e(score)

			motif.set_number_of_sites(instances)
			return motif

		def get_section(line, section):
			if "Motif:" in line:
				return "name"
			if "Length:" in line:
				return "length"
			if "Comparison Score:" in line:
				return "score"
			if "Position Weight Matrix" in line:
				return "matrix"
			if "instances found" in line:
				return "instances"
			if "</h4>" in line:
				return "next_motif"
				
			return section

		rows_name = []
		rows_length = []
		rows_score = []
		rows_matrix = []
		rows_instances = []
		section=""
		for line in motif_file:
			# removing trailing tabs too
			clean_line = line.strip()
			section = get_section(clean_line, section)
			if section == "name":
				rows_name.append(clean_line)
			if section == "length":
				rows_length.append(clean_line)
			if section == "score":
				rows_score.append(clean_line)
			if section == "matrix":
				rows_matrix.append(clean_line)
			if section == "instances":
				rows_instances.append(clean_line)
			if section == "next_motif":
				if rows_name and rows_matrix:
					name = self._parse_name(rows_name,motifs)
					length = self._parse_length(rows_length)
					e,z = self._parse_score(rows_score)
					matrix, alphabet = self._parse_matrix(rows_matrix,length)
					instances = self._parse_instances(rows_instances)
					motifs.append(create_motif(name,length,e,matrix,alphabet,instances))
				rows_name = []
				rows_length = []
				rows_score = []
				rows_matrix = []
				rows_instances = []
				section = ""

		return motifs


	def _parse_name(self, rows, motifs):
		try:
			# <h1>Motif: GACGTA</h1>
			return "M" + str(len(motifs)) + "_" + rows[0].split("Motif:")[-1].replace("</h1>","").strip()
		except:
			return "NONAME_ERROR"

	def _parse_length(self, rows):
		# Length: 6<br>
		return int(''.join(re.findall('\d+', rows[0])))

	def _parse_score(self, rows):
		# Comparison Score: 10535.000<br>Log Likelihood: 10.935<br>P-value: 1.829e-40<br>Z-Score: 1.247e+01<br>
		values = rows[0].split("<br>")
		e = 0
		z = 0
		for value in values:
			if "P-value:" in value:
				try:
					e = float(value.split(":")[1])
				except:
					print("invalid p-value")
			if "Z-Score:" in value:
				try:
					z = float(value.split(":")[1])
				except:
					print("invalid z-score")
		return (e,z)



	def _parse_matrix(self, rows, length):

		# <pre style="margin-top: 0px; margin-bottom: 0px;">A: 0.01 | 0.93 | 0.02 | 0.01 | 0.09 | 0.65 | 
		# C: 0.02 | 0.02 | 0.95 | 0.03 | 0.08 | 0.06 | 
		# G: 0.95 | 0.05 | 0.01 | 0.95 | 0.04 | 0.09 | 
		# T: 0.02 | 0.01 | 0.02 | 0.02 | 0.79 | 0.20 | 
		# N: 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 

		matrix = []
		alphabet = []
		for line in rows:
			if ">" in line:
				line = line.split(">")[-1]
			if ":" in line:
				data = line.split(":")
				letter = re.findall('[A-Z]', data[0])[0]
				values = data[-1].split("|")
				row = []
				for value in values:
					value = value.strip()
					if value:
						row.append(float(value))
				if len(row) == length and (sum(row) > 0 or (not 'N' in letter)):
					if 'N' in letter:
						# todo fix later with param
						continue
					alphabet.append(letter)
					matrix.append(row)


		matrix = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

		return matrix, alphabet

	def _parse_instances(self, rows):
		return int(''.join(re.findall('\d+', rows[0])))
