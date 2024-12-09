.PHONY: install prepare run up down db-remove

install:
	@echo "Installing dependencies..."
	pip3 install -r src/requirements.txt

prepare:
	@echo "Preparing the environment..."
	cd src && python3 prepare.py

run:
	@echo "Running the application..."
	cd src && python3 main.py

up:
	@echo "Starting Docker Compose services..."
	docker-compose -f docker-compose.yaml up -d

down:
	@echo "Stopping Docker Compose services..."
	docker-compose -f docker-compose.yaml down

db-remove:
	@echo "Removing database..."
	test -f src/${DATABASE_PATH} && rm src/${DATABASE_PATH} || echo Database not found
