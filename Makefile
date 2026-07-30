.PHONY: install debug build test format lint clean

install:
	npm ci

debug:
	npm start

build:
	npm run build

test:
	npm test

format:
	npm run lint -- --fix
	npx prettier --write .

lint:
	npm run lint -- --max-warnings=0

clean:
	rm -rf node_modules build coverage
paper: figures values
	cd paper && PATH=/Library/TeX/texbin:$$PATH latexmk -pdf -interaction=nonstopmode main.tex

values:
	.venv/bin/python analysis/emit_paper_values.py

figures:
	.venv/bin/python analysis/paper_figures.py
