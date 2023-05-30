#!/bin/sh
# A script to run the flatten_clause_notation.py script over multiple files at a time. It returns a series of files with the same names as the originals, so using it in the same directory will result in information loss.

for f in "$@"
do
	cat $f | python3 flatten_clause_notation.py > ./temp_file
	cp temp_file $f
done
