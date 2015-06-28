all: test.bib
	diff -s $<.ref $<

clean:
	-rm test.bib references.txt

test.bib: references.txt ../doi2bibtex.sh
	$(word 2, $^) <$< >$@

references.txt: json_to_doi.py references.json
	python3 $< <$(word 2, $^) >$@
