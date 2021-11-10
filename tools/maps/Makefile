python_dir:=$(HOME)/.venvs/zero
python_bin:=$(python_dir)/bin/python
node_bin:=node
src_file:=tmx/map.tmx
map_json:=$(src_file).json
dest_file_client:=../../Web/maps/world_client.new.json
dest_file_server:=../../Server/Maps/world_server.new.json


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
	$(python_bin) ./main.py export2json --src $(map_json) --dest $(dest_file_client) --mode client


server: $(map_json)
	@echo generating map data for server
	$(python_bin) ./main.py export2json --src $(map_json) --dest $(dest_file_server) --mode server


diff:
	json_diff $(subst .new,,$(dest_file_client))   $(dest_file_client)
