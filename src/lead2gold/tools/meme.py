import ntpath
import re
import string
from iteround import saferound

from lead2gold.motif import Motif
from lead2gold.tools.tool import Tool

class MEME(Tool):
	"""Class implementing a MEME search tool motif convertor.
	"""

	toolName = "MEME"

	def __init__(self):
		"""Initialize all class attributes with their default values.
		"""
		super(self.__class__, self).__init__(self.toolName)

	def parse(self, motif_file, type=None):
		"""Loads the searcher parameters specified in the configuration file.

		Args:
			motif_file: file containing motif file in MEME format.

		Returns:
			[Motif()]
		"""

		basename=ntpath.basename(motif_file.name)

		def get_section(line, section, order):
			if "MEME version" in line:
				return "version", 1
			if "ALPHABET=" in line:
				return "alphabet", 2
			if "strands:" in line:
				return "strands", 3
			if "MOTIF" in line:
				return "name", 4
			if "letter-probability matrix:" in line:
				return "matrix", 5
			if "URL " in line:
				return "url", 6
			return section, order

		def get_template(t_motif={"version": [], "alphabet": [], "strands": []}):
			return {
				"start": [],
				"version": t_motif["version"],
				"alphabet": t_motif["alphabet"],
				"strands": t_motif["strands"],
				"name": [],
				"matrix": [],
				"url": []
			}

		motifs = []

		section = "start"
		order = 0
		t_motif = get_template()
		for line in motif_file:
			clean_line = line.strip()
			section, order_new = get_section(line, section, order)
			if order_new < order:
				motifs.append(self._parse_motif_lines(t_motif))
				t_motif = get_template(t_motif)
			order=order_new

			t_motif[section].append(clean_line)

		motifs.append(self._parse_motif_lines(t_motif))
	
		return motifs

	def _parse_motif_lines(self, t_motif):
		identifier=""
		alternate_name=""
		alphabet_length=1
		if t_motif["version"]:
			version = re.sub('MEME version.*([0-9]|.).*', r'\1', t_motif["version"][0]).strip()
		if t_motif["alphabet"]:
			alphabet = list(re.sub('ALPHABET=(.*)', r'\1', t_motif["alphabet"][0]).strip().replace(" ", ""))
			alphabet_length = len(alphabet)
		if t_motif["strands"]:
			alphabet = re.sub('strands(.*)', r'\1', t_motif["strands"][0]).strip()
		if t_motif["name"]:
			names = re.sub('MOTIF:*\ *(.*)', r'\1', t_motif["name"][0].replace("\t", " ")).strip()
			# splice names correctly even when multiple spaces
			names_list = names.split()
			if len(names_list):
				identifier = names_list[0]
				names_list.pop(0)
			if len(names_list):
				alternate_name = names_list[0]
		
		matrix = []
		e_value = 0
		if type(t_motif["matrix"]) is list and len(t_motif["matrix"]):
			first_line = t_motif["matrix"][0]
			t_motif["matrix"].pop(0)

			section_match = 'letter-probability matrix:.*'
			line_match = section_match + 'alength=(.*)w=(.*)nsites=(.*)E=(.*)'
			matrix_header_values = re.sub(line_match, r'\1 \2 \3 \4', first_line)
			if matrix_header_values:
				matrix_header_values = matrix_header_values.split()
				# TODO expecting well fomated
				if len(matrix_header_values) == 4:
					# print(matrix_header_values[3],float(matrix_header_values[3]))
					e_value = float(matrix_header_values[3])
			for row in t_motif["matrix"]:
				# can not be only one due to numbers with exponent 3.3e-7
				if "-----" in row:
					break
				if "#" in row:
					break
				values = row.split()
				if len(values) >= alphabet_length:
					matrix.append([float(value) for value in values])

		motif = Motif(identifier=identifier, ppm=matrix)
		motif.set_e(e_value)

		return motif

	def print(self, motifs, file):

		# http://meme-suite.org/doc/alphabet-format.html#ordering
		meme_alphabet = string.ascii_uppercase + \
			string.ascii_lowercase+string.digits+"*-."
		ordering = dict(zip(meme_alphabet, range(len(meme_alphabet))))

		first = True
		for motif in motifs:
			if first:
			# def print_header():
				alphabet = motif.get_alphabet()
				alphabet_sorted = sorted(alphabet, key=lambda word: [ordering[c] for c in word])

				file.write("MEME version 4\n\n")

				file.write("ALPHABET= {}\n\n".format(''.join(alphabet_sorted)))

				background = motif.get_background()
				if background:
					source_file = motif.get_source()
					if source_file:
						file.write(
							"Background letter frequencies (from {}):\n".format(source_file))
					else:
						file.write("Background letter frequencies\n")
					safe_background = saferound(background, places=6)
					for letter in alphabet_sorted:
						file.write("{} {} ".format(letter, safe_background[letter]))
					file.write("\n\n")
			# if first:
				# print_header()

			# # Motif name line (required)
			# # The motif name line indicates the start of a new motif and designates an identifier for it that must be unique to the file. It also allows for an alternate name that does not have to be unique. Neither the identifier nor the alternate name may contain spaces or equal signs (=).

			# # MOTIF identifier alternate name
			# # For example:

			# # MOTIF MA0002.1 RUNX1

			def escape_name(name):
				if not name:
					return ""
				# as defined above
				return name.replace(" ", "_").replace("=", "_")

			file.write("MOTIF {} {}\n\n".format(escape_name(
				motif.get_identifier()), escape_name(motif.get_alternate_name())))

			# The letter probability matrix is a table of probabilities where the rows are positions in the motif and the columns are letters in the alphabet. The columns are ordered alphabetically so for DNA the first column is A, the second is C, the third is G and the last is T. For protein motifs the columns come in the order A, C, D, E, F, G, H, I, K, L, M, N, P, Q, R, S, T, V, W and Y (see also custom alphabet ordering). As each row contains the probability of each letter in the alphabet the probabilities in the row must sum to 1.

			# letter-probability matrix: alength= alphabet length w= motif length nsites= source sites E= source E-value

			alphabet_length = len(alphabet)
			motif_length = motif.get_length()
			source_sites = motif.get_number_of_sites()
			source_sites = source_sites if source_sites != None else 20
			e = motif.get_e()
			file.write("letter-probability matrix: alength= {} w= {} nsites= {} E= {}\n".format(
				alphabet_length, motif_length, source_sites, e))

			# ... (letter-probability matrix goes here) ...
			matrix = motif.get_PPM()
			for row in matrix:
				safe_row = saferound(row, places=6)
				# do not forget on custom ordering
				file.write("{}\n".format(" ".join(
					[str(safe_row[alphabet.index(letter)]) for letter in alphabet_sorted])))

			file.write("\n\n")

			# All the "key= value" pairs after the "letter-probability matrix:" text are optional. The "alength= alphabet length" and "w= motif length" can be derived from the matrix if they are not specified, provided there is an empty line following the letter probability matrix. The "nsites= source sites" will default to 20 if it is not provided and the "E= source E-value" will default to zero. The source sites is used to apply pseudocounts to the motif and the source E-value is used for filtering the motifs input to some MEME Suite programs (see MAST's -mev option).
			first = False
