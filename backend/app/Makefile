.PHONY: test

default: test

test:
	cd tests \
	&& env SECRET_KEY='JDD108@HAREKRISHNA' \
    FLASK_ENV='default' \
    MODEL_DIR=`pwd`'/../app/models' \
	  pytest
