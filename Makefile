clean:
	rm -rf csvprint.egg-info dist build __pycache__
	pip uninstall csvprint

wheel:
	make clean
	python setup.py sdist bdist_wheel

pypi-test:
	make wheel
	twine upload -r test dist/csvprint*
	pip install -i https://testpypi.python.org/pypi csvprint
	pytest
	pip uninstall csvprint

pypi:
	make wheel
	twine upload -r pypi dist/csvprint*
	pip install csvprint
	pytest
	pip uninstall csvprint