clean:
	rm -rf csvprint.egg-info dist build __pycache__

uninstall:
	pip uninstall csvprint

wheel:
	make clean
	python setup.py sdist bdist_wheel

upload-test:
	make clean
	make wheel
	twine upload -r test dist/csvprint*

pypi-test:
	pip install -i https://testpypi.python.org/pypi csvprint
	pytest

upload-pypi:
	make clean
	make wheel
	twine upload -r pypi dist/csvprint*
	
pypi:
	pip install csvprint
	pytest