#author: plachta11b (janholcak@gmail.com)

import argparse
import os
import io
import sys
import traceback
from lead2gold.tools import get_tool
from lead2gold.motif import MotifFix

def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)

def main():

	parser = argparse.ArgumentParser(
		description="Convert motifs",
		usage='''lead2gold --motif-in STR --motif-out STR --file-in FILEPATH --file-out FILEPATH
				lead2gold --motif-in STR --motif-out STR --folder-in PATH_TO_DIRECTORY --file-out FILEPATH ''')
	parser.add_argument('--motif-in', type=str, help="meme", required=True)
	parser.add_argument('--motif-out', type=str, help="meme", required=True)
	parser.add_argument('--best', type=int, help="5", required=False)
	parser.add_argument('--filter', default=False, action="store_true" , help="Filter above zero")
	parser.add_argument('--fix', default=False, action="store_true" , help="Fix invalid values")
	parser.add_argument('--folder-in', type=dir_path, help="/path/to/motif/directory")
	parser.add_argument('--file-in', type=argparse.FileType('r'), help="motif.meme")
	parser.add_argument('--file-out', type=argparse.FileType('w'), help="motif.meme", required=True)
	ns = parser.parse_args(sys.argv[1:])

	if (not ns.folder_in) and (not ns.file_in):
		print("--file-in or --folder-in required")
		exit(1)

	listOfFiles = []
	if ns.folder_in:
		listOfFiles = [os.path.join(ns.folder_in,f) for f in os.listdir(ns.folder_in) if os.path.isfile(os.path.join(ns.folder_in,f))]

	if ns.file_in:
		listOfFiles.append(ns.file_in)

	filter = False
	if ns.filter:
		filter = True

	fix = False
	if ns.fix:
		fix = True

	best = 1000000
	if ns.best:
		best = ns.best

	convert(ns.motif_in, ns.motif_out, listOfFiles, ns.file_out, filter, fix, best)

	if ns.file_in:
		ns.file_in.close()
	ns.file_out.close()

def convert(motif_in, motif_out, files_in, file_out, filter, fix, best):
	tool_in = get_tool(motif_in)
	tool_out = get_tool(motif_out)

	motifs = []
	try:
		for file_in in files_in:
			if isinstance(file_in, io.IOBase):
				motifs = motifs + tool_in.parse(file_in)
			else:
				with open(file_in, "r") as file_in_h:
					motifs = motifs + tool_in.parse(file_in_h)
		motifs_filtered = motifs
		if filter:
			motifs_filtered = [motif for motif in motifs if motif.get_e() <= 0.05]
		if fix:
			motifs_fix = MotifFix(motifs_filtered)
			motifs_fix.filter_matrix_zero_occurrence()
			motifs_filtered = motifs_fix.get_motifs()

		motifs_filtered_sorted = sorted(motifs_filtered, key=lambda x: x.get_e(), reverse=False)

		tool_out.print(motifs_filtered_sorted[:best], file_out)
	except Exception as e:
		print(e)
		# print("How could i convert this?")
		# file_in.seek(0)
		# print(file_in.read())
		traceback.print_exc()
		exit(1)



if __name__ == "__main__":
	# execute only if run as a script
	main()

# python code/lead2gold/__main__.py --motif-in graphprot --motif-out meme --file-in ./code/test_data/w7.sequence_motif  --file-out -