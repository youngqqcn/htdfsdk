.PHONY: clean-pyc clean-build

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "test - run tests quickly with the default Python"
	@echo "upload - upload to pypi"
	@echo "bumpversion 0.0.x  - update version"

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +


dist: clean
	-python3 setup.py sdist bdist_wheel

upload: dist
	twine upload dist/*  --verbose

test:
	cd tests && pytest ./

#test_func:
	#pytest tests/test_htdfsdk.py::$(func)

bumpversion:
# 	@echo "version is:" $(version)
	@bumpversion --new-version $(version) part

