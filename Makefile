PYCACHE = $$(find . -type d -name "__pycache__")

install:
	@uv sync

run:
	@uv run main.py


clean:
	rm -rf $(PYCACHE)
