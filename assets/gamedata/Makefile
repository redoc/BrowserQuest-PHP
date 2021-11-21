python_dir:=$(HOME)/.venvs/zero
python_bin:=$(python_dir)/bin/python
data_file:=gamedata.json


all: build
	@echo all done.


clean:
	rm -f $(data_file)


build: clean $(data_file)


$(data_file):
	$(python_bin) ./build.py export --output $(data_file)
