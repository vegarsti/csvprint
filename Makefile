clean:
	rm -rf csvprint.egg-info dist build

install:
	pip install -r requirements.txt
	pip install .

uninstall:
	pip uninstall csvprint