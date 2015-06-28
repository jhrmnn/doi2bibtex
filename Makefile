.PHONY: test unicode2latex clean

test:
	$(MAKE) -C test

unicode2latex:
	$(MAKE) -C unicode2latex

clean:
	$(MAKE) -C test clean
	$(MAKE) -C unicode2latex clean

jabbrv.db: jabbrv.db.downloaded process.sql
	cp $< $@
	sqlite3 $@ <$(word 2, $^)

download:
	$(MAKE) -B jabbrv.db.downloaded

jabbrv.db.downloaded: download_jabbrv.py
	-rm jabbrv.db
	time python3 $<
	mv jabbrv.db $@

