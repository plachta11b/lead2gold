# lead2gold
Motif alchemy has never been easier

## convert motif

### one motif only
```
python -m lead2gold --motif-in meme --motif-out consensus --file-in /path/to/motif/meme.txt --file-out -
```

### Merging multiple motifs
Folder must contain only motif files.
```
python -m lead2gold \
			--motif-in pfm_horizontal \
			--motif-out meme \
			--folder-in /path/to/your/motifs \
			--file-out -
```

## dependencies
Python package: iteround==1.0.2
Consensus function was taken from [GimmeMotifs](https://github.com/vanheeringen-lab/gimmemotifs) written by simonvh.

## Help
* The preferred way to get support is through the Github
  [issues](https://github.com/plachta11b/lead2gold/issues/) page
* You can reach me by [mail](janholcak@gmail.com) too.
