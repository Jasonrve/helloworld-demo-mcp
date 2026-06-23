.PHONY: test lint format docker-build helm-template

test:
	pytest

lint:
	python -m compileall src tests

format:
	python -m compileall src tests

docker-build:
	docker build -t helloworld-demo-mcp:local .

helm-template:
	hemdir=charts/helloworld-demo-mcp && helm template helloworld-demo-mcp $$hemdir
