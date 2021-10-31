python_dir:=$(HOME)/.venvs/zero
python_bin:=$(python_dir)/bin/python
node_bin:=node
src_file:=tmx/map.tmx
map_json:=$(src_file).json
dest_file_client:=../../Web/maps/world_client
dest_file_server:=../../Server/Maps/world_server.json


all: build
	@echo all done.


init:
	# mkdir -p $(shell dirname $(python_dir))
	python3 -m venv $(python_dir)
	$(python_bin) -m pip install -r requirements.txt


clean:
	rm -f $(map_json)


build: clean $(map_json)
	@echo build OK.


$(map_json):
	$(python_bin) ./main.py tmx2json --tmx $(src_file) --dest $(map_json)


client: $(map_json)
	@echo generating map data for client
	$(node_bin) ./exportmap.js $(dest_file_client) $(map_json) client


server: $(map_json)
	@echo generating map data for server
	$(node_bin) ./exportmap.js $(map_json) $(dest_file_server) server
