**!! functional but experimental !!**

# `doi2bibtex`

This project is a proof-of-principle implementation of the idea to automatically 
convert a list of DOIs into a useful bibtex file. This means that:

- Bibtex keys need to be nice and unique.
- Journal titles need to be consistently abbreviated.
- Unicode needs to be consistently encoded in latex commands.

## Prerequisites

- Python 3 with [BeautifulSoup][bs], [bibtexparser][bibparser] and 
	[python-slugify][slugify]. The modules can be installed with

	```bash
	pip3 install beautifulsoup4 bibtexparser python-slugify
	```

- GNU `realpath`

## Installation

```bash
make
```

This builds a couple of tools within the repository directory.

```bash
make test
```

This should print

> Files test.bib.ref and test.bib are identical

## Usage

```bash
doi2bibtex.sh <dois.txt >references.bib
```

`dois.txt` is a text file with one DOI per line.

## Notes

The conversion from DOI to bibtex consists of five steps:

1. DOI is converted to raw bibtex using a HTTP resolver

	```bash
	curl -LH 'Accept: application/x-bibtex' http://data.crossref.org/10.1002/qua.0315
	```

2. Fields `author`, `title` and `journal` in raw bibtex are converted from latex 
   to Unicode.
3. Journal names are abbreviated using the [List of Title Word 
   Abbreviations][ltwa].
4. Pseudo-unique ASCII-converted bibtex keys are generated in format

	```
	<last name of first author><initials of journal><last 2 digits of 
	year>*<last two digits of SHA1 hash of DOI>
	```

5. Fields from (2) are converted from Unicode to latex.

## Developer notes

- Whenever pushing changes to `download_abbrv.py` or `process.sql`, also update 
	the `abbrv.db` file if it changes.

[bibparser]: https://github.com/sciunto-org/python-bibtexparser
[bs]: http://www.crummy.com/software/BeautifulSoup/
[bibtool]: http://www.gerd-neugebauer.de/software/TeX/BibTool/index.en.html
[slugify]: https://github.com/un33k/python-slugify
[ltwa]: http://www.issn.org/services/online-services/access-to-the-ltwa/
