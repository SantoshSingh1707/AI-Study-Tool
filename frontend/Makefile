.PHONY: install test test-coverage lint format clean dev build

install:
	npm ci

test:
	npm test -- --run

test-coverage:
	npm run test:coverage

test-watch:
	npm test

test-ui:
	npm run test:ui

lint:
	npm run lint
	eslint src/ --fix

format:
	npx prettier --write src/

clean:
	rm -rf node_modules/.cache
	rm -rf coverage
	rm -rf dist

dev:
	npm run dev

build:
	npm run build

preview:
	npm run preview

install-all:
	npm ci && cd ../backend && make install

test-all:
	cd backend && make test && cd ../frontend && make test
