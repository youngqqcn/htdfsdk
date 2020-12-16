
build_wheel:
	-rm -r dist/*
	-python3 setup.py sdist bdist_wheel

upload:
	twine upload dist/*  --verbose


test:
	-python3 -m unittest ./tests/htdfsdk_test.MyTestCase  ./tests
