# <this code belongs to vanheeringen-lab/gimmemotifs written by @simonvh (Simon van Heeringen)>
def pwm2consensus(pwm):

	iupac_rev = {
		"CG": "S",
		"AG": "R",
		"AT": "W",
		"CT": "Y",
		"GT": "K",
		"AC": "M",
		"CGT": "B",
		"ACT": "H",
		"AGT": "D",
		"ACG": "V",
	}

	consensus = ""
	for row in pwm:
		weights = sorted(zip(["A", "C", "G", "T"], row), key=lambda x: x[1])
		if weights[-1][1] >= 0.5:
			if weights[-2][1] >= 0.25:
				consensus += iupac_rev[
					"".join(sorted([weights[-1][0], weights[-2][0]]))
				]
			else:
				consensus += weights[-1][0]
		elif weights[-1][1] + weights[-2][1] >= 0.75:
			consensus += iupac_rev[
				"".join(sorted([weights[-1][0], weights[-2][0]]))
			]
		elif weights[-1][1] + weights[-2][1] + weights[-3][1] >= 0.9:
			consensus += iupac_rev[
				"".join(
					sorted([weights[-1][0], weights[-2][0], weights[-3][0]])
				)
			]
		else:
			consensus += "n"
	return consensus
# </this code belongs to vanheeringen-lab/gimmemotifs written by @simonvh (Simon van Heeringen)>