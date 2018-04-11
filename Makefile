clean:
	rm -rf csvprint.egg-info dist build __pycache__
	pip uninstall csvprint

wheel:
	python setup.py sdist bdist_wheel

pypi-test:
	twine upload -r test --sign dist/csvprint*

pypi:
	twine upload -r pypi --sign dist/attrs-15.1.0

uninstall:
	pip uninstall csvprint