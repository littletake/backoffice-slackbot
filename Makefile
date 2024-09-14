include ./src/.env
export

.PHONY: install
install:
	poetry install

.PHONY: update
update:
	poetry update

.PHONY: run
run:
	OPENAI_API_KEY=${OPENAI_API_KEY} SLACK_BOT_TOKEN=${SLACK_BOT_TOKEN} SLACK_APP_TOKEN=${SLACK_APP_TOKEN} poetry run python ./src/main.py poetry run python your_script.py

.PHONY: test
test:
	poetry run pytest

.PHONY: lint
lint:
	poetry run flake8 your_package

.PHONY: format
format:
	poetry run black your_package