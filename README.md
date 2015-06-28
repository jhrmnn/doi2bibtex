**!! functional but experimental !!**

# `doi2bibtex`

This project is a proof-of-principle implementation of the idea to automatically 
convert a list of DOIs into a useful bibtex file. This means that:

- Bibtex keys need to be nice and unique.
- Journal titles need to be consistently abbreviated.
- Unicode needs to be consistently encoded in latex commands.

## Dependencies

- Python 3 with [BeautifulSoup][bs], [bibtexparser][bibparser] and 
	[python-slugify][slugify]. The modules can be installed with

	```bash
	$ pip3 install beautifulsoup4 bibtexparser python-slugify
	```

- GNU `realpath`

## Installation

```bash
$ make
```

This builds a couple of tools within the repository directory.

```bash
$ make test
```

This should print

> Files test.bib.ref and test.bib are identical

## Usage

```bash
$ doi2bibtex.sh <dois.txt >references.bib
```

[bibparser]: https://github.com/sciunto-org/python-bibtexparser
[bs]: http://www.crummy.com/software/BeautifulSoup/
[bibtool]: http://www.gerd-neugebauer.de/software/TeX/BibTool/index.en.html
[slugify]: https://github.com/un33k/python-slugify

## Notes

## Developer notes

- Whenever pushing changes to `download_abbrv.py` or `process.sql`, also update 
	the `abbrv.db` file if it changes.

### TODO

- Describe functionality in README.
- Put the separation of suffixes in words before abbreviation from `sciabbr` in 
	`do_abbrv.py`.
