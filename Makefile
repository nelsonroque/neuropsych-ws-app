APP_NAME=app
HOST=127.0.0.1
PORT=8000
VENV=.venv

.PHONY: install run dev clean

install:
	uv pip install fastapi uvicorn jinja2 uvicorn[standard]

run:
	uv $(APP_NAME):app --host $(HOST) --port $(PORT)

dev:
	$(VENV)/bin/uvicorn $(APP_NAME):app --reload --host $(HOST) --port $(PORT)

clean:
	rm -rf $(VENV)
