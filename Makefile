install:
	uv sync

build:
	uv build

dev:
	uvx --refresh --no-browser --from "langgraph-cli[inmem]" --with-editable . --python 3.12 langgraph dev --allow-blocking
