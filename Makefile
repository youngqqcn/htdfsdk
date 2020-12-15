
build_wheel:
	-rm -r dist/*
	-python3 setup.py sdist bdist_wheel

upload:
	twine upload dist/*  --verbose
