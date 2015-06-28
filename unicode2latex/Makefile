all: unicode_latex.py

update:
	make -B pythonize.xslt unicode.xml

clean:
	-rm *.py *.xml *.xslt

unicode_latex.py: unicode.xml pythonize.xslt
	xslty $< $(word 2, $^) | python -c 'import sys, bs4; print bs4.BeautifulSoup(sys.stdin).text' >$@

pythonize.xslt:
	curl https://gist.githubusercontent.com/piquadrat/798546/raw/cbc1ee6deb8d2ff192dd3543ddfcc5d2db839ae4/unicode_to_latex.xslt >$@

unicode.xml:
	curl http://www.w3.org/Math/characters/unicode.xml >$@
