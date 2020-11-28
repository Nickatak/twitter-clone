.\activate
coverage run -m pytest
coverage html
start chrome htmlcov/index.html