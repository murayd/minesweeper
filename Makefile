# DIRECTORIES
PROJECT_DIR  := $$(pwd)
APP_DIR      := ${PROJECT_DIR}/app

# PROJECT SPECIFIC COMMANDS
PYTHON3      := $$(which python3)
PIP3         := $$(which pip3)
PYLINT       := $$(which pylint)

# TARGETS
default: run force

run: force
	${PYTHON3} ${APP_DIR}/main.py

install: force
	${PIP3} install -r requirements.txt

lint: force
	${PYLINT} ${APP_DIR}

# https://docs.python.org/3/library/unittest.html
test: force
	${PYTHON3} -m unittest discover -s ${APP_DIR} -p "*_test.py" -v

# depend on this fake target to cause a target to always run
force: ;

# this target silences echoing of any target
.SILENT:
