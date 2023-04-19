lint:
	poetry run isort .
	poetry run black .
	poetry run flake8
	poetry run djlint --reformat .

check:
	poetry run isort --check .
	poetry run black --check .
	poetry run flake8
	poetry run djlint .

test:
	poetry run tox
