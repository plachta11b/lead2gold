import ntpath
import re

from lead2gold.tools.tool import Tool
from lead2gold.motif import Motif

class CMF(Tool):
	"""Class implementing a CMF search tool motif convertor.
	"""

	toolName = "CMF"

	def __init__(self):
		"""Initialize all class attributes with their default values.
		"""
		super(self.__class__, self).__init__(self.toolName)


	def parse(self, motif_file, type=None):
		"""Loads the searcher parameters specified in the configuration file.

		Args:
			motif_file: file of the CMF motif.

		Returns:
			[Motif()]
		"""

		basename=ntpath.basename(motif_file.name)

		motifs=[]

		def create_motif(header,matrix,alphabet,positive_sites,negative_sites):
			# header_values = self._parse_header(header)
			# motif = Motif(ppm=matrix, identifier=header_values["motif_name"])
			# motif.set_alternate_name(header_values["consensus_sequence"])
			# motif.set_e(2**float(header_values["logp_value"]))
			# op = header_values["occurence"]["primary"]
			# # T:14.0(4.67%) => 14
			# motif.set_number_of_sites()
			# motif.set_source(basename)

			motif = Motif(header["identificator"], ppm=matrix)

			# 2.90668(log2) => 2.90668
			e = re.sub('([0-9]+\.*)\(log2\)', r'\1', header["enrichment"])
			motif.set_enrichment(2**(float(e)))

			motif.set_number_of_sites(len(positive_sites))
			return motif

		def get_section(line, section):
			if "MOTIF:" in line:
				return "header"
			if "PWM:" in line:
				return "matrix"
			if "Positive Sites:" in line:
				return "pos_site"
			if "Negative Sites:" in line:
				return "neg_site"
			if "####################" in line:
				return "next_motif"
			return section

		rows_header=[]
		rows_matrix=[]
		rows_positive_sites=[]
		rows_negative_sites=[]
		section=""
		for line in motif_file:
			# removing trailing tabs too
			clean_line = line.strip()
			section = get_section(clean_line, section)
			if section == "header":
				rows_header.append(clean_line)
			if section == "matrix":
				rows_matrix.append(clean_line)
			if section == "pos_site":
				rows_positive_sites.append(clean_line)
			if section == "neg_site":
				rows_negative_sites.append(clean_line)
			if section == "next_motif":
				if rows_header and rows_matrix:
					header = self._parse_header(rows_header)
					matrix, alphabet = self._parse_matrix(rows_matrix)
					positive_sites = self._parse_sites(rows_positive_sites)
					negative_sites = self._parse_sites(rows_negative_sites)
					motifs.append(create_motif(header,matrix,alphabet,positive_sites,negative_sites))
				rows_header=[]
				rows_matrix=[]
				rows_positive_sites=[]
				rows_negative_sites=[]


		# 	if len(matrix) > 0:
		# 			motifs.append(parse_one_motif(header,matrix))
		# 		header=""
		# 		matrix=[]
		# 		header=clean_line
		# 	else:
		# 		matrix.append(self._parse_row(clean_line))

		# if len(matrix) > 0:
		# 	motifs.append(parse_one_motif(header,matrix))

		# lines = 
		# counters, _ = sequence2pwm(lines)

		# basename=ntpath.basename(motif_file.name)

		# motif = Motif(identifier=basename, counters=counters)
		# motif.set_source(basename)
		# motif.set_number_of_sites(len(lines))

		return motifs

	def _parse_header(self, rows):
		# Example:
		# MOTIF:	CAATTAAGCC
		# Initial Seed:	AATTAATT
		# Flexible Seed Positions: 7, 8
		# Likelihood Threshold:	100.00000
		# t-score:	13.95899
		# Enrichment:	2.90668(log2)
		header = {}
		for row in rows:
			try:
				if "MOTIF:" in row:
					header["identificator"] = row.split(':')[1].strip()
				elif "Initial Seed:" in row:
					header["initial_seed"] = row.split(':')[1].strip()
				elif "Flexible Seed Positions:" in row:
					header["seed_positions"] = row.split(':')[1].strip()
				elif "Likelihood Threshold:" in row:
					header["likelihood_threshold"] = row.split(':')[1].strip()
				elif "t-score:" in row:
					header["t_score"] = row.split(':')[1].strip()
				elif "Enrichment:" in row:
					header["enrichment"] = row.split(':')[1].strip()
			except:
				print("invalid header")
		return header

	def _parse_matrix(self, rows):
		matrix = []
		# pop 'PWM:' line
		rows.pop(0)
		alphabet = rows[0].split('\t')
		# pop alphabet line
		rows.pop(0)
		for row in rows:
			# line was stripped from trailing tabs in preceding function
			if any(i.isdigit() for i in row):
				matrix.append([float(value) for value in row.split('\t')])
		return matrix, alphabet

	def _parse_sites(self, rows):
		if len(rows) <= 2:
			return []
		rows.pop(0)

		sites = []

		header=""
		value=""
		for row in rows:
			if ">" in row:
				if len(header) > 0:
					sites.append((header,value))
				header=row
			elif len(row) > 0:
				value=row

		return sites


