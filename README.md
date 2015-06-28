**!! not yet functional !!**

# `doi2bibtex`

This project is a proof-of-principle implementation of the idea to automatically 
convert a list of DOIs into a useful bibtex file. This means that i) the bibtex 
keys need to be nice and unique and ii) the journal titles need to be 
consistently abbreviated.

## Dependencies

- Python 3 with [BeautifulSoup][bs] and [bibtexparser][bibparser]
- [bibtool][bibtool]
- [xslty][xslty]

[bibparser]: https://github.com/sciunto-org/python-bibtexparser
[bs]: http://www.crummy.com/software/BeautifulSoup/
[bibtool]: http://www.gerd-neugebauer.de/software/TeX/BibTool/index.en.html
[xslty]: https://github.com/sergi/xslty

## Usage

```bash
doi2bibtex.sh <dois.txt >references.bib
```
