python_dir:=$(HOME)/.venvs/zero
python_bin:=$(python_dir)/bin/python
gamedata_file:=shared/gamedata.json
map_file:=shared/map.json

all: build
	@echo all done.


init:
	mkdir -p $(shell dirname $(python_dir))
	python3 -m venv $(python_dir)
	$(python_bin) -m pip install -U pip wheel
	$(python_bin) -m pip install -r requirements.txt


init-renew:
	rm -fr $(python_dir)
	make init


clean:
	rm -f $(gamedata_file) $(map_file) 


build: $(gamedata_file)
	cd maps && make all


$(gamedata_file):
	$(python_bin) build.py gamedata --output $(gamedata_file)
