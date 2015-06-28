all: unicode2latex.db

update:
	make -B unicode.xml

clean:
	-rm *.db *.xml

unicode2latex.db: unicode.xml process_xml.py
	python3 $(word 2, $^) <$<

unicode.xml:
	curl http://www.w3.org/Math/characters/unicode.xml >$@
