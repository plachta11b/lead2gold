from copy import copy, deepcopy

class MotifFix():

	def __init__(self, motifs):
		self.motifs = []
		if motifs:
			for motif in motifs:
				if motif:
					self.motifs.append(deepcopy(motif))

	def filter_matrix_zero_occurrence(self):

		filtered_motifs = []
		for motif in self.motifs:

			# TODO try to cut from ends first

			def get_nonzero_row_counter(motif, counter):
				if sum([counter[letter] for letter in motif.alphabet]) > 0:
					return counter
				else:
					return [1 for letter in motif.alphabet]

			def get_nonzero_row_pfm(motif, row):
				if sum([row[index] for index, letter in enumerate(motif.alphabet)]) > 0:
					return row
				else:
					return [1 for letter in motif.alphabet]

			def get_nonzero_row_ppm(motif, row):
				if sum([row[index] for index, value in enumerate(motif.alphabet)]) > 0:
					return row
				else:
					return motif.get_background().values()

			if motif.counters:
				motif.counters = [get_nonzero_row_counter(motif, counter) for counter in motif.counters]
			if motif.pfm:
				motif.pfm = [get_nonzero_row_pfm(motif, row) for row in motif.pfm]
			if motif.ppm:
				motif.ppm = [get_nonzero_row_ppm(motif, row) for row in motif.ppm]
			filtered_motifs.append(motif)

		self.motifs = filtered_motifs

	def get_motifs(self):
		return self.motifs
