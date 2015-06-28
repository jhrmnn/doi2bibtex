all: test.bib

clean:
	-rm test.bib references.txt

test.bib: references.txt
	../doi2bibtex.sh <$< >$@

references.txt: json_to_doi.py references.json
	python3 $< <$(word 2, $^) >$@
