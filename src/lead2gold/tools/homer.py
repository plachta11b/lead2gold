import ntpath
import re

from lead2gold.tools.tool import Tool
from lead2gold.motif import Motif

class Homer(Tool):
	"""Class implementing a Homer search tool motif convertor.
	"""

	toolName = "Homer"

	def __init__(self):
		"""Initialize all class attributes with their default values.
		"""
		super(self.__class__, self).__init__(self.toolName)


	def parse(self, motif_file, type=None):
		"""Loads the searcher parameters specified in the configuration file.

		Args:
			motif_file: file containing one or more Homer motifs.

		Returns:
			[Motif()]
		"""

		basename=ntpath.basename(motif_file.name)

		motifs=[]

		def parse_one_motif(header, matrix):
			header_values = self._parse_header(header)
			motif = Motif(ppm=matrix, identifier=header_values["motif_name"])
			motif.set_alternate_name(header_values["consensus_sequence"])
			motif.set_e(2**float(header_values["logp_value"]))
			op = header_values["occurence"]["primary"]
			# T:14.0(4.67%) => 14
			motif.set_number_of_sites(re.sub('T:([0-9]+).*', r'\1', op))
			motif.set_source(basename)
			return motif


		header=""
		matrix=[]
		for line in motif_file:
			clean_line = line.strip()
			if ">" in clean_line:
				if len(matrix) > 0:
					motifs.append(parse_one_motif(header,matrix))
				header=""
				matrix=[]
				header=clean_line
			else:
				matrix.append(self._parse_row(clean_line))
				
		if len(matrix) > 0:
			motifs.append(parse_one_motif(header,matrix))

		# lines = 
		# counters, _ = sequence2pwm(lines)

		# basename=ntpath.basename(motif_file.name)

		# motif = Motif(identifier=basename, counters=counters)
		# motif.set_source(basename)
		# motif.set_number_of_sites(len(lines))

		return motifs

	def _parse_header(self, header_list):
		header_list=header_list.replace(">","").split('\t')
		header = {}
		# 1) (required) ">" + Consensus sequence (not actually used for anything, can be blank)
		#      example: >ASTTCCTCTT
		header["consensus_sequence"] = header_list[0]
		# 2) (required) Motif name (should be unique if several motifs are in the same file)
		#      example: 1-ASTTCCTCTT  or NFkB
		header["motif_name"] = header_list[1]
		# 3) (required) Log odds detection threshold, used to determine bound vs. unbound sites (mandatory)
		#      example: 8.059752
		header["log_odds"] = header_list[2]
		# 4) (optional) log P-value of enrichment,
		#      example: -23791.535714
		header["logp_value"] = header_list[3]
		# 5) (optional) 0 (A place holder for backward compatibility, used to describe "gapped" motifs in old version,
		#      turns out it wasn't very useful :)
		header["gapped_compatibility"] = header_list[4]
		# 6) (optional) Occurence Information separated by commas
		#      example: T:17311.0(44.36%),B:2181.5(5.80%),P:1e-10317
		header["occurence"] = {}
		values = header_list[5].split(',')
		#    1) T:#(%) - number of target sequences with motif, % of total of total targets
		for n in values:
			if "T:" in n:
				header["occurence"]["primary"] = n
		#    2) B:#(%) - number of background sequences with motif, % of total background
		for n in values:
			if "B:" in n:
				header["occurence"]["background"] = n
		#    3) P:# - final enrichment p-value
		for n in values:
			if "P:" in n:
				header["occurence"]["p_value"] = n
		# 7) (optional) Motif statistics separated by commas
		#      example: Tpos:100.7,Tstd:32.6,Bpos:100.1,Bstd:64.6,StrandBias:0.0,Multiplicity:1.13
		header["statistics"] = {}
		#    1) Tpos: average position of motif in target sequences (0 = start of sequences)
		#    2) Tstd: standard deviation of position in target sequences
		#    3) Bpos: average position of motif in background sequences (0 = start of sequences)
		#    4) Bstd: standard deviation of position in background sequences
		#    5) StrandBias: log ratio of + strand occurrences to - strand occurrences.
		#    6) Multiplicity: The averge number of occurrences per sequence in sequences with 1 or more binding site.

		return header

	def _parse_row(self, row):
		return [float(value) for value in row.split('\t')]
