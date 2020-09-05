from collections import Counter

def sequence2pwm(sequences, sameLength=True):

		n=0
		alphabet=set()

		if type(sequences) is str:
			n=len(sequences)
			sequences=[sequences]
		elif type(sequences) is list:
			n=len(sequences[0])
		else:
			raise ValueError

		counters = [Counter() for i in range(n)]

		for sequence in sequences:
			if len(sequence) == n:
				for counter, letter in zip(counters,sequence):
					counter.update(letter)
			else:
				print("Not counting {} due to different length".format(sequence))

		for counter in counters:
			for letter in counter.keys():
				alphabet.add(letter)

		# TODO: this should be based on tool used
		if not ("a" in str(alphabet).lower()):
			alphabet.add("A")
		if not ("c" in str(alphabet).lower()):
			alphabet.add("C")
		if not ("g" in str(alphabet).lower()):
			alphabet.add("G")
		if not ("t" in str(alphabet).lower() or "u" in str(alphabet).lower()):
			alphabet.add("T")

		for counter in counters:
			counter.update({letter:0 for letter in alphabet})

		return [counters, sorted(alphabet)]

