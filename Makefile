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
