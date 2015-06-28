all: test.bib

clean:
	-rm test.bib references.txt

test.bib: references.txt
	python3 ../get_bibtex.py <$< | bibtool -r ../bibtool.conf >$@

references.txt: json_to_doi.py references.json
	python3 $< <$(word 2, $^) >$@
