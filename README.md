# 🦌 deer-code

A minimalist yet sufficient project for enabling everyone to learn how to develop an AI Coding Agent.

Brought you by [🦌 The DeerFlow Team](https://github.com/bytedance/deer-flow).

## How to install

### Prerequisites

- Python 3.12
- fd: A fast, modern alternative to `find`
    - **Ubuntu/Debian**: `sudo apt install fd-find`
    - **macOS**: `brew install fd`
    - **Windows**: `scoop install fd` or `choco install fd`

### Install dependencies

```bash
make install
```

### How to run

```bash
uv run -m deer_code.main
```

> Change the `root_dir` located in [project.py](./src/deer_code/project.py)
> when debugging.

## How to debug in LangGraph CLI

```bash
make dev
```
