from collections import Counter

class Motif():

	def __init__(self, identifier, counters=None, pfm=None, ppm=None):


		self.alphabet = ["A", "C", "G", "T"]
		self.alternate_name = ""
		self.e = 0
		self.enrichment = 0
		self.number_of_sites = None
		self.pfm = None
		self.source_file=None
		self.width = 0
		self.strand = "+ -"
		# specific data for given format
		self.specific = {}

		# Log Likelihood
		# P-value
		# E-value
		# Z-Score
		# t-score

		if counters:
			# get alphabet
			alphabet=set()
			for counter in counters:
				for letter in counter.keys():
					alphabet.add(letter)
			self.alphabet = sorted(alphabet)
			# get PFM and PPM
			pfm = [[counter[letter] for letter in self.alphabet ] for counter in counters]
			# some motifs have zero sum on row :(
			ppm = [[float(counter[letter])/float(sum(counter.values())) if sum(counter.values()) else 0.0 for letter in self.alphabet] for counter in counters]
			if not all(len(e) == len(counters[0]) for e in counters):
				raise(ValueError("counters not matrix"))

		if pfm:
			if not all(len(e) == len(pfm[0]) for e in pfm):
				raise(ValueError("pfm not matrix"))
			ppm = [[float(letter)/float(sum(row)) if sum(row) else 0.0 for letter in row] for row in pfm]

		if not all(len(e) == len(ppm[0]) for e in ppm):
			raise(ValueError("ppm not matrix"))

		# motif width
		self.width = len(ppm)
		self.counters = counters
		self.pfm = pfm
		self.ppm = ppm
		self.identifier = identifier
		

	def get_name(self):
		return self.identifier, self.alternate_name

	def get_identifier(self):
		return self.identifier

	def get_alternate_name(self):
		return self.alternate_name

	def set_alternate_name(self, alternate_name):
		self.alternate_name = alternate_name

	# Return position frequency matrix
	def get_PFM(self):
		return self.pfm

	# Return position probability matrix
	def get_PPM(self):
		return self.ppm

	def get_alphabet(self):
		return self.alphabet

	def set_alphabet(self, alphabet):
		self.alphabet = alphabet

	def get_length(self):
		return self.width

	def get_number_of_sites(self):
		return self.number_of_sites

	def set_number_of_sites(self, number_of_sites):
		self.number_of_sites = number_of_sites

	def get_e(self):
		return self.e

	def set_e(self, e):
		self.e = e

	def set_enrichment(self, enrichment):
		self.enrichment = enrichment

	def get_source(self):
		return self.source_file

	def set_source(self, source_file):
		self.source_file = source_file

	def get_background(self):
		counter=Counter()
		for letter in self.alphabet:
			counter.update(letter)
		return {k: v / total for total in (sum(counter.values()),) for k, v in counter.items()}

	def set_specific(self,key,value):
		self.specific["key"] = "value"
