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

manage = poetry run python ./manage.py

migrate:
	$(manage) migrate

makemigrations:
	$(manage) makemigrations

build-package:
	poetry build

push-pypi-test:
	poetry publish -r test-pypi

push-pypi:
	poetry publish
